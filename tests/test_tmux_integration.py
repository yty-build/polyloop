from __future__ import annotations

import json
import os
import shutil
import subprocess
import time
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
        "external-researcher",
    ]
    output = capsys.readouterr().out
    assert "Experiments: 0 recorded in none, 0 recorded across workspace" in output
    assert "Campaign:  none draft, auto-start=off" in output
    assert "Attach: tattach test-strategy" in output


def test_external_researcher_launches_in_its_own_window(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    tmux_socket: str,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.setenv("POLYLOOP_NOTES_FILE", str(tmp_path / "tmux-notes"))
    fake_bin = tmp_path / "bin"
    fake_bin.mkdir()
    fake_codex = fake_bin / "codex"
    fake_codex.write_text("#!/bin/sh\nexec sleep 30\n", encoding="utf-8")
    fake_codex.chmod(0o755)
    fake_grok = fake_bin / "grok"
    fake_grok.write_text(
        "#!/bin/sh\n"
        "printf '%s\\n' \"$*\" > external-researcher.args\n"
        "printf 'FAKE GROK READY\\n'\n"
        "exec sleep 30\n",
        encoding="utf-8",
    )
    fake_grok.chmod(0o755)
    monkeypatch.setenv("PATH", f"{fake_bin}{os.pathsep}{os.environ.get('PATH', '')}")
    project = tmp_path / "strategy"

    assert (
        main(
            [
                "init",
                "--root",
                str(project),
                "--session",
                "research-window",
                "--description",
                "Research window test",
                "--no-launch",
            ]
        )
        == 0
    )

    for role in (
        "manager",
        "council",
        "builder",
        "verifier",
        "reality",
        "retrospector",
    ):
        subprocess.run(
            [
                "tmux",
                "-L",
                tmux_socket,
                "respawn-pane",
                "-k",
                "-t",
                f"research-window:{role}",
                "exec sleep 30",
            ],
            check=True,
        )
    config_path = project / "polyloop.toml"
    config_text = config_path.read_text(encoding="utf-8")
    config_path.write_text(
        config_text.replace(
            'command = ["grok", "--yolo"]',
            "command = " + json.dumps([str(fake_grok), "--yolo"]),
        ),
        encoding="utf-8",
    )

    assert main(["init", "--root", str(project)]) == 0

    panes = subprocess.run(
        [
            "tmux",
            "-L",
            tmux_socket,
            "list-panes",
            "-t",
            "research-window:external-researcher",
            "-F",
            "#{pane_current_command}|#{@polyloop_role}|#{@polyloop_provider}",
        ],
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()
    assert panes.endswith("|external-researcher|grok")
    researcher_args = project / "external-researcher.args"
    for _ in range(100):
        if researcher_args.exists():
            break
        time.sleep(0.01)
    assert researcher_args.read_text(encoding="utf-8").strip() == "--yolo"
    assert "Launched tools: external-researcher" in capsys.readouterr().out


def test_session_cannot_be_claimed_by_two_workspaces(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    tmux_socket: str,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.setenv("POLYLOOP_NOTES_FILE", str(tmp_path / "tmux-notes"))
    common = ["--session", "shared-name", "--no-launch"]

    assert main(["init", "--root", str(tmp_path / "one"), *common]) == 0
    assert main(["init", "--root", str(tmp_path / "two"), *common]) == 2
    assert "belongs to" in capsys.readouterr().err


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
