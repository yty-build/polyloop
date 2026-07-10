from __future__ import annotations

import os
import shutil
import subprocess
import uuid
from pathlib import Path

import pytest

from polyloop.cli import main


pytestmark = pytest.mark.skipif(shutil.which("tmux") is None, reason="tmux is required")


@pytest.fixture
def tmux_socket(monkeypatch: pytest.MonkeyPatch):
    socket = f"polyloop-test-{uuid.uuid4().hex}"
    monkeypatch.setenv("POLYLOOP_TMUX_SOCKET", socket)
    yield socket
    subprocess.run(
        ["tmux", "-L", socket, "kill-server"],
        capture_output=True,
        text=True,
        check=False,
    )


def test_init_is_idempotent_and_status_is_healthy(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    tmux_socket: str,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.setenv("POLYLOOP_NOTES_FILE", str(tmp_path / "tmux-notes"))
    fake_bin = tmp_path / "bin"
    fake_bin.mkdir()
    fake_codex = fake_bin / "codex"
    fake_codex.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
    fake_codex.chmod(0o755)
    monkeypatch.setenv("PATH", f"{fake_bin}{os.pathsep}{os.environ.get('PATH', '')}")
    project = tmp_path / "strategy"
    args = [
        "init",
        "--root",
        str(project),
        "--session",
        "test-strategy",
        "--description",
        "Test strategy",
        "--market",
        "Synthetic market",
        "--objective",
        "Test orchestration",
        "--experiments",
        "2",
        "--no-launch",
    ]

    assert main(args) == 0
    assert main(["init", "--root", str(project), "--no-launch"]) == 0
    assert main(["status", "--root", str(project)]) == 0

    windows = subprocess.run(
        [
            "tmux",
            "-L",
            tmux_socket,
            "list-windows",
            "-t",
            "test-strategy",
            "-F",
            "#{window_name}",
        ],
        capture_output=True,
        text=True,
        check=True,
    ).stdout.splitlines()
    assert windows == [
        "manager",
        "council",
        "builder",
        "verifier",
        "reality",
        "retrospector",
    ]
    assert "Attach: tattach test-strategy" in capsys.readouterr().out


def test_session_cannot_be_claimed_by_two_workspaces(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    tmux_socket: str,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.setenv("POLYLOOP_NOTES_FILE", str(tmp_path / "tmux-notes"))
    common = ["--session", "shared-name", "--experiments", "1", "--no-launch"]

    assert main(["init", "--root", str(tmp_path / "one"), *common]) == 0
    assert main(["init", "--root", str(tmp_path / "two"), *common]) == 2
    assert "belongs to" in capsys.readouterr().err


def test_zero_experiment_campaign_is_rejected(tmp_path: Path) -> None:
    project = tmp_path / "invalid"

    assert (
        main(
            [
                "init",
                "--root",
                str(project),
                "--session",
                "invalid-count",
                "--experiments",
                "0",
                "--no-launch",
            ]
        )
        == 2
    )
    assert not (project / "polyloop.toml").exists()


def test_failed_adoption_does_not_claim_existing_session(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    tmux_socket: str,
) -> None:
    monkeypatch.setenv("POLYLOOP_NOTES_FILE", str(tmp_path / "tmux-notes"))
    subprocess.run(
        [
            "tmux",
            "-L",
            tmux_socket,
            "new-session",
            "-d",
            "-s",
            "external",
            "-n",
            "manager",
        ],
        check=True,
    )
    subprocess.run(
        [
            "tmux",
            "-L",
            tmux_socket,
            "new-window",
            "-d",
            "-t",
            "external",
            "-n",
            "manager",
        ],
        check=True,
    )

    assert (
        main(
            [
                "init",
                "--root",
                str(tmp_path / "adopt"),
                "--session",
                "external",
                "--adopt",
                "--no-launch",
            ]
        )
        == 2
    )
    owner = subprocess.run(
        [
            "tmux",
            "-L",
            tmux_socket,
            "show-options",
            "-qv",
            "-t",
            "external",
            "@polyloop_root",
        ],
        capture_output=True,
        text=True,
        check=False,
    ).stdout.strip()
    assert owner == ""
