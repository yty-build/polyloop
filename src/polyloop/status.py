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


@dataclass(frozen=True)
class ExperimentObservation:
    current_campaign_closed: int
    total_closed: int
    closed_ids: frozenset[str]
    warnings: tuple[str, ...]


TERMINAL_DECISIONS = {"promote", "reject", "inconclusive", "blocked"}


def build_status_report(
    config: ProjectConfig, tmux: Tmux | None = None
) -> StatusReport:
    tmux = tmux or Tmux()
    lines = [
        f"Strategy:  {config.session}",
        f"Workspace: {config.root}",
    ]
    healthy = True

    campaign_line, experiment_line, campaign_warnings = _campaign_status(config)
    lines.append(f"Campaign:  {campaign_line}")
    lines.append(f"Experiments: {experiment_line}")
    if campaign_warnings:
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
    warnings.extend(campaign_warnings)
    if git_warning:
        warnings.append(git_warning)
    if warnings:
        lines.append("\nWarnings:")
        lines.extend(f"- {warning}" for warning in warnings)
    lines.extend(("", f"Attach: tattach {config.session}"))
    return StatusReport("\n".join(lines), healthy)


def _campaign_status(config: ProjectConfig) -> tuple[str, str, list[str]]:
    try:
        campaign = read_toml_frontmatter(config.root / "CAMPAIGN.md")
        experiment = read_toml_frontmatter(config.root / "CURRENT_EXPERIMENT.md")
    except FrontmatterError as exc:
        return "invalid metadata", "unknown", [str(exc)]
    if not campaign:
        return (
            "missing CAMPAIGN.md metadata",
            "unknown",
            ["CAMPAIGN.md has no TOML front matter"],
        )
    if not experiment:
        return (
            "missing CURRENT_EXPERIMENT.md metadata",
            "unknown",
            ["CURRENT_EXPERIMENT.md has no TOML front matter"],
        )
    raw_campaign_id = str(campaign.get("id", "")).strip()
    campaign_id = raw_campaign_id or "none"
    status = str(campaign.get("status", "unknown"))
    experiment_id = str(experiment.get("experiment", "")).strip() or "none"
    stage = str(experiment.get("stage", "unknown"))
    warnings: list[str] = []
    experiment_campaign = str(experiment.get("campaign", "")).strip()
    if experiment_id != "none" and experiment_campaign != raw_campaign_id:
        warnings.append(
            f"active experiment {experiment_id} belongs to campaign "
            f"{experiment_campaign or 'none'}, not {campaign_id}"
        )

    observation = observe_experiments(config.root, raw_campaign_id)
    warnings.extend(observation.warnings)
    current_status = str(experiment.get("status", "")).strip().lower()
    if (
        experiment_id != "none"
        and current_status == "closed"
        and experiment_id not in observation.closed_ids
    ):
        warnings.append(
            f"closed current experiment {experiment_id} has not been archived under experiments/"
        )

    return (
        f"{campaign_id} {status}, active={experiment_id}, stage={stage}",
        f"{observation.current_campaign_closed} closed in {campaign_id}, "
        f"{observation.total_closed} closed across workspace",
        warnings,
    )


def observe_experiments(root: Path, current_campaign: str) -> ExperimentObservation:
    experiment_root = root / "experiments"
    candidates = set(experiment_root.glob("*.md"))
    candidates.update(experiment_root.glob("*/EXPERIMENT.md"))
    closed: dict[str, str] = {}
    warnings: list[str] = []

    for path in sorted(candidates):
        try:
            metadata = read_toml_frontmatter(path)
        except FrontmatterError as exc:
            warnings.append(str(exc))
            continue
        experiment_id = str(metadata.get("experiment", metadata.get("id", ""))).strip()
        if not experiment_id:
            if path.name != "EXPERIMENT_TEMPLATE.md":
                warnings.append(f"{path} has no experiment identifier")
            continue
        if experiment_id in closed:
            warnings.append(f"duplicate closed experiment identifier {experiment_id}")
            continue

        campaign_id = str(metadata.get("campaign", "")).strip()
        record_status = str(metadata.get("status", "")).strip().lower()
        decision = str(metadata.get("decision", "")).strip().lower()
        if record_status != "closed":
            warnings.append(f"{path} is archived but status is not closed")
            continue
        if decision not in TERMINAL_DECISIONS:
            warnings.append(f"{path} has no valid terminal decision")
            continue
        if not campaign_id:
            warnings.append(f"{path} has no campaign identifier")
            continue
        closed[experiment_id] = campaign_id

    current_count = sum(
        1 for campaign_id in closed.values() if campaign_id == current_campaign
    )
    return ExperimentObservation(
        current_campaign_closed=current_count,
        total_closed=len(closed),
        closed_ids=frozenset(closed),
        warnings=tuple(warnings),
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
