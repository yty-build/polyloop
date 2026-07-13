from __future__ import annotations

import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path

from .config import ProjectConfig
from .constants import (
    BOT_BUILDER_ROLE,
    EXTERNAL_RESEARCHER_WINDOW,
    FUNCTION_BY_ROLE,
    ROLE_FUNCTIONS,
    ROLES,
    SHELL_COMMANDS,
)
from .frontmatter import FrontmatterError, read_toml_frontmatter
from .providers import PROVIDER_EXECUTABLES
from .tmux import PaneState, Tmux, TmuxError, WindowState


@dataclass(frozen=True)
class StatusReport:
    text: str
    healthy: bool


@dataclass(frozen=True)
class ExperimentObservation:
    current_campaign_recorded: int
    total_recorded: int
    recorded_ids: frozenset[str]
    warnings: tuple[str, ...]


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

    researcher_line, researcher_warning = _external_researcher_status(config)
    lines.append(f"Research:  {researcher_line}")

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
        panes = tmux.list_panes(config.session)
    except TmuxError as exc:
        lines.extend(("", f"Could not inspect windows: {exc}"))
        return StatusReport("\n".join(lines), False)
    by_name = {window.name: window for window in windows}

    rows: list[tuple[str, str, str, str, str]] = []
    warnings: list[str] = []
    panes_by_function: dict[str, PaneState] = {}
    for pane in panes:
        if not pane.function_marker:
            continue
        if pane.function_marker in panes_by_function:
            warnings.append(f"multiple panes are marked {pane.function_marker}")
            healthy = False
            continue
        panes_by_function[pane.function_marker] = pane

    for role_name in ROLE_FUNCTIONS:
        function_name = FUNCTION_BY_ROLE[role_name]
        role = config.roles[role_name]
        executable = PROVIDER_EXECUTABLES[role.provider]
        installed = shutil.which(executable) is not None
        pane = panes_by_function.get(function_name)
        state, process = _pane_state(pane)
        if not installed:
            state = "MISSING CLI"
            healthy = False
        if pane is None or pane.dead:
            healthy = False
        expected_window = "reality" if role_name == BOT_BUILDER_ROLE else role_name
        if pane and pane.window_name != expected_window:
            warnings.append(
                f"{function_name} is in window {pane.window_name}, expected "
                f"{expected_window}"
            )
            state = "CONFIG DRIFT"
            healthy = False
        if pane and pane.provider_marker and pane.provider_marker != role.provider:
            warnings.append(
                f"{function_name} is marked {pane.provider_marker}, configured "
                f"{role.provider}"
            )
            state = "CONFIG DRIFT"
            healthy = False
        rows.append(
            (
                function_name,
                role.provider,
                role.effort or "default",
                state,
                process,
            )
        )

    researcher = config.external_researcher
    if researcher:
        window = by_name.get(EXTERNAL_RESEARCHER_WINDOW)
        state, process = _window_state(window)
        installed = shutil.which(researcher.command[0]) is not None
        if not installed:
            state = "MISSING CLI"
        elif window is None or window.dead:
            healthy = False
            warnings.append(f"{EXTERNAL_RESEARCHER_WINDOW} window is {state.lower()}")
        if (
            window
            and window.provider_marker
            and window.provider_marker != researcher.provider
        ):
            warnings.append(
                f"{EXTERNAL_RESEARCHER_WINDOW} is marked "
                f"{window.provider_marker}, configured {researcher.provider}"
            )
            state = "CONFIG DRIFT"
            healthy = False
        rows.append(
            (
                EXTERNAL_RESEARCHER_WINDOW,
                researcher.provider,
                "n/a",
                state,
                process,
            )
        )

    lines.extend(("", _format_table(rows)))
    expected_windows = set(ROLES)
    if researcher:
        expected_windows.add(EXTERNAL_RESEARCHER_WINDOW)
    extra_windows = sorted(set(by_name) - expected_windows)
    if extra_windows:
        warnings.append("extra tmux windows: " + ", ".join(extra_windows))
    unclaimed_panes = [
        f"{pane.window_name}.{pane.index}"
        for pane in panes
        if pane.window_name in ROLES and not pane.function_marker
    ]
    if unclaimed_panes:
        warnings.append("unclaimed managed panes: " + ", ".join(unclaimed_panes))
    warnings.extend(campaign_warnings)
    if researcher_warning:
        warnings.append(researcher_warning)
    if git_warning:
        warnings.append(git_warning)
    if warnings:
        lines.append("\nWarnings:")
        lines.extend(f"- {warning}" for warning in warnings)
    lines.extend(("", f"Attach: tattach {config.session}"))
    return StatusReport("\n".join(lines), healthy)


