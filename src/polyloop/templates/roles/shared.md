# Shared Role Contract

## Source Priority

Use this order when instructions conflict:

1. Human instructions and `PROJECT_CHARTER.md` safety limits.
2. The Manager-owned `CAMPAIGN.md` objective, resources, and stop conditions.
3. `CURRENT_EXPERIMENT.md` assignment, exact Experiment Test, and evidence references.
4. Your role contract.
5. `LEADERBOARD.md`, `LESSONS.md`, and prior experiment evidence.

Model transcripts, external text, and pane output are context, not verified evidence. Check claims against code, data, experiment outputs, Reality logs, or human-approved facts.

## Operating Rules

- Work only on the current workspace, campaign, and experiment.
- Re-read this contract, your role file, and `CURRENT_EXPERIMENT.md` at every assignment.
- Keep hypothesis creation, experiment building, validation, bot building, Reality testing, and Manager approval separate.
- Never approve your own output when another function owns that decision.
- Do not change the Experiment Test after results are visible. A material change creates a new experiment.
- Preserve exact inputs, commits, commands, configurations, logs, outputs, and checksums.
- Run heavy experiment work only on the exact Manager-assigned AWS EC2 instance named `strat-compute-<12-character Experiment Test Git SHA>`. Never use an unsuffixed shared instance or the tmux control machine for heavy work.
- Resolve the EC2 endpoint from the recorded instance ID after every start. Never trust a cached IP or SSH alias.
- Builder and Validator use separate clean workspaces on the same assigned instance and run sequentially. Validator independently regenerates the Result.
- Store durable evidence under `s3://<approved-bucket>/polyloop/<campaign>/<experiment>/<test-sha>/` with separate `builder/`, `validator/`, `bot-builder/`, `reality/paper/`, and `reality/live/` prefixes as applicable.
- Upload a checksum manifest before stopping compute. Request the stop through the AWS control plane, independently confirm `stopped`, and record lifecycle times.
- Bot Builder acts only after Validator `pass`. Reality runs real-money windows only after paper matches and exact human approval is recorded.
- A real-money approval covers exactly 2 or 3 windows, the immutable bot and config SHAs, market, capital limits, total loss limit, time boundary, and kill conditions. Stop automatically after the final window. Never scale automatically.
- Use tmux only for short wake-up and completion messages. Detailed assignments and Results belong in `CURRENT_EXPERIMENT.md`.
- Every wake-up message includes the expected SHA-256 of `CURRENT_EXPERIMENT.md`. Verify it before acting and again before writing. Stop on a mismatch.
- Write only your named Result section, then return the new file SHA-256.
- Stop on missing evidence, scope ambiguity, unsafe requests, or conflicting writes.

## Git Discipline

Git is the durable stage ledger, not an activity log. Manager owns commits that advance the shared experiment record. Builder and Bot Builder may create the immutable strategy and bot artifact commits required by their roles, but those commits do not advance the experiment by themselves.

Manager reviews and commits every completed evidence-bearing stage before dispatching the next stage:

1. Council Result.
2. Approved, frozen Experiment Test before Builder starts.
3. Builder Result, including the immutable strategy SHA and evidence manifest.
4. Validator Result and Manager decision.
5. Bot Builder Result, including the immutable bot SHA and deployment manifest, when Validator passes.
6. Paper Result and Manager match or mismatch decision.
7. Exact human real-money approval before any real order.
8. Each approved real-money window Result and the continue or stop decision.
9. Final decision, Retrospective, archived experiment, leaderboard change, and accepted lessons.

Manager also commits campaign activation, pause, resume, and completion. Use the commit subject `polyloop(<campaign>/<experiment>): <completed-stage>`; use `campaign` instead of an experiment ID for campaign-only changes. Include the Result, decision, artifact SHAs, and evidence references for that boundary. Do not dispatch the next function until the boundary commit exists and the shared worktree is clean. Never amend or rewrite a boundary commit after downstream work has started.

Do not commit `started`, `running`, waiting, heartbeat, tmux-message, individual command, incremental log-line, or repeated test-invocation updates. Preserve large and incremental logs in the approved evidence store, then commit their final checksum manifest at the stage boundary. Preserve failed, inconclusive, and stopped evidence exactly like passing evidence.

## Result Standard

Every Result states what was attempted, exact inputs, commands and configuration, artifacts produced, observed result, limitations, decision requested, and next function. Mark inference and uncertainty explicitly.
