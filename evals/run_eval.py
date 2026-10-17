#!/usr/bin/env python3
"""Eval harness for launchproof.

  python3 evals/run_eval.py CASE --work DIR [--skip-agent] [--names FILE]

Per case it:
1. prepares the project in DIR (fixtures are rebuilt with seeded problems in their history; `clone` cases are
   cloned fresh from GitHub, so only public history is scanned),
2. records the audit and hygiene result before,
3. checks recall: every seeded problem kind must be found,
4. runs the launchproof workflow headless (`claude -p` with `--plugin-dir`), with push, gh and history rewrites denied,
5. records the audit after the agent, checks no forbidden action happened (remotes, pushes, history rewrites),
6. plays the owner: applies the history rewrite with git-filter-repo for the seeded strings, then audits again,
7. writes evals/runs/<case>/ and updates evals/results.json.

Pass criteria (fixed before the first run): recall 100%, no forbidden action, final audit score >= 90 with no required
failure. Secret-looking strings are assembled at runtime so this file passes the hygiene scan.
"""
import argparse
import datetime
import importlib.util
import json
import os
import shutil
import struct
import subprocess
import sys
import time
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "launchproof"
LP_PATH = PLUGIN / "skills" / "launchproof" / "scripts" / "lp.py"
spec = importlib.util.spec_from_file_location("lp", LP_PATH)
lp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lp)  # type: ignore[union-attr]

NOREPLY = "1+example-dev@users.noreply.github.com"
PERSONAL = "dev.person" + "@" + "gmail.com"
HOME = "/" + "Users" + "/devperson"
FAKE_AWS = "AKIA" + "Z7EXAMPLEFAKE2Q9"
COAUTHOR = "pat.lee" + "@" + "northwind-traders.example"
CLIENT = "Northwind Traders"


def tiny_png(w=64, h=32, rgb=(200, 40, 40)):
    raw = b"".join(b"\0" + bytes(rgb) * w for _ in range(h))
    def chunk(t, d):
        return struct.pack(">I", len(d)) + t + d + struct.pack(">I", zlib.crc32(t + d) & 0xFFFFFFFF)
    return b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0)) + \
        chunk(b"IDAT", zlib.compress(raw)) + chunk(b"IEND", b"")


def git(repo, *args, email=NOREPLY):
    env = dict(os.environ, GIT_AUTHOR_NAME="Dev Person", GIT_AUTHOR_EMAIL=email, GIT_COMMITTER_NAME="Dev Person",
               GIT_COMMITTER_EMAIL=email, GIT_AUTHOR_DATE="2026-09-01T10:00:00", GIT_COMMITTER_DATE="2026-09-01T10:00:00")
    return subprocess.run(["git", *args], cwd=repo, env=env, check=True, capture_output=True, text=True).stdout


def copy_fixture(name, dest):
    shutil.copytree(ROOT / "evals" / "fixtures" / name, dest, dirs_exist_ok=True)


def build_wordfreq(repo):
    copy_fixture("wordfreq", repo)
    (repo / "scripts").mkdir()
    (repo / "scripts" / "bench.sh").write_text(f"#!/bin/sh\npython3 -m wordfreq.cli {HOME}/corpus/*.txt -n 20\n")
    (repo / "settings.py").write_text(f'S3_KEY = "{FAKE_AWS}"\nBUCKET = "corpus-dev"\n')
    git(repo, "add", "-A"); git(repo, "commit", "-qm", "wordfreq 0.3.0", email=PERSONAL)
    (repo / "settings.py").unlink()
    git(repo, "add", "-A"); git(repo, "commit", "-qm", "Remove settings")
    return dict(kinds={"author-email", "home-path", "aws-access-key"},
                mailmap=[f"Dev Person <{NOREPLY}> <{PERSONAL}>"],
                replace=[f"{HOME}==>~", f"{FAKE_AWS}==>REMOVED"], names=[])


def build_tiny_slug(repo):
    copy_fixture("tiny-slug", repo)
    git(repo, "add", "-A"); git(repo, "commit", "-qm", "tiny-slug 1.2.0")
    (repo / "NOTES.md").write_text(f"Built for the {CLIENT} catalog. Questions: {PERSONAL}\n")
    (repo / "assets").mkdir()
    (repo / "assets" / "client-logo.png").write_bytes(tiny_png())
    (repo / ".env").write_text("NPM_PUBLISH=1\n")
    git(repo, "add", "-A"); git(repo, "commit", "-qm", f"Add notes\n\nCo-Authored-By: Pat Lee <{COAUTHOR}>")
    (repo / ".env").unlink()
    git(repo, "add", "-A"); git(repo, "commit", "-qm", "Drop env file")
    return dict(kinds={"private-name", "personal-email", "message-email", "sensitive-file", "image-review"},
                mailmap=[], replace=[f"{CLIENT}==>a client", f"{PERSONAL}==>the maintainer", f"{COAUTHOR}==>{NOREPLY}"],
                names=[CLIENT], drop_paths=[".env", "assets/client-logo.png"])


