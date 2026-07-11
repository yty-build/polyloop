from __future__ import annotations

__version__ = "0.7.0"

ROLES = (
    "manager",
    "strat-council",
    "strat-builder",
    "strat-verifier",
    "bot-reality",
    "retrospector",
)

BOT_INTEGRATOR_ROLE = "bot-integrator"
ROLE_FUNCTIONS = (
    "manager",
    "strat-council",
    "strat-builder",
    "strat-verifier",
    "bot-reality",
    BOT_INTEGRATOR_ROLE,
    "retrospector",
)
FUNCTION_BY_ROLE = {role: role for role in ROLE_FUNCTIONS}

LEGACY_ROLE_NAMES = {
    "strat-council": "council",
    "strat-builder": "builder",
    "strat-verifier": "verifier",
    "bot-reality": "reality",
}
LEGACY_WINDOW_NAMES = {legacy: current for current, legacy in LEGACY_ROLE_NAMES.items()}
LEGACY_FUNCTION_NAMES = {
    "council": "strat-council",
    "builder": "strat-builder",
    "verifier": "strat-verifier",
    "reality-controller": "bot-reality",
}

EXTERNAL_RESEARCHER_WINDOW = "external-researcher"

PROVIDERS = ("codex", "claude", "grok", "opencode")
EFFORT_LEVELS = ("low", "medium", "high", "xhigh", "max")
SHELL_COMMANDS = {"bash", "dash", "fish", "sh", "zsh"}
