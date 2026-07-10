from pathlib import Path

import pytest

from polyloop.frontmatter import FrontmatterError, read_toml_frontmatter


def test_reads_toml_frontmatter(tmp_path: Path) -> None:
    document = tmp_path / "CAMPAIGN.md"
    document.write_text(
        '+++\nid = "C002"\nstatus = "active"\n+++\n\n# Campaign\n',
        encoding="utf-8",
    )

    assert read_toml_frontmatter(document) == {
        "id": "C002",
        "status": "active",
    }


def test_rejects_unclosed_frontmatter(tmp_path: Path) -> None:
    document = tmp_path / "broken.md"
    document.write_text('+++\nid = "C001"\n', encoding="utf-8")

    with pytest.raises(FrontmatterError):
        read_toml_frontmatter(document)
