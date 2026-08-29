#!/usr/bin/env python3
"""Verify that the uncontested upper evidence area matches the direct source crop."""

from __future__ import annotations

import argparse
import json

from PIL import Image, ImageChops, ImageOps, ImageStat

from lock_evidence import evidence_ratio, fit_source, unit_interval


def verify(args: argparse.Namespace) -> int:
    final = ImageOps.exif_transpose(Image.open(args.final)).convert("RGB")
    source = Image.open(args.source)
    width, height = final.size
    evidence_h = int(round(height * args.evidence_ratio))
    protected_h = evidence_h - args.tear_amplitude - args.margin
    if protected_h <= 0:
        raise ValueError("protected comparison area is empty")

    expected = fit_source(source, (width, evidence_h), args.focal_x, args.focal_y)
    expected = expected.crop((0, 0, width, protected_h))
    actual = final.crop((0, 0, width, protected_h))
    difference = ImageChops.difference(expected, actual)
    means = ImageStat.Stat(difference).mean
    mae = sum(means) / len(means)
    passed = mae <= args.max_mae
    report = {
        "passed": passed,
        "mean_absolute_error": round(mae, 4),
        "threshold": args.max_mae,
        "checked_region": [0, 0, width, protected_h],
        "evidence_height": evidence_h,
        "interpretation": "direct crop/scale preserved" if passed else "upper evidence differs from expected source crop",
    }
    print(json.dumps(report, indent=2))
    return 0 if passed else 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source")
    parser.add_argument("final")
    parser.add_argument("--evidence-ratio", type=evidence_ratio, default=0.30)
    parser.add_argument("--focal-x", type=unit_interval, default=0.50)
    parser.add_argument("--focal-y", type=unit_interval, default=0.50)
    parser.add_argument("--tear-amplitude", type=int, default=22)
    parser.add_argument("--margin", type=int, default=8)
    parser.add_argument("--max-mae", type=float, default=0.75)
    return parser


if __name__ == "__main__":
    raise SystemExit(verify(build_parser().parse_args()))
