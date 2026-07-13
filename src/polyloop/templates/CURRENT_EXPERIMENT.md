+++
campaign = ""
experiment = ""
stage = "idle"
status = "not_started"
decision = ""
+++

# Current Experiment

Only Manager may activate an experiment. Polyloop observes records but does not create, count, advance, or close experiments.

## Manager Assignment

- Hypothesis: `not assigned`
- Why it should work: `not assigned`
- Current winner comparison: `not assigned`
- Expected paper and real behavior: `not assigned`
- Evidence snapshot: `not assigned`
- Branch or worktree: `not assigned`

## Experiment Test

Complete and commit this section before Builder starts. A material change after results exist creates a new experiment.

- Experiment Test full Git SHA: `not assigned`
- Metric and minimum improvement that moves the needle: `not assigned`
- Risk and rejection limits: `not assigned`
- Data Builder may use: `not assigned`
- Data Validator will independently use: `not assigned`
- Planned strategy, rule, feature, and parameter comparison count: `not assigned`
- Significance, confidence interval, effective sample, and comparison correction: `not assigned`
- Outcome and settlement truth source: `not assigned`
- Feature source, source time, available time, maximum age, and live computability: `not assigned`
- Fill, fee, latency, partial-fill, cancel, and settlement assumptions: `not assigned`
- Exact pass, fail, inconclusive, and invalid rules: `not assigned`
- Required paper behavior and valid windows: `not assigned`
- Real-money window count (`2` or `3`), capital and loss limits, time boundary, and kill conditions: `filled only after paper matches`
- Human approval reference for the real-money run: `filled only after paper matches`

## Evidence Snapshot

Record immutable paths, timestamps, row and window counts, checksums, feature definitions, exclusions, and known data limitations. Store large data outside this file and reference its checksum manifest.

## Experiment Compute And S3

- Exact EC2 Name `strat-compute-<first 12 characters of Experiment Test Git SHA>`: `not assigned`
- Instance ID, AWS account, region, AMI, and tags: `not assigned`
- Endpoint resolved from instance ID and UTC time: `not assigned`
- Strategy full Git SHA: `filled after Builder Result and before Validator starts`
- Current winner full Git SHA: `not assigned`
- Experiment tester version or full Git SHA: `not assigned`
- Data checksums: `not assigned`
- Strategy-spec path and SHA-256: `filled after Builder Result`
- Builder and Validator remote workspaces: `not assigned`
- S3 root `s3://<bucket>/polyloop/<campaign>/<experiment>/<test-sha>/`: `not assigned`
- Builder S3 prefix and manifest: `not assigned`
- Validator S3 prefix and manifest: `not assigned`
- Bot Builder S3 prefix and manifest: `not assigned`
- Reality paper S3 prefix and manifest: `not assigned`
- Reality live S3 prefix and manifest: `not assigned`
- EC2 start, upload, stop-request, and stopped-state UTC times: `not assigned`
- Cleanup action or deadline: `not assigned`
- Final stopped-state evidence: `not assigned`

## Council Result

No result yet.

## Builder Result

No result yet.

## Validator Result

No result yet.

## Bot Builder Result

No result yet. State when Validator did not pass and no bot was built.

## Reality Result

No result yet. Record paper first, then the explicitly approved 2-3 real-money windows when applicable.

## Decision

No decision yet. Manager records `reject`, `inconclusive`, `blocked`, or `stage1_winner` from the recorded Results.

## Retrospective

No retrospective yet.

## Git Stage History

Before final archive, list the full Git SHAs for the Council Result, Experiment Test, Builder Result, Validator Result and decision, Bot Builder Result when applicable, paper Result, exact human approval when applicable, every real-money window, and final pre-archive decision. Use `not applicable` for stages that were correctly skipped. Git history for the archived experiment file identifies the final archive commit; a commit cannot contain its own SHA.

- Council Result commit: `not assigned`
- Experiment Test commit: `not assigned`
- Builder Result commit: `not assigned`
- Validator Result and decision commit: `not assigned`
- Bot Builder Result commit: `not assigned`
- Paper Result and decision commit: `not assigned`
- Human real-money approval commit: `not assigned`
- Real-money window Result commits: `not assigned`
- Final pre-archive decision commit: `not assigned`

## History

Before starting another hypothesis, preserve this record as `experiments/<experiment-id>.md` and commit its evidence and lessons. Use stage subjects in the form `polyloop(<campaign>/<experiment>): <completed-stage>`. `polyloop status` observes unique experiment IDs but never controls their lifecycle.
