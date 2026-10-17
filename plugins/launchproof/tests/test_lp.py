"""Self-tests for lp.py. Standard library only: python3 -m unittest discover -s plugins/launchproof/tests -v

Secret-looking and personal strings are assembled at runtime so this file itself passes the hygiene scan.
"""
import importlib.util
import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

LP_PATH = Path(__file__).resolve().parents[1] / "skills" / "launchproof" / "scripts" / "lp.py"
spec = importlib.util.spec_from_file_location("lp", LP_PATH)
lp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lp)

NOREPLY = "1+tester@users.noreply.github.com"
PERSONAL = "jane.doe" + "@" + "gmail.com"
HOME = "/" + "Users" + "/janedoe/projects/app"
AWS = "AKIA" + "Q3EXAMPLEKEY7Z2B"  # 20 chars, fake


def git(repo, *args, email=NOREPLY):
    env = {"GIT_AUTHOR_NAME": "T", "GIT_AUTHOR_EMAIL": email, "GIT_COMMITTER_NAME": "T", "GIT_COMMITTER_EMAIL": email,
           "PATH": "/usr/bin:/bin:/usr/local/bin:/opt/homebrew/bin", "HOME": str(repo)}
    subprocess.run(["git", *args], cwd=repo, env=env, check=True, capture_output=True)


def new_repo():
    d = Path(tempfile.mkdtemp(prefix="lp-test-"))
    git(d, "init", "-q", "-b", "main")
    return d


class Hygiene(unittest.TestCase):
    def tearDown(self):
        shutil.rmtree(getattr(self, "repo", ""), ignore_errors=True)

    def test_clean_repo_has_no_blocking_findings(self):
        self.repo = new_repo()
        (self.repo / "README.md").write_text("# app\nRun it from ~/projects/app or /Users/<you>/app.\n")
        git(self.repo, "add", "-A"); git(self.repo, "commit", "-qm", "init")
        self.assertEqual([f for f in lp.hygiene(self.repo) if f["severity"] == "block"], [])

    def test_finds_issues_deleted_from_history(self):
        self.repo = new_repo()
        (self.repo / "config.py").write_text(f'API_KEY = "{AWS}"\nROOT = "{HOME}"\nOWNER = "{PERSONAL}"\n')
        (self.repo / ".env").write_text("X=1\n")
        git(self.repo, "add", "-A"); git(self.repo, "commit", "-qm", "oops", email=PERSONAL)
        (self.repo / "config.py").unlink(); (self.repo / ".env").unlink()
        git(self.repo, "add", "-A"); git(self.repo, "commit", "-qm", "clean up")
        kinds = {f["kind"] for f in lp.hygiene(self.repo)}
        for k in ("aws-access-key", "home-path", "personal-email", "author-email", "sensitive-file"):
            self.assertIn(k, kinds)

    def test_evidence_is_masked(self):
        self.repo = new_repo()
        (self.repo / "a.txt").write_text(AWS + "\n")
        git(self.repo, "add", "-A"); git(self.repo, "commit", "-qm", "x")
        out = json.dumps(lp.hygiene(self.repo))
        self.assertNotIn(AWS, out)

    def test_private_names_and_allow(self):
        self.repo = new_repo()
        (self.repo / "notes.md").write_text("Built for Acme Widgets Inc last spring.\n")
        git(self.repo, "add", "-A"); git(self.repo, "commit", "-qm", "x")
        names = self.repo.parent / (self.repo.name + "-names.txt")
        names.write_text("# clients\nAcme Widgets\n")
        try:
            self.assertIn("private-name", {f["kind"] for f in lp.hygiene(self.repo, names)})
            self.assertNotIn("private-name", {f["kind"] for f in lp.hygiene(self.repo, names, allow=["Acme"])})
        finally:
            names.unlink()

    def test_rev_limits_scan_to_published_branch(self):
        self.repo = new_repo()
        (self.repo / "a.txt").write_text("ok\n")
        git(self.repo, "add", "-A"); git(self.repo, "commit", "-qm", "x")
        git(self.repo, "checkout", "-qb", "old")
        (self.repo / "b.txt").write_text(HOME + "\n")
        git(self.repo, "add", "-A"); git(self.repo, "commit", "-qm", "y")
        git(self.repo, "checkout", "-q", "main")
        self.assertTrue(any(f["kind"] == "home-path" for f in lp.hygiene(self.repo)))
        self.assertFalse(any(f["kind"] == "home-path" for f in lp.hygiene(self.repo, revs=["main"])))

    def test_images_are_flagged_for_review(self):
        self.repo = new_repo()
        (self.repo / "logo.png").write_bytes(b"\x89PNG\r\n\x1a\n" + b"\0" * 20)
        git(self.repo, "add", "-A"); git(self.repo, "commit", "-qm", "x")
        found = lp.hygiene(self.repo)
        self.assertTrue(any(f["kind"] == "image-review" and f["severity"] == "review" for f in found))


