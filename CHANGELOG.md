# Changelog

All notable changes to this project are documented here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project uses [Semantic Versioning](https://semver.org/).

## [Unreleased]

## [0.1.0] - 2026-10-17

### Added

- `launchproof` skill for Claude Code and Codex (invoke as `/launchproof` or by asking): hygiene scan, proof, scaffold, README, discoverability files, CI, release notes, launch plan, audit-and-fix loop, owner-approval report.
- `lp.py` helper (standard library only): `facts`, `hygiene` (full git history: commit emails, personal emails, home paths, 10 secret patterns, sensitive files, private names, images to review), `scaffold`, `audit` (scored launch checklist), `render` (social preview).
- Templates for community health files, llms.txt, Pages landing page with JSON-LD and Open Graph, robots.txt, sitemap, repo metadata and release notes.
- Self-tests, an eval harness with two seeded fixtures and the shotproof repo, and CI that runs the hygiene scan and the audit on this repo.
