+++
campaign = ""
experiment = ""
stage = "idle"
status = "not_started"
decision = ""
+++

# Current Experiment

Only the strategy manager may activate an experiment. Polyloop observes experiment records but does not create, count, advance, or close them.

## Manager Assignment

- Hypothesis: `not assigned`
- Mechanism: `not assigned`
- Champion comparison: `not assigned`
- Success and rejection criteria: `not assigned`
- Evidence snapshot: `not assigned`
- Candidate branch or worktree: `not assigned`

## Evidence Snapshot

Record immutable source paths, timestamps, row/window counts, checksums, feature definitions, exclusions, and known data-quality limitations. Store large raw data outside this document and reference it precisely.

## Strategy Compute

- Per-experiment SHA/loop-suffixed EC2 strategy-compute Name, `PolyLoopId`, and instance ID: `not assigned`
- AWS region and baseline AMI: `not assigned`
- Candidate full Git SHA: `filled by manager after the Strategy Builder Result and before Verifier dispatch`
- Champion full Git SHA: `not assigned`
- Evaluator version or full Git SHA: `not assigned`
- Data snapshot checksums: `not assigned`
- Builder remote workspace: `not assigned`
- Verifier clean remote workspace: `not assigned`
- Durable S3 experiment prefix: `not assigned`
- Builder and Verifier artifact subprefixes: `not assigned`
- Final EC2 stopped-state evidence: `not assigned`

## Strategy Council Result

No result yet.

## Strategy Builder Result

No result yet.

## Strategy Verifier Result

No result yet.

## Bot Integration Result

No result yet.

## Bot Reality Result

No result yet.

## Decision

No decision yet. The strategy manager records the outcome appropriate to the experiment.

## Retrospective

No retrospective yet.

## History

Before replacing this experiment with another, preserve its current record as `experiments/<experiment-id>.md`. `polyloop status` counts the unique experiment ID whether it is current, completed, failed, paused, or otherwise recorded; it does not interpret or control the lifecycle.
