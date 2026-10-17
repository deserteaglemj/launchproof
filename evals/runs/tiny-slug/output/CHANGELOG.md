# Changelog

All notable changes to this project are documented here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project uses [Semantic Versioning](https://semver.org/).

## [Unreleased]

## [1.2.0] - 2026-10-17

First public release.

### Added

- `slugify(input, { separator, maxLength })`: lowercase ASCII slugs with accent stripping and `&` to `and`.
- Unit tests (`npm test`) and an edge-case eval (`node evals/run.js`) with recorded results in `evals/RESULTS.md`.
- README, license, contributing guide, security policy, CI and a GitHub Pages site.
