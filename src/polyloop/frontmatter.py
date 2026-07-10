from __future__ import annotations

import tomllib
from pathlib import Path


class FrontmatterError(ValueError):
    """Raised when a Polyloop Markdown document has invalid TOML front matter."""


def read_toml_frontmatter(path: Path) -> dict[str, object]:
    try:
        text = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return {}
    lines = text.splitlines()
    if not lines or lines[0].strip() != "+++":
        return {}
    try:
        end = next(
            index
            for index, line in enumerate(lines[1:], start=1)
            if line.strip() == "+++"
        )
    except StopIteration as exc:
        raise FrontmatterError(f"unclosed TOML front matter in {path}") from exc
    payload = "\n".join(lines[1:end])
    try:
        return tomllib.loads(payload)
    except tomllib.TOMLDecodeError as exc:
        raise FrontmatterError(f"invalid TOML front matter in {path}: {exc}") from exc
