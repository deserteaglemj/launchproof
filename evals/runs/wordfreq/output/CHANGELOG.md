# Changelog

All notable changes to this project are documented here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project uses [Semantic Versioning](https://semver.org/).

## [Unreleased]

## [0.3.0] - 2026-10-17

First public release.

### Added

- `wordfreq FILE... [-n N] [--stop w1,w2]` prints the N most common words across all files.
- Case-insensitive counting; apostrophes kept inside words and stripped at the edges.
- Invalid UTF-8 bytes are replaced instead of crashing.
- Eval set (`evals/`), sample texts (`examples/`), CI, and project docs.

### Fixed

- Unit tests were not discovered by `python3 -m unittest discover` (missing `tests/__init__.py`).
- `scripts/bench.sh` no longer points at a hard-coded local path.
