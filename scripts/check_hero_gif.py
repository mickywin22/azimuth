#!/usr/bin/env python3
"""CI guard for the committed README hero (``docs/assets/hero.gif``).

The hero GIF is a landing artifact, and azimuth's promise is that CI proves its artifacts
on every push. Byte-for-byte re-checking the GIF would need Pillow at a *pinned* version
(the ``[demo]`` extra floats ``Pillow>=11.0``, and GIF encoding can shift between Pillow
releases), so a byte ``--check`` in CI would be fragile. This guard instead validates the
**committed GIF's own bytes with the standard library only** — no Pillow, no browser, no
version coupling — so it runs in any CI job and can never flake on a dependency bump.

It asserts the file exists, is a valid GIF, has the expected 900x840 logical screen size,
and contains the expected six frames — catching a deleted, corrupted, or wrongly
regenerated hero without re-encoding it. Regenerate the asset with
``scripts/build_hero_gif.py`` (which owns the exact-bytes ``--check``).

Usage:
    python scripts/check_hero_gif.py     # exit 1 if docs/assets/hero.gif is missing/wrong
"""

from __future__ import annotations

import struct
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parent.parent
_GIF = _REPO_ROOT / "docs" / "assets" / "hero.gif"

# Expected shape — must track scripts/build_hero_gif.py (_CANVAS_W/_H and len(_SCENES)*2).
_EXPECT_W = 900
_EXPECT_H = 840
_EXPECT_FRAMES = 6


def _read_subblocks(data: bytes, pos: int) -> int:
    """Advance past a GIF sub-block chain (length-prefixed, 0 terminates). Returns new pos."""
    while True:
        size = data[pos]
        pos += 1
        if size == 0:
            return pos
        pos += size


def parse_gif(data: bytes) -> tuple[int, int, int]:
    """Return (logical_width, logical_height, frame_count) from raw GIF bytes (stdlib only)."""
    if data[:6] not in (b"GIF87a", b"GIF89a"):
        raise ValueError("not a GIF (bad magic header)")

    width, height, packed = struct.unpack_from("<HHB", data, 6)
    pos = 13
    # Skip the global colour table if present.
    if packed & 0x80:
        pos += 3 * (2 ** ((packed & 0x07) + 1))

    frames = 0
    n = len(data)
    while pos < n:
        block = data[pos]
        pos += 1
        if block == 0x3B:  # trailer
            break
        if block == 0x21:  # extension: label byte, then a sub-block chain
            pos += 1
            pos = _read_subblocks(data, pos)
        elif block == 0x2C:  # image descriptor -> one frame
            frames += 1
            img_packed = data[pos + 8]
            pos += 9
            if img_packed & 0x80:  # local colour table
                pos += 3 * (2 ** ((img_packed & 0x07) + 1))
            pos += 1  # LZW minimum code size
            pos = _read_subblocks(data, pos)  # image data
        else:
            raise ValueError(f"unexpected GIF block 0x{block:02x} at {pos - 1}")

    return width, height, frames


def problems(gif: Path = _GIF) -> list[str]:
    """Human-readable reasons the committed hero fails the guard. Empty list = healthy."""
    if not gif.exists():
        return [f"missing: {gif} — run `python scripts/build_hero_gif.py`"]
    try:
        w, h, frames = parse_gif(gif.read_bytes())
    except (ValueError, IndexError, struct.error) as exc:
        return [f"not a valid GIF: {exc}"]

    out: list[str] = []
    if (w, h) != (_EXPECT_W, _EXPECT_H):
        out.append(f"wrong size: {w}x{h}, expected {_EXPECT_W}x{_EXPECT_H}")
    if frames != _EXPECT_FRAMES:
        out.append(f"wrong frame count: {frames}, expected {_EXPECT_FRAMES}")
    return out


def main(argv: list[str] | None = None) -> int:
    issues = problems()
    if issues:
        for line in issues:
            print(f"hero.gif: {line}", file=sys.stderr)
        return 1
    print(f"hero.gif: OK ({_EXPECT_W}x{_EXPECT_H}, {_EXPECT_FRAMES} frames).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
