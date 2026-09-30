# Publishing the GitHub profile

Public destination: [danielcamposramos/danielcamposramos](https://github.com/danielcamposramos/danielcamposramos).
Daniel authorized initial publication on 2026-09-30.

GitHub displays a profile README from a **public** repository whose name matches
the account: `danielcamposramos/danielcamposramos`, with `README.md` at its root.
See the [official requirements](https://docs.github.com/en/account-and-profile/how-tos/profile-customization/managing-your-profile-readme).

The original local draft history contains links to an unlisted biographical
source. Removing them from the current files does not remove them from Git
history. **Do not publish the draft history.** It is retained locally on
`private/local-draft`; the public `main` branch starts with a clean snapshot,
without the draft commits as ancestors. Both branches stay in the canonical
local repository at `/K3D/GitHub/danielcamposramos`.

For later approved updates, work on `main` and push only that branch:

```bash
cd /K3D/GitHub/danielcamposramos
git switch main
python3 tools/profile.py check --history
git diff --check
git push origin main
```

Run validation successfully before pushing; do not continue after a failed
check. The local privacy-check setting must remain configured; do not print its
value or commit it. Editor backups are ignored and excluded from publication.

Never push `--all`, `--mirror`, or the `private/local-draft` branch. Do not merge
the draft branch into `main`. Preserve the local draft record; no history
deletion or force-push is needed.

Before initial creation, the authenticated account and destination absence
were checked. If another partner creates the destination before publication,
inspect and reconcile it rather than overwriting it. The clean root's privacy
check must pass before `gh repo create --public --source . --remote origin --push`.

Suggested native GitHub pins: Knowledge3D, sony-bravia-linux, Array42,
respec-mcp, awesome-stereoscopy and awesome-linux-hdr. Pinning and account-bio
updates are separate owner choices, not automated by this repository.

The existing GitHub bio still describes degree study in progress. The profile
draft uses Daniel's current biography. A possible owner-approved
replacement is:

> Electrical engineer · EchoSystems AI Studios founder · W3C PM-KR Community Group co-chair · Open systems & human–AI collective intelligence

## Maintaining the profile

Edit the introduction directly in `README.md`. Keep sources and claim
boundaries in [profile-provenance.md](profile-provenance.md). For artwork, edit
the `.svg.source` files and run `python3 tools/profile.py build`, then
`python3 tools/profile.py check`. Commit the sources and their generated SVGs
together.
