from __future__ import annotations

__version__ = "0.6.0"

ROLES = (
    "manager",
    "council",
    "builder",
    "verifier",
    "reality",
    "retrospector",
)

BOT_INTEGRATOR_ROLE = "bot-integrator"
ROLE_FUNCTIONS = (
    "manager",
    "council",
    "builder",
    "verifier",
    "reality",
    BOT_INTEGRATOR_ROLE,
    "retrospector",
)
REALITY_CONTROLLER_FUNCTION = "reality-controller"
FUNCTION_BY_ROLE = {
    **{role: role for role in ROLES},
    "reality": REALITY_CONTROLLER_FUNCTION,
    BOT_INTEGRATOR_ROLE: BOT_INTEGRATOR_ROLE,
}

EXTERNAL_RESEARCHER_WINDOW = "external-researcher"

PROVIDERS = ("codex", "claude", "grok", "opencode")
EFFORT_LEVELS = ("low", "medium", "high", "xhigh", "max")
SHELL_COMMANDS = {"bash", "dash", "fish", "sh", "zsh"}
