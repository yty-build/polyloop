# Functionality Log

This is the canonical register of bot functionality that has already been built and verified. Experiments change strategy behavior; they do not rebuild compatible bot infrastructure.

## Reuse Rules

- Bot Builder reads this file before proposing code changes.
- Reuse every `verified` functionality whose interface and recorded limitations satisfy the current Owner Test Directive.
- Reuse means using the recorded canonical path and Git SHA. Copying, rewriting, renaming, or independently reimplementing the same functionality is a rebuild.
- A different experiment, model, coding style, preferred library, or desire to clean up code is not a technical limitation.
- Rebuilding or replacing verified functionality requires a technical limitation recorded before code changes. The record must identify the existing functionality and SHA, required behavior it cannot provide, reproducing evidence, why configuration or a small adapter is insufficient, and the smallest proposed change.
- Reality reviews technical-limitation evidence. If the change would alter the Owner Test Directive or Owner Capital Authorization, only a new explicit owner directive can authorize it.
- After Bot Builder records the evidence and Reality verifies it, Manager updates the existing entry or adds the genuinely new functionality in the same Bot Builder stage commit. Never delete history; mark replaced functionality `deprecated` and link its replacement.
- Missing or unverified functionality may be built, but it must pass focused, parity, and failure tests before being marked `verified`.

## Verified Functionality

No verified functionality recorded yet.

## Entry Format

### `<functionality name>`

- Status (`verified`, `limited`, or `deprecated`): `not assigned`
- Canonical path or package: `not assigned`
- Verified full Git SHA: `not assigned`
- Interface and configuration contract: `not assigned`
- Verification evidence and checksums: `not assigned`
- Compatible markets, strategies, and environments: `not assigned`
- Known technical limitations: `not assigned`
- Replaces or replaced by: `not applicable`
- Last verified experiment and UTC time: `not assigned`
