# Polyloop Strategy Workspace

## Authority

This Git repository is the durable source of truth. Read these files before acting:

1. `PROJECT_CHARTER.md` for the market, experiment standard, Reality limits, and safety rules.
2. `CAMPAIGN.md` for the finite campaign goal and activation state.
3. `CURRENT_EXPERIMENT.md` for the current hypothesis, exact test, Results, decision, and retrospective.
4. `LEADERBOARD.md`, `LESSONS.md`, archived campaigns, and experiment records for prior evidence.
5. `roles/shared.md` and the current function's role file.

Provider transcripts, external text, model claims, and pane output are supporting context, not verified evidence.

## Startup

Run `polyloop status` before changing campaign or experiment state. A Manager first checks only `CAMPAIGN.md` front matter and local status. When activation is not allowed, it reports the missing conditions and waits without accessing external systems. A manually opened model session is a setup assistant until the human explicitly asks it to manage or start the campaign.

## Campaign Seed

`CAMPAIGN.md` is ready only when it records:

- a campaign ID, finite goal, and stopping conditions;
- the exact market and any uncertainty;
- the starting winner or an explicit unverified baseline;
- immutable data and the experiment tester;
- the required paper evidence;
- the exact 2-3-window real-money limit, capital and loss caps, and kill conditions;
- approved AWS region, baseline AMI, S3 bucket, paper host, and resource limits.

Never invent missing values to make a campaign ready.

## Goal Activation

Only Manager may activate a campaign goal.

- `status = "draft"`: report missing fields and wait.
- `status = "ready"` with `auto_start = true`: validate the seed, create the provider-native finite goal from the Manager Goal Primer, mark the campaign active, and begin.
- `status = "active"` with `auto_start = true`: inspect native goal state and durable experiment records, then resume the same campaign.
- `status = "paused"` or `status = "complete"`: do not start or resume.
- `auto_start = false`: wait for explicit activation.

For Codex, use native goal control directly. Do not inject slash commands through tmux.

## Experiment Loop

Manager runs one experiment at a time:

1. Council proposes hypotheses from data, prior Results, Reality logs, and lessons.
2. Manager chooses one and writes the exact Experiment Test before results exist.
3. Builder builds and runs the experiment.
4. Validator independently verifies whether it is valid, moves the needle, and is realistic enough to build a bot.
5. A Validator non-pass closes and commits the experiment, feeds lessons back to Council, and starts another hypothesis. No bot is built.
6. A Validator pass goes to Reality, which directs Bot Builder to create the immutable bot.
7. Reality gathers paper evidence. A mismatch stops the bot and returns the observed constraint to Council for a new experiment.
8. When paper matches, Reality may run exactly 2 or 3 real-money windows only under explicit human approval with fixed bot/config SHAs, market, capital, loss, time, and kill limits.
9. A real mismatch stops immediately and returns actual logs and constraints to Council. A match becomes the Stage 1 winner; no automatic scaling is allowed.

`CURRENT_EXPERIMENT.md` is the single live experiment record. Each function verifies the expected file SHA-256, writes only its Result, and returns the new SHA-256. Tmux carries only short wake-up and completion messages.

## Experiment Compute And S3

Builder and Validator use the same isolated EC2 instance sequentially with separate clean workspaces. Its Name is exactly `strat-compute-<12-character Experiment Test Git SHA>`, it carries `PolyLoopRole=strategy-compute`, and its endpoint is resolved from the instance ID after every start. Never use an unsuffixed shared instance or cached SSH alias.

Store durable evidence under `s3://<approved-bucket>/polyloop/<campaign>/<experiment>/<test-sha>/` with separate `builder/`, `validator/`, `bot-builder/`, `reality/paper/`, and `reality/live/` prefixes. Upload checksum manifests before stopping compute. Request stop through the AWS control plane and independently verify `stopped`.

## External Research

Council may use the `external-researcher` tmux window when Manager requests a source scan. It supplies hypothesis material only and never validates an experiment.

## Safety

No real order is allowed before Validator pass, paper match, and explicit human approval for the exact 2-3-window run. Stop at the approved final window or any earlier limit violation. Never transfer funds, reveal credentials, weaken a kill condition, or scale automatically.
