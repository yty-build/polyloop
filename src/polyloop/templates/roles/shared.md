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
- Use short tmux wake-up messages; put detailed assignments and handoffs in repository files.
- Do not start another experiment until the manager closes the current one.
- Stop on missing evidence, scope ambiguity, unsafe requests, or conflicting writes.
- Never enable live trading or expose secrets.

## Git Discipline

Evaluations may run many times without creating a commit. The builder creates an immutable candidate commit before independent verification. Before replacing the current experiment, the manager preserves its record under `experiments/` and commits the accumulated evidence. Do not rewrite or discard evidence from rejected, paused, or inconclusive experiments.

## Handoff Standard

Every handoff states what was attempted, exact inputs, commands or configuration, artifacts produced, observed results, limitations, and the next role expected to act. Mark inference as inference and unresolved uncertainty explicitly.
