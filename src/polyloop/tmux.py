from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path

from .config import ProjectConfig
from .constants import EXTERNAL_RESEARCHER_WINDOW, ROLES, SHELL_COMMANDS, __version__
from .providers import (
    build_launch_argv,
    build_launch_command,
    load_role_context,
    provider_available,
    startup_prompt,
)


class TmuxError(RuntimeError):
    """Raised when tmux cannot create or inspect a Polyloop session."""


@dataclass(frozen=True)
class WindowState:
    name: str
    index: int
    panes: int
    dead: bool
    command: str
    pid: int
    role_marker: str
    provider_marker: str


@dataclass
class EnsureResult:
    created_session: bool
    created_windows: list[str]
    launched_roles: list[str]
    launched_tools: list[str]
    warnings: list[str]


class Tmux:
    def __init__(self) -> None:
        self.base = ["tmux"]
        socket_name = os.environ.get("POLYLOOP_TMUX_SOCKET", "").strip()
        if socket_name:
            self.base.extend(["-L", socket_name])

    def available(self) -> bool:
        try:
            result = subprocess.run(
                [*self.base, "-V"], capture_output=True, text=True, check=False
            )
        except FileNotFoundError:
            return False
        return result.returncode == 0

    def run(self, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
        try:
            result = subprocess.run(
                [*self.base, *args], capture_output=True, text=True, check=False
            )
        except FileNotFoundError as exc:
            raise TmuxError("tmux is not installed or not on PATH") from exc
        if check and result.returncode != 0:
            detail = (
                result.stderr.strip() or result.stdout.strip() or "tmux command failed"
            )
            raise TmuxError(detail)
        return result

    def session_exists(self, session: str) -> bool:
        return self.run("has-session", "-t", session, check=False).returncode == 0

    def get_session_option(self, session: str, option: str) -> str:
        result = self.run("show-options", "-qv", "-t", session, option, check=False)
        return result.stdout.strip() if result.returncode == 0 else ""

    def set_session_option(self, session: str, option: str, value: str) -> None:
        self.run("set-option", "-q", "-t", session, option, value)

    def set_window_option(self, target: str, option: str, value: str) -> None:
        self.run("set-window-option", "-q", "-t", target, option, value)

    def list_windows(self, session: str) -> list[WindowState]:
        format_string = "\t".join(
            (
                "#{window_name}",
                "#{window_index}",
                "#{window_panes}",
                "#{pane_dead}",
                "#{pane_current_command}",
                "#{pane_pid}",
                "#{@polyloop_role}",
                "#{@polyloop_provider}",
            )
        )
        result = self.run("list-windows", "-t", session, "-F", format_string)
        windows: list[WindowState] = []
        for line in result.stdout.splitlines():
            parts = line.split("\t")
            if len(parts) != 8:
                continue
            name, index, panes, dead, command, pid, role, provider = parts
            windows.append(
                WindowState(
                    name=name,
                    index=int(index),
                    panes=int(panes),
                    dead=dead == "1",
                    command=command,
                    pid=int(pid or 0),
                    role_marker=role,
                    provider_marker=provider,
                )
            )
        return windows

    def set_environment(self, session: str, key: str, value: str) -> None:
        self.run("set-environment", "-t", session, key, value)

    def unset_environment(self, session: str, key: str) -> None:
        self.run("set-environment", "-u", "-t", session, key, check=False)


def ensure_tmux_session(
    config: ProjectConfig,
    *,
    launch: bool,
    restart: bool,
    adopt: bool,
    tmux: Tmux | None = None,
) -> EnsureResult:
    tmux = tmux or Tmux()
    if not tmux.available():
        raise TmuxError("tmux is not installed or not available")

    result = EnsureResult(False, [], [], [], [])
    exists = tmux.session_exists(config.session)
    if exists:
        owner = tmux.get_session_option(config.session, "@polyloop_root")
        if owner and Path(owner).expanduser().resolve() != config.root:
            raise TmuxError(
                f"tmux session {config.session!r} belongs to {owner}, not {config.root}"
            )
        if not owner and not adopt:
            raise TmuxError(
                f"tmux session {config.session!r} already exists and is not managed by Polyloop; "
                "rerun with --adopt to add role windows without deleting existing windows"
            )
    else:
        tmux.run(
            "new-session",
            "-d",
            "-s",
            config.session,
            "-n",
            ROLES[0],
            "-c",
            str(config.root),
        )
        result.created_session = True

    windows = tmux.list_windows(config.session)
    duplicate_names = _duplicate_window_names(windows)
    if duplicate_names:
        raise TmuxError(
            "duplicate tmux window names prevent safe role targeting: "
            + ", ".join(duplicate_names)
        )
    managed_windows = set(ROLES)
    if config.external_researcher:
        managed_windows.add(EXTERNAL_RESEARCHER_WINDOW)
    for window in windows:
        if (
            window.name in managed_windows
            and window.role_marker
            and window.role_marker != window.name
        ):
            raise TmuxError(
                f"window {config.session}:{window.name} is marked for role "
                f"{window.role_marker!r}; refusing to claim the session"
            )

    tmux.set_session_option(config.session, "@polyloop_root", str(config.root))
    tmux.set_session_option(config.session, "@polyloop_version", __version__)
    tmux.set_session_option(config.session, "@polyloop_description", config.description)
    tmux.set_environment(config.session, "POLYLOOP_SESSION", config.session)
    tmux.set_environment(config.session, "POLYLOOP_ROOT", str(config.root))
    tmux.unset_environment(config.session, "POLYLOOP_CAMPAIGN")
    if os.environ.get("PATH"):
        tmux.set_environment(config.session, "PATH", os.environ["PATH"])

    by_name = {window.name: window for window in windows}

    for role_name in ROLES:
        target = f"{config.session}:{role_name}"
        window = by_name.get(role_name)
        if window is None:
            tmux.run(
                "new-window",
                "-d",
                "-t",
                config.session,
                "-n",
                role_name,
                "-c",
                str(config.root),
            )
            result.created_windows.append(role_name)
            window = next(
                item
                for item in tmux.list_windows(config.session)
                if item.name == role_name
            )
        elif window.role_marker and window.role_marker != role_name:
            raise TmuxError(
                f"window {target} is marked for role {window.role_marker!r}; refusing to reuse it"
            )

        tmux.set_window_option(target, "@polyloop_role", role_name)
        tmux.set_window_option(target, "remain-on-exit", "on")

        if not launch:
            continue
        role = config.roles[role_name]
        if not provider_available(role.provider):
            result.warnings.append(
                f"{role_name}: provider executable {role.provider!r} is not installed"
            )
            continue

        should_launch = restart or window.dead or window.command in SHELL_COMMANDS
        if not should_launch:
            if window.provider_marker and window.provider_marker != role.provider:
                result.warnings.append(
                    f"{role_name}: running {window.provider_marker}, configured for {role.provider}; "
                    "use polyloop init --restart to apply the change"
                )
            continue

        context = load_role_context(config, role_name)
        argv = build_launch_argv(
            config,
            role,
            role_context=context,
            startup_prompt=startup_prompt(role_name, role.provider),
        )
        tmux.run(
            "respawn-pane",
            "-k",
            "-t",
            target,
            "-c",
            str(config.root),
            build_launch_command(argv),
        )
        tmux.set_window_option(target, "@polyloop_provider", role.provider)
        result.launched_roles.append(role_name)

    researcher = config.external_researcher
    if researcher:
        target = f"{config.session}:{EXTERNAL_RESEARCHER_WINDOW}"
        window = by_name.get(EXTERNAL_RESEARCHER_WINDOW)
        if window is None:
            tmux.run(
                "new-window",
                "-d",
                "-t",
                config.session,
                "-n",
                EXTERNAL_RESEARCHER_WINDOW,
                "-c",
                str(config.root),
            )
            result.created_windows.append(EXTERNAL_RESEARCHER_WINDOW)
            window = next(
                item
                for item in tmux.list_windows(config.session)
                if item.name == EXTERNAL_RESEARCHER_WINDOW
            )
        elif window.role_marker and window.role_marker != EXTERNAL_RESEARCHER_WINDOW:
            raise TmuxError(
                f"window {target} is marked for role {window.role_marker!r}; "
                "refusing to reuse it"
            )

        tmux.set_window_option(target, "@polyloop_role", EXTERNAL_RESEARCHER_WINDOW)
        tmux.set_window_option(target, "remain-on-exit", "on")

        if launch:
            executable = researcher.command[0]
            if shutil.which(executable) is None:
                result.warnings.append(
                    f"{EXTERNAL_RESEARCHER_WINDOW}: executable {executable!r} "
                    "is not installed"
                )
            else:
                should_launch = (
                    restart or window.dead or window.command in SHELL_COMMANDS
                )
                if not should_launch:
                    if (
                        window.provider_marker
                        and window.provider_marker != researcher.provider
                    ):
                        result.warnings.append(
                            f"{EXTERNAL_RESEARCHER_WINDOW}: running "
                            f"{window.provider_marker}, configured for "
                            f"{researcher.provider}; use polyloop init --restart "
                            "to apply the change"
                        )
                else:
                    tmux.run(
                        "respawn-pane",
                        "-k",
                        "-t",
                        target,
                        "-c",
                        str(config.root),
                        build_launch_command(list(researcher.command)),
                    )
                    tmux.set_window_option(
                        target, "@polyloop_provider", researcher.provider
                    )
                    result.launched_tools.append(EXTERNAL_RESEARCHER_WINDOW)

    tmux.run("select-window", "-t", f"{config.session}:manager")
    return result


def upsert_tmux_note(path: Path | None, session: str, description: str) -> str | None:
    if path is None or not description.strip():
        return None
    clean_description = " ".join(description.replace("|", "/").splitlines()).strip()
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        existing = (
            path.read_text(encoding="utf-8").splitlines() if path.exists() else []
        )
        lines = [line for line in existing if not line.startswith(f"{session}|")]
        lines.append(f"{session}|{clean_description}")
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", dir=path.parent, delete=False
        ) as handle:
            handle.write("\n".join(lines) + "\n")
            temporary = Path(handle.name)
        temporary.replace(path)
    except OSError as exc:
        return f"could not update {path}: {exc}"
    return None


def _duplicate_window_names(windows: list[WindowState]) -> list[str]:
    seen: set[str] = set()
    duplicates: set[str] = set()
    for window in windows:
        if window.name in seen:
            duplicates.add(window.name)
        seen.add(window.name)
    return sorted(duplicates)
