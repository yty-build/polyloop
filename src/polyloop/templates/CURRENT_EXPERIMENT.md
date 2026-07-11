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

## Council Result

No result yet.

## Builder Result

No result yet.

## Verifier Result

No result yet.

## Bot Integration Result

No result yet.

## Reality Result

No result yet.

## Decision

No decision yet. The strategy manager records the outcome appropriate to the experiment.

## Retrospective

No retrospective yet.

## History

Before replacing this experiment with another, preserve its current record as `experiments/<experiment-id>.md`. `polyloop status` counts the unique experiment ID whether it is current, completed, failed, paused, or otherwise recorded; it does not interpret or control the lifecycle.
