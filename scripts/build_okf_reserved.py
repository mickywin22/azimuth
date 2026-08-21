#!/usr/bin/env python3
"""Generate the reserved OKF bundle files — ``index.md`` (per level) + ``log.md`` (root).

The Open Knowledge Format v0.1 reserves two filenames a conformant bundle must ship
(``docs/strategy/okf-and-knowledge-graph.md``, gaps **G2** + **G3**):

  * **``index.md`` (SPEC §6)** — a directory-listing / progressive-disclosure file at the
    bundle root and at each layer folder, so an OKF-aware consumer can traverse the bundle
    top-down without a bespoke parser. It coexists with ``README.md`` (the human landing
    page): OKF consumers read ``index.md``, humans read ``README.md``.
  * **``log.md`` (SPEC §7)** — a chronological, newest-first update history at the bundle
    root, ISO ``YYYY-MM-DD`` headings.

Every file is derived **purely from committed data** (the layer folders, the dated L1 day
directories, and note frontmatter) and **never from the wall clock**, exactly like
``build_autonomy.py`` / ``build_brief_index.py`` / ``build_graph.py``: so ``--check`` on any
checkout of a given commit yields the same bytes, and the daily ingest workflow regenerates
them in the same run that commits a new L1 day. The listing content is kept to the STABLE
facts (titles, themes, folder structure, ingest cadence) rather than the volatile per-brief
``updated`` timestamp, so a weekly brief evolution does not churn these files between daily
regenerations — only a genuinely new ingest day moves them.

Pure stdlib; reuses ``synthesis.lint`` (``split_frontmatter`` + the ``RESERVED_FILES`` set so
the generator and every concept-glob agree on which ``.md`` are bundle files, not concepts).
``scripts/check_okf_conformance.py`` gates that these files exist + stay hygienic.

Usage:
    python scripts/build_okf_reserved.py            # write vault/index.md (x4) + vault/log.md
    python scripts/build_okf_reserved.py --check     # exit 1 if any reserved file is stale
    python scripts/build_okf_reserved.py --vault DIR # explicit bundle root
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from urllib.parse import quote

_REPO_ROOT = Path(__file__).resolve().parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from synthesis.lint import RESERVED_FILES, split_frontmatter  # noqa: E402

DEFAULT_VAULT = _REPO_ROOT / "vault"

_DAY_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

# Layer folder -> (short label, one-line purpose) for the root index.
_LAYERS: tuple[tuple[str, str], ...] = (
    ("00 Rules", "L3 doctrine — the rules synthesis is held to"),
    ("01 Sources", "L1 verbatim source pulls — machine-written, one dated folder per ingest"),
    ("02 Briefs", "L2 synthesised briefs — the claims azimuth makes from the open data"),
)


def _enc(rel: str) -> str:
    """Percent-encode a bundle-relative link target, preserving path separators."""
    return quote(rel, safe="/")


def _title(path: Path) -> str:
    """A note's frontmatter ``title``, falling back to its filename stem."""
    fm, _ = split_frontmatter(path.read_text(encoding="utf-8"))
    return (fm or {}).get("title") or path.stem


def _concept_files(folder: Path) -> list[Path]:
    """Concept ``.md`` directly under a layer folder, reserved names excluded, sorted."""
    return sorted(p for p in folder.glob("*.md") if p.name.lower() not in RESERVED_FILES)


def _day_dirs(sources: Path) -> list[str]:
    """Dated ``YYYY-MM-DD`` L1 day directories, newest-first."""
    if not sources.is_dir():
        return []
    return sorted(
        (p.name for p in sources.iterdir() if p.is_dir() and _DAY_RE.match(p.name)),
        reverse=True,
    )


def _day_source_keys(day_dir: Path) -> list[str]:
    """Sorted source keys (note stems) pulled on one ingest day."""
    return sorted(p.stem for p in day_dir.glob("*.md") if p.name.lower() not in RESERVED_FILES)


def _root_index(vault: Path) -> str:
    lines = [
        "# azimuth — Open Knowledge Bundle",
        "",
        "Machine-readable directory listing for this OKF v0.1 Knowledge Bundle "
        "(Markdown + YAML frontmatter, one `type` per concept). Humans may prefer "
        "[README.md](README.md); OKF-aware consumers start here.",
        "",
        "## Layers",
        "",
    ]
    for folder, purpose in _LAYERS:
        target = _enc(f"{folder}/index.md")
        n = len(_concept_files(vault / folder))
        if folder == "01 Sources":
            days = _day_dirs(vault / "01 Sources")
            total = sum(len(_day_source_keys(vault / "01 Sources" / d)) for d in days)
            count = f"{total} notes across {len(days)} ingest days"
        else:
            count = f"{n} concept(s)"
        lines.append(f"- [{folder}/]({target}) — {purpose} ({count})")
    lines += [
        "",
        "## Bundle files",
        "",
        "- [log.md](log.md) — chronological update history (newest first)",
        "- [README.md](README.md) — human landing page",
        "",
    ]
    return "\n".join(lines)


