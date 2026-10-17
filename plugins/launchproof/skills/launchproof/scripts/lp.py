#!/usr/bin/env python3
"""launchproof helper: facts, hygiene, scaffold, audit, render.

Standard library only (Python 3.9+). Never pushes, publishes or posts.

  lp.py facts PATH                      project facts as JSON
  lp.py hygiene PATH [--names FILE] [--allow REGEX ...] [--json]
                                        scan full git history + working tree; exit 1 on blocking findings
  lp.py scaffold PATH --name N --owner O --description D [--contact EMAIL] [--homepage URL]
                                        copy missing templates (never overwrites)
  lp.py audit PATH [--json] [--min 90] [--names FILE]
                                        scored launch checklist; exit 1 below --min or on a required failure
  lp.py render HTML OUT.png [--size 1280x640]
                                        screenshot an HTML file (social preview) with Playwright or Chrome
"""
import argparse
import datetime
import json
import os
import re
import shutil
import struct
import subprocess
import sys
from html.parser import HTMLParser
from pathlib import Path

HERE = Path(__file__).resolve().parent
TEMPLATES = HERE.parent / "templates"

SKIP_DIRS = {".git", "node_modules", ".venv", "venv", "__pycache__", "dist", "build", ".next", ".tox", "target"}
IMAGE_EXT = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".ico", ".bmp", ".tiff", ".avif"}
NOREPLY = re.compile(r"(@users\.noreply\.github\.com|^noreply@|^no-reply@|@noreply\.)", re.I)
EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
PERSONAL_EMAIL = re.compile(
    r"[A-Za-z0-9._%+-]+@(?:gmail|googlemail|yahoo|ymail|hotmail|outlook|live|msn|icloud|me|mac|aol|"
    r"proton|protonmail|pm|gmx|yandex|mail|zoho|fastmail|hey)\.(?:com|me|net|ch|de|ru)\b", re.I)
