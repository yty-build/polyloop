from __future__ import annotations

import shlex
import shutil
from pathlib import Path

from .config import ProjectConfig, RoleConfig


PROVIDER_EXECUTABLES = {
    "codex": "codex",
    "claude": "claude",
    "grok": "grok",
    "opencode": "opencode",
}


def provider_available(provider: str) -> bool:
    return shutil.which(PROVIDER_EXECUTABLES[provider]) is not None


def build_launch_argv(
    config: ProjectConfig,
    role: RoleConfig,
    *,
    role_context: str,
    startup_prompt: str,
) -> list[str]:
    root = str(config.root)
    session_label = f"{config.session}-{role.name}"
    full_prompt = (
        f"{role_context.rstrip()}\n\nStartup instruction:\n{startup_prompt.strip()}"
    )

    if role.provider == "codex":
        common = ["-C", root]
        if role.model:
            common.extend(["--model", role.model])
        if role.effort:
            common.extend(["--config", f'model_reasoning_effort="{role.effort}"'])
        common.extend(role.extra_args)
        if role.resume_session:
            return ["codex", "resume", *common, role.resume_session, full_prompt]
        return ["codex", *common, full_prompt]

    if role.provider == "claude":
        args = [
            "claude",
            "--name",
            session_label,
            "--append-system-prompt",
            role_context,
        ]
        if role.model:
            args.extend(["--model", role.model])
        if role.effort:
            args.extend(["--effort", role.effort])
        args.extend(role.extra_args)
        if role.resume_session:
            args.extend(["--resume", role.resume_session])
        args.append(startup_prompt)
        return args

    if role.provider == "grok":
        args = ["grok", "--cwd", root, "--rules", role_context]
        if role.model:
            args.extend(["--model", role.model])
        if role.effort:
            args.extend(["--effort", role.effort])
        args.extend(role.extra_args)
        if role.resume_session:
            args.extend(["--resume", role.resume_session])
        args.append(startup_prompt)
        return args

    args = ["opencode", root]
    if role.model:
        args.extend(["--model", role.model])
    args.extend(role.extra_args)
    if role.resume_session:
        args.extend(["--session", role.resume_session])
    args.extend(["--prompt", full_prompt])
    return args


def build_launch_command(argv: list[str]) -> str:
    return "exec " + shlex.join(argv)


def load_role_context(root: Path, role_name: str) -> str:
    shared_path = root / "roles" / "shared.md"
    role_path = root / "roles" / f"{role_name}.md"
    shared = shared_path.read_text(encoding="utf-8")
    role = role_path.read_text(encoding="utf-8")
    return (
        "# Polyloop Runtime Contract\n\n"
        f"Workspace: {root}\n"
        f"Role: {role_name}\n\n"
        f"{shared.rstrip()}\n\n{role.rstrip()}\n"
    )


def startup_prompt(role_name: str) -> str:
    if role_name == "manager":
        return (
            "Read PROJECT_CHARTER.md, CAMPAIGN.md, CURRENT_EXPERIMENT.md, "
            "LEADERBOARD.md, and LESSONS.md. This is initialization only. "
            "Reply exactly 'READY: manager' and wait for the user to activate "
            "the bounded campaign goal. Do not modify files or dispatch work yet."
        )
    return (
        "Read PROJECT_CHARTER.md, CAMPAIGN.md, CURRENT_EXPERIMENT.md, "
        "LEADERBOARD.md, and LESSONS.md. This is initialization only. "
        f"Reply exactly 'READY: {role_name}' and wait for a finite manager assignment. "
        "Do not modify files or begin work yet."
    )
