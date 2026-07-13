+++
id = ""
status = "draft"
auto_start = false
+++

# Current Campaign

Manager owns this campaign. Polyloop creates the workspace and tmux functions but does not create experiments, limit their count, advance them, or decide when the campaign is complete.

## Activation

Keep `status = "draft"` and `auto_start = false` while required fields are missing. Set `status = "ready"` and `auto_start = true` only after this seed is complete. Use `status = "paused"` to freeze the campaign. Paused and completed campaigns never auto-start.

## Campaign Goal

$objective

## Starting Evidence

- Current winner and immutable commit: `not assigned`
- Authoritative data snapshot and checksums: `not assigned`
- Experiment tester and version or Git SHA: `not assigned`
- Relevant lessons and failed experiments: `not assigned`

## AWS And S3

- AWS account and region: `not assigned`
- Baseline strategy-compute AMI: `not assigned`
- Approved S3 bucket: `not assigned`
- Approved paper and real-test host: `not assigned`
- EC2 and S3 cleanup deadline: `not assigned`

## Reality Limits

- Required paper windows or duration: `not assigned`
- Approved real-money window count (`2` or `3`): `not assigned`
- Maximum capital per real window: `not assigned`
- Maximum position and total loss: `not assigned`
- Start/end boundary and kill conditions: `not assigned`
- Human approval rule: `not assigned`

## Resource Boundary

- Time or usage budget: `not assigned`
- Operational constraints: `not assigned`
- Safety constraints: `not assigned`

## Stop Conditions

Manager stops when a Stage 1 winner matches paper in the approved real windows, resources are exhausted, evidence is blocked or unsafe, or no materially new hypothesis remains.

## Manager Goal Primer

> Run the current campaign under CAMPAIGN.md and PROJECT_CHARTER.md. Test one hypothesis at a time through Builder and Validator. Continue with new experiments until Validator confirms one moves the needle. Then build the bot, gather paper evidence, and only with exact human approval run 2-3 real-money windows. If paper or real behavior does not match, stop, record the Reality constraint, and return to Council for a new hypothesis. Stop when a Stage 1 winner is confirmed or a campaign stop condition is reached. Never scale automatically.

## Campaign Learning

Summarize experiment, Validator, paper, and real-market patterns for this campaign. Add only reusable evidence to `LESSONS.md`.

## Closeout

At completion, record the Stage 1 winner or failure state, experiments run, rejected hypotheses, Validator findings, Reality constraints, resources used, unresolved risks, and ranked follow-ups. Preserve this record under `campaigns/<campaign-id>.md`.