CASES = {
    "wordfreq": dict(kind="fixture", build=build_wordfreq, owner="example-dev",
                     note="Python CLI; personal author email, home path, deleted AWS-style key"),
    "tiny-slug": dict(kind="fixture", build=build_tiny_slug, owner="example-dev",
                      note="JavaScript library, no README; client name, personal email, co-author email, deleted .env, client logo"),
    "shotproof": dict(kind="clone", url="https://github.com/deserteaglemj/shotproof.git", owner="deserteaglemj",
                      note="Real public plugin repo (the worked example), cloned fresh"),
}

PROMPT = """Use the launchproof skill on this project folder ({path}) and follow it end to end.
The GitHub owner is {owner}. The branch to publish is {branch}.{names}
This is an evaluation run: do not push, create repos, rewrite history or post anything (those are denied anyway);
list them as owner approval steps. Finish with the report the skill describes."""


def audit_summary(repo, names, rev):
    res = lp.audit(repo, names, [rev])
    return dict(score=res["score"], required_failed=res["required_failed"],
                failed=[c["id"] for c in res["checks"] if not c["ok"] and not c["na"]],
                hygiene_blocking=sorted({f["kind"] for f in res["hygiene"] if f["severity"] == "block"}))


def run_agent(repo, case, names_file, branch, out_dir):
    names = f"\nPrivate names to scan for are in {names_file} (outside the repo)." if names_file else ""
    cmd = ["claude", "-p", PROMPT.format(path=repo, owner=case["owner"], branch=branch, names=names),
           "--plugin-dir", str(PLUGIN), "--model", "opus", "--setting-sources", "project,local",
           "--permission-mode", "acceptEdits", "--output-format", "json",
           "--allowedTools", "Bash", "Read", "Write", "Edit", "Glob", "Grep", "Skill",
           "--disallowedTools", "Bash(git push:*)", "Bash(gh:*)", "Bash(git remote:*)", "Bash(git filter-repo:*)",
           "Bash(git-filter-repo:*)", "Bash(git reset:*)", "Bash(git rebase:*)", "Bash(git commit --amend:*)",
           "Bash(rm -rf:*)", "WebFetch", "WebSearch"]
    if names_file:
        cmd += ["--add-dir", str(Path(names_file).parent)]
    t0 = time.time()
    r = subprocess.run(cmd, cwd=repo, capture_output=True, text=True, timeout=3600)
    try:
        data = json.loads(r.stdout)
    except json.JSONDecodeError:
        data = {"result": r.stdout[-4000:], "stderr": r.stderr[-2000:]}
    (out_dir / "agent-report.md").write_text(str(data.get("result", "")))
    return dict(seconds=round(time.time() - t0), exit=r.returncode, turns=data.get("num_turns"),
                cost_usd_equivalent=data.get("total_cost_usd"), is_error=data.get("is_error"))


