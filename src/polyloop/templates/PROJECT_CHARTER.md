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
3. Under a committed Owner Capital Authorization, Reality performs exactly the owner-directed real-world test and confirms that actual behavior matches paper evidence.

Any failure or mismatch stops progression, records the constraint, closes and commits the experiment, and sends the lesson back to Council for a new hypothesis.

Before Builder starts, commit the exact Experiment Test matching the Owner Test Directive: metric and minimum improvement, data Builder may use, data Validator will use, comparison count, outcome truth, feature timing, fills, fees, latency, risk, pass/fail rules, and expected paper behavior. Results never rewrite this test.

Every strategy, bot, Validator run, paper run, and real run must have immutable Git identities where applicable and machine-readable checksum manifests.

## Owner Authority

The human owner is the sole authority for the test method and every use of money. Models may analyze, recommend, or report a technical limitation, but may not reinterpret an Owner Test Directive or choose, infer, change, redirect, extend, or reuse an account, market, allocation, sizing method, timing, duration or count, financial control, or authorization. If the owner's instruction cannot be executed exactly, stop and request clarification rather than substituting another test.

The framework imposes no default real-money window count or model-created financial limit. Missing Owner Capital Authorization means no money is authorized.

Git records completed stage boundaries, not every activity. Manager commits the Owner Test Directive, Council Result, frozen Experiment Test, Builder Result, Validator Result and decision, Bot Builder Result plus functionality-log changes, paper Result, Owner Capital Authorization, each owner-defined real-world evidence unit, and final Retrospective/archive before advancing. Manager also commits campaign activation, pause, resume, and completion. Do not advance from a dirty shared worktree, and do not rewrite a boundary commit after downstream work begins.

## Strategy Compute And S3

Run heavy Builder and Validator work only on the Manager-assigned AWS EC2 instance named `strat-compute-<12-character Experiment Test Git SHA>` and tagged `PolyLoopRole=strategy-compute`. Record the instance ID, region, AMI, tags, and endpoint-resolution evidence. Never use an unsuffixed shared instance or cached alias.

Builder and Validator run sequentially against the same strategy SHA, evaluator, and data checksums in separate clean workspaces. Store artifacts under `s3://<approved-bucket>/polyloop/<campaign>/<experiment>/<test-sha>/builder/` and `validator/`. Upload checksum manifests, request stop through the AWS control plane, and independently confirm `stopped` after each assignment.

Bot and Reality evidence use sibling `bot-builder/`, `reality/paper/`, and `reality/live/` prefixes.

## Functionality Reuse

`FUNCTIONALITY_LOG.md` is the canonical register of verified bot functionality. Bot Builder reuses compatible entries at their exact recorded SHAs. Rebuilding requires a demonstrated technical limitation recorded before changes, Reality review, and the smallest necessary replacement. A new experiment, model preference, style preference, library preference, or cleanup is not a technical limitation.

## Reality Limits

Paper must match before any use of money. Owner Capital Authorization must record the exact bot and config SHAs, account identifier without credentials, market, allocation, order sizing, test method, timing, duration or count, owner-defined controls, permitted operational discretion, expiry, and revocation reference. The bot follows these values exactly and stops when the authorization ends or technical integrity fails. A passing run does not authorize another run or scaling.

## Current Baseline

Record the current winner, immutable commit, experiment tester, data snapshot, paper and real evidence, and known limitations. Use `unverified baseline` until these exist.

## Outside Scope

Model-directed portfolio allocation, model-created financial controls, authorization reuse or extension, automatic scaling, and unattended continuation beyond the exact Owner Capital Authorization are outside Stage 1.
