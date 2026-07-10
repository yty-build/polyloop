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
        campaign_id="C001",
        max_experiments=4,
        provider="codex",
    )
    config = load_config(tmp_path)

    assert config.session == "btc5m-straddle"
    assert config.description == "BTC 5-minute research"
    assert config.notes_file == notes
    assert config.campaign.campaign_id == "C001"
    assert config.campaign.max_experiments == 4
    assert set(config.roles) == {
        "manager",
        "council",
        "builder",
        "verifier",
        "reality",
        "retrospector",
    }
    assert all(role.provider == "codex" for role in config.roles.values())


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
            campaign_id="C001",
            max_experiments=1,
            provider="codex",
        )
