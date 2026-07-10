+++
id = ""
status = "not_started"
+++

# Current Campaign

The strategy manager owns this campaign record. Polyloop does not create experiments, impose an experiment limit, advance stages, or decide when the campaign is complete.

## Campaign Objective

No campaign has been activated. Define a concrete research outcome that can be completed or stopped without requiring an indefinite loop.

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
