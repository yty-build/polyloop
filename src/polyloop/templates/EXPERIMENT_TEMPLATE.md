+++
campaign = ""
experiment = ""
status = ""
decision = ""
+++

# Experiment Record

Preserve one record for every Manager-run experiment as `experiments/<experiment-id>.md` before replacing `CURRENT_EXPERIMENT.md`.

## Hypothesis And Experiment Test

Record the hypothesis, why it should work, the committed test SHA, metric and minimum improvement, risk, Builder and Validator data, comparison count, statistics, truth source, feature timing, execution assumptions, pass/fail rules, expected Reality behavior, paper requirement, and real-window limits.

## Builder Result

Record the strategy commit and spec, changed files, tests, EC2 identity, commands, experiment metrics, S3 manifest, and stopped-state evidence.

## Validator Result

Record the independent `pass`, `fail`, `inconclusive`, or `invalid` result, winner comparison, integrity checks, rule removal, parameter stability, statistics, Reality expectations, S3 manifest, and stopped-state evidence.

## Bot Builder Result

For Validator passes, record the reviewed plan, immutable bot commit, parity and failure tests, deployment manifest, and S3 evidence. State when no bot was built.

## Reality Result

Record paper windows, comparison with Validator, logs, failures, and S3 evidence. When paper matches and human approval exists, record the exact 2-3 real-money window approval, orders, fills, latency, rejects, partials, cancels, heartbeat behavior, settlement, actual P&L, stops, and S3 evidence.

## Decision And Retrospective

Record Manager's decision, what moved the needle, what failed, the exact Validator or Reality constraint, reusable lessons, and the next hypothesis direction.

## Git Stage History

List the full Git SHAs for the Council Result, Experiment Test, Builder Result, Validator Result and decision, Bot Builder Result when applicable, paper Result, exact human approval when applicable, every real-money window, and final pre-archive decision. Use `not applicable` for correctly skipped stages. The Git commit that adds this archived file is the final archive identity.
