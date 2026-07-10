# Polyloop Repository Instructions

## Scope

This repository builds the `polyloop` CLI. It is not itself a strategy workspace. Do not initialize a strategy in this repository unless the user explicitly requests that location.

Keep Polyloop limited to scaffolding, tmux role processes, provider launch context, and status observation. Campaign and experiment decisions belong to the strategy manager. Polyloop must not submit trades, connect wallets, control capital, invent market facts, or impose an experiment count.

## Development

- Read the surrounding implementation and tests before changing behavior.
- Preserve compatibility with existing strategy workspaces whenever practical.
- Run the full test suite after code changes.
- Keep provider-specific behavior at the launch boundary; role and evidence contracts remain provider-neutral.

## Strategy Bootstrap

When the user asks this Codex session to create or start a strategy:

1. Resolve a separate target Git directory and a unique tmux session name.
2. Gather the campaign seed. At minimum it needs a finite objective and stopping condition, the exact market or clearly marked uncertainties, starting baseline, authoritative data snapshot, canonical evaluator, paper-observation requirement, resource boundary, and safety constraints. Never invent missing facts.
3. For a new workspace, run `polyloop init --no-launch` with the target `--root`, `--session`, market, and objective. This creates the files and tmux windows without starting role models before the seed is ready.
4. Complete the target workspace's `PROJECT_CHARTER.md` and `CAMPAIGN.md`. Set a campaign ID, keep `status = "draft"` while required fields are missing, and keep `auto_start = false`.
5. Only after the seed is complete, set `status = "ready"` and `auto_start = true`.
6. Run `polyloop status --root <target>` and resolve material warnings.
7. Ensure the manager provider can reach the local tmux socket without disabling its filesystem sandbox. For current Codex CLI versions, set the manager's `extra_args` to `["--sandbox", "workspace-write", "--config", "sandbox_workspace_write.network_access=true"]` when the owner accepts network access. Do not use full-access or sandbox-bypass flags. Other roles should receive only the permissions their function needs.
8. When external discovery is requested, configure `[external_researcher]` with the chosen provider command. Keep the function name provider-neutral and let that provider use its own native tools.
9. Confirm the `reality` window contains its prebuilt `reality-controller` and `bot-integrator` panes. The controller checks and deploys the integrator's immutable artifact; neither replaces the canonical offline verifier.
10. Run `polyloop init --root <target>` to launch idle role windows. The manager launch prompt will validate the seed and directly create its native finite goal. Do not automate a literal `/goal` by injecting keystrokes into tmux.

For an existing running session, do not use `--restart` until you have verified that replacing every role process will not interrupt active work. A paused campaign remains paused until the human owner explicitly resumes it.
