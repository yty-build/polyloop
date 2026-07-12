# Polyloop

Polyloop is a small Python CLI that creates bounded, evidence-driven strategy experiment councils inside named tmux sessions. Tmux keeps the model processes alive; provider-native sessions retain conversational context; Git and experiment artifacts carry verified learning between finite campaign goals.

Polyloop is not a daemon, scheduler, trading engine, or replacement for native Codex, Claude Code, Grok, or OpenCode goal/session controls.

## Runtime Model

One strategy workspace maps to one user-named tmux session with six stable role windows plus an optional research-tool window:

```text
manager  strat-council  strat-builder  strat-verifier  bot-reality             retrospector  external-researcher
                                                     ├── bot-reality    (main pane)
                                                     └── bot-integrator (second pane)
```

Window names describe functions rather than providers. Each function defaults to Codex and can independently use Claude, Grok, or OpenCode through `polyloop.toml`. The `bot-reality` window is always prebuilt with two panes: the main pane is the deployer and paper-evidence checker, while the bot integrator converts only an offline-approved strategy into an immutable deployable artifact. When external research is configured, Polyloop also creates an `external-researcher` tool window for its interactive CLI. The strategy manager owns campaigns and executes one experiment at a time; Polyloop does not create experiments or impose an experiment count.

The evidence sequence is: campaign objective, pre-registered experiment, immutable strategy candidate, independent offline verification, immutable paper-bot artifact, paper observation, manager decision, retrospective, and archived evidence. The strategy must be built before it can be verified; the paper bot is built only after the strategy passes offline verification.

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
  --objective "Find robust paper-only challengers to the verified champion"
```

Polyloop creates project contracts, a repository-level `AGENTS.md`, role prompts, a named tmux session, and one model process per function, including both Reality panes. It does not attach automatically:

```bash
tls
tattach btc5m-straddle
```

On first launch, a provider may ask you to trust the strategy directory. Review the generated files and approve that prompt in each waiting pane. Polyloop deliberately does not bypass or auto-accept provider trust checks.

Initialization is idempotent. Running `polyloop init` again repairs missing files and windows without overwriting project content or restarting healthy panes. Use `--restart` only when model or tool configuration changes. Use `--no-launch` to test tmux topology without starting model or tool sessions.

## Inspect

```bash
polyloop status
```

Status reports the current manager-owned campaign, unique recorded experiment IDs, market-wide experiment totals, Git state, provider availability, function pane state, process names, configuration drift, and the existing `tattach` command.

## Configure Models

Edit the role tables in `polyloop.toml`:

```toml
[roles.manager]
provider = "codex"
model = ""
effort = "high"
resume_session = ""
extra_args = []

[roles.strat-council]
provider = "claude"
model = "opus"
effort = "high"
resume_session = ""
extra_args = []

[roles.strat-builder]
provider = "codex"
model = ""
effort = "high"
resume_session = ""
extra_args = ["--sandbox", "workspace-write", "--config", "sandbox_workspace_write.network_access=true"]

[roles.strat-verifier]
provider = "codex"
model = ""
effort = "high"
resume_session = ""
extra_args = ["--sandbox", "workspace-write", "--config", "sandbox_workspace_write.network_access=true"]

[roles.bot-reality]
provider = "codex" # main pane in the bot-reality window
model = ""
effort = "medium"
resume_session = ""
extra_args = []

