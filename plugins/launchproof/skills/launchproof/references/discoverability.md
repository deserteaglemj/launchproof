# Discoverability: people, search engines and AI agents

## GitHub repo metadata (`docs/launch/repo-metadata.json`)

- **description**: 1 sentence, under 350 characters, starts with the category words people search ("Screenshot to code plugin for Claude Code and Codex: ..."). No superlatives.
- **topics**: 8 to 20, lowercase, hyphens, under 50 characters each. Mix: category (`readme-generator`), ecosystem (`claude-code`, `codex`, `python`), task (`open-source`, `launch-checklist`), format (`llms-txt`).
- **homepage**: the GitHub Pages URL.
- Applied by the owner after approval: `gh repo edit OWNER/REPO --description "..." --homepage "..." --add-topic t1 --add-topic t2`.

## Social preview

1280x640 PNG (2:1), readable at thumbnail size: name, one-line value, repo URL. Build `docs/social-preview.html` and render it with `lp.py render docs/social-preview.html docs/social-preview.png`. GitHub has no API for this: the owner uploads it in Settings > General > Social preview.

## llms.txt (spec: https://llmstxt.org, AnswerDotAI/llms-txt, Apache-2.0)

At the repo root (and copied to `docs/` so Pages serves it):

```
# Name

> One-paragraph summary that answers "what is it, who is it for, how is it different".

Optional short notes.

## Docs

- [README](absolute URL): what it covers
- [AGENTS.md](absolute URL): commands and layout

## Optional

- [Secondary links](URL)
```

Use absolute GitHub URLs so the file works when fetched alone.

## AGENTS.md (spec: https://agents.md)

For coding agents working in the repo: one-line purpose, install, the exact test commands CI runs, a layout map, and rules for changes (version sync, evidence for claims). Keep it short and command-first.

## GitHub Pages landing page (`docs/index.html`)

- `<title>` and meta description with the same category words as the README's first sentence.
- `<link rel="canonical">` to the Pages URL.
- Open Graph: `og:title`, `og:description`, `og:image` (absolute URL to the social preview), `og:url`, plus `twitter:card` = `summary_large_image`.
- JSON-LD: `SoftwareSourceCode` (or `SoftwareApplication` with `applicationCategory` `DeveloperApplication`) with `name`, `description`, `codeRepository`, `license`, `author`, `programmingLanguage`, and `softwareVersion`. Add a `FAQPage` block that mirrors the README FAQ.
- `docs/robots.txt` allowing all and naming the sitemap; `docs/sitemap.xml` listing the page.
- Same content as the README in fewer words; links back to GitHub. Works at 375px wide, light and dark.
- The owner enables Pages (Settings > Pages > main /docs) or with `gh api -X POST repos/OWNER/REPO/pages -f source[branch]=main -f source[path]=/docs` after approval.

## Plugin and package manifests

- Claude Code plugin: `.claude-plugin/plugin.json` (name, version, description, author, homepage, repository, license, keywords) and a `marketplace.json` so `/plugin marketplace add OWNER/REPO` works. Validate with `claude plugin validate --strict`.
- Codex plugin: `.codex-plugin/plugin.json` with `skills` and an `interface` block (displayName, shortDescription, category, defaultPrompt). Same marketplace file works for `codex plugin marketplace add OWNER/REPO`.
- Skills: the `description` field decides when an agent loads the skill. List the phrases people actually type ("make this repo public", "polish my README", "launch my project").
- npm `package.json` / PyPI `pyproject.toml`: description, keywords, repository, homepage, license, matching version.

## Search indexing

Indexing by search engines and AI crawlers takes days to weeks and cannot be verified at publish time. Report it as unproven. Speed it up only through legitimate means: a linked Pages site, a sitemap, and real links from launch posts.
