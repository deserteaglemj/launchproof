"""Run the CLI eval cases in evals/cases.json and write evals/RESULTS.md."""
import datetime
import json
import os
import platform
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)


def run_case(case, tmp):
    paths = []
    blobs = [t.encode("utf-8") for t in case.get("files", [])]
    blobs += [bytes.fromhex(h) for h in case.get("files_hex", [])]
    for i, blob in enumerate(blobs):
        p = os.path.join(tmp, f"{case['id']}-{i}.txt")
        with open(p, "wb") as fh:
            fh.write(blob)
        paths.append(p)
    proc = subprocess.run(
        [sys.executable, "-m", "wordfreq.cli", *paths, *case["args"]],
        cwd=ROOT, capture_output=True, env={**os.environ, "PYTHONIOENCODING": "utf-8"},
    )
    out = proc.stdout.decode("utf-8", "replace")
    return proc.returncode == 0 and out == case["expected"], out


def main():
    with open(os.path.join(HERE, "cases.json"), encoding="utf-8") as fh:
        spec = json.load(fh)
    rows, passed = [], 0
    with tempfile.TemporaryDirectory() as tmp:
        for case in spec["cases"]:
            ok, out = run_case(case, tmp)
            passed += ok
            got = out.strip().replace("\n", " / ") or "(empty)"
            rows.append(f"| `{case['id']}` | {'pass' if ok else 'FAIL'} | `{got}` |")
            print(f"{'pass' if ok else 'FAIL'}  {case['id']}")
    total = len(spec["cases"])
    print(f"{passed}/{total} cases passed")
    report = [
        "# Eval results",
        "",
        f"- Date: {datetime.date.today().isoformat()}",
        f"- Python: {platform.python_version()} on {platform.system()}",
        "- Command: `python3 evals/run.py` (this file is written by that command; do not edit by hand)",
        f"- Criteria: {spec['criteria']}",
        f"- Result: **{passed}/{total} cases passed**",
        "",
        "| Case | Result | Output |",
        "|---|---|---|",
        *rows,
        "",
    ]
    with open(os.path.join(HERE, "RESULTS.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(report))
    return 0


if __name__ == "__main__":
    sys.exit(main())
