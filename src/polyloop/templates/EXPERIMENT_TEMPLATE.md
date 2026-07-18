+++
campaign = ""
experiment = ""
status = ""
decision = ""
+++

# Experiment Record

Preserve one record for every Manager-run experiment as `experiments/<experiment-id>.md` before replacing `CURRENT_EXPERIMENT.md`.

## Owner Test Directive

Record the owner's exact instruction or durable reference, required test method and evidence checkpoints, permitted model discretion, and directive commit. State whether every stage followed it without additions or substitutions.

## Hypothesis And Experiment Test

Record the hypothesis, why it should work, the committed test SHA, metric and minimum improvement, risk, Builder and Validator data, comparison count, statistics, truth source, feature timing, execution assumptions, pass/fail rules, expected Reality behavior, and exact owner-directed paper requirement.

## Owner Capital Authorization

When applicable, record the exact owner approval, bot and config SHAs, account identifier without credentials, market, allocation, sizing, test method, timing, duration or count, owner-defined controls, permitted discretion, expiry, revocation terms, and authorization commit. Otherwise record that no money was authorized.

## Functionality Reuse

Record the input `FUNCTIONALITY_LOG.md` commit, every verified functionality and canonical SHA reused, missing functionality built, demonstrated technical limitations, Reality approvals for replacements, and resulting functionality-log updates.

## Builder Result

Record the strategy commit and spec, changed files, tests, EC2 identity, commands, experiment metrics, S3 manifest, and stopped-state evidence.

## Validator Result

Record the independent `pass`, `fail`, `inconclusive`, or `invalid` result, winner comparison, integrity checks, rule removal, parameter stability, statistics, Reality expectations, S3 manifest, and stopped-state evidence.

## Bot Builder Result

For Validator passes, record the reviewed plan, immutable bot commit, parity and failure tests, deployment manifest, and S3 evidence. State when no bot was built.

## Reality Result

Record the owner-directed paper test, comparison with Validator, logs, failures, and S3 evidence. When paper matches and Owner Capital Authorization exists, record the exact authorized test, orders, fills, latency, rejects, partials, cancels, heartbeat behavior, settlement, actual P&L, stops, and S3 evidence.

## Decision And Retrospective

Record Manager's decision, what moved the needle, what failed, the exact Validator or Reality constraint, reusable lessons, and the next hypothesis direction.

## Git Stage History

List the full Git SHAs for the Owner Test Directive, Council Result, Experiment Test, Builder Result, Validator Result and decision, Bot Builder Result and functionality-log update when applicable, paper Result, Owner Capital Authorization when applicable, every owner-defined real-world evidence unit, and final pre-archive decision. Use `not applicable` for correctly skipped stages. The Git commit that adds this archived file is the final archive identity.
