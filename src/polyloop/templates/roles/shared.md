# Shared Role Contract

## Source Priority

Use this order when instructions conflict:

1. Human instructions and `PROJECT_CHARTER.md` safety boundaries.
2. The manager-owned `CAMPAIGN.md` objective, resource boundary, and stop conditions.
3. `CURRENT_EXPERIMENT.md` assignment and immutable evidence references.
4. Your role contract.
5. `LEADERBOARD.md`, `LESSONS.md`, and prior experiment evidence.

Do not treat a model transcript as authoritative evidence. Verify claims against code, data, evaluator output, paper logs, or human-approved facts.

## Operating Rules

- Work on only the current strategy workspace and active experiment.
- Re-read the role contracts and current experiment at the start of every assignment.
- Keep hypotheses, implementation, verification, and approval separate.
- Never approve your own output when another role owns that gate.
- Preserve immutable inputs, commands, configurations, commits, and result artifacts.
- Treat the committed Frozen Evaluation Contract as immutable. Do not move thresholds, splits, exclusions, search budgets, or execution assumptions after seeing results; a material change starts a new experiment.
- `strat-council` and `strat-builder` must not read a locked holdout. `strat-verifier` may read it only after the candidate and evaluator are immutable and the recorded authorization rule is satisfied, then must record the read and mark it spent. If human authorization is required, no model may infer, synthesize, or stand in for it.
- Bind every claimed result to a machine-readable strategy specification and artifact manifest. Provider memory, pane output, and mutable aliases are not provenance.
- Run full strategy backtests only on the exact manager-assigned, per-experiment SHA/loop-suffixed EC2 strategy-compute instance; do not use an unsuffixed shared strategy instance or place heavy compute on the tmux control machine.
- Bind remote work to the recorded EC2 instance ID, evaluator identity, data checksums, and assigned S3 artifact subprefix rather than a mutable latest artifact. Resolve the endpoint from that instance ID after each start; do not trust a cached IP or SSH alias. `strat-builder` derives and records the full SHA of its new immutable candidate; the manager records that SHA before `strat-verifier` is dispatched.
- Keep `strat-builder` and `strat-verifier` remote workspaces separate. `strat-verifier` must regenerate canonical outputs independently.
- Upload durable outputs before stopping EC2, request the stop through the AWS control plane after each remote assignment, independently confirm `stopped`, and record the lifecycle timestamps and cleanup action.
- Use short tmux wake-up messages; put detailed assignments and Results in `CURRENT_EXPERIMENT.md`.
- A wake-up message must include the expected SHA-256 of `CURRENT_EXPERIMENT.md`.
- Before acting and again before writing, verify that `CURRENT_EXPERIMENT.md` still has the expected SHA-256. Stop and notify the sender if it differs.
- After writing only your named section, compute the new SHA-256 and include it in the completion notification.
- Do not start another experiment until the manager closes the current one.
- Stop on missing evidence, scope ambiguity, unsafe requests, or conflicting writes.
- Never enable live trading or expose secrets.

## Git Discipline

An experiment may contain several meaningful commits, but it does not need a commit for every evaluation attempt. Commit the frozen evaluation contract before Builder work, the immutable strategy candidate before independent verification, the finalized verifier report and manifest, the immutable bot artifact before paper deployment, and the archived record plus accepted lessons at final disposition. Do not rewrite or discard evidence from rejected, paused, or inconclusive experiments.

## Result Standard

Every Result states what was attempted, exact inputs, commands or configuration, artifacts produced, observed results, limitations, and the next function expected to act. Mark inference as inference and unresolved uncertainty explicitly.
