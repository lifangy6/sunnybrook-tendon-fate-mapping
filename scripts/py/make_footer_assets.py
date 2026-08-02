"""Build the two derived footer assets used by the poster.

Both source files are unusable as shipped:

  * the Chrome-generated QR is 450 px with stylised dot modules and a dino
    glyph over the centre -- it prints soft at poster size and strict decoders
    fail on it, so a clean high-error-correction QR is generated instead;
  * the official DRAC lockup is 2048x1152 but only 2.6% ink -- the artwork
    occupies a 1586x194 band and the rest is padding, so placing the file as-is
    wastes most of the width and renders the mark far smaller than requested.

Outputs land next to their sources in BINF6999/drafts/logos/ and are committed,
so the poster build does not depend on this script at render time.

Run:  uv run --python 3.12 --with pillow --with qrcode \
          --with opencv-python-headless --with numpy \
          python scripts/py/make_footer_assets.py
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
LOGO = ROOT / "BINF6999" / "drafts" / "logos"

REPO_URL = "https://github.com/lifangy6/sunnybrook-tendon-fate-mapping"


def build_qr() -> Path:
    """Crisp QR at ~1.8k px, error correction H so it survives print wear."""
    import qrcode

    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=48,
        border=2,          # quiet zone; below 2 modules many scanners give up
    )
    qr.add_data(REPO_URL)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white").convert("RGB")
    out = LOGO / "qr_github_hires.png"
    img.save(out, dpi=(600, 600))
    print(f"  QR   {img.size[0]}x{img.size[1]} px -> {out.name}")
    return out


def trim(src: Path, out_name: str) -> Path:
    """Crop to the bounding box of actual ink, keeping a small even margin."""
    im = Image.open(src).convert("RGBA")
    a = np.array(im)
    mask = (a[..., 3] > 10) & (a[..., :3].min(axis=-1) < 240)
    ys, xs = np.where(mask)
    pad = 6
    box = (max(xs.min() - pad, 0), max(ys.min() - pad, 0),
           min(xs.max() + 1 + pad, im.width), min(ys.max() + 1 + pad, im.height))
    cropped = im.crop(box)
    out = LOGO / out_name
    cropped.save(out, dpi=(600, 600))
    print(f"  trim {im.size[0]}x{im.size[1]} -> {cropped.size[0]}x{cropped.size[1]} px"
          f"  ({out.name})")
    return out


def upscale_mark(src: Path, out_name: str, target: int = 1200) -> Path:
    """Re-rasterise the flat-colour DRAC mark at high resolution.

    The shipped mark is 260x260 with only a 195x195 artwork area, which prints
    at roughly 175 dpi once placed -- visibly soft. It is a single flat colour
    (#D6A500) carried entirely by an anti-aliased alpha channel, so the shape
    can be reconstructed rather than merely interpolated: resample alpha
    smoothly, then push it back through a steep ramp centred on 0.5 so the
    contour resolves to a ~1 px edge at the new size instead of a wide blur.
    Plain LANCZOS would keep the soft edge and just make it bigger.
    """
    im = Image.open(src).convert("RGBA")
    a = np.array(im)
    mask = a[..., 3] > 10
    ys, xs = np.where(mask)
    im = im.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))

    alpha = Image.fromarray(np.array(im)[..., 3]).resize(
        (target, target), Image.LANCZOS)
    al = np.asarray(alpha).astype(np.float32) / 255.0
    scale = target / max(im.size)                 # edge sharpening strength
    al = np.clip((al - 0.5) * scale + 0.5, 0.0, 1.0)

    rgb = np.array([0xD6, 0xA5, 0x00], dtype=np.uint8)
    out_arr = np.zeros((target, target, 4), dtype=np.uint8)
    out_arr[..., :3] = rgb
    out_arr[..., 3] = (al * 255).round().astype(np.uint8)

    out = LOGO / out_name
    Image.fromarray(out_arr, "RGBA").save(out, dpi=(600, 600))
    soft = ((al > 0.02) & (al < 0.98)).mean() * 100
    print(f"  mark {im.size[0]}x{im.size[1]} -> {target}x{target} px"
          f"  ({soft:.1f}% soft edge)  ({out.name})")
    return out


def verify(qr_path: Path) -> None:
    import cv2
    data, _, _ = cv2.QRCodeDetector().detectAndDecode(cv2.imread(str(qr_path)))
    assert data == REPO_URL, f"QR decodes to {data!r}, expected {REPO_URL!r}"
    print(f"  verified: QR decodes to {data}")


if __name__ == "__main__":
    print(f"Building footer assets -> {LOGO}")
    qr = build_qr()
    trim(LOGO / "DRAC_logo.png", "DRAC_logo_trimmed.png")
    upscale_mark(LOGO / "DRAC_logo_only.png", "DRAC_mark_hires.png")
    verify(qr)
    print("done")
