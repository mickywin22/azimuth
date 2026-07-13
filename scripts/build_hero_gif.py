#!/usr/bin/env python3
"""Build the azimuth README hero animation (``docs/assets/hero.gif``).

The repo *is* the landing page for the GitHub / HN audience, so the README opens with an
animated walkthrough of the read-only site: the home page and its two demonstrator cards,
the cross-channel knowledge graph, and a weekly L2 brief. This is the last public-flip
landing asset (Azimuth KR2, the "hero-GIF tail").

**Why this builder and not the browser recorder.** azimuth's whole promise is a
pure-standard-library runtime whose every derived artifact **rebuilds byte-for-byte from
committed inputs** — no server, no third-party runtime, no hidden state, CI-checkable
(see ``build_graph.py --check``, ``build_autonomy.py --check``). A Playwright/chromium
screen-recording cannot honour that: it needs a heavyweight non-stdlib browser and its
frames vary run-to-run (timing, GPU, anti-aliasing), so the result can never be committed
as a reproducible asset. This builder instead composes the hero **deterministically from
the three committed page previews** in ``docs/assets/*.png`` using only Pillow (already the
``[demo]`` extra) — a fixed frame order, fixed crop boxes, a fixed LANCZOS resample and a
single shared median-cut palette. Same inputs + same Pillow ⇒ the same GIF bytes, so
``build_hero_gif.py --check`` guards the committed asset exactly like the data builders.

The optional ``scripts/record_hero_gif.py`` remains as a live browser-recorded variant for
anyone who wants a full-fidelity capture; it is **not** required and does not produce the
committed asset.

Usage:
    python scripts/build_hero_gif.py            # write docs/assets/hero.gif
    python scripts/build_hero_gif.py --check     # exit 1 if the committed GIF is stale
"""

from __future__ import annotations

import argparse
import sys
from io import BytesIO
from pathlib import Path
from typing import TYPE_CHECKING, NamedTuple

if TYPE_CHECKING:
    from PIL.Image import Image as PILImage

_REPO_ROOT = Path(__file__).resolve().parent.parent
_ASSETS = _REPO_ROOT / "docs" / "assets"
_OUT = _ASSETS / "hero.gif"

# --- Deterministic composition parameters -----------------------------------
# Output canvas. 900 wide reads full-bleed in a GitHub README; the height keeps the source
# 2400x2240 preview aspect so nothing is stretched.
_CANVAS_W = 900
_CANVAS_H = 840

# One 128-colour shared palette across every frame — no per-frame palette flicker and it
# lets the encoder delta-compress the zoom pairs.
_PALETTE_COLORS = 128

# The walkthrough: each committed preview plays as a two-frame "zoom-out reveal" — a tight
# hero crop of the headline area, then the full page. ``*_cs`` is that frame's on-screen
# time in centiseconds (GIF's native unit), so playback is identical everywhere.
# ``hero_box`` is the fractional crop (left, top, right, bottom) of the source used for the
# zoomed frame; the full frame always uses the whole preview.
class _Scene(NamedTuple):
    src: str
    hero_box: tuple[float, float, float, float]
    hero_cs: int
    full_cs: int


_SCENES = [
    # nav + title + the "Ask the World Data" card
    _Scene("site-preview-home.png", (0.06, 0.0, 0.94, 0.62), 105, 170),
    # graph header, Trace controls + the live nodes
    _Scene("graph-preview.png", (0.06, 0.30, 0.94, 0.95), 105, 185),
    # a weekly L2 brief, from the top
    _Scene("site-preview-brief.png", (0.06, 0.0, 0.94, 0.62), 105, 185),
]


