# Polyloop

Polyloop is a small Python CLI that creates bounded, evidence-driven strategy experiment councils inside named tmux sessions. Tmux keeps the model processes alive; provider-native sessions retain conversational context; Git and experiment artifacts carry verified learning between finite campaign goals.

Polyloop is not a daemon, scheduler, trading engine, or replacement for native Codex, Claude Code, Grok, or OpenCode goal/session controls.

## Runtime Model

One strategy workspace maps to one user-named tmux session with six stable function windows:

```text
manager  council  builder  verifier  reality  retrospector
```

Window names describe functions rather than providers. Each role defaults to Codex and can independently use Claude, Grok, or OpenCode through `polyloop.toml`. A campaign is bounded by a maximum experiment count and executes one experiment at a time.

## Requirements

- Python 3.11 or newer
- Git
- tmux
- At least one supported coding CLI: `codex`, `claude`, `grok`, or `opencode`

## Install

```bash
python3 -m pip install .
```

For development:

```bash
python3 -m venv .venv
.venv/bin/pip install -e .
```

## Initialize A Strategy

Run this from an empty strategy directory or an existing Git repository:

```bash
polyloop init \
  --session btc5m-straddle \
  --description "BTC 5-minute straddle research" \
  --market "Polymarket BTC 5-minute market; exact resolution specification pending" \
  --objective "Find robust paper-only challengers to the verified champion" \
  --experiments 3
```

Polyloop creates project contracts, role prompts, a named tmux session, and one model process per role. It does not attach automatically:

```bash
tls
tattach btc5m-straddle
```

On first launch, a provider may ask you to trust the strategy directory. Review the generated files and approve that prompt in each waiting pane. Polyloop deliberately does not bypass or auto-accept provider trust checks.

Initialization is idempotent. Running `polyloop init` again repairs missing files and windows without overwriting project content or restarting healthy panes. Use `--restart` only when model configuration changes. Use `--no-launch` to test tmux topology without starting model sessions.

## Inspect

```bash
polyloop status
```

Status reports campaign progress, Git state, provider availability, role window state, process names, configuration drift, and the existing `tattach` command.

## Configure Models

Edit the role tables in `polyloop.toml`:

```toml
[roles.manager]
provider = "codex"
model = ""
effort = "high"
resume_session = ""
extra_args = []

[roles.council]
provider = "claude"
model = "opus"
effort = "high"
resume_session = ""
extra_args = []
```

`resume_session` is optional and provider-native. Polyloop never reads or modifies provider goal databases and does not install hooks.

## Prompt Model

The files in `roles/` are the authoritative runtime contracts. On launch, Polyloop reads `roles/shared.md` and the function-specific role file and injects that content using the provider's supported context mechanism. The model is then told to read the current project and campaign files and wait for a finite assignment.

Detailed assignments and handoffs belong in `CURRENT_EXPERIMENT.md`; tmux messages should only wake the relevant role. Completed experiment evidence belongs under `experiments/` and is preserved through Git.

## Campaign Goals

`CAMPAIGN.md` contains a ready-to-use native manager goal for at most `N` experiments. Activate it manually in the manager window using the provider's native goal command. Worker assignments remain finite to one stage of one experiment.

Pause and resume through tmux and the provider's native controls. A new campaign reads the committed charter, champion, leaderboard, lessons, and closed experiments rather than depending on transcript memory.

## Parallel Strategies

Use a unique tmux session and a separate writable Git directory or worktree for every parallel strategy:

```text
~/strategies/btc5m-straddle  <->  tmux btc5m-straddle
~/strategies/eth15m-maker    <->  tmux eth15m-maker
```

Polyloop refuses to claim a tmux session already owned by another workspace.

## Safety

The generated charter and reality-operator contract are paper-only. Polyloop does not connect to Polymarket, AWS, exchanges, wallets, or trading APIs. Infrastructure access and paper-bot commands must be supplied explicitly by the strategy project, and live trading remains outside the generated scope.
