"""Render docs/demo.svg from a real run of the CLI on examples/*.txt."""
import glob
import html
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARGS = ["-n", "8", "--stop", "the,and,is,in,of,a"]


def main():
    files = sorted(os.path.relpath(p, ROOT) for p in glob.glob(os.path.join(ROOT, "examples", "*.txt")))
    out = subprocess.run([sys.executable, "-m", "wordfreq.cli", *files, *ARGS],
                         cwd=ROOT, capture_output=True, text=True, check=True).stdout
    lines = ["$ wordfreq " + " ".join(files + ARGS)] + out.rstrip("\n").split("\n")
    lh, pad, width = 26, 24, 880
    height = pad * 2 + lh * len(lines) + 28
    text = "\n".join(
        f'<text x="{pad}" y="{pad + 40 + i * lh}" fill="{"#8fb0ff" if i == 0 else "#f2f0ea"}">{html.escape(l)}</text>'
        for i, l in enumerate(lines))
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="wordfreq output on two sample texts">
<rect width="100%" height="100%" rx="10" fill="#141413"/>
<circle cx="24" cy="20" r="6" fill="#e5534b"/><circle cx="44" cy="20" r="6" fill="#d4a72c"/><circle cx="64" cy="20" r="6" fill="#57ab5a"/>
<g font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" font-size="17" xml:space="preserve">
{text}
</g>
</svg>
'''
    with open(os.path.join(ROOT, "docs", "demo.svg"), "w", encoding="utf-8") as fh:
        fh.write(svg)
    print(out, end="")


if __name__ == "__main__":
    main()