def _fit(img: PILImage, box_frac: tuple[float, float, float, float] | None = None) -> PILImage:
    """Crop ``img`` to ``box_frac`` (fractions of its size) then resize to the canvas.

    ``box_frac`` is corrected to the canvas aspect ratio (widening/heightening the crop
    symmetrically) so the final resize never distorts the page. ``None`` uses the whole
    image. Deterministic: fixed integer box + fixed LANCZOS filter.
    """
    from PIL import Image

    w, h = img.size
    if box_frac is None:
        left, top, right, bottom = 0, 0, w, h
    else:
        left = round(box_frac[0] * w)
        top = round(box_frac[1] * h)
        right = round(box_frac[2] * w)
        bottom = round(box_frac[3] * h)

    # Grow the crop to the canvas aspect so the resize preserves proportions.
    cw, ch = right - left, bottom - top
    target = _CANVAS_W / _CANVAS_H
    if cw / ch > target:  # too wide -> add height
        need = round(cw / target)
        pad = (need - ch) // 2
        top = max(0, top - pad)
        bottom = min(h, top + need)
        top = max(0, bottom - need)
    else:  # too tall -> add width
        need = round(ch * target)
        pad = (need - cw) // 2
        left = max(0, left - pad)
        right = min(w, left + need)
        left = max(0, right - need)

    crop = img.crop((left, top, right, bottom))
    return crop.resize((_CANVAS_W, _CANVAS_H), Image.Resampling.LANCZOS)


def _frames_and_durations() -> list[tuple[PILImage, int]]:
    """Build the ordered (RGB frame, duration-cs) list from the committed previews."""
    from PIL import Image

    out: list[tuple[PILImage, int]] = []
    for scene in _SCENES:
        src = _ASSETS / scene.src
        if not src.is_file():
            raise FileNotFoundError(f"missing committed preview: {src}")
        base = Image.open(src).convert("RGB")
        out.append((_fit(base, scene.hero_box), scene.hero_cs))
        out.append((_fit(base, None), scene.full_cs))
    return out


def render_gif_bytes() -> bytes:
    """Compose the hero GIF fully in memory and return its exact bytes (deterministic)."""
    from PIL import Image

    pairs = _frames_and_durations()
    frames = [f for f, _ in pairs]
    durations_ms = [cs * 10 for _, cs in pairs]  # Pillow wants milliseconds

    # One shared palette built from every frame stacked vertically -> no inter-frame
    # palette flicker and the encoder can delta the near-identical zoom pairs.
    stack = Image.new("RGB", (_CANVAS_W, _CANVAS_H * len(frames)))
    for i, f in enumerate(frames):
        stack.paste(f, (0, i * _CANVAS_H))
    palette = stack.quantize(
        colors=_PALETTE_COLORS, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE
    )
    paletted = [f.quantize(palette=palette, dither=Image.Dither.NONE) for f in frames]

    buf = BytesIO()
    paletted[0].save(
        buf,
        format="GIF",
        save_all=True,
        append_images=paletted[1:],
        loop=0,
        duration=durations_ms,
        disposal=2,
        optimize=True,
    )
    return buf.getvalue()


def build(out: Path = _OUT) -> Path:
    data = render_gif_bytes()
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(data)
    return out


def is_stale(out: Path = _OUT) -> bool:
    """True if the committed GIF is missing or differs from a fresh build."""
    if not out.exists():
        return True
    return out.read_bytes() != render_gif_bytes()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="build the azimuth README hero GIF")
    parser.add_argument(
        "--check", action="store_true", help="exit 1 if docs/assets/hero.gif is stale"
    )
    args = parser.parse_args(argv)

    try:
        import PIL  # noqa: F401
    except ImportError:
        print(
            "ERROR: Pillow is not installed. Run:  uv pip install -e '.[demo]'",
            file=sys.stderr,
        )
        return 1

    if args.check:
        if is_stale():
            print(
                "hero.gif: STALE — run `python scripts/build_hero_gif.py` and commit.",
                file=sys.stderr,
            )
            return 1
        print("hero.gif: up to date.")
        return 0

    path = build()
    size_kb = path.stat().st_size // 1024
    print(f"hero.gif: wrote {path.relative_to(_REPO_ROOT)} ({len(_SCENES) * 2} frames, {size_kb} KB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
