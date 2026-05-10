# Security and Privacy

This project stores personal reflection data as local markdown. It is not a secure vault.

## Privacy Model

- `private/` is gitignored and should never be pushed to a remote.
- `private/system-instructions.md` is the single personal configuration file.
- `AGENTS.md` is public scaffolding. Do not put personal ritual preferences, relationship details, or private context there.
- `CLAUDE.md` is only a Claude Code compatibility shim to the public `AGENTS.md`.
- Backups archive `private/` only, excluding generated/cache material and imports by default.

## Provider Caveat

When you use an AI coding assistant, prompts and file contents may be sent to that provider's servers. Do not put passwords, financial account numbers, API keys, or material that would harm you or others if exposed into this system.

## Before Publishing a Fork

Run:

```bash
bash scripts/public-sanity-check.sh
```

Also review git history for author identity and accidentally committed private material:

```bash
git log --all --format='%h %an <%ae> %s'
git log --all --name-status -- private .env '*.pem' '*.key'
```

If sensitive data was ever committed, a normal cleanup commit is not enough. Rewrite history or publish a fresh repository.
