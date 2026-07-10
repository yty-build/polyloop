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

## Reality Handoff

No handoff yet.

## Decision

No decision yet. Allowed terminal decisions are `promote`, `reject`, `inconclusive`, or `blocked`.

## Retrospective

No retrospective yet.

## Closure

After decision and retrospection, set `status = "closed"`, set `decision`, preserve the completed record as `experiments/<experiment-id>.md`, and reset this file. `polyloop status` derives observed counts only from those closed records.

