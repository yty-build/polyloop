from pathlib import Path

from polyloop.config import load_config, write_default_config
from polyloop.providers import build_launch_argv, load_role_context, startup_prompt


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


def test_codex_manager_can_activate_a_ready_campaign_without_typed_slash_command() -> (
    None
):
    prompt = startup_prompt("manager", "codex")

    assert "auto_start = true" in prompt
    assert "directly create or resume the native goal" in prompt
    assert "do not merely print a /goal command" in prompt
    assert "First read only the TOML front matter" in prompt
    assert "If and only if activation is eligible" in prompt
    assert "do not load domain skills or sync skills" in prompt


def test_worker_still_waits_for_a_finite_manager_assignment() -> None:
    prompt = startup_prompt("builder", "codex")

    assert "initialization only" in prompt
    assert "wait for a finite manager assignment" in prompt
    assert "auto_start" not in prompt


def test_external_researcher_is_injected_only_into_council(
    tmp_path: Path,
) -> None:
    write_default_config(
        tmp_path,
        session="research-test",
        description="test",
        provider="codex",
    )
    roles = tmp_path / "roles"
    roles.mkdir()
    (roles / "shared.md").write_text("SHARED\n", encoding="utf-8")
    (roles / "council.md").write_text("COUNCIL\n", encoding="utf-8")
    (roles / "manager.md").write_text("MANAGER\n", encoding="utf-8")
    config = load_config(tmp_path)

    council = load_role_context(config, "council")
    manager = load_role_context(config, "manager")

    assert "Function: external-researcher" in council
    assert "grok --yolo" in council
    assert "Function: external-researcher" not in manager
