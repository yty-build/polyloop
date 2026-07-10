from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .config import (
    ConfigError,
    ProjectConfig,
    find_project_root,
    load_config,
    validate_session_name,
    write_default_config,
)
from .constants import PROVIDERS, __version__
from .scaffold import ScaffoldError, create_project_files, ensure_git_repository
from .status import build_status_report
from .tmux import TmuxError, ensure_tmux_session, upsert_tmux_note


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="polyloop",
        description="Create and inspect bounded, tmux-native experiment councils.",
    )
    parser.add_argument(
        "--version", action="version", version=f"polyloop {__version__}"
    )
    commands = parser.add_subparsers(dest="command", required=True)

    init_parser = commands.add_parser(
        "init", help="create or repair a Polyloop strategy workspace and tmux session"
    )
    init_parser.add_argument("--root", type=Path, default=Path.cwd())
    init_parser.add_argument("--session", help="tmux session and strategy identifier")
    init_parser.add_argument("--description", default="")
    init_parser.add_argument("--market", default="")
    init_parser.add_argument("--objective", default="")
    init_parser.add_argument("--campaign", default=None)
    init_parser.add_argument("--experiments", type=int, default=None)
    init_parser.add_argument("--provider", choices=PROVIDERS, default=None)
    init_parser.add_argument(
        "--no-launch",
        action="store_true",
        help="create role windows but leave their shells idle",
    )
    init_parser.add_argument(
        "--restart",
        action="store_true",
        help="restart every managed role pane using the current configuration",
    )
    init_parser.add_argument(
        "--adopt",
        action="store_true",
        help="adopt an existing non-Polyloop tmux session without deleting windows",
    )

    status_parser = commands.add_parser(
        "status", help="inspect project, Git, provider, and tmux health"
    )
    status_parser.add_argument("--root", type=Path, default=Path.cwd())
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        if args.command == "init":
            return _run_init(args)
        return _run_status(args)
    except (ConfigError, ScaffoldError, TmuxError) as exc:
        print(f"polyloop: {exc}", file=sys.stderr)
        return 2


def _run_init(args: argparse.Namespace) -> int:
    if args.no_launch and args.restart:
        raise ConfigError("--no-launch and --restart cannot be used together")
    root = args.root.expanduser().resolve()
    root.mkdir(parents=True, exist_ok=True)
    config_path = root / "polyloop.toml"
    created_config = False
    initialized_git = False

    if config_path.exists():
        config = load_config(root)
        _validate_existing_options(config, args)
        initialized_git = ensure_git_repository(root)
    else:
        session = args.session or _prompt_session()
        campaign_id = args.campaign or "C001"
        max_experiments = args.experiments if args.experiments is not None else 3
        provider = args.provider or "codex"
        validate_session_name(session)
        if max_experiments < 1:
            raise ConfigError("max experiments must be positive")
        initialized_git = ensure_git_repository(root)
        write_default_config(
            root,
            session=session,
            description=args.description or session,
            campaign_id=campaign_id,
            max_experiments=max_experiments,
            provider=provider,
        )
        created_config = True
        config = load_config(root)

    created_files = create_project_files(
        root,
        session=config.session,
        description=config.description,
        campaign_id=config.campaign.campaign_id,
        max_experiments=config.campaign.max_experiments,
        market=args.market,
        objective=args.objective,
    )
    result = ensure_tmux_session(
        config,
        launch=not args.no_launch,
        restart=args.restart,
        adopt=args.adopt,
    )
    note_warning = upsert_tmux_note(
        config.notes_file, config.session, config.description
    )

    print(f"Polyloop strategy: {config.session}")
    print(f"Workspace: {config.root}")
    if created_config:
        print("Created: polyloop.toml")
    if initialized_git:
        print("Created: Git repository")
    if created_files:
        print(f"Created: {len(created_files)} scaffold files")
    if result.created_session:
        print(f"Created: tmux session {config.session}")
    if result.created_windows:
        print("Added windows: " + ", ".join(result.created_windows))
    if result.launched_roles:
        print("Launched roles: " + ", ".join(result.launched_roles))
        print(
            "First launch may require workspace trust; review and approve it with "
            f"tattach {config.session}. Polyloop never auto-approves trust prompts."
        )
    elif args.no_launch:
        print("Role windows are idle (--no-launch).")
    for warning in (*result.warnings, *((note_warning,) if note_warning else ())):
        print(f"Warning: {warning}")
    print(f"Attach: tattach {config.session}")
    print("Inspect: polyloop status")
    return 0


def _run_status(args: argparse.Namespace) -> int:
    root = find_project_root(args.root)
    config = load_config(root)
    report = build_status_report(config)
    print(report.text)
    return 0 if report.healthy else 1


def _prompt_session() -> str:
    if not sys.stdin.isatty():
        raise ConfigError("--session is required for first-time non-interactive init")
    session = input("Tmux session / strategy name: ").strip()
    if not session:
        raise ConfigError("session name cannot be empty")
    return session


def _validate_existing_options(config: ProjectConfig, args: argparse.Namespace) -> None:
    if args.session and args.session != config.session:
        raise ConfigError(
            f"this workspace is configured for session {config.session!r}, not {args.session!r}"
        )
    if args.campaign and args.campaign != config.campaign.campaign_id:
        raise ConfigError(
            "edit polyloop.toml and CAMPAIGN.md to begin another campaign"
        )
    if (
        args.experiments is not None
        and args.experiments != config.campaign.max_experiments
    ):
        raise ConfigError(
            "edit polyloop.toml and CAMPAIGN.md to change the campaign limit"
        )
    if args.provider and any(
        role.provider != args.provider for role in config.roles.values()
    ):
        raise ConfigError(
            "edit [roles.*] in polyloop.toml to change existing providers"
        )
