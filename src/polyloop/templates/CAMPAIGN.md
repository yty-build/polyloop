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

## Owner Authority

The human owner alone defines how strategies are tested and whether, where, and how money is allocated. Models may recommend or flag risk, but cannot create or change authority. Record the owner's exact campaign instruction or a durable reference; do not paraphrase away constraints.

- Exact owner campaign instruction or reference: `not assigned`
- What models may decide: `not assigned`
- What requires a new owner instruction: `test method or any use of money`

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

## Owner-Directed Reality Test

- Required paper windows or duration: `not assigned`
- Owner-defined real-world test method, duration or count: `not assigned`
- Owner-defined allocation, sizing, account, and market rule: `no money authorized until explicitly assigned`
- Owner-defined controls and permitted operational discretion: `not assigned`
- Owner authorization, expiry, and revocation rule: `not assigned`

## Resource Boundary

- Time or usage budget: `not assigned`
- Operational constraints: `not assigned`
- Safety constraints: `not assigned`

## Stop Conditions

Manager stops when a Stage 1 winner matches paper in the exact owner-authorized real-world test, resources are exhausted, evidence or technical integrity is blocked, or no materially new hypothesis remains.

## Manager Goal Primer

> Run the current campaign under the owner's exact instruction in CAMPAIGN.md and PROJECT_CHARTER.md. Test one hypothesis at a time through Builder and Validator without changing the Owner Test Directive. Then reuse verified bot functionality, gather the owner-directed paper evidence, and use money only under the exact committed Owner Capital Authorization. If paper or real behavior does not match, stop, record the Reality constraint, and return to Council for a new hypothesis. Stop when a Stage 1 winner is confirmed or a campaign stop condition is reached. Never let a model allocate money, extend authorization, or scale automatically.

## Campaign Learning

Summarize experiment, Validator, paper, and real-market patterns for this campaign. Add only reusable evidence to `LESSONS.md` and verified bot functionality or technical limitations to `FUNCTIONALITY_LOG.md`.

## Closeout

At completion, record the Stage 1 winner or failure state, experiments run, rejected hypotheses, Validator findings, Reality constraints, resources used, unresolved risks, and ranked follow-ups. Preserve this record under `campaigns/<campaign-id>.md`.
