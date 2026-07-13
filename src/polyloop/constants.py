from __future__ import annotations

__version__ = "0.9.1"

ROLES = (
    "manager",
    "council",
    "builder",
    "validator",
    "reality",
    "retrospector",
)

BOT_BUILDER_ROLE = "bot-builder"
ROLE_FUNCTIONS = (
    "manager",
    "council",
    "builder",
    "validator",
    "reality",
    BOT_BUILDER_ROLE,
    "retrospector",
)
FUNCTION_BY_ROLE = {role: role for role in ROLE_FUNCTIONS}

LEGACY_ROLE_NAMES = {
    "council": ("strat-council",),
    "builder": ("strat-builder",),
    "validator": ("strat-verifier", "verifier"),
    "reality": ("bot-reality",),
    BOT_BUILDER_ROLE: ("bot-integrator",),
}
LEGACY_WINDOW_NAMES = {
    "strat-council": "council",
    "strat-builder": "builder",
    "strat-verifier": "validator",
    "verifier": "validator",
    "bot-reality": "reality",
}
LEGACY_FUNCTION_NAMES = {
    "strat-council": "council",
    "strat-builder": "builder",
    "strat-verifier": "validator",
    "verifier": "validator",
    "bot-reality": "reality",
    "reality-controller": "reality",
    "bot-integrator": BOT_BUILDER_ROLE,
}

EXTERNAL_RESEARCHER_WINDOW = "external-researcher"

PROVIDERS = ("codex", "claude", "grok", "opencode")
EFFORT_LEVELS = ("low", "medium", "high", "xhigh", "max")
SHELL_COMMANDS = {"bash", "dash", "fish", "sh", "zsh"}