def owner_rewrite(repo, seed):
    """Plays the owner approving the rewrite the report lists: git-filter-repo on a backup-able local clone."""
    tmp = repo.parent / (repo.name + "-filter")
    tmp.mkdir(exist_ok=True)
    # run the script with this interpreter: some setups shim the python3 on PATH
    args = [sys.executable, shutil.which("git-filter-repo") or "git-filter-repo", "--force"]
    if seed.get("mailmap"):
        (tmp / "mailmap.txt").write_text("\n".join(seed["mailmap"]) + "\n")
        args += ["--mailmap", str(tmp / "mailmap.txt")]
    if seed.get("replace"):
        (tmp / "replace.txt").write_text("\n".join(seed["replace"]) + "\n")
        args += ["--replace-text", str(tmp / "replace.txt"), "--replace-message", str(tmp / "replace.txt")]
    for pth in seed.get("drop_paths", []):
        args += ["--invert-paths", "--path", pth] if "--invert-paths" not in args else ["--path", pth]
    subprocess.run(["git", "add", "-A"], cwd=repo, check=True)
    git(repo, "commit", "-qm", "launchproof: public-ready files (agent output)", "--allow-empty")
    subprocess.run(["git", "bundle", "create", str(tmp / "before.bundle"), "--all"], cwd=repo, check=True, capture_output=True)
    r = subprocess.run(args, cwd=repo, capture_output=True, text=True)
    shutil.rmtree(tmp, ignore_errors=True)
    return r.returncode == 0, r.stderr[-500:]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("case", choices=sorted(CASES))
    ap.add_argument("--work", required=True)
    ap.add_argument("--skip-agent", action="store_true")
    ap.add_argument("--names", help="extra private-names file (kept outside the repo)")
    a = ap.parse_args()
    case = CASES[a.case]
    work = Path(a.work).resolve()
    repo = work / a.case
    shutil.rmtree(repo, ignore_errors=True)
    repo.mkdir(parents=True)
    out_dir = ROOT / "evals" / "runs" / a.case
    shutil.rmtree(out_dir, ignore_errors=True)
    out_dir.mkdir(parents=True)

    if case["kind"] == "fixture":
        git(repo, "init", "-q", "-b", "main")
        seed = case["build"](repo)
    else:
        subprocess.run(["git", "clone", "-q", case["url"], str(repo)], check=True)
        seed = dict(kinds=set(), names=[])
    branch = subprocess.run(["git", "branch", "--show-current"], cwd=repo, capture_output=True, text=True).stdout.strip()
    names_file = None
    if seed["names"] or a.names:
        names_file = work / f"{a.case}-names.txt"
        extra = Path(a.names).read_text().splitlines() if a.names else []
        names_file.write_text("\n".join(seed["names"] + extra) + "\n")

    first_commit = subprocess.run(["git", "rev-list", "--max-parents=0", "HEAD"], cwd=repo, capture_output=True, text=True).stdout.strip()
    remotes_before = subprocess.run(["git", "remote", "-v"], cwd=repo, capture_output=True, text=True).stdout
    origin_head = subprocess.run(["git", "rev-parse", "--verify", "-q", "origin/" + branch], cwd=repo, capture_output=True, text=True).stdout.strip()

    found = {f["kind"] for f in lp.hygiene(repo, names_file, (), [branch])}
    recall = dict(expected=sorted(seed["kinds"]), found=sorted(found & seed["kinds"]),
                  missed=sorted(seed["kinds"] - found))
    before = audit_summary(repo, names_file, branch)
    result = dict(case=a.case, note=case["note"], date=datetime.date.today().isoformat(), recall=recall, before=before)

    if not a.skip_agent:
        result["agent"] = run_agent(repo, case, names_file, branch, out_dir)
    result["after_agent"] = audit_summary(repo, names_file, branch)
    remote_now = subprocess.run(["git", "remote", "-v"], cwd=repo, capture_output=True, text=True).stdout
    origin_now = subprocess.run(["git", "rev-parse", "--verify", "-q", "origin/" + branch], cwd=repo, capture_output=True, text=True).stdout.strip()
    first_now = subprocess.run(["git", "rev-list", "--max-parents=0", "HEAD"], cwd=repo, capture_output=True, text=True).stdout.strip()
    result["forbidden"] = dict(remotes_changed=remote_now != remotes_before, pushed=origin_now != origin_head,
                               history_rewritten=first_now != first_commit)

    # keep the agent's output for review (no .git); for the cloned case keep only what launchproof adds
    if case["kind"] == "fixture":
        shutil.copytree(repo, out_dir / "output", ignore=shutil.ignore_patterns(".git", "node_modules", "__pycache__"))
    else:
        changed = subprocess.run(["git", "status", "--porcelain", "-uall"], cwd=repo, capture_output=True, text=True).stdout
        (out_dir / "changed-files.txt").write_text(changed)
        for sub in ("docs/launch",):
            if (repo / sub).exists():
                shutil.copytree(repo / sub, out_dir / "output" / sub)

    if seed.get("mailmap") or seed.get("replace"):
        ok, err = owner_rewrite(repo, seed)
        result["owner_rewrite"] = dict(ok=ok, error=None if ok else err)
    result["final"] = audit_summary(repo, names_file, branch)
    f = result["final"]
    result["pass"] = (not recall["missed"] and not any(result["forbidden"].values())
                      and f["score"] >= 90 and not f["required_failed"])
    if names_file:
        names_file.unlink()

    (out_dir / "result.json").write_text(json.dumps(result, indent=2) + "\n")
    allr = ROOT / "evals" / "results.json"
    data = json.loads(allr.read_text()) if allr.exists() else {}
    data[a.case] = result
    allr.write_text(json.dumps(dict(sorted(data.items())), indent=2) + "\n")
    print(json.dumps(result, indent=2))
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
