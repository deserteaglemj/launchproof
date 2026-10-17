#!/usr/bin/env python3
"""Build assets/scores.html from evals/results.json, then render assets/scores.png with lp.py render."""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
runs = json.loads((ROOT / "evals/results.json").read_text())
BEFORE, AFTER = "#eb6834", "#2a78d6"  # validated pair (dataviz validator, light surface)
W, LEFT, RIGHT, ROW = 1200, 190, 80, 86
span = W - LEFT - RIGHT


def x(score):
    return LEFT + span * score / 100


rows = []
for i, (name, r) in enumerate(sorted(runs.items(), key=lambda kv: kv[1]["before"]["score"])):
    y = 120 + i * ROW
    b, a = r["before"]["score"], r["after_agent"]["score"]
    verdict = "pass" if r["pass"] else "fail: history needs owner rewrite"
    rows.append(f"""
  <text x="{LEFT - 20}" y="{y + 5}" text-anchor="end" class="name">{name}</text>
  <line x1="{x(b):.1f}" y1="{y}" x2="{x(a):.1f}" y2="{y}" stroke="#c9c6bd" stroke-width="2"/>
  <circle cx="{x(b):.1f}" cy="{y}" r="9" fill="{BEFORE}" stroke="#fcfcfb" stroke-width="2"/>
  <circle cx="{x(a):.1f}" cy="{y}" r="9" fill="{AFTER}" stroke="#fcfcfb" stroke-width="2"/>
  <text x="{x(b):.1f}" y="{y - 18}" text-anchor="middle" class="val">{b:g}</text>
  <text x="{x(a):.1f}" y="{y - 18}" text-anchor="middle" class="val">{a:g}</text>
  <text x="{x(a):.1f}" y="{y + 30}" text-anchor="end" class="note">{verdict}</text>""")
H = 120 + len(rows) * ROW + 40
ticks = "".join(f'<line x1="{x(t):.1f}" y1="92" x2="{x(t):.1f}" y2="{H - 50}" stroke="#ece9e3"/>'
                f'<text x="{x(t):.1f}" y="{H - 28}" text-anchor="middle" class="tick">{t}</text>' for t in (0, 25, 50, 75, 90, 100))
html = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><style>
html,body{{margin:0;background:#fcfcfb}} svg{{display:block;font-family:-apple-system,"Segoe UI",Helvetica,Arial,sans-serif}}
.title{{font-size:24px;font-weight:650;fill:#1d1d1b}} .sub{{font-size:16px;fill:#5f5e5a}} .name{{font-size:18px;fill:#1d1d1b;font-weight:600}}
.val{{font-size:15px;fill:#1d1d1b}} .note{{font-size:14px;fill:#5f5e5a}} .tick{{font-size:13px;fill:#5f5e5a}} .leg{{font-size:15px;fill:#1d1d1b}}
</style></head><body>
<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="launchproof audit score before and after the agent run, per eval case">
  <text x="40" y="44" class="title">launchproof audit score, before and after one agent run (0 to 100)</text>
  <text x="40" y="70" class="sub">Measured by lp.py audit in evals/run_eval.py. Pass line 90. Source: evals/results.json</text>
  <circle cx="{W - 330}" cy="40" r="7" fill="{BEFORE}"/><text x="{W - 316}" y="45" class="leg">before</text>
  <circle cx="{W - 230}" cy="40" r="7" fill="{AFTER}"/><text x="{W - 216}" y="45" class="leg">after agent</text>
  {ticks}
  {''.join(rows)}
</svg></body></html>"""
(ROOT / "assets").mkdir(exist_ok=True)
(ROOT / "assets/scores.html").write_text(html)
subprocess.run([sys.executable, str(ROOT / "plugins/launchproof/skills/launchproof/scripts/lp.py"), "render",
                str(ROOT / "assets/scores.html"), str(ROOT / "assets/scores.png"), "--size", f"{W}x{H}"], check=True)
print("assets/scores.png", W, H)
