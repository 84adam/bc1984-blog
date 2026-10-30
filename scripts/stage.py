#!/usr/bin/env python3
"""Stage published articles for Hugo.

Source files keep their metadata at the end. Hugo only reads front matter
at the top, so this writes a temporary copy with that block moved up.
Drafts are left out.
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OPEN = "\n<!--\n"
CLOSE = "\n-->"
OUT = ROOT / ".hugo" / "content"


def split_end_matter(text, path):
    start = text.rfind(OPEN)
    end = text.rfind(CLOSE)
    if start < 0 or end < start or "title:" not in text[start:end]:
        raise SystemExit(f"no trailing metadata in {path}")
    if text[end + len(CLOSE) :].strip() != "":
        raise SystemExit(f"metadata comment is not at the end of {path}")
    front = text[start + len(OPEN) : end].strip("\n")
    body = text[:start].rstrip() + "\n"
    return front, body


def main():
    if OUT.exists():
        for old in OUT.rglob("*"):
            if old.is_file():
                old.unlink()
    posts = OUT / "posts"
    posts.mkdir(parents=True, exist_ok=True)
    (posts / "_index.md").write_text(
        "---\nbuild:\n  render: never\n---\n",
        encoding="utf-8",
    )

    count = 0
    for path in sorted((ROOT / "published").glob("*.md")):
        front, body = split_end_matter(path.read_text(encoding="utf-8"), path)
        slug = next(
            (line.split(":", 1)[1].strip().strip("'\"") for line in front.splitlines() if line.startswith("slug:")),
            path.stem,
        )
        target = posts / f"{slug}.md"
        target.write_text(f"---\n{front}\n---\n\n{body}", encoding="utf-8")
        count += 1

    about = ROOT / "about.md"
    front, body = split_end_matter(about.read_text(encoding="utf-8"), about)
    (OUT / "donate.md").write_text(f"---\n{front}\n---\n\n{body}", encoding="utf-8")
    print(f"staged {count} posts and the about page")


if __name__ == "__main__":
    main()