HOME_PATH = re.compile(r"(?<![\w$])(?:/Users/|/home/|[A-Za-z]:\\+Users\\+)([A-Za-z0-9._-]+)")
PLACEHOLDER_USERS = {
    "user", "username", "you", "yourname", "your-name", "me", "name", "runner", "example", "foo", "bar",
    "alice", "bob", "jane", "john", "jdoe", "shared", "guest", "admin", "ubuntu", "root", "vscode", "node",
    "app", "codespace", "codespaces", "default", "public", "test", "dev", "x", "someone", "a", "u",
}
SECRETS = [
    ("aws-access-key", re.compile(r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b")),
    ("github-token", re.compile(r"\bgh[pousr]_[A-Za-z0-9]{36,}\b")),
    ("github-pat", re.compile(r"\bgithub_pat_[A-Za-z0-9_]{50,}\b")),
    ("anthropic-key", re.compile(r"\bsk-ant-[A-Za-z0-9_-]{20,}")),
    ("openai-key", re.compile(r"\bsk-(?:proj-|svcacct-)?[A-Za-z0-9_-]{32,}")),
    ("slack-token", re.compile(r"\bxox[abprs]-[A-Za-z0-9-]{10,}")),
    ("google-api-key", re.compile(r"\bAIza[0-9A-Za-z_-]{35}\b")),
    ("stripe-live-key", re.compile(r"\b[sr]k_live_[0-9A-Za-z]{20,}")),
    ("private-key", re.compile(r"-----BEGIN (?:[A-Z]+ )?PRIVATE KEY-----")),
    ("assigned-secret", re.compile(
        r"(?i)\b(?:api[_-]?key|secret|token|passwd|password|client[_-]?secret)\b[\"']?\s*[:=]\s*[\"']([^\"'\s$<>{}]{12,})[\"']")),
]
SENSITIVE_FILES = re.compile(r"(^|/)(\.env(\..+)?|id_rsa|id_ed25519|id_ecdsa|.+\.pem|.+\.p12|.+\.pfx|.+\.key|"
                             r"credentials\.json|service-account.*\.json|\.npmrc|\.pypirc|\.netrc)$")
ENV_EXAMPLE = re.compile(r"\.env\.(example|sample|template|dist)$")
_SUPER = r"(?:first|only|best|fastest|leading|most advanced|most powerful|most complete)"
_THING = r"(?:tool|plugin|app|library|framework|platform|solution|project|cli|skill|way|option|choice|agent|extension)"
BANNED_CLAIMS = re.compile(
    r"(?i)(?:\b(?:is|are|was|as|be|being)\s+(?:the|our)\s+" + _SUPER + r"\b|[\w)]['\u2019]s\s+" + _SUPER + r"\b|"
    r"\bworld['\u2019]?s\s+" + _SUPER + r"\b|\bthe\s+" + _SUPER + r"\s+(?:[\w+-]+\s+){0,3}" + _THING + r"s?\b|"
    r"\bbest[- ]in[- ]class|#1\b|\bnumber one\b|\bgame[- ]chang\w*|\brevolutionary\b|\bblazing(?:ly)?[- ]fast|"
    r"\bindustry[- ]leading|\bunparalleled\b|\bcutting[- ]edge\b|\bstate[- ]of[- ]the[- ]art\b)")


PLACEHOLDER = re.compile(r"(?<!\$)\{\{[A-Z][A-Z_]*\}\}")  # scaffold tokens like {{NAME}}, not GitHub Actions ${{ }}


def run(args, cwd=None, check=False, binary=False):
    r = subprocess.run(args, cwd=cwd, capture_output=True, text=not binary)
    if check and r.returncode:
        raise SystemExit(f"command failed: {' '.join(args)}\n{r.stderr}")
    return r


def is_git(path):
    return run(["git", "rev-parse", "--is-inside-work-tree"], cwd=path).returncode == 0


def mask(s):
    s = str(s)
    return s[:2] + "***" if len(s) > 2 else "***"


def mask_in(line, token):
    return line.replace(token, mask(token))


# ---------------------------------------------------------------- facts

def facts(path):
    p = Path(path).resolve()
    f = {"path_name": p.name, "git": is_git(p)}
    if f["git"]:
        f["remote"] = run(["git", "remote", "get-url", "origin"], cwd=p).stdout.strip() or None
        f["branch"] = run(["git", "branch", "--show-current"], cwd=p).stdout.strip()
        f["commits"] = int(run(["git", "rev-list", "--all", "--count"], cwd=p).stdout.strip() or 0)
        f["tags"] = run(["git", "tag", "--sort=-v:refname"], cwd=p).stdout.split()[:5]
        f["files"] = run(["git", "ls-files"], cwd=p).stdout.splitlines()
    else:
        f["files"] = [str(x.relative_to(p)) for x in walk(p)]
    exts = {}
    for name in f["files"]:
        e = Path(name).suffix.lower()
        if e:
            exts[e] = exts.get(e, 0) + 1
    f["top_extensions"] = sorted(exts.items(), key=lambda kv: -kv[1])[:8]
    manifests = [m for m in ("package.json", "pyproject.toml", "setup.py", "Cargo.toml", "go.mod", "Gemfile",
                             "composer.json", ".claude-plugin/plugin.json", ".claude-plugin/marketplace.json",
                             ".codex-plugin/plugin.json") if (p / m).exists()]
    manifests += [str(x.relative_to(p)) for x in p.glob("plugins/*/.*-plugin/plugin.json")]
    f["manifests"] = manifests
    f["version"] = detect_version(p)
    tests = []
    if (p / "package.json").exists():
        scripts = load_json(p / "package.json").get("scripts", {}) or {}
        tests += [f"npm run {k}" for k in scripts if k in ("test", "lint", "build")]
    if any(n.endswith(".py") for n in f["files"]):
        tests.append("python3 -m unittest discover" if not (p / "pytest.ini").exists() else "pytest")
    if (p / "Cargo.toml").exists():
        tests.append("cargo test")
    if (p / "go.mod").exists():
        tests.append("go test ./...")
    f["test_command_guesses"] = tests
    lic = p / "LICENSE"
    f["license_first_line"] = lic.read_text(errors="ignore").splitlines()[0] if lic.exists() else None
    f["present"] = {k: bool(v) for k, v in present_files(p).items()}
    del f["files"]
    return f


def load_json(path):
    try:
        return json.loads(Path(path).read_text())
    except Exception:
        return {}


def detect_version(p):
    for m in ["package.json", ".claude-plugin/plugin.json"] + [str(x.relative_to(p)) for x in p.glob("plugins/*/.claude-plugin/plugin.json")]:
        v = load_json(p / m).get("version")
        if v:
            return v
    for m in ("pyproject.toml", "Cargo.toml"):
        if (p / m).exists():
            hit = re.search(r'(?m)^version\s*=\s*"([^"]+)"', (p / m).read_text(errors="ignore"))
            if hit:
                return hit.group(1)
    return None


def walk(root):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fn in filenames:
            yield Path(dirpath) / fn


# ---------------------------------------------------------------- hygiene

def scan_text(text, where, path, names, allow, out):
    if path and SENSITIVE_FILES.search(path) and not ENV_EXAMPLE.search(path):
        out.append(dict(kind="sensitive-file", severity="block", where=where, path=path, line=0, evidence=Path(path).name))
    for i, line in enumerate(text.splitlines(), 1):
        if len(line) > 4000:
            line = line[:4000]
        if allow and any(a.search(line) for a in allow):
            continue
        for m in HOME_PATH.finditer(line):
            if m.group(1).lower() not in PLACEHOLDER_USERS and not m.group(1).startswith(("<", "$", "{")):
                out.append(dict(kind="home-path", severity="block", where=where, path=path, line=i,
                                evidence=mask_in(m.group(0), m.group(1))))
        for m in PERSONAL_EMAIL.finditer(line):
            out.append(dict(kind="personal-email", severity="block", where=where, path=path, line=i, evidence=mask(m.group(0))))
        for kind, rx in SECRETS:
            for m in rx.finditer(line):
                tok = m.group(1) if m.groups() else m.group(0)
                if kind == "assigned-secret" and re.search(r"(?i)(example|placeholder|your[_-]|xxxx|changeme|dummy|fake|test)", tok):
                    continue
                out.append(dict(kind=kind, severity="block", where=where, path=path, line=i, evidence=mask(tok)))
        for n in names:
            m = n.search(line)
            if m:
                out.append(dict(kind="private-name", severity="block", where=where, path=path, line=i, evidence=mask(m.group(0))))


def hygiene(path, names_file=None, allow=(), revs=()):
    p = Path(path).resolve()
    names = []
    if names_file:
        for raw in Path(names_file).read_text().splitlines():
            raw = raw.strip()
            if raw and not raw.startswith("#"):
                names.append(re.compile(r"(?i)\b" + re.escape(raw) + r"\b"))
    allow = [re.compile(a) for a in allow]
    out = []
    if is_git(p):
        refs = list(revs) or ["--all"]
        log = run(["git", "log", *refs, "--format=%H%x1f%an%x1f%ae%x1f%cn%x1f%ce%x1f%B%x1e"], cwd=p).stdout
        seen = set()
        for rec in log.split("\x1e"):
            parts = rec.strip("\n").split("\x1f")
            if len(parts) < 6:
                continue
            sha, _an, ae, _cn, ce, body = parts
            for role, email in (("author", ae), ("committer", ce)):
                if email and not NOREPLY.search(email) and not any(a.search(email) for a in allow) and (role, email) not in seen:
                    seen.add((role, email))
                    out.append(dict(kind=f"{role}-email", severity="block", where=sha[:8], path="(commit metadata)",
                                    line=0, evidence=mask(email)))
            for m in EMAIL.finditer(body):
                e = m.group(0)
                if not NOREPLY.search(e) and not any(a.search(e) for a in allow) and ("body", e) not in seen:
                    seen.add(("body", e))
                    out.append(dict(kind="message-email", severity="block", where=sha[:8], path="(commit message)",
                                    line=0, evidence=mask(e)))
            scan_text(body, sha[:8], "(commit message)", names, allow, out)
        # every blob reachable from any ref, deleted files included
        objs = run(["git", "rev-list", *refs, "--objects"], cwd=p).stdout.splitlines()
        paths = {}
        for o in objs:
            sha, _, name = o.partition(" ")
            if name:
                paths.setdefault(sha, name)
        if paths:
            r = subprocess.run(["git", "cat-file", "--batch-check"], cwd=p, input="\n".join(paths) + "\n",
                               capture_output=True, text=True)
            blobs = []
            for line in r.stdout.splitlines():
                bits = line.split()
                if len(bits) == 3 and bits[1] == "blob":
                    blobs.append((bits[0], int(bits[2])))
            for sha, size in blobs:
                name = paths[sha]
                if Path(name).suffix.lower() in IMAGE_EXT:
                    out.append(dict(kind="image-review", severity="review", where=sha[:8], path=name, line=0,
                                    evidence="check you own or may publish this image (no third-party logos or real-site screenshots)"))
                if size > 2_000_000:
                    continue
                data = run(["git", "cat-file", "blob", sha], cwd=p, binary=True).stdout
                if b"\0" in data[:8000]:
                    if SENSITIVE_FILES.search(name):
                        scan_text("", "history", name, names, allow, out)
                    continue
                scan_text(data.decode("utf-8", "ignore"), "history", name, names, allow, out)
        # the files as they are on disk now (tracked and untracked, not ignored)
        current = run(["git", "ls-files", "-c", "-o", "--exclude-standard"], cwd=p).stdout.splitlines()
        files = [p / x for x in dict.fromkeys(current) if (p / x).is_file()]
    else:
        files = list(walk(p))
    for fp in files:
        rel = str(fp.relative_to(p))
        if fp.suffix.lower() in IMAGE_EXT and not is_git(p):
            out.append(dict(kind="image-review", severity="review", where="worktree", path=rel, line=0,
                            evidence="check you own or may publish this image"))
        try:
            if fp.stat().st_size > 2_000_000:
                continue
            data = fp.read_bytes()
        except OSError:
            continue
        if b"\0" in data[:8000]:
            continue
        scan_text(data.decode("utf-8", "ignore"), "worktree", rel, names, allow, out)
    # one finding per (kind, path, evidence)
    uniq, keys = [], set()
    for f in out:
        k = (f["kind"], f["path"], f["evidence"], f["where"] == "worktree")
        if k not in keys:
            keys.add(k)
            uniq.append(f)
    return uniq


FIX_HINTS = {
    "author-email": "Rewrite authorship to your GitHub noreply address: git filter-repo --mailmap mailmap.txt (after a git bundle backup); set git config user.email to the noreply address for future commits.",
    "committer-email": "Same as author-email: rewrite with git filter-repo --mailmap.",
    "message-email": "Rewrite commit messages: git filter-repo --replace-message replacements.txt.",
    "personal-email": "Replace the address in the file; if it is in history, git filter-repo --replace-text replacements.txt.",
    "home-path": "Use relative paths or ~ in docs and code; purge from history with git filter-repo --replace-text.",
    "private-name": "Remove or genericize the name; purge from history with git filter-repo --replace-text.",
    "sensitive-file": "Delete the file, add it to .gitignore, purge with git filter-repo --invert-paths --path FILE, and rotate anything it held.",
    "image-review": "Confirm you own or may publish it; replace third-party logos and real-site screenshots with your own.",
}


def secret_hint(kind):
    return FIX_HINTS.get(kind, "Revoke and rotate the secret first, then purge it with git filter-repo --replace-text; a rewrite alone does not make a leaked secret safe.")


# ---------------------------------------------------------------- scaffold

def scaffold(path, values):
    p = Path(path).resolve()
    created, kept = [], []
    for src in sorted(TEMPLATES.rglob("*")):
        if src.is_dir():
            continue
        rel = src.relative_to(TEMPLATES)
        dest = p / rel
        if dest.exists() or (rel.name == "CODE_OF_CONDUCT.md" and (p / ".github" / rel.name).exists()):
            kept.append(str(rel))
            continue
        dest.parent.mkdir(parents=True, exist_ok=True)
        text = src.read_text()
        for k, v in values.items():
            text = text.replace("{{" + k + "}}", v)
        dest.write_text(text)
        created.append(str(rel))
    return created, kept


# ---------------------------------------------------------------- audit

class Meta(HTMLParser):
    def __init__(self):
        super().__init__()
        self.meta, self.ld, self.title, self.canonical, self._ld, self._t = {}, [], "", None, False, False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "meta":
            k = a.get("property") or a.get("name")
            if k:
                self.meta[k.lower()] = a.get("content", "")
        elif tag == "script" and (a.get("type") or "").lower() == "application/ld+json":
            self._ld = True
            self.ld.append("")
        elif tag == "title":
            self._t = True
        elif tag == "link" and (a.get("rel") or "").lower() == "canonical":
            self.canonical = a.get("href")

    def handle_endtag(self, tag):
        if tag == "script":
            self._ld = False
        if tag == "title":
            self._t = False

    def handle_data(self, data):
        if self._ld:
            self.ld[-1] += data
        if self._t:
            self.title += data


def strip_code(md):
    return re.sub(r"```.*?```", "", md, flags=re.S)


def section(md, heading_rx):
    """Text of the first heading matching heading_rx up to the next heading of the same or higher level."""
    lines = md.splitlines()
    for i, line in enumerate(lines):
        m = re.match(r"^(#{1,6})\s+(.*)", line)
        if m and re.search(heading_rx, m.group(2), re.I):
            level = len(m.group(1))
            body = []
            for nxt in lines[i + 1:]:
                n = re.match(r"^(#{1,6})\s", nxt)
                if n and len(n.group(1)) <= level:
                    break
                body.append(nxt)
            return "\n".join(body)
    return None


def png_size(path):
    with open(path, "rb") as fh:
        head = fh.read(24)
    if head[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    return struct.unpack(">II", head[16:24])


def present_files(p):
    def first(*cands):
        for c in cands:
            hits = list(p.glob(c))
            if hits:
                return hits[0]
        return None
    return {
        "readme": first("README.md", "readme.md", "README"),
        "license": first("LICENSE", "LICENSE.md", "LICENSE.txt"),
        "contributing": first("CONTRIBUTING.md", ".github/CONTRIBUTING.md", "docs/CONTRIBUTING.md"),
        "code_of_conduct": first("CODE_OF_CONDUCT.md", ".github/CODE_OF_CONDUCT.md", "docs/CODE_OF_CONDUCT.md"),
        "security": first("SECURITY.md", ".github/SECURITY.md", "docs/SECURITY.md"),
        "changelog": first("CHANGELOG.md", "CHANGES.md", "HISTORY.md"),
        "issue_templates": first(".github/ISSUE_TEMPLATE/*.yml", ".github/ISSUE_TEMPLATE/*.md", ".github/ISSUE_TEMPLATE.md"),
        "pr_template": first(".github/pull_request_template.md", ".github/PULL_REQUEST_TEMPLATE.md", "pull_request_template.md", "docs/pull_request_template.md"),
        "workflow": first(".github/workflows/*.yml", ".github/workflows/*.yaml"),
        "llms_txt": first("llms.txt", "docs/llms.txt"),
        "agents_md": first("AGENTS.md"),
        "pages_index": first("docs/index.html", "index.html"),
        "robots": first("docs/robots.txt", "robots.txt"),
        "sitemap": first("docs/sitemap.xml", "sitemap.xml"),
        "repo_metadata": first("docs/launch/repo-metadata.json"),
        "social_preview": first("docs/social-preview.png", "assets/social-preview.png", ".github/social-preview.png"),
        "launch_plan": first("docs/launch/LAUNCH-PLAN.md"),
        "release_notes": first("docs/releases/*.md", "RELEASE_NOTES.md", "docs/RELEASE_NOTES.md"),
    }


CHANNELS = ["show hn", "reddit", "x (twitter)", "linkedin", "product hunt", "dev.to", "hashnode", "discord", "slack",
            "awesome", "plugin directory", "newsletter", "mastodon", "bluesky", "lobsters", "codex", "skill"]


def audit(path, names_file=None, revs=()):
    p = Path(path).resolve()
    files = present_files(p)
    checks = []

    def add(cid, ok, weight, detail="", required=False, na=False):
        checks.append(dict(id=cid, ok=bool(ok), weight=weight, detail=detail, required=required, na=na))

    readme_path = files["readme"]
    readme = readme_path.read_text(errors="ignore") if readme_path else ""
    prose = strip_code(readme)
    head = "\n".join(readme.splitlines()[:40])

    add("readme", readme_path, 5, "README.md exists", required=True)
    add("license", files["license"], 5, "LICENSE exists", required=True)
    top = "\n".join(readme.splitlines()[:12])
    add("hero", (re.search(r"(?m)^#\s+\S", head) or re.search(r"<h1|!\[|<img\s", top, re.I))
        and re.search(r"(?m)^(?!#|\s*$|!\[|<|\[!\[|\s*[-*|>]).{60,}", head),
        3, "title or hero image plus a one-line description in the first 40 lines")
    badges = re.findall(r"(?:!\[[^\]]*\]\(|<img[^>]*src=[\"'])(https?://[^)\"']*(?:badge|shields\.io)[^)\"']*)", head)
    add("badges", badges, 2, f"{len(badges)} badge(s) near the top")
    demo = re.search(r"(!\[[^\]]*\]\([^)]+\)|<img\s|<video\s|\.(gif|mp4|webm|mov)\b)", "\n".join(readme.splitlines()[:80]), re.I)
    add("demo", demo, 3, "image, GIF or video in the first 80 lines")
    qs = section(readme, r"install|quick ?start|getting started|usage|setup")
    add("quickstart", qs and "```" in qs, 4, "install/quickstart section with a code block")
    faq = section(readme, r"^faq|frequently asked")
    nq = len(re.findall(r"(?m)^(?:#{2,5}\s+[^\n]{8,}\?\s*$|[-*]?\s*\*\*[^*\n]{8,}\?\*\*|[^\n#*][^\n]{8,}\?\s*$)", faq or ""))
    add("faq", faq is not None and nq >= 5, 4, f"FAQ with {nq} question(s), need 5+")
    lim = section(readme, r"limitation|known issues|caveats")
    nl = len(re.findall(r"(?m)^\s*[-*]\s+\S", lim or ""))
    add("limitations", lim is not None and nl >= 3, 4, f"Limitations with {nl} bullet(s), need 3+")
    comp = section(readme, r"compar|alternative|\bvs\b|versus|how .* differ")
    add("comparison", comp and re.search(r"\]\(https?://", comp), 3, "comparison section that links its sources")
    proof = section(readme, r"eval|benchmark|proof|results|test results|numbers")
    proof_ok, proof_detail = False, "no eval/proof section"
    if proof:
        links = [l for l in re.findall(r"\]\(([^)#\s]+)", proof) if not l.startswith(("http", "mailto"))]
        nums = set(re.findall(r"\d+(?:\.\d+)?%?", strip_code(proof)))
        backed = []
        for l in links:
            fp = (p / l).resolve()
            if fp.is_file():
                body = fp.read_text(errors="ignore")
                backed += [n for n in nums if len(n.rstrip("%")) > 1 and n in body]
        proof_ok = bool(links) and bool(backed)
        proof_detail = f"{len(links)} local link(s); {len(set(backed))} number(s) found in the linked file(s)"
    add("proof", proof_ok, 5, proof_detail, required=True)
    surfaces = [("README.md", prose)]
    for extra in ("llms.txt", "docs/index.html"):
        if (p / extra).exists():
            surfaces.append((extra, re.sub(r"<[^>]+>", " ", (p / extra).read_text(errors="ignore"))))
    hits = [(n, m.group(0)) for n, t in surfaces for m in BANNED_CLAIMS.finditer(t)]
    add("no-superlatives", not hits, 4, "no first/only/best-style claims" if not hits else f"found: {hits[:5]}", required=True)
    broken = []
    for target in re.findall(r"\]\(([^)\s]+)\)", prose):
        t = target.split("#")[0]
        if t and not re.match(r"^(https?:|mailto:|#)", target) and not (p / t).exists():
            broken.append(t)
    add("readme-links", not broken, 3, "relative links resolve" if not broken else f"missing: {broken[:5]}")
    leftovers = []
    for fp in [x for x in walk(p) if x.suffix in (".md", ".txt", ".html", ".yml", ".yaml", ".json", ".xml")]:
        if PLACEHOLDER.search(fp.read_text(errors="ignore")) and "templates" not in fp.parts:
            leftovers.append(str(fp.relative_to(p)))
    add("no-placeholders", not leftovers, 3, "no {{PLACEHOLDER}} left" if not leftovers else f"in: {leftovers[:5]}")

    for k, w in (("contributing", 2), ("code_of_conduct", 2), ("security", 2), ("issue_templates", 2), ("pr_template", 1)):
        add(k, files[k], w, f"{k.replace('_', ' ')} present")
    ch = files["changelog"]
    add("changelog", ch and re.search(r"(?m)^##\s+\[?v?\d+\.\d+", ch.read_text(errors="ignore")), 2, "CHANGELOG with a version heading")
    add("release-notes", files["release_notes"], 2, "release notes file (docs/releases/vX.Y.Z.md)")
    wf = files["workflow"]
    wf_ok = wf and re.search(r"(?m)^on:|^\"?on\"?:", wf.read_text(errors="ignore"))
    add("ci", wf_ok, 4, "GitHub Actions workflow")
    ci_badge = re.search(r"actions/workflows/([\w.-]+)/badge\.svg", readme)
    add("ci-badge", ci_badge and (p / ".github/workflows" / ci_badge.group(1)).exists(), 2,
        "README badge points at an existing workflow")

    llms = files["llms_txt"]
    lt = llms.read_text(errors="ignore") if llms else ""
    add("llms-txt", llms and lt.startswith("# ") and re.search(r"(?m)^> \S", lt) and re.search(r"(?m)^- \[.+\]\(.+\)", lt), 3,
        "llms.txt: H1, > summary, link list (llmstxt.org)")
    ag = files["agents_md"]
    add("agents-md", ag and "```" in ag.read_text(errors="ignore"), 3, "AGENTS.md with runnable commands")

    idx = files["pages_index"]
    if idx:
        mp = Meta()
        mp.feed(idx.read_text(errors="ignore"))
        ld_ok = False
        for block in mp.ld:
            try:
                data = json.loads(block)
                items = data if isinstance(data, list) else data.get("@graph", [data])
                ld_ok = ld_ok or ("schema.org" in json.dumps(data) and any("@type" in i for i in items))
            except Exception:
                pass
        add("pages-jsonld", ld_ok, 3, "docs/index.html has valid schema.org JSON-LD")
        og = [k for k in ("og:title", "og:description", "og:image", "og:url", "twitter:card") if mp.meta.get(k)]
        add("pages-opengraph", len(og) == 5, 3, f"Open Graph/Twitter tags: {og}")
        add("pages-basics", mp.title.strip() and mp.meta.get("description") and mp.canonical, 2, "title, meta description, canonical")
    else:
        for cid in ("pages-jsonld", "pages-opengraph", "pages-basics"):
            add(cid, False, 3 if cid != "pages-basics" else 2, "docs/index.html missing")
    rb = files["robots"]
    add("robots", rb and re.search(r"(?im)^sitemap:\s*https?://", rb.read_text(errors="ignore")), 1, "robots.txt with Sitemap line")
    sm = files["sitemap"]
    sm_ok = False
    if sm:  # regex, not an XML parser: no entity expansion on untrusted files
        st = sm.read_text(errors="ignore")
        sm_ok = "<urlset" in st and bool(re.search(r"<loc>\s*https?://[^<\s]+\s*</loc>", st))
    add("sitemap", sm_ok, 1, "sitemap.xml parses with <loc>")

    md = files["repo_metadata"]
    meta = load_json(md) if md else {}
    topics = meta.get("topics") or []
    topics_ok = 3 <= len(topics) <= 20 and all(re.fullmatch(r"[a-z0-9][a-z0-9-]{0,49}", t) for t in topics)
    desc = meta.get("description") or ""
    add("repo-metadata", md and topics_ok and 20 <= len(desc) <= 350 and not BANNED_CLAIMS.search(desc), 3,
        f"docs/launch/repo-metadata.json: {len(topics)} topic(s), description {len(desc)} chars")
    sp = files["social_preview"]
    size = png_size(sp) if sp else None
    add("social-preview", size and size[0] >= 640 and abs(size[0] / size[1] - 2) < 0.05, 2,
        f"social preview PNG 2:1, at least 640x320 (got {size})")

    manifests = [m for m in [p / "package.json", p / "pyproject.toml", p / ".claude-plugin/marketplace.json"]
                 + list(p.glob("plugins/*/.claude-plugin/plugin.json")) + list(p.glob("plugins/*/.codex-plugin/plugin.json"))
                 + [p / ".claude-plugin/plugin.json"] if m.exists()]
    if manifests:
        bad, versions = [], set()
        for m in manifests:
            if m.suffix == ".json":
                d = load_json(m)
                if not d or not d.get("name") or (m.name != "marketplace.json" and not d.get("description")):
                    bad.append(str(m.relative_to(p)))
                if d.get("version"):
                    versions.add(d["version"])
        add("manifests", not bad, 3, "manifests parse with name and description" if not bad else f"incomplete: {bad}")
        add("version-sync", len(versions) <= 1 and (not ch or not versions or next(iter(versions)) in ch.read_text(errors="ignore")),
            2, f"manifest version(s) {sorted(versions)} match each other and CHANGELOG")
    else:
        add("manifests", True, 0, "no package or plugin manifest", na=True)

    lp = files["launch_plan"]
    if lp:
        plan = lp.read_text(errors="ignore").lower()
        found = [c for c in CHANNELS if c in plan]
        add("launch-plan", len(found) >= 8, 4, f"{len(found)} channel(s) covered: {found}", required=True)
        add("launch-approval-gate", re.search(r"approv", plan) and re.search(r"not (yet )?(posted|submitted|published)|draft", plan), 2,
            "plan marks posts as drafts awaiting approval")
        add("launch-timing", re.search(r"\b(utc|pt|et|pst|pdt|cet)\b|\d{1,2}(:\d\d)?\s?(am|pm)", plan), 1, "plan gives timing")
    else:
        add("launch-plan", False, 4, "docs/launch/LAUNCH-PLAN.md missing", required=True)
        add("launch-approval-gate", False, 2, "no plan")
        add("launch-timing", False, 1, "no plan")

    findings = hygiene(p, names_file, (), revs)
    blocks = [f for f in findings if f["severity"] == "block"]
    now = [f for f in blocks if f["where"] == "worktree"]
    past = [f for f in blocks if f["where"] != "worktree"]
    add("hygiene-current", not now, 5, f"{len(now)} blocking finding(s) in the files as they are now", required=True)
    add("hygiene-history", not past, 3,
        f"{len(past)} blocking finding(s) in git history or commit metadata (fixed only by an owner-approved rewrite)", required=True)

    scored = [c for c in checks if not c["na"]]
    total = sum(c["weight"] for c in scored)
    got = sum(c["weight"] for c in scored if c["ok"])
    score = round(100 * got / total, 1) if total else 0.0
    return dict(score=score, required_failed=[c["id"] for c in scored if c["required"] and not c["ok"]],
                checks=checks, hygiene=findings)


# ---------------------------------------------------------------- render

def render(html, out, size):
    w, h = (int(x) for x in size.split("x"))
    url = Path(html).resolve().as_uri()
    try:
        from playwright.sync_api import sync_playwright  # type: ignore
        with sync_playwright() as pw:
            b = pw.chromium.launch()
            pg = b.new_page(viewport={"width": w, "height": h})
            pg.goto(url)
            pg.wait_for_timeout(300)
            pg.screenshot(path=out)
            b.close()
        return "playwright"
    except Exception:
        pass
    for exe in ("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
                "/Applications/Chromium.app/Contents/MacOS/Chromium",
                shutil.which("google-chrome") or "", shutil.which("chromium") or "", shutil.which("chromium-browser") or ""):
        if exe and Path(exe).exists():
            run([exe, "--headless=new", "--disable-gpu", "--hide-scrollbars", f"--window-size={w},{h}",
                     f"--screenshot={Path(out).resolve()}", url])
            if Path(out).exists():
                return Path(exe).name
    raise SystemExit("no renderer: install Playwright (python3 -m pip install playwright && python3 -m playwright install chromium) or Chrome")


# ---------------------------------------------------------------- cli

def main(argv=None):
    ap = argparse.ArgumentParser(prog="lp.py", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("facts"); s.add_argument("path")
    s = sub.add_parser("hygiene"); s.add_argument("path"); s.add_argument("--names"); s.add_argument("--rev", action="append", default=[], help="refs to scan (default: all local refs); use the branch you will push"); s.add_argument("--allow", action="append", default=[]); s.add_argument("--json", action="store_true")
    s = sub.add_parser("scaffold"); s.add_argument("path")
    for k in ("name", "owner", "description"):
        s.add_argument("--" + k, required=True)
    s.add_argument("--contact", default=""); s.add_argument("--homepage", default=""); s.add_argument("--author", default="")
    s = sub.add_parser("audit"); s.add_argument("path"); s.add_argument("--json", action="store_true"); s.add_argument("--min", type=float, default=90); s.add_argument("--names"); s.add_argument("--rev", action="append", default=[])
    s = sub.add_parser("render"); s.add_argument("html"); s.add_argument("out"); s.add_argument("--size", default="1280x640")
    a = ap.parse_args(argv)

    if a.cmd == "facts":
        print(json.dumps(facts(a.path), indent=2))
        return 0
    if a.cmd == "hygiene":
        found = hygiene(a.path, a.names, a.allow, a.rev)
        blocks = [f for f in found if f["severity"] == "block"]
        if a.json:
            print(json.dumps(dict(blocking=len(blocks), findings=found), indent=2))
        else:
            for f in found:
                print(f"{f['severity'].upper():6} {f['kind']:16} {f['where']:9} {f['path']}:{f['line']}  {f['evidence']}")
            kinds = sorted({f["kind"] for f in blocks})
            for k in kinds:
                print(f"fix {k}: {secret_hint(k)}")
            print(f"{len(blocks)} blocking, {len(found) - len(blocks)} to review")
        return 1 if blocks else 0
    if a.cmd == "scaffold":
        owner, name = a.owner, a.name
        values = dict(NAME=name, OWNER=owner, REPO=f"{owner}/{name}", DESCRIPTION=a.description,
                      YEAR=str(datetime.date.today().year), DATE=datetime.date.today().isoformat(),
                      AUTHOR=a.author or owner, CONTACT=a.contact or f"https://github.com/{owner}/{name}/security/advisories/new",
                      HOMEPAGE=a.homepage or f"https://{owner.lower()}.github.io/{name}/")
        created, kept = scaffold(a.path, values)
        print(json.dumps(dict(created=created, kept_existing=kept), indent=2))
        return 0
    if a.cmd == "audit":
        res = audit(a.path, a.names, a.rev)
        if a.json:
            print(json.dumps(res, indent=2))
        else:
            for c in res["checks"]:
                mark = "n/a " if c["na"] else ("PASS" if c["ok"] else "FAIL")
                req = " (required)" if c["required"] else ""
                print(f"{mark} {c['id']:22} w{c['weight']}{req}  {c['detail']}")
            print(f"score {res['score']}/100, required failed: {res['required_failed'] or 'none'}")
        return 0 if res["score"] >= a.min and not res["required_failed"] else 1
    if a.cmd == "render":
        print(render(a.html, a.out, a.size))
        return 0


if __name__ == "__main__":
    sys.exit(main())
