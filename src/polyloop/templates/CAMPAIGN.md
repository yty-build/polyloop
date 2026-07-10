+++
id = "$campaign_id"
status = "draft"
max_experiments = $max_experiments
completed_experiments = 0
+++

# Campaign $campaign_id

## Bounded Goal

$objective

Run no more than `$max_experiments` completed experiments. Execute one experiment at a time and close each experiment before selecting another.

## Starting Point

- Champion: `unverified baseline`
- Baseline commit: `not recorded`
- Evidence snapshot: `not recorded`
- Campaign budget: `not recorded`
- Paper-window requirement: `not recorded`

## Early Stop Conditions

Stop and return control to the human owner when:

- The campaign reaches `$max_experiments` completed experiments.
- Required data, evaluator, credentials, or paper infrastructure is unavailable.
- No materially new, falsifiable hypothesis remains.
- A safety boundary or campaign budget would be exceeded.
- Results cannot be reproduced or evidence integrity is uncertain.

## Manager Goal Primer

Use this as the basis for the manager's native `/goal`:

> Run campaign $campaign_id for at most $max_experiments completed experiments under PROJECT_CHARTER.md. Execute one experiment at a time through hypothesis, build, canonical offline verification, paper evidence, decision, and retrospection. Commit every closed experiment. Stop when the experiment limit or any early stop condition is reached.

## Campaign Closeout

At completion, record the final champion, experiments attempted, winners, rejected hypotheses, unresolved risks, budget used, and ranked candidates for the next bounded campaign.

