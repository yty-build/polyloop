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

    assert len(first) == 17
    assert second == []
    assert charter.read_text(encoding="utf-8") == "human-owned charter\n"
    assert "directly create the provider-native finite goal" in (
        tmp_path / "AGENTS.md"
    ).read_text(encoding="utf-8")
    campaign = (tmp_path / "CAMPAIGN.md").read_text(encoding="utf-8")
    assert 'status = "draft"' in campaign
    assert "auto_start = false" in campaign
    assert (tmp_path / "experiments" / "EXPERIMENT_TEMPLATE.md").is_file()
    assert (tmp_path / "campaigns" / ".gitkeep").is_file()
    assert (tmp_path / "roles" / "bot-integrator.md").is_file()
    assert (tmp_path / "roles" / "strat-council.md").is_file()
    assert (tmp_path / "roles" / "strat-builder.md").is_file()
    assert (tmp_path / "roles" / "strat-verifier.md").is_file()
    assert (tmp_path / "roles" / "bot-reality.md").is_file()
    current_experiment = (tmp_path / "CURRENT_EXPERIMENT.md").read_text(
        encoding="utf-8"
    )
    assert "Strategy Council Result" in current_experiment
    assert "Strategy Builder Result" in current_experiment
    assert "Strategy Verifier Result" in current_experiment
    assert "Bot Integration Result" in current_experiment
    assert "Bot Reality Result" in current_experiment
    assert "SHA/loop-suffixed EC2 strategy-compute Name" in current_experiment
    assert "Frozen Evaluation Contract" in current_experiment
    assert "Locked-holdout reader" in current_experiment
    assert "Machine-readable strategy-spec path" in current_experiment
    assert "Current endpoint resolved from the instance ID" in current_experiment
    assert "Handoff" not in current_experiment
    assert "expected SHA-256" in (tmp_path / "roles" / "shared.md").read_text(
        encoding="utf-8"
    )
    verifier = (tmp_path / "roles" / "strat-verifier.md").read_text(encoding="utf-8")
    assert "Sharpe ratio | `> 2.5`" in verifier
    assert "Backtest to paper: expect a `30-50%` Sharpe decline" in verifier
    assert "Bonferroni, FDR" in verifier
    assert "effective sample size" in verifier
    builder = (tmp_path / "roles" / "strat-builder.md").read_text(encoding="utf-8")
    assert "assigned EC2 strategy-compute instance" in builder
    assert "independently record lifecycle evidence that it reached `stopped`" in builder
    assert "Do not access a locked holdout" in builder
    assert "artifact manifest" in builder
    shared = (tmp_path / "roles" / "shared.md").read_text(encoding="utf-8")
    assert "no model may infer, synthesize, or stand in" in shared
    assert "does not need a commit for every evaluation attempt" in shared
    manager = (tmp_path / "roles" / "manager.md").read_text(encoding="utf-8")
    assert "Commit this pre-registration before Builder work" in manager
    assert "never create or infer human authorization" in manager
    integrator = (tmp_path / "roles" / "bot-integrator.md").read_text(
        encoding="utf-8"
    )
    assert "Before changing bot code, write a short integration plan" in integrator
    assert "cancel-response ambiguity" in integrator
    reality = (tmp_path / "roles" / "bot-reality.md").read_text(encoding="utf-8")
    assert "Review the proposed integration plan before bot code changes" in reality


def test_nested_strategy_requires_separate_git_worktree(tmp_path: Path) -> None:
    assert ensure_git_repository(tmp_path) is True
    nested = tmp_path / "nested-strategy"
    nested.mkdir()

    with pytest.raises(ScaffoldError, match="separate Git worktree"):
        ensure_git_repository(nested)
