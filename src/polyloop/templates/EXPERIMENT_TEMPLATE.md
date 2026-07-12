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

## Frozen Evaluation Contract

Record the pre-registration commit, primary metric and minimum useful effect, risk limits, data splits, locked-holdout state and read timestamp, search budget, statistical correction, truth source, feature-availability rules, execution tiers, and quantitative paper gate. This contract must predate Builder work; a material post-result change creates a new experiment.

## Evidence Manifest

Record the machine-readable strategy-spec and artifact-manifest paths and SHA-256 values. The manifest must bind data, evaluator, environment, commands, outputs, and compute lifecycle evidence.

## Implementation

Record the candidate commit, configuration, changed files, tests, and reproduction command.

## Offline Verification

Record canonical evaluator inputs, outputs, champion comparison, holdout-read and spent-state evidence, outcome-truth and feature-availability audits, execution tiers, leakage checks, ablations, parameter-neighborhood checks, and limitations.

## Bot Integration

Record the offline-approved strategy commit, immutable bot commit, adapter changes, strategy-to-bot parity evidence, smoke tests, deployment manifest, and unresolved translation risks. State when the candidate failed before this gate.

## Paper Evidence

Record paper run identifiers, valid and excluded market windows, raw log and artifact-manifest references, observed execution drift, quantitative gate checks, and integrity checks. State when the candidate failed before this gate.

## Decision And Retrospective

Record the manager's decision or current disposition, evidence-based reasoning, reusable learning, failed assumptions, and campaign follow-ups.