class Claims(unittest.TestCase):
    def test_banned_claims(self):
        for bad in ("X is the best plugin", "the first tool to do it", "world's fastest", "It's the only app that",
                    "state of the art results", "a revolutionary approach"):
            self.assertTrue(lp.BANNED_CLAIMS.search(bad), bad)
        for ok in ("keep the best round", "the first run takes a minute", "Our first release", "only works on macOS"):
            self.assertFalse(lp.BANNED_CLAIMS.search(ok), ok)


class ScaffoldAndAudit(unittest.TestCase):
    def setUp(self):
        self.repo = new_repo()

    def tearDown(self):
        shutil.rmtree(self.repo, ignore_errors=True)

    def test_scaffold_never_overwrites(self):
        (self.repo / "SECURITY.md").write_text("mine\n")
        created, kept = lp.scaffold(self.repo, dict(NAME="app", OWNER="o", REPO="o/app", DESCRIPTION="d", YEAR="2026",
                                                    DATE="2026-01-01", AUTHOR="A", CONTACT="c", HOMEPAGE="https://o.github.io/app/"))
        self.assertEqual((self.repo / "SECURITY.md").read_text(), "mine\n")
        self.assertIn("SECURITY.md", kept)
        self.assertIn("llms.txt", created)
        self.assertNotIn("{{", (self.repo / "docs/index.html").read_text())

    def test_bare_repo_scores_low_and_fails_required(self):
        (self.repo / "main.py").write_text("print('hi')\n")
        git(self.repo, "add", "-A"); git(self.repo, "commit", "-qm", "x")
        res = lp.audit(self.repo)
        self.assertLess(res["score"], 30)
        self.assertIn("readme", res["required_failed"])
        self.assertIn("launch-plan", res["required_failed"])

    def test_placeholder_and_jsonld_checks(self):
        (self.repo / "docs").mkdir()
        (self.repo / "docs/index.html").write_text('<script type="application/ld+json">{not json</script>{{NAME}}')
        res = {c["id"]: c for c in lp.audit(self.repo)["checks"]}
        self.assertFalse(res["pages-jsonld"]["ok"])
        self.assertFalse(res["no-placeholders"]["ok"])

    def test_actions_expressions_are_not_placeholders(self):
        self.assertFalse(lp.PLACEHOLDER.search("python-version: ${{ matrix.python }}"))
        self.assertTrue(lp.PLACEHOLDER.search("# {{NAME}}"))

    def test_proof_numbers_must_appear_in_linked_file(self):
        (self.repo / "evals").mkdir()
        (self.repo / "evals/RESULTS.md").write_text("pass rate 0.93 on 12 cases\n")
        (self.repo / "README.md").write_text("# a\n\n## Proof\n\n12 cases, 0.93 pass rate ([results](evals/RESULTS.md)).\n")
        self.assertTrue({c["id"]: c for c in lp.audit(self.repo)["checks"]}["proof"]["ok"])
        (self.repo / "README.md").write_text("# a\n\n## Proof\n\n40 cases, 0.99 pass rate ([results](evals/RESULTS.md)).\n")
        self.assertFalse({c["id"]: c for c in lp.audit(self.repo)["checks"]}["proof"]["ok"])

    def test_faq_counts_inline_bold_questions(self):
        qs = "\n\n".join(f"**How do I do thing {i}?** Like this." for i in range(6))
        (self.repo / "README.md").write_text("# a\n\n## FAQ\n\n" + qs + "\n")
        self.assertTrue({c["id"]: c for c in lp.audit(self.repo)["checks"]}["faq"]["ok"])

    def test_png_size(self):
        p = self.repo / "x.png"
        p.write_bytes(b"\x89PNG\r\n\x1a\n" + b"\0\0\0\rIHDR" + (1280).to_bytes(4, "big") + (640).to_bytes(4, "big"))
        self.assertEqual(lp.png_size(p), (1280, 640))


class Cli(unittest.TestCase):
    def test_hygiene_exit_codes(self):
        repo = new_repo()
        try:
            (repo / "a.txt").write_text("fine\n")
            git(repo, "add", "-A"); git(repo, "commit", "-qm", "x")
            self.assertEqual(lp.main(["hygiene", str(repo)]), 0)
            (repo / "b.txt").write_text(HOME + "\n")
            self.assertEqual(lp.main(["hygiene", str(repo)]), 1)
        finally:
            shutil.rmtree(repo, ignore_errors=True)


if __name__ == "__main__":
    unittest.main()