def _folder_index(vault: Path, folder: str, heading: str, *, with_theme: bool) -> str:
    lines = [f"# {heading}", ""]
    if folder == "00 Rules":
        lines.append("The L3 rules synthesis is held to. Concepts:")
    else:
        lines.append("The L2 briefs azimuth publishes. Concepts:")
    lines.append("")
    for path in _concept_files(vault / folder):
        target = _enc(path.name)
        entry = f"- [{_title(path)}]({target})"
        if with_theme:
            fm, _ = split_frontmatter(path.read_text(encoding="utf-8"))
            theme = (fm or {}).get("theme")
            if theme:
                entry += f" — theme: {theme}"
        lines.append(entry)
    lines += ["", "See [README.md](README.md) for the prose index.", ""]
    return "\n".join(lines)


def _sources_index(vault: Path) -> str:
    sources = vault / "01 Sources"
    lines = [
        "# 01 Sources — L1 verbatim pulls",
        "",
        "Machine-written verbatim transforms of the WorldMonitor API, one dated folder per "
        "daily ingest (`YYYY-MM-DD/<source_key>.md`); never hand-edited. Newest first.",
        "",
    ]
    for day in _day_dirs(sources):
        keys = _day_source_keys(sources / day)
        lines.append(f"- [{day}/]({_enc(day + '/')}) — {len(keys)} source note(s)")
    lines += ["", "See [README.md](README.md) for the lane's contract.", ""]
    return "\n".join(lines)


def _log(vault: Path) -> str:
    sources = vault / "01 Sources"
    lines = [
        "# Changelog — azimuth Open Knowledge Bundle",
        "",
        "Chronological update history of the bundle, newest first. Generated from the L1 "
        "ingest cadence by `scripts/build_okf_reserved.py`; the L2 briefs carry their own "
        "per-brief `## Changelog`.",
        "",
    ]
    for day in _day_dirs(sources):
        keys = _day_source_keys(sources / day)
        lines.append(f"## {day}")
        lines.append(f"- L1 ingest — {len(keys)} source note(s): {', '.join(keys)}")
        lines.append("")
    return "\n".join(lines).rstrip("\n") + "\n"


def generate(vault: Path = DEFAULT_VAULT) -> dict[Path, str]:
    """The full reserved-file set: {absolute path -> desired content}."""
    return {
        vault / "index.md": _root_index(vault),
        vault / "00 Rules" / "index.md": _folder_index(
            vault, "00 Rules", "00 Rules — L3 doctrine", with_theme=False
        ),
        vault / "01 Sources" / "index.md": _sources_index(vault),
        vault / "02 Briefs" / "index.md": _folder_index(
            vault, "02 Briefs", "02 Briefs — L2 synthesised briefs", with_theme=True
        ),
        vault / "log.md": _log(vault),
    }


def _rel(vault: Path, path: Path) -> str:
    try:
        return path.relative_to(vault).as_posix()
    except ValueError:
        return path.as_posix()


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Generate the reserved OKF bundle files.")
    ap.add_argument(
        "--vault", type=Path, default=DEFAULT_VAULT, help="bundle root (default: ./vault)"
    )
    ap.add_argument("--check", action="store_true", help="exit 1 if any reserved file is stale")
    ns = ap.parse_args(argv)

    if not ns.vault.is_dir():
        print(f"error: bundle root not found: {ns.vault}", file=sys.stderr)
        return 2

    files = generate(ns.vault)
    if ns.check:
        stale = [
            _rel(ns.vault, path)
            for path, content in files.items()
            if not path.is_file() or path.read_text(encoding="utf-8") != content
        ]
        if stale:
            print(
                "okf-reserved: STALE — run `python scripts/build_okf_reserved.py` and commit: "
                + ", ".join(sorted(stale))
            )
            return 1
        print(f"okf-reserved: all {len(files)} reserved file(s) in sync.")
        return 0

    for path, content in files.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        print(f"wrote {_rel(ns.vault, path)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
