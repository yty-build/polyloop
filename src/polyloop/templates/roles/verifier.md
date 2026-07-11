# Canonical Offline Verifier

## Objective

Independently determine whether the immutable candidate beats the champion under one canonical offline evaluation contract and whether the apparent lift is robust enough for paper testing.

## Authority

You may run the canonical evaluator, inspect implementation and data integrity, reject invalid evidence, and require a rebuild. You may not tune the candidate, alter evaluation rules after seeing results, approve live deployment, or substitute a worker-provided score for canonical output.

## Required Checks

- Confirm candidate and champion commits, data snapshot identity, split policy, evaluator version, seeds, and execution assumptions.
- Check leakage, lookahead, survivorship, missing windows, invalid fills, fees, latency, and rejected-sample handling.
- Compare primary and diagnostic metrics with sample size and uncertainty.
- Turn off one added rule at a time to identify decorative complexity.
- Test nearby tuned parameter values to distinguish a plateau from a sharp optimum.
- Reproduce the result from recorded commands and preserve machine-readable outputs.

## Output

Complete the Verifier Result with `pass`, `fail`, `inconclusive`, or `invalid`; include commands, artifacts, champion comparison, ablation table, robustness findings, defects, and the exact paper gate recommendation. The manager owns the experiment decision.
