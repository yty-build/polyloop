# Project Charter

Strategy workspace: `$session`

## Objective

$objective

## Market

$market

Before activating a campaign, record the exact market identifier, duration, resolution source, payout, fees, order constraints, latency assumptions, and available history. Mark uncertainty as an assumption.

## Evidence Standard

A strategy becomes the Stage 1 winner only after all three checks succeed:

1. Builder runs the agreed experiment and Validator independently confirms that it is valid, moves the needle, and is realistic enough to build a bot.
2. Reality deploys the immutable bot in paper mode and confirms that bot behavior matches the Validator-confirmed experiment.
3. Under explicit human approval, Reality runs exactly 2 or 3 real-money windows and confirms that actual behavior matches paper evidence.

Any failure or mismatch stops progression, records the constraint, closes and commits the experiment, and sends the lesson back to Council for a new hypothesis.

Before Builder starts, commit the exact Experiment Test: metric and minimum improvement, data Builder may use, data Validator will use, comparison count, outcome truth, feature timing, fills, fees, latency, risk, pass/fail rules, expected paper behavior, and Reality limits. Results never rewrite this test.

Every strategy, bot, Validator run, paper run, and real run must have immutable Git identities where applicable and machine-readable checksum manifests.

## Strategy Compute And S3

Run heavy Builder and Validator work only on the Manager-assigned AWS EC2 instance named `strat-compute-<12-character Experiment Test Git SHA>` and tagged `PolyLoopRole=strategy-compute`. Record the instance ID, region, AMI, tags, and endpoint-resolution evidence. Never use an unsuffixed shared instance or cached alias.

Builder and Validator run sequentially against the same strategy SHA, evaluator, and data checksums in separate clean workspaces. Store artifacts under `s3://<approved-bucket>/polyloop/<campaign>/<experiment>/<test-sha>/builder/` and `validator/`. Upload checksum manifests, request stop through the AWS control plane, and independently confirm `stopped` after each assignment.

Bot and Reality evidence use sibling `bot-builder/`, `reality/paper/`, and `reality/live/` prefixes.

## Reality Limits

Paper must match before any real-money test. Human approval must record the exact bot SHA, config SHA, market, whether 2 or 3 windows are approved, maximum capital per window, maximum position, total loss limit, start/end boundary, and kill conditions. The bot stops automatically after the final approved window and immediately on any violation. A passing 2-3-window run does not authorize scaling.

## Current Baseline

Record the current winner, immutable commit, experiment tester, data snapshot, paper and real evidence, and known limitations. Use `unverified baseline` until these exist.

## Outside Scope

Automatic scaling, portfolio allocation, capital changes beyond the approved 2-3-window test, and unattended real-money continuation are outside Stage 1.
