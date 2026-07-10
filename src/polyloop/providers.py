from __future__ import annotations

import shlex
import shutil

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


def load_role_context(config: ProjectConfig, role_name: str) -> str:
    root = config.root
    shared_path = root / "roles" / "shared.md"
    role_path = root / "roles" / f"{role_name}.md"
    shared = shared_path.read_text(encoding="utf-8")
    role = role_path.read_text(encoding="utf-8")
    context = (
        "# Polyloop Runtime Contract\n\n"
        f"Workspace: {root}\n"
        f"Role: {role_name}\n\n"
        f"{shared.rstrip()}\n\n{role.rstrip()}\n"
    )
    researcher = config.external_researcher
    if role_name == "council" and researcher and researcher.enabled:
        context += (
            "\n# External Researcher Runtime\n\n"
            "Function: external-researcher\n"
            f"Provider: {researcher.provider}\n"
            f"Command prefix: {shlex.join(researcher.command)}\n\n"
            "Append exactly one bounded research brief as the final command argument. "
            "Capture and parse stdout as the response. Do not start a persistent process.\n"
        )
    return context


def startup_prompt(role_name: str, provider: str = "codex") -> str:
    if role_name == "manager":
        if provider == "codex":
            native_goal = (
                "For Codex, directly create or resume the native goal; do not merely "
                "print a /goal command for the human to type. "
            )
        else:
            native_goal = (
                "Use the provider's native durable goal or loop control when available; "
                "otherwise report that the campaign is ready and wait. "
            )
        return (
            "First read only the TOML front matter in CAMPAIGN.md and run polyloop "
            "status. If the campaign is not status ready or active with auto_start = "
            "true, immediately reply 'READY: manager' with the missing activation "
            "conditions and wait. In that waiting path, do not load domain skills or "
            "sync skills; do not access external systems, modify files, or dispatch work. "
            "If and only if activation is eligible, read AGENTS.md, PROJECT_CHARTER.md, "
            "the full CAMPAIGN.md, CURRENT_EXPERIMENT.md, LEADERBOARD.md, and LESSONS.md. "
            "Validate its finite objective, stopping conditions, starting evidence, "
            "evaluator, paper requirement, resource boundary, and safety limits. "
            + native_goal
            + "Use the Manager Goal Primer as the objective, mark a ready campaign active "
            "after the goal is attached, and begin the manager loop. If validation fails, "
            "report the blockers, leave the campaign unstarted, and wait. Never start a "
            "different campaign."
        )
    return (
        "Read AGENTS.md, PROJECT_CHARTER.md, CAMPAIGN.md, CURRENT_EXPERIMENT.md, "
        "LEADERBOARD.md, and LESSONS.md. This is initialization only. "
        f"Reply exactly 'READY: {role_name}' and wait for a finite manager assignment. "
        "Do not modify files or begin work yet."
    )
