+++
id = ""
status = "draft"
auto_start = false
+++

# Current Campaign

The strategy manager owns this campaign record. Polyloop does not create experiments, impose an experiment limit, advance stages, or decide when the campaign is complete.

## Activation

Keep `status = "draft"` and `auto_start = false` while required seed fields are missing. After the seed is complete, set `status = "ready"` and `auto_start = true` to let the next manager launch validate this record and directly create its provider-native finite goal. Use `status = "paused"` to freeze the campaign; paused and completed campaigns never auto-start.

## Campaign Objective

$objective

## Starting Evidence

- Champion and immutable commit: `not assigned`
- Authoritative data snapshot: `not assigned`
- Canonical evaluator: `not assigned`
- Relevant market-level lessons: `not assigned`

## Resource Boundary

- Time or usage budget: `not assigned`
- Paper-observation requirement: `not assigned`
- Operational constraints: `not assigned`

## Stop Conditions

The strategy manager must stop and return control when the campaign objective is achieved, its resource boundary is reached, evidence is blocked or unsafe, or no materially new falsifiable hypothesis remains.

## Manager Goal Primer

Use this as the basis for the manager's native `/goal` after completing this record:

> Run the current campaign under CAMPAIGN.md and PROJECT_CHARTER.md. Select and execute one falsifiable experiment at a time. Continue only while another experiment is materially useful to the campaign objective and remains inside its resource and safety boundaries. Stop under the recorded campaign stop conditions and leave a closeout; do not silently begin another campaign.

## Campaign Learning

Summarize patterns that apply to this campaign. Promote a lesson to the market-level `LESSONS.md` only when its evidence justifies reuse beyond this campaign.

## Closeout

At completion, record the final champion, experiments run, rejected mechanisms, unresolved risks, resource use, and ranked follow-ups. Preserve this record under `campaigns/<campaign-id>.md`, then reset `CAMPAIGN.md` before another campaign is activated.
