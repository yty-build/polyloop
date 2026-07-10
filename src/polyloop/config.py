from __future__ import annotations

import json
import os
import re
import tomllib
from dataclasses import dataclass
from pathlib import Path

from .constants import BOT_INTEGRATOR_ROLE, EFFORT_LEVELS, PROVIDERS, ROLE_FUNCTIONS


class ConfigError(ValueError):
    """Raised when polyloop.toml is missing or invalid."""


SESSION_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]{0,63}$")


@dataclass(frozen=True)
class RoleConfig:
    name: str
    provider: str
    model: str
    effort: str
    resume_session: str
    extra_args: tuple[str, ...]


@dataclass(frozen=True)
class ExternalResearcherConfig:
    provider: str
    command: tuple[str, ...]


@dataclass(frozen=True)
class ProjectConfig:
    root: Path
    session: str
    description: str
    notes_file: Path | None
    external_researcher: ExternalResearcherConfig | None
    roles: dict[str, RoleConfig]


def validate_session_name(session: str) -> str:
    if not SESSION_PATTERN.fullmatch(session):
        raise ConfigError(
            "session must start with a letter or number and contain at most 64 "
            "letters, numbers, dots, underscores, or hyphens"
        )
    return session


def find_project_root(start: Path) -> Path:
    current = start.expanduser().resolve()
    for candidate in (current, *current.parents):
        if (candidate / "polyloop.toml").is_file():
            return candidate
    raise ConfigError(f"no polyloop.toml found from {current}")


def load_config(root: Path) -> ProjectConfig:
    root = root.expanduser().resolve()
    config_path = root / "polyloop.toml"
    try:
        with config_path.open("rb") as handle:
            raw = tomllib.load(handle)
    except FileNotFoundError as exc:
        raise ConfigError(f"missing {config_path}") from exc
    except tomllib.TOMLDecodeError as exc:
        raise ConfigError(f"invalid {config_path}: {exc}") from exc

    if raw.get("schema_version") != 1:
        raise ConfigError("polyloop.toml schema_version must be 1")

    session = validate_session_name(_required_string(raw, "session"))
    description = str(raw.get("description", "")).strip()
    notes_value = str(raw.get("notes_file", "")).strip()
    notes_file = (
        Path(os.path.expandvars(notes_value)).expanduser() if notes_value else None
    )

    external_researcher = _load_external_researcher(raw)

    roles_raw = raw.get("roles")
    if not isinstance(roles_raw, dict):
        raise ConfigError("polyloop.toml must contain [roles.*] tables")

    roles: dict[str, RoleConfig] = {}
    for role_name in ROLE_FUNCTIONS:
        role_raw = roles_raw.get(role_name)
        inherited = False
        if role_name == BOT_INTEGRATOR_ROLE and role_raw is None:
            role_raw = roles_raw.get("reality")
            inherited = True
        if not isinstance(role_raw, dict):
            raise ConfigError(f"missing [roles.{role_name}] table")
        provider = _required_string(role_raw, "provider")
        if provider not in PROVIDERS:
            raise ConfigError(
                f"roles.{role_name}.provider must be one of {', '.join(PROVIDERS)}"
            )
        effort = str(role_raw.get("effort", "")).strip()
        if effort and effort not in EFFORT_LEVELS:
            raise ConfigError(
                f"roles.{role_name}.effort must be one of {', '.join(EFFORT_LEVELS)}"
            )
        extra_args_raw = role_raw.get("extra_args", [])
        if not isinstance(extra_args_raw, list) or not all(
            isinstance(value, str) for value in extra_args_raw
        ):
            raise ConfigError(
                f"roles.{role_name}.extra_args must be an array of strings"
            )
        roles[role_name] = RoleConfig(
            name=role_name,
            provider=provider,
            model=str(role_raw.get("model", "")).strip(),
            effort=effort,
            resume_session=(
                "" if inherited else str(role_raw.get("resume_session", "")).strip()
            ),
            extra_args=tuple(extra_args_raw),
        )

    unknown_roles = sorted(set(roles_raw) - set(ROLE_FUNCTIONS))
    if unknown_roles:
        raise ConfigError(f"unknown role tables: {', '.join(unknown_roles)}")

    return ProjectConfig(
        root=root,
        session=session,
        description=description,
        notes_file=notes_file,
        external_researcher=external_researcher,
        roles=roles,
    )


def write_default_config(
    root: Path,
    *,
    session: str,
    description: str,
    provider: str,
) -> Path:
    validate_session_name(session)
    if provider not in PROVIDERS:
        raise ConfigError(f"provider must be one of {', '.join(PROVIDERS)}")
    notes_file = os.environ.get("POLYLOOP_NOTES_FILE", "~/.tmux-notes")
    effort_by_role = {
        "manager": "high",
        "council": "high",
        "builder": "high",
        "verifier": "high",
        "reality": "high",
        "retrospector": "high",
        BOT_INTEGRATOR_ROLE: "high",
    }

    lines = [
        "schema_version = 1",
        f"session = {_toml_string(session)}",
        f"description = {_toml_string(description)}",
        f"notes_file = {_toml_string(notes_file)}",
        "",
        "[external_researcher]",
        'provider = "grok"',
        "command = " + json.dumps(["grok", "--yolo"]),
    ]
    tmux_roles = {"manager", "council", "reality", BOT_INTEGRATOR_ROLE}
    for role in ROLE_FUNCTIONS:
        extra_args = (
            [
                "--sandbox",
                "workspace-write",
                "--config",
                "sandbox_workspace_write.network_access=true",
            ]
            if provider == "codex" and role in tmux_roles
            else []
        )
        lines.extend(
            [
                "",
                f"[roles.{role}]",
                f"provider = {_toml_string(provider)}",
                'model = ""',
                f"effort = {_toml_string(effort_by_role[role])}",
                'resume_session = ""',
                "extra_args = " + json.dumps(extra_args),
            ]
        )

    path = root / "polyloop.toml"
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def _required_string(data: dict[str, object], key: str) -> str:
    value = data.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ConfigError(f"{key} must be a non-empty string")
    return value.strip()


def _load_external_researcher(
    raw: dict[str, object],
) -> ExternalResearcherConfig | None:
    researcher_raw = raw.get("external_researcher")
    if researcher_raw is None:
        return None
    if not isinstance(researcher_raw, dict):
        raise ConfigError("external_researcher must be a TOML table")
    provider = _required_string(researcher_raw, "provider")
    command_raw = researcher_raw.get("command")
    if (
        not isinstance(command_raw, list)
        or not command_raw
        or not all(isinstance(value, str) and value for value in command_raw)
    ):
        raise ConfigError(
            "external_researcher.command must be a non-empty array of strings"
        )
    return ExternalResearcherConfig(
        provider=provider,
        command=tuple(command_raw),
    )


def _toml_string(value: str) -> str:
    return json.dumps(value, ensure_ascii=True)
