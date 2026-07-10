from pathlib import Path

from polyloop.status import observe_experiments


def test_counts_unique_experiment_ids_regardless_of_status(tmp_path: Path) -> None:
    experiments = tmp_path / "experiments"
    experiments.mkdir()
    (experiments / "EXPERIMENT_TEMPLATE.md").write_text(
        '+++\ncampaign = ""\nexperiment = ""\nstatus = ""\ndecision = ""\n+++\n',
        encoding="utf-8",
    )
    _write_record(experiments / "E0001.md", "C001", "E0001", "completed")
    _write_record(experiments / "E0002.md", "C002", "E0002", "running")
    nested = experiments / "E0003"
    nested.mkdir()
    _write_record(nested / "EXPERIMENT.md", "C001", "E0003", "blocked")
    _write_record(experiments / "E0004.md", "C001", "E0004", "active")

    observation = observe_experiments(
        tmp_path,
        "C001",
        current_experiment="E0005",
        current_experiment_campaign="C001",
    )

    assert observation.current_campaign_recorded == 4
    assert observation.total_recorded == 5
    assert observation.recorded_ids == frozenset(
        {"E0001", "E0002", "E0003", "E0004", "E0005"}
    )
    assert observation.warnings == ()


def _write_record(path: Path, campaign: str, experiment: str, status: str) -> None:
    path.write_text(
        "\n".join(
            (
                "+++",
                f'campaign = "{campaign}"',
                f'experiment = "{experiment}"',
                f'status = "{status}"',
                'decision = ""',
                "+++",
                "",
                f"# {experiment}",
                "",
            )
        ),
        encoding="utf-8",
    )
