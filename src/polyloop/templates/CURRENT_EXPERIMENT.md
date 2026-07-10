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

## Council Handoff

No handoff yet.

## Builder Handoff

No handoff yet.

## Verifier Handoff

No handoff yet.

## Bot Integration Handoff

No handoff yet.

## Reality Handoff

No handoff yet.

## Decision

No decision yet. The strategy manager records the outcome appropriate to the experiment.

## Retrospective

No retrospective yet.

## History

Before replacing this experiment with another, preserve its current record as `experiments/<experiment-id>.md`. `polyloop status` counts the unique experiment ID whether it is current, completed, failed, paused, or otherwise recorded; it does not interpret or control the lifecycle.
