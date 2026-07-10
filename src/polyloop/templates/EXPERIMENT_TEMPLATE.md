+++
campaign = ""
experiment = ""
status = ""
decision = ""
+++

# Experiment Record

Preserve one record for every experiment run by the strategy manager. Use a globally unique ID such as `E0001` and store the record as `experiments/E0001.md` before replacing it in `CURRENT_EXPERIMENT.md`.

## Hypothesis

Record the approved falsifiable hypothesis and proposed mechanism.

## Implementation

Record the candidate commit, configuration, changed files, tests, and reproduction command.

## Offline Verification

Record canonical evaluator inputs, outputs, champion comparison, leakage checks, ablations, parameter-neighborhood checks, and limitations.

## Paper Evidence

Record paper run identifiers, valid and excluded market windows, raw log references, observed execution drift, and integrity checks. State when the candidate failed before this gate.

## Decision And Retrospective

Record the manager's decision or current disposition, evidence-based reasoning, reusable learning, failed assumptions, and campaign follow-ups.
