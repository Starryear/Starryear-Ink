#!/usr/bin/env python3
"""Composite a direct source-photo crop over a generated Starryear-Ink base.

The visible evidence is cropped/scaled source data, never regenerated imagery.
"""

from __future__ import annotations

import argparse
import math
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps


def unit_interval(value: str) -> float:
    number = float(value)
    if not 0.0 <= number <= 1.0:
        raise argparse.ArgumentTypeError("value must be between 0 and 1")
    return number


def evidence_ratio(value: str) -> float:
    number = float(value)
    if not 0.26 <= number <= 0.35:
        raise argparse.ArgumentTypeError("evidence ratio must be between 0.26 and 0.35")
    return number


def fit_source(
    source: Image.Image,
    size: tuple[int, int],
    focal_x: float,
    focal_y: float,
) -> Image.Image:
    """Crop around a normalized focal point, then resize without reconstruction."""
    source = ImageOps.exif_transpose(source).convert("RGB")
    target_w, target_h = size
    source_w, source_h = source.size
    target_aspect = target_w / target_h
    source_aspect = source_w / source_h

    if source_aspect > target_aspect:
        crop_h = source_h
        crop_w = int(round(crop_h * target_aspect))
        left = int(round((source_w - crop_w) * focal_x))
        top = 0
    else:
        crop_w = source_w
        crop_h = int(round(crop_w / target_aspect))
        left = 0
        top = int(round((source_h - crop_h) * focal_y))

    left = max(0, min(left, source_w - crop_w))
    top = max(0, min(top, source_h - crop_h))
    crop = source.crop((left, top, left + crop_w, top + crop_h))
    return crop.resize(size, Image.Resampling.LANCZOS)


def build_tear_mask(
    canvas_size: tuple[int, int],
    evidence_h: int,
    amplitude: int,
    seed: int,
) -> Image.Image:
    """Build one continuous source-responsive-looking fibrous lower boundary."""
    width, height = canvas_size
    rng = random.Random(seed)
    step = max(28, width // 24)
    controls = []
    for x in range(-step, width + step * 2, step):
        controls.append((x, rng.uniform(-amplitude, amplitude)))

    boundary: list[tuple[int, int]] = []
    for x in range(width):
        index = (x + step) // step
        x0, y0 = controls[index]
        x1, y1 = controls[index + 1]
        t = (x - x0) / (x1 - x0)
        smooth_t = t * t * (3.0 - 2.0 * t)
        variation = y0 + (y1 - y0) * smooth_t
        fine = math.sin(x * 0.071 + seed) * amplitude * 0.12

        edge_distance = min(x, width - 1 - x)
        embrace = max(0.0, 1.0 - edge_distance / (width * 0.16))
        corner_lift = embrace * amplitude * 1.35
        y = int(round(evidence_h + variation + fine - corner_lift))
        boundary.append((x, max(1, min(height - 2, y))))

    mask = Image.new("L", canvas_size, 0)
    draw = ImageDraw.Draw(mask)
    polygon = [(0, 0), (width - 1, 0)] + list(reversed(boundary))
    draw.polygon(polygon, fill=255)

    # Sparse downward paper fibers soften the tear without creating a digital wave.
    for _ in range(max(80, width // 5)):
        x = rng.randrange(width)
        y = boundary[x][1]
        length = rng.randint(2, max(4, amplitude // 2))
        alpha = rng.randint(45, 155)
        draw.line((x, y - rng.randint(0, 2), x + rng.randint(-2, 2), y + length), fill=alpha, width=1)

    return mask.filter(ImageFilter.GaussianBlur(0.35))


def find_font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = (
        "/System/Library/Fonts/NewYork.ttf",
        "/System/Library/Fonts/Supplemental/Times New Roman.ttf",
        "/Library/Fonts/Times New Roman.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
    )
    for candidate in candidates:
        if Path(candidate).exists():
            return ImageFont.truetype(candidate, size=size)
    return ImageFont.load_default()


def add_signature(image: Image.Image, signature: str) -> None:
    if not signature:
        return
    draw = ImageDraw.Draw(image)
    font = find_font(max(12, image.width // 64))
    box = draw.textbbox((0, 0), signature, font=font)
    text_w = box[2] - box[0]
    text_h = box[3] - box[1]
    x = (image.width - text_w) // 2
    y = image.height - text_h - max(18, image.height // 52)
    draw.text((x, y), signature, font=font, fill=(82, 75, 68, 205))


def compose(args: argparse.Namespace) -> None:
    base = ImageOps.exif_transpose(Image.open(args.base)).convert("RGBA")
    canvas_w, canvas_h = base.size
    evidence_h = int(round(canvas_h * args.evidence_ratio))
    source = Image.open(args.source)
    photo = fit_source(source, (canvas_w, evidence_h), args.focal_x, args.focal_y).convert("RGBA")

    photo_layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    photo_layer.paste(photo, (0, 0))
    mask = build_tear_mask(base.size, evidence_h, args.tear_amplitude, args.seed)

    if not args.no_shadow:
        shifted = Image.new("L", base.size, 0)
        shifted.paste(mask, (0, max(2, canvas_h // 512)))
        shadow_mask = shifted.filter(ImageFilter.GaussianBlur(max(2.0, canvas_w / 280.0)))
        shadow = Image.new("RGBA", base.size, (48, 40, 34, 38))
        base = Image.composite(shadow, base, shadow_mask.point(lambda p: int(p * 0.16)))

    result = Image.composite(photo_layer, base, mask).convert("RGB")
    add_signature(result, args.signature)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    result.save(output, format="PNG", optimize=True)
    print(f"saved={output}")
    print(f"canvas={canvas_w}x{canvas_h} evidence_height={evidence_h} source_lock=direct_crop_scale")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", help="User-supplied source photograph")
    parser.add_argument("base", help="Generated paper/print/ink base artwork")
    parser.add_argument("output", help="Output PNG path")
    parser.add_argument("--evidence-ratio", type=evidence_ratio, default=0.30)
    parser.add_argument("--focal-x", type=unit_interval, default=0.50)
    parser.add_argument("--focal-y", type=unit_interval, default=0.50)
    parser.add_argument("--tear-amplitude", type=int, default=22)
    parser.add_argument("--seed", type=int, default=2026)
    parser.add_argument("--signature", default="Starryear")
    parser.add_argument("--no-shadow", action="store_true")
    return parser


if __name__ == "__main__":
    compose(build_parser().parse_args())