[roles.bot-integrator]
provider = "codex"
model = ""
effort = "high"
resume_session = ""
extra_args = []
```

`resume_session` is optional and provider-native. Polyloop never reads or modifies provider goal databases and does not install hooks.

Codex's workspace-write sandbox blocks the local tmux Unix socket unless network access is enabled. A manager that must inspect or message its role windows can use `extra_args = ["--sandbox", "workspace-write", "--config", "sandbox_workspace_write.network_access=true"]`. This keeps filesystem writes scoped to the workspace but enables network access, so apply it only to roles that need it. Polyloop does not use full-access or sandbox-bypass flags by default.

## External Research

External discovery is a `strat-council`-owned tool, not an additional decision-making role. Configure its current provider and command independently:

```toml
[external_researcher]
provider = "grok"
command = ["grok", "--yolo"]
```

Polyloop launches that exact command in a dedicated `external-researcher` tmux window. When the manager requests an external scan, `strat-council` sends one simple question such as `What do X and the internet say about BTC 5-minute market behavior?` to that window and reads the visible response. `strat-council` never launches a nested Grok process. Grok chooses its own native tools. Social sources can generate experiment ideas, but every used source must be carried into the experiment record and independently tested by `strat-verifier`. Replacing Grok later changes the provider and command, not the function name.

## Strategy Compute

`strat-builder` and `strat-verifier` both use the manager-assigned isolated EC2 strategy-compute instance. Its Name is per-experiment and SHA/loop-suffixed, and it must carry `PolyLoopRole=strategy-compute`; unsuffixed shared strategy instances are not used. The current experiment records its exact Name, `PolyLoopId`, instance ID, region, baseline AMI, evaluator identity, data checksums, separate remote workspaces, one S3 experiment prefix, and separate artifact subprefixes. Builder creates and remotely proves the immutable candidate Git SHA; Manager records it before dispatching Verifier. Verifier starts from a clean independent checkout of that same SHA and regenerates the canonical outputs. They run sequentially, resolve the current endpoint from the instance ID instead of a cached alias, upload durable artifacts, request stop through the AWS control plane, independently confirm `stopped`, and record lifecycle and cleanup evidence.

Polyloop injects this contract but does not start EC2 automatically or store AWS credentials. The manager and roles use the strategy project's approved AWS procedure.

## Reality Gate

`strat-verifier` owns canonical offline backtesting and sends only an immutable survivor into the Bot Reality gate. The bot integrator reuses the approved strategy module, adds paper-bot adapters and deterministic strategy-to-bot parity tests, then creates a separate immutable bot commit. It cannot deploy or approve that work. `bot-reality` reviews the Bot Integration Result, deploys the exact artifact to the approved remote paper host, operates the required real-market windows, preserves raw logs, and recommends the Bot Reality Result. It cannot modify bot code or rerun the canonical evaluator.

Both panes are local control agents; heavy integration tests, builds, and paper services belong on the strategy's configured remote infrastructure. Polyloop does not store SSH keys or hard-code a server.

## Prompt Model

`AGENTS.md` is the workspace-wide Codex contract. The files in `roles/` are the authoritative function contracts. On launch, Polyloop reads `roles/shared.md` and the function-specific role file and injects that content using the provider's supported context mechanism. Workers are then told to read the current project and campaign files and wait for a finite assignment.

The assignment, function Results, decision, and retrospective belong in `CURRENT_EXPERIMENT.md`; tmux messages should only wake the relevant function or report completion with the new file SHA-256. Before the manager replaces the current experiment, it preserves that experiment as `experiments/E####.md`. Polyloop counts unique experiment IDs from the current record and historical records regardless of status or decision; it never increments, limits, or controls them.

An experiment may contain several meaningful Git commits without committing every evaluator invocation: freeze the evaluation contract before Builder work, commit the immutable candidate before Verifier work, preserve finalized verifier evidence, commit the immutable bot artifact before paper deployment, and commit the archived record and accepted lessons at final disposition. A locked holdout is a one-read Verifier resource, not development data. Strategy specifications and evidence manifests are machine-readable so a result does not depend on a pane transcript or mutable provider memory.

## Campaign Goals

`CAMPAIGN.md` is owned by the strategy manager and is also the campaign seed. It defines a finite research objective, starting evidence, paper requirement, resource boundary, and stop conditions. It deliberately contains no Polyloop-controlled experiment limit.

Campaign auto-start is explicit. Keep `status = "draft"` and `auto_start = false` until the seed is complete. Setting `status = "ready"` and `auto_start = true` tells the next manager launch to validate the seed and directly create its provider-native finite goal. For Codex this uses native goal control, so no `/goal` command needs to be typed in the manager window. `paused` and `complete` never auto-start.

For a model-assisted bootstrap, start Codex in this repository and ask it to initialize a target strategy. The repository `AGENTS.md` tells it to scaffold with `--no-launch`, complete the seed, and launch the roles only after the seed is ready. `AGENTS.md` supplies instructions but does not execute merely because a bare Codex TUI was opened; either the bootstrap request or Polyloop's injected manager startup prompt begins work.

Only one campaign is active in a strategy session at a time. At close, preserve its record under `campaigns/`; the next campaign reads the committed charter, champion, leaderboard, market-level lessons, campaign closeouts, and recorded experiments rather than depending on transcript memory. Pause and resume through tmux and the provider's native controls.

## Parallel Strategies

Use a unique tmux session and a separate writable Git directory or worktree for every parallel strategy:

```text
~/strategies/btc5m-straddle  <->  tmux btc5m-straddle
~/strategies/eth15m-maker    <->  tmux eth15m-maker
```

Polyloop refuses to claim a tmux session already owned by another workspace.

## Safety

The generated charter and `bot-reality` contract are paper-only. Polyloop does not connect to Polymarket, AWS, exchanges, wallets, or trading APIs. Infrastructure access and paper-bot commands must be supplied explicitly by the strategy project, and live trading remains outside the generated scope.
