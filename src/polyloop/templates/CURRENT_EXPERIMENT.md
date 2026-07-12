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
- Frozen evaluation-contract commit: `not assigned`

## Frozen Evaluation Contract

Complete and commit this section before `strat-builder` begins. Results do not change these fields; a material change requires a new experiment.

- Primary metric and minimum economically useful improvement: `not assigned`
- Secondary diagnostics and risk limits: `not assigned`
- Development, validation, locked-holdout, and forward/paper split policy: `not assigned`
- Locked-holdout reader and state (`locked-unread`, `authorized`, or `spent`): `not assigned`
- Holdout-read authorization rule and, after use, read timestamp: `not assigned`
- Search budget and total planned strategy, rule, feature, and parameter comparisons: `not assigned`
- Significance level, confidence-interval method, effective-sample method, and multiple-testing correction: `not assigned`
- Authoritative outcome/settlement truth source and availability timestamp: `not assigned`
- Feature source, source timestamp, available timestamp, maximum age, and live-computability requirements: `not assigned`
- Canonical execution tier plus optimistic and pessimistic stress tiers: `not assigned`
- Quantitative paper gate, required valid windows or duration, exclusions, and kill conditions: `not assigned`

## Evidence Snapshot

Record immutable source paths, timestamps, row/window counts, checksums, feature definitions, exclusions, and known data-quality limitations. Store large raw data outside this document and reference it precisely. Record the evidence-manifest path and SHA-256 that binds these inputs.

## Strategy Compute

- Per-experiment SHA/loop-suffixed EC2 strategy-compute Name, `PolyLoopId`, and instance ID: `not assigned`
- AWS region and baseline AMI: `not assigned`
- Candidate full Git SHA: `filled by manager after the Strategy Builder Result and before Verifier dispatch`
- Champion full Git SHA: `not assigned`
- Evaluator version or full Git SHA: `not assigned`
- Data snapshot checksums: `not assigned`
- Machine-readable strategy-spec path and SHA-256: `filled by manager after the Strategy Builder Result`
- Evidence/artifact-manifest path and SHA-256: `not assigned`
- Builder remote workspace: `not assigned`
- Verifier clean remote workspace: `not assigned`
- Durable S3 experiment prefix: `not assigned`
- Builder and Verifier artifact subprefixes: `not assigned`
- Current endpoint resolved from the instance ID and UTC timestamp: `not assigned`
- Start, artifact-upload, stop-request, and stopped-state UTC timestamps: `not assigned`
- Cleanup disposition or retention deadline: `not assigned`
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
