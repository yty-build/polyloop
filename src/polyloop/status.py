from __future__ import annotations

import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path

from .config import ProjectConfig
from .constants import ROLES, SHELL_COMMANDS
from .frontmatter import FrontmatterError, read_toml_frontmatter
from .providers import PROVIDER_EXECUTABLES
from .tmux import Tmux, TmuxError, WindowState


@dataclass(frozen=True)
class StatusReport:
    text: str
    healthy: bool


def build_status_report(
    config: ProjectConfig, tmux: Tmux | None = None
) -> StatusReport:
    tmux = tmux or Tmux()
    lines = [
        f"Strategy:  {config.session}",
        f"Workspace: {config.root}",
    ]
    healthy = True

    campaign_line, campaign_warning = _campaign_status(config)
    lines.append(f"Campaign:  {campaign_line}")
    if campaign_warning:
        healthy = False

    git_line, git_warning = _git_status(config)
    lines.append(f"Git:       {git_line}")
    if git_warning:
        healthy = False

    if not tmux.available():
        lines.extend(
            ("Session:   unavailable", "", "tmux is not installed or not on PATH")
        )
        return StatusReport("\n".join(lines), False)

    if not tmux.session_exists(config.session):
        lines.extend(
            (
                "Session:   DOWN",
                "",
                "Run: polyloop init",
                f"Then: tattach {config.session}",
            )
        )
        return StatusReport("\n".join(lines), False)

    owner = tmux.get_session_option(config.session, "@polyloop_root")
    if owner and Path(owner).expanduser().resolve() != config.root:
        lines.append(f"Session:   CONFLICT (owned by {owner})")
        return StatusReport("\n".join(lines), False)
    lines.append("Session:   UP")

    try:
        windows = tmux.list_windows(config.session)
    except TmuxError as exc:
        lines.extend(("", f"Could not inspect windows: {exc}"))
        return StatusReport("\n".join(lines), False)
    by_name = {window.name: window for window in windows}

    rows: list[tuple[str, str, str, str, str]] = []
    warnings: list[str] = []
    for role_name in ROLES:
        role = config.roles[role_name]
        executable = PROVIDER_EXECUTABLES[role.provider]
        installed = shutil.which(executable) is not None
        window = by_name.get(role_name)
        state, process = _window_state(window)
        if not installed:
            state = "MISSING CLI"
            healthy = False
        if window is None or window.dead:
            healthy = False
        if (
            window
            and window.provider_marker
            and window.provider_marker != role.provider
        ):
            warnings.append(
                f"{role_name} is marked {window.provider_marker}, configured {role.provider}"
            )
            state = "CONFIG DRIFT"
            healthy = False
        rows.append(
            (role_name, role.provider, role.effort or "default", state, process)
        )

    lines.extend(("", _format_table(rows)))
    extra_windows = sorted(set(by_name) - set(ROLES))
    if extra_windows:
        warnings.append("extra tmux windows: " + ", ".join(extra_windows))
    if campaign_warning:
        warnings.append(campaign_warning)
    if git_warning:
        warnings.append(git_warning)
    if warnings:
        lines.append("\nWarnings:")
        lines.extend(f"- {warning}" for warning in warnings)
    lines.extend(("", f"Attach: tattach {config.session}"))
    return StatusReport("\n".join(lines), healthy)


def _campaign_status(config: ProjectConfig) -> tuple[str, str | None]:
    try:
        campaign = read_toml_frontmatter(config.root / "CAMPAIGN.md")
        experiment = read_toml_frontmatter(config.root / "CURRENT_EXPERIMENT.md")
    except FrontmatterError as exc:
        return "invalid metadata", str(exc)
    if not campaign:
        return "missing CAMPAIGN.md metadata", "CAMPAIGN.md has no TOML front matter"
    if not experiment:
        return (
            "missing CURRENT_EXPERIMENT.md metadata",
            "CURRENT_EXPERIMENT.md has no TOML front matter",
        )
    campaign_id = str(campaign.get("id", config.campaign.campaign_id))
    status = str(campaign.get("status", "unknown"))
    completed = campaign.get("completed_experiments", "?")
    maximum = campaign.get("max_experiments", config.campaign.max_experiments)
    experiment_id = str(experiment.get("experiment", "")).strip() or "none"
    stage = str(experiment.get("stage", "unknown"))
    drift: list[str] = []
    if campaign_id != config.campaign.campaign_id:
        drift.append(
            f"campaign id is {campaign_id} in CAMPAIGN.md and "
            f"{config.campaign.campaign_id} in polyloop.toml"
        )
    if maximum != config.campaign.max_experiments:
        drift.append(
            f"experiment limit is {maximum} in CAMPAIGN.md and "
            f"{config.campaign.max_experiments} in polyloop.toml"
        )
    if isinstance(completed, int) and isinstance(maximum, int) and completed > maximum:
        drift.append(f"completed experiment count {completed} exceeds limit {maximum}")
    return (
        f"{campaign_id} {status}, {completed}/{maximum} complete, "
        f"experiment={experiment_id}, stage={stage}",
        "; ".join(drift) or None,
    )


def _git_status(config: ProjectConfig) -> tuple[str, str | None]:
    branch = _git(config, "branch", "--show-current") or "unborn"
    commit = _git(config, "rev-parse", "--short", "HEAD") or "no commits"
    dirty_output = _git(config, "status", "--porcelain", allow_failure=False)
    if dirty_output is None:
        return "unavailable", "workspace is not a readable Git repository"
    dirty = "dirty" if dirty_output.strip() else "clean"
    return f"{branch} @ {commit}, {dirty}", None


def _git(config: ProjectConfig, *args: str, allow_failure: bool = True) -> str | None:
    try:
        result = subprocess.run(
            ["git", "-C", str(config.root), *args],
            capture_output=True,
            text=True,
            check=False,
        )
    except FileNotFoundError:
        return None
    if result.returncode != 0:
        return "" if allow_failure else None
    return result.stdout.strip()


def _window_state(window: WindowState | None) -> tuple[str, str]:
    if window is None:
        return "MISSING", "-"
    if window.dead:
        return "DEAD", window.command or "-"
    if window.command in SHELL_COMMANDS:
        return "IDLE", window.command
    return "RUNNING", window.command or "unknown"


def _format_table(rows: list[tuple[str, str, str, str, str]]) -> str:
    headers = ("ROLE", "PROVIDER", "EFFORT", "STATE", "PROCESS")
    all_rows = [headers, *rows]
    widths = [
        max(len(str(row[index])) for row in all_rows) for index in range(len(headers))
    ]
    output = [
        "  ".join(value.ljust(widths[index]) for index, value in enumerate(headers)),
        "  ".join("-" * width for width in widths),
    ]
    output.extend(
        "  ".join(str(value).ljust(widths[index]) for index, value in enumerate(row))
        for row in rows
    )
    return "\n".join(output)