def _external_researcher_status(
    config: ProjectConfig,
) -> tuple[str, str | None]:
    researcher = config.external_researcher
    if researcher is None:
        return "not configured", None
    executable = researcher.command[0]
    if shutil.which(executable) is None:
        return (
            f"{researcher.provider} missing ({executable})",
            f"external researcher executable {executable!r} is not installed",
        )
    return f"{researcher.provider} ready ({executable})", None


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
    raw_auto_start = campaign.get("auto_start", False)
    auto_start = raw_auto_start if isinstance(raw_auto_start, bool) else False
    experiment_id = str(experiment.get("experiment", "")).strip() or "none"
    stage = str(experiment.get("stage", "unknown"))
    warnings: list[str] = []
    if not isinstance(raw_auto_start, bool):
        warnings.append("CAMPAIGN.md auto_start must be a TOML boolean")
    if auto_start and status not in {"ready", "active"}:
        warnings.append(
            f"campaign auto_start is enabled while status is {status}; manager will not activate it"
        )
    experiment_campaign = str(experiment.get("campaign", "")).strip()
    if experiment_id != "none" and experiment_campaign != raw_campaign_id:
        warnings.append(
            f"active experiment {experiment_id} belongs to campaign "
            f"{experiment_campaign or 'none'}, not {campaign_id}"
        )

    observation = observe_experiments(
        config.root,
        raw_campaign_id,
        current_experiment=experiment_id if experiment_id != "none" else "",
        current_experiment_campaign=experiment_campaign,
    )
    warnings.extend(observation.warnings)

    return (
        f"{campaign_id} {status}, auto-start={'on' if auto_start else 'off'}, "
        f"active={experiment_id}, stage={stage}",
        f"{observation.current_campaign_recorded} recorded in {campaign_id}, "
        f"{observation.total_recorded} recorded across workspace",
        warnings,
    )


def observe_experiments(
    root: Path,
    current_campaign: str,
    *,
    current_experiment: str = "",
    current_experiment_campaign: str = "",
) -> ExperimentObservation:
    experiment_root = root / "experiments"
    candidates = set(experiment_root.glob("*.md"))
    candidates.update(experiment_root.glob("*/EXPERIMENT.md"))
    recorded: dict[str, str] = {}
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
        if experiment_id in recorded:
            warnings.append(f"duplicate experiment identifier {experiment_id}")
            continue

        campaign_id = str(metadata.get("campaign", "")).strip()
        if not campaign_id:
            warnings.append(f"{path} has no campaign identifier")
        recorded[experiment_id] = campaign_id

    if current_experiment and current_experiment not in recorded:
        recorded[current_experiment] = current_experiment_campaign or current_campaign

    current_count = sum(
        1 for campaign_id in recorded.values() if campaign_id == current_campaign
    )
    return ExperimentObservation(
        current_campaign_recorded=current_count,
        total_recorded=len(recorded),
        recorded_ids=frozenset(recorded),
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


def _pane_state(pane: PaneState | None) -> tuple[str, str]:
    if pane is None:
        return "MISSING", "-"
    if pane.dead:
        return "DEAD", pane.command or "-"
    if pane.command in SHELL_COMMANDS:
        return "IDLE", pane.command
    return "RUNNING", pane.command or "unknown"


def _format_table(rows: list[tuple[str, str, str, str, str]]) -> str:
    headers = ("FUNCTION", "PROVIDER", "EFFORT", "STATE", "PROCESS")
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
