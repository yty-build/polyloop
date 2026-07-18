from pathlib import Path

import pytest

from polyloop.scaffold import ScaffoldError, create_project_files, ensure_git_repository


def test_scaffold_is_idempotent_and_does_not_overwrite(tmp_path: Path) -> None:
    arguments = {
        "session": "btc5m-straddle",
        "description": "BTC test",
        "market": "BTC 5-minute",
        "objective": "Test bounded loops",
    }
    first = create_project_files(tmp_path, **arguments)
    charter = tmp_path / "PROJECT_CHARTER.md"
    charter.write_text("human-owned charter\n", encoding="utf-8")

    second = create_project_files(tmp_path, **arguments)

    assert len(first) == 18
    assert second == []
    assert charter.read_text(encoding="utf-8") == "human-owned charter\n"
    assert "create the provider-native finite goal" in (
        tmp_path / "AGENTS.md"
    ).read_text(encoding="utf-8")
    campaign = (tmp_path / "CAMPAIGN.md").read_text(encoding="utf-8")
    assert 'status = "draft"' in campaign
    assert "auto_start = false" in campaign
    assert (tmp_path / "experiments" / "EXPERIMENT_TEMPLATE.md").is_file()
    assert (tmp_path / "campaigns" / ".gitkeep").is_file()
    assert (tmp_path / "roles" / "bot-builder.md").is_file()
    assert (tmp_path / "roles" / "council.md").is_file()
    assert (tmp_path / "roles" / "builder.md").is_file()
    assert (tmp_path / "roles" / "validator.md").is_file()
    assert (tmp_path / "roles" / "reality.md").is_file()
    functionality_log = (tmp_path / "FUNCTIONALITY_LOG.md").read_text(encoding="utf-8")
    assert "canonical register of bot functionality" in functionality_log
    assert "different experiment, model, coding style" in functionality_log
    assert "technical limitation recorded before code changes" in functionality_log
    current_experiment = (tmp_path / "CURRENT_EXPERIMENT.md").read_text(
        encoding="utf-8"
    )
    assert "Council Result" in current_experiment
    assert "Builder Result" in current_experiment
    assert "Validator Result" in current_experiment
    assert "Bot Builder Result" in current_experiment
    assert "Reality Result" in current_experiment
    assert "Git Stage History" in current_experiment
    assert "Owner Test Directive" in current_experiment
    assert "Owner Capital Authorization" in current_experiment
    assert "Functionality Reuse" in current_experiment
    assert "Owner-defined real-world evidence-unit Result commits" in current_experiment
    assert "Experiment Test full Git SHA" in current_experiment
    assert "strat-compute-<first 12 characters" in current_experiment
    assert "Data Validator will independently use" in current_experiment
    assert "Strategy-spec path and SHA-256" in current_experiment
    assert "Endpoint resolved from instance ID" in current_experiment
    assert "Reality live S3 prefix and manifest" in current_experiment
    assert "Handoff" not in current_experiment
    assert "expected SHA-256" in (tmp_path / "roles" / "shared.md").read_text(
        encoding="utf-8"
    )
    validator = (tmp_path / "roles" / "validator.md").read_text(encoding="utf-8")
    assert "Sharpe ratio | `> 2.5`" in validator
    assert "`30-50%` Sharpe decline" in validator
    assert "comparison count and correction" in validator
    assert "effective sample" in validator
    builder = (tmp_path / "roles" / "builder.md").read_text(encoding="utf-8")
    assert "strat-compute-<12-character Experiment Test Git SHA>" in builder
    assert "independently confirm `stopped`" in builder
    assert "data reserved for Validator" in builder
    assert "checksum manifest" in builder
    shared = (tmp_path / "roles" / "shared.md").read_text(encoding="utf-8")
    assert "The human owner alone controls" in shared
    assert "Missing scope means no authority" in shared
    assert "reuses compatible `verified` entries" in shared
    assert "Git is the durable stage ledger, not an activity log" in shared
    assert "Exact Owner Test Directive before Council starts" in shared
    assert "Each owner-defined real-world evidence unit" in shared
    assert "Do not commit `started`, `running`" in shared
    manager = (tmp_path / "roles" / "manager.md").read_text(encoding="utf-8")
    assert "repeatedly run experiments through Builder and Validator" in manager
    assert "may not reinterpret an Owner Test Directive" in manager
    assert "Do not fill gaps or add model-created financial controls" in manager
    assert "reuse all compatible verified functionality" in manager
    assert "record the full Git SHA before Council starts" in manager
    assert "git status --porcelain" in manager
    bot_builder = (tmp_path / "roles" / "bot-builder.md").read_text(encoding="utf-8")
    assert "Before changing code, write the reuse plan" in bot_builder
    assert "different model, experiment, style, or library preference" in bot_builder
    assert "cancel-response ambiguity" in bot_builder
    reality = (tmp_path / "roles" / "reality.md").read_text(encoding="utf-8")
    assert "exact Owner Capital Authorization" in reality
    assert "A missing field grants no discretion" in reality
    assert "A mismatch stops the bot" in reality


def test_nested_strategy_requires_separate_git_worktree(tmp_path: Path) -> None:
    assert ensure_git_repository(tmp_path) is True
    nested = tmp_path / "nested-strategy"
    nested.mkdir()

    with pytest.raises(ScaffoldError, match="separate Git worktree"):
        ensure_git_repository(nested)
