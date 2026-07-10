from pathlib import Path

from polyloop.config import load_config, write_default_config
from polyloop.providers import build_launch_argv


def _config(tmp_path: Path, provider: str):
    write_default_config(
        tmp_path,
        session="test-strategy",
        description="test",
        provider=provider,
    )
    return load_config(tmp_path)


def test_codex_launch_contains_root_effort_and_context(tmp_path: Path) -> None:
    config = _config(tmp_path, "codex")
    argv = build_launch_argv(
        config,
        config.roles["manager"],
        role_context="ROLE CONTRACT",
        startup_prompt="WAIT",
    )

    assert argv[:3] == ["codex", "-C", str(tmp_path)]
    assert 'model_reasoning_effort="high"' in argv
    assert "ROLE CONTRACT" in argv[-1]
    assert "WAIT" in argv[-1]


def test_claude_uses_role_contract_as_system_context(tmp_path: Path) -> None:
    config = _config(tmp_path, "claude")
    argv = build_launch_argv(
        config,
        config.roles["council"],
        role_context="COUNCIL CONTRACT",
        startup_prompt="WAIT",
    )

    assert argv[0] == "claude"
    assert argv[argv.index("--name") + 1] == "test-strategy-council"
    assert argv[argv.index("--append-system-prompt") + 1] == "COUNCIL CONTRACT"
    assert argv[-1] == "WAIT"


def test_grok_uses_rules_and_working_directory(tmp_path: Path) -> None:
    config = _config(tmp_path, "grok")
    argv = build_launch_argv(
        config,
        config.roles["verifier"],
        role_context="VERIFY CONTRACT",
        startup_prompt="WAIT",
    )

    assert argv[:3] == ["grok", "--cwd", str(tmp_path)]
    assert argv[argv.index("--rules") + 1] == "VERIFY CONTRACT"
