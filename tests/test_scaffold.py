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

    assert len(first) == 15
    assert second == []
    assert charter.read_text(encoding="utf-8") == "human-owned charter\n"
    assert (tmp_path / "experiments" / "EXPERIMENT_TEMPLATE.md").is_file()
    assert (tmp_path / "campaigns" / ".gitkeep").is_file()


def test_nested_strategy_requires_separate_git_worktree(tmp_path: Path) -> None:
    assert ensure_git_repository(tmp_path) is True
    nested = tmp_path / "nested-strategy"
    nested.mkdir()

    with pytest.raises(ScaffoldError, match="separate Git worktree"):
        ensure_git_repository(nested)
