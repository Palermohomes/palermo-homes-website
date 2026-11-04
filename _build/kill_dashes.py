"""Strip em dashes and space-separated en dashes from all HTML content and build scripts.
Em dashes are an AI-writing tell — user asked to remove them site-wide.

Replacement rules:
  ' — X'  where X is lowercase  -> '. X' (uppercased) — clause boundary becomes new sentence
  ' — X'  where X is uppercase  -> '. X'
  '—' with no surrounding spaces -> ', '
  Same rules for ' – ' (en dash with spaces). Bare en dashes (like 2019-2024 ranges) untouched.
"""
import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def replace(text: str) -> tuple[str, int]:
    count = 0

    def spaced_dash(m):
        nonlocal count
        count += 1
        nxt = m.group(1)
        return ". " + nxt.upper()

    # Em/en dash surrounded by spaces followed by a letter -> ". " + uppercased letter
    text, n = re.subn(r" [—–] ([A-Za-z])", spaced_dash, text)

    # Any leftover em/en dash (mid-word or no spaces) -> comma
    def bare_dash(m):
        nonlocal count
        count += 1
        # if surrounded by digits it's likely a range — leave alone
        return m.group(0)
    # only replace bare em dashes (never en dashes — those may be legit ranges)
    def em(m):
        nonlocal count
        count += 1
        return ", "
    text = re.sub(r"—", em, text)

    return text, count


def main():
    total = 0
    files_touched = 0
    for base in ("site", "_build"):
        for root, _, files in os.walk(ROOT / base):
            for f in files:
                if not f.endswith((".html", ".css", ".js", ".py")):
                    continue
                p = Path(root) / f
                if p.name == "kill_dashes.py":
                    continue
                try:
                    txt = p.read_text(encoding="utf-8")
                except UnicodeDecodeError:
                    continue
                new, n = replace(txt)
                if n:
                    p.write_text(new, encoding="utf-8")
                    total += n
                    files_touched += 1
    print(f"Removed {total} em/en dashes across {files_touched} files")


if __name__ == "__main__":
    main()
