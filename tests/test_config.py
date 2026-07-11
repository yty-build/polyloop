from pathlib import Path

import pytest

from polyloop.config import ConfigError, load_config, write_default_config


def test_default_config_round_trip(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    notes = tmp_path / "tmux-notes"
    monkeypatch.setenv("POLYLOOP_NOTES_FILE", str(notes))

    write_default_config(
        tmp_path,
        session="btc5m-straddle",
        description="BTC 5-minute research",
        provider="codex",
    )
    config = load_config(tmp_path)

    assert config.session == "btc5m-straddle"
    assert config.description == "BTC 5-minute research"
    assert config.notes_file == notes
    assert "[campaign]" not in (tmp_path / "polyloop.toml").read_text(encoding="utf-8")
    assert set(config.roles) == {
        "manager",
        "strat-council",
        "strat-builder",
        "strat-verifier",
        "bot-reality",
        "retrospector",
        "bot-integrator",
    }
    assert all(role.provider == "codex" for role in config.roles.values())
    assert config.external_researcher is not None
    assert config.external_researcher.provider == "grok"
    assert config.external_researcher.command == ("grok", "--yolo")
    assert (
        "sandbox_workspace_write.network_access=true"
        in config.roles["strat-builder"].extra_args
    )
    assert (
        "sandbox_workspace_write.network_access=true"
        in config.roles["strat-verifier"].extra_args
    )


def test_config_inherits_bot_reality_settings_for_bot_integrator(
    tmp_path: Path,
) -> None:
    path = write_default_config(
        tmp_path,
        session="legacy-reality",
        description="legacy",
        provider="codex",
    )
    content = path.read_text(encoding="utf-8")
    start = content.index("\n[roles.bot-integrator]")
    end = content.index("\n[roles.retrospector]", start)
    path.write_text(content[:start] + content[end:], encoding="utf-8")

    config = load_config(tmp_path)

    assert config.roles["bot-integrator"].provider == "codex"
    assert (
        "sandbox_workspace_write.network_access=true"
        in config.roles["bot-integrator"].extra_args
    )
    assert config.roles["bot-integrator"].resume_session == ""


def test_legacy_role_names_are_loaded_as_current_functions(tmp_path: Path) -> None:
    path = write_default_config(
        tmp_path,
        session="legacy-names",
        description="legacy",
        provider="codex",
    )
    content = path.read_text(encoding="utf-8")
    for current, legacy in (
        ("strat-council", "council"),
        ("strat-builder", "builder"),
        ("strat-verifier", "verifier"),
        ("bot-reality", "reality"),
    ):
        content = content.replace(f"[roles.{current}]", f"[roles.{legacy}]")
    path.write_text(content, encoding="utf-8")

    config = load_config(tmp_path)

    assert set(config.roles) == {
        "manager",
        "strat-council",
        "strat-builder",
        "strat-verifier",
        "bot-reality",
        "bot-integrator",
        "retrospector",
    }


def test_external_researcher_must_have_a_command(tmp_path: Path) -> None:
    path = write_default_config(
        tmp_path,
        session="bad-researcher",
        description="bad",
        provider="codex",
    )
    content = path.read_text(encoding="utf-8")
    start = content.index("command = [")
    end = content.index("\n", start)
    path.write_text(content[:start] + "command = []" + content[end:], encoding="utf-8")

    with pytest.raises(ConfigError, match="non-empty array"):
        load_config(tmp_path)


@pytest.mark.parametrize(
    "session",
    ("bad session", "bad:session", "-leading-dash", "x" * 65),
)
def test_invalid_session_names_are_rejected(tmp_path: Path, session: str) -> None:
    with pytest.raises(ConfigError):
        write_default_config(
            tmp_path,
            session=session,
            description="bad",
            provider="codex",
        )


def test_legacy_campaign_table_is_ignored(tmp_path: Path) -> None:
    path = write_default_config(
        tmp_path,
        session="legacy-strategy",
        description="legacy",
        provider="codex",
    )
    with path.open("a", encoding="utf-8") as handle:
        handle.write('\n[campaign]\nid = "C001"\nmax_experiments = 20\n')

    config = load_config(tmp_path)

    assert config.session == "legacy-strategy"
