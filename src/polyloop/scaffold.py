from __future__ import annotations

import subprocess
from importlib import resources
from pathlib import Path
from string import Template

from .constants import ROLE_FUNCTIONS


class ScaffoldError(RuntimeError):
    """Raised when project scaffolding cannot be created safely."""


def ensure_git_repository(root: Path) -> bool:
    result = subprocess.run(
        ["git", "-C", str(root), "rev-parse", "--show-toplevel"],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode == 0:
        repository_root = Path(result.stdout.strip()).resolve()
        if repository_root != root.resolve():
            raise ScaffoldError(
                f"{root} is inside Git repository {repository_root}; initialize at the "
                "repository root or create a separate Git worktree for this strategy"
            )
        return False
    initialized = subprocess.run(
        ["git", "init", "-b", "main", str(root)],
        capture_output=True,
        text=True,
        check=False,
    )
    if initialized.returncode != 0:
        raise ScaffoldError(initialized.stderr.strip() or "git init failed")
    return True


def create_project_files(
    root: Path,
    *,
    session: str,
    description: str,
    market: str,
    objective: str,
) -> list[Path]:
    substitutions = {
        "session": session,
        "description": description or session,
        "market": market
        or "Define the exact Polymarket market before activating the campaign.",
        "objective": objective
        or "Find a strategy that improves on the current verified champion without weakening evidence quality.",
    }
    created: list[Path] = []
    project_templates = {
        ".gitignore": "gitignore.md",
        "AGENTS.md": "AGENTS.md",
        "PROJECT_CHARTER.md": "PROJECT_CHARTER.md",
        "CAMPAIGN.md": "CAMPAIGN.md",
        "CURRENT_EXPERIMENT.md": "CURRENT_EXPERIMENT.md",
        "LEADERBOARD.md": "LEADERBOARD.md",
        "LESSONS.md": "LESSONS.md",
        "experiments/EXPERIMENT_TEMPLATE.md": "EXPERIMENT_TEMPLATE.md",
    }
    for destination, template_name in project_templates.items():
        path = root / destination
        if _create_from_template(path, template_name, substitutions):
            created.append(path)

    roles_dir = root / "roles"
    roles_dir.mkdir(parents=True, exist_ok=True)
    for role in ("shared", *ROLE_FUNCTIONS):
        path = roles_dir / f"{role}.md"
        if _create_from_template(path, f"roles/{role}.md", substitutions):
            created.append(path)

    campaigns_dir = root / "campaigns"
    campaigns_dir.mkdir(parents=True, exist_ok=True)
    keep = campaigns_dir / ".gitkeep"
    if not keep.exists():
        keep.touch()
        created.append(keep)
    return created


def _create_from_template(
    destination: Path, template_name: str, substitutions: dict[str, str]
) -> bool:
    if destination.exists():
        return False
    source = resources.files("polyloop").joinpath("templates", template_name)
    content = Template(source.read_text(encoding="utf-8")).safe_substitute(
        substitutions
    )
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(content, encoding="utf-8")
    return True
