"""Remove the injected 'Built in [city]' service area links from all project pages.
Reverts inject_project_service_links.py."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"

MARKER_START = "<!-- PROJ-SVC-LINK START -->"
MARKER_END = "<!-- PROJ-SVC-LINK END -->"
CSS_START = "/* ==== PROJ-SVC-LINK CSS START ==== */"
CSS_END = "/* ==== PROJ-SVC-LINK CSS END ==== */"


def revert_file(path):
    html = path.read_text(encoding="utf-8")
    # Remove the HTML block (including markers)
    new_html = re.sub(
        re.escape(MARKER_START) + ".*?" + re.escape(MARKER_END) + r"\n?",
        "",
        html,
        flags=re.DOTALL,
    )
    # Remove the CSS block
    new_html = re.sub(
        re.escape(CSS_START) + ".*?" + re.escape(CSS_END),
        "",
        new_html,
        flags=re.DOTALL,
    )
    # Remove the empty <style></style> if we left one
    new_html = re.sub(r"<style>\s*</style>", "", new_html)
    if new_html != html:
        path.write_text(new_html, encoding="utf-8")
        return True
    return False


def main():
    print("Reverting project -> service area links...")
    count = 0
    project_dir = SITE / "project"
    for slug_dir in sorted(project_dir.iterdir()):
        if slug_dir.is_dir():
            path = slug_dir / "index.html"
            if path.exists() and revert_file(path):
                print(f"  cleaned project/{slug_dir.name}/")
                count += 1
    print(f"Done. Removed from {count} project pages.")


if __name__ == "__main__":
    main()
