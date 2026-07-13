# Polyloop

Polyloop is a small Python CLI that creates evidence-driven strategy experiment teams inside named tmux sessions. Tmux keeps model processes alive; Git, S3 manifests, and experiment records carry evidence between finite campaign goals.

Polyloop is not a scheduler, trading engine, wallet, or replacement for native Codex, Claude Code, Grok, or OpenCode session controls.

## Tmux Layout

One strategy workspace maps to one user-named tmux session:

```text
manager  council  builder  validator  reality             retrospector  external-researcher
                                      |-- reality     (pane 0)
                                      `-- bot-builder (pane 1)
```

Window and pane names describe functions, not providers. Each defaults to Codex and may independently use Claude, Grok, or OpenCode through `polyloop.toml`.

- Manager owns the campaign and experiment loop.
- Council proposes hypotheses from data, past Results, and Reality constraints.
- Builder builds and runs each approved experiment.
- Validator independently decides whether the experiment validly moves the needle and is realistic enough to build a bot.
- Bot Builder acts only after Validator pass.
- Reality tests paper first and, under exact human approval, 2-3 real-money windows.
- Retrospector feeds every Validator or Reality failure into the next hypothesis.
- External Researcher is an optional Council tool.

## Stage 1 Loop

```text
Council hypothesis
  -> Manager-approved Experiment Test
  -> Builder experiment
  -> Validator
       fail: commit evidence and lessons -> Council hypothesis
       pass: Bot Builder -> Reality paper
                  paper mismatch: stop -> Council hypothesis
                  paper match: approved 2-3 real-money windows
                       real mismatch: stop -> Council hypothesis
                       real match: Stage 1 winner, stop without scaling
```

Polyloop does not create experiments or impose an experiment count. Manager decides when another experiment is materially useful within the campaign's finite resource and safety limits.

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

Run from an empty strategy directory or existing Git repository:

```bash
polyloop init \
  --session btc5m-straddle \
  --description "BTC 5-minute straddle research" \
  --market "Polymarket BTC 5-minute market; exact resolution specification pending" \
  --objective "Find a Stage 1 strategy that passes Validator, paper, and approved Reality windows"
```

Polyloop creates the contracts, role prompts, named tmux session, and both Reality panes. It does not attach automatically:

```bash
tls
tattach btc5m-straddle
```

Initialization is idempotent. Re-running `polyloop init` repairs missing files and windows without overwriting project content or restarting healthy panes. Use `--restart` only when prompt or provider configuration changes. Use `--no-launch` to inspect topology without starting models.

## Inspect

```bash
polyloop status
```

Status reports campaign state, recorded experiment IDs, Git state, provider availability, pane state, configuration drift, and the attach command.

## Configure Models

Edit role tables in `polyloop.toml`:

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

[roles.builder]
provider = "codex"
model = ""
effort = "high"
resume_session = ""
extra_args = ["--sandbox", "workspace-write", "--config", "sandbox_workspace_write.network_access=true"]

[roles.validator]
provider = "codex"
model = ""
effort = "high"
resume_session = ""
extra_args = ["--sandbox", "workspace-write", "--config", "sandbox_workspace_write.network_access=true"]

[roles.reality]
provider = "codex"
model = ""
effort = "high"
resume_session = ""
extra_args = []

[roles.bot-builder]
provider = "codex"
model = ""
effort = "high"
resume_session = ""
extra_args = []
```

`resume_session` is optional and provider-native. Polyloop does not read provider goal databases or install provider hooks.

Codex's workspace-write sandbox blocks the local tmux Unix socket unless network access is enabled. Roles that must inspect or message panes can use `extra_args = ["--sandbox", "workspace-write", "--config", "sandbox_workspace_write.network_access=true"]`. Polyloop does not use sandbox-bypass flags by default.

## External Research

Configure the provider-neutral Council tool independently:

```toml
[external_researcher]
provider = "grok"
command = ["grok", "--yolo"]
```

Polyloop launches that exact command in `external-researcher`. When Manager requests a scan, Council sends one simple question such as `What do X and the internet say about BTC 5-minute market behavior?` and reads the visible response. The tool chooses its own native capabilities. External claims may inspire an experiment but never validate it.

## AWS Strategy Compute And S3

Builder and Validator use the same isolated EC2 instance sequentially with separate clean workspaces. Its exact Name is `strat-compute-<12-character Experiment Test Git SHA>`, and it must carry `PolyLoopRole=strategy-compute`. The current experiment records the Name, instance ID, region, AMI, tags, strategy SHA, experiment tester, data checksums, workspaces, and lifecycle evidence. The endpoint is resolved from the instance ID after each start rather than a cached alias.

Evidence is stored under:

```text
s3://<approved-bucket>/polyloop/<campaign>/<experiment>/<test-sha>/
  builder/
  validator/
  bot-builder/
  reality/paper/
  reality/live/
```

Each function uploads a checksum manifest. Builder and Validator request EC2 stop through the AWS control plane and independently confirm `stopped` after their assignments. Polyloop injects this contract but does not store AWS credentials or run EC2 itself.

## Reality

Reality directs Bot Builder only after Validator pass. Bot Builder creates an immutable bot, parity tests, failure tests, and deployment manifest but never deploys it. Reality independently checks the bot and runs paper.

If paper matches, a real-money test requires explicit human approval containing the exact bot and config SHAs, market, exactly 2 or 3 windows, capital per window, maximum position, total loss, time boundary, and kill conditions. Reality stops after the final approved window or any earlier violation. A mismatch returns logs and constraints to Council. A match completes Stage 1 but never authorizes automatic scaling.

## Prompt And Git Model

`AGENTS.md` is the workspace contract. Files in `roles/` define each function. Polyloop injects `roles/shared.md` plus the function role file through the provider's supported context mechanism.

Detailed assignments and Results live in `CURRENT_EXPERIMENT.md`. Tmux messages carry only wake-ups and completion notifications with the expected file SHA-256. Before another hypothesis starts, Manager archives the record under `experiments/` and commits evidence and lessons.

An experiment can have meaningful commits for the Experiment Test, strategy, Validator Result, bot, and final record. It does not need a commit for every test invocation.

## Parallel Strategies

Use a unique tmux session and separate writable Git directory or worktree for every parallel strategy:

```text
~/strategies/btc5m-straddle  <->  tmux btc5m-straddle
~/strategies/eth15m-maker    <->  tmux eth15m-maker
```

Polyloop refuses to claim a tmux session owned by another workspace.

## Safety

Polyloop does not connect to Polymarket, AWS, exchanges, or wallets. Project-specific infrastructure procedures and credentials stay outside the framework. No real order is allowed before Validator pass, paper match, and exact human approval for the bounded Reality run.
