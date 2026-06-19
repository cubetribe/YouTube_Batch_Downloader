# Repository Governance

This is an open-source Python CLI repository for a local YouTube downloader.

## Workflow

- Use GitHub Flow: work on short-lived branches and integrate through pull requests.
- Do not edit `main` directly.
- Do not commit, push, publish, or deploy without explicit maintainer approval.
- Keep changes scoped and buildable; avoid unrelated refactors.

## Safety

- Do not commit secrets, local credentials, cookies, tokens, or generated downloads.
- Tests must not perform real downloads.
- Mock `yt_dlp`, network calls, browser cookies, filesystem download outputs, and other external services in automated tests.
- Keep local logs such as `/download_log.txt` out of version control.

## Release Model

- This repository uses a manual Keep a Changelog release model.
- Record user-visible or project-governance changes under `CHANGELOG.md` `[Unreleased]`.
- Do not bump versions unless explicitly preparing a release.

## Validation

Run the checks that match the changed scope. For repo hardening and Python CLI changes, use:

```bash
python -m ruff check start.py src tests --select E9,F63,F7,F82 --target-version py310
python -m compileall -q start.py src gui download_4k.py download_best.py download_force_4k.py download_hd.py download_strict_hd.py download_ultimate.py
python -m pytest -q
```
