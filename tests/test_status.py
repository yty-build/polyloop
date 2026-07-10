from pathlib import Path

from polyloop.status import observe_experiments


def test_observes_closed_experiments_without_controlling_count(tmp_path: Path) -> None:
    experiments = tmp_path / "experiments"
    experiments.mkdir()
    (experiments / "EXPERIMENT_TEMPLATE.md").write_text(
        '+++\ncampaign = ""\nexperiment = ""\nstatus = "closed"\ndecision = ""\n+++\n',
        encoding="utf-8",
    )
    _write_record(experiments / "E0001.md", "C001", "E0001", "reject")
    _write_record(experiments / "E0002.md", "C002", "E0002", "promote")
    nested = experiments / "E0003"
    nested.mkdir()
    _write_record(nested / "EXPERIMENT.md", "C001", "E0003", "inconclusive")
    (experiments / "E0004.md").write_text(
        '+++\ncampaign = "C001"\nexperiment = "E0004"\nstatus = "active"\ndecision = ""\n+++\n',
        encoding="utf-8",
    )

    observation = observe_experiments(tmp_path, "C001")

    assert observation.current_campaign_closed == 2
    assert observation.total_closed == 3
    assert observation.closed_ids == frozenset({"E0001", "E0002", "E0003"})
    assert any(
        "E0004.md is archived but status is not closed" in warning
        for warning in observation.warnings
    )


def _write_record(path: Path, campaign: str, experiment: str, decision: str) -> None:
    path.write_text(
        "\n".join(
            (
                "+++",
                f'campaign = "{campaign}"',
                f'experiment = "{experiment}"',
                'status = "closed"',
                f'decision = "{decision}"',
                "+++",
                "",
                f"# {experiment}",
                "",
            )
        ),
        encoding="utf-8",
    )
