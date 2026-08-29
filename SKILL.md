---
name: starryear-ink
description: Transform one user-supplied photograph into a vertical Starryear-Ink artwork that keeps a direct source-photo evidence band, fractures the scene into dry printed memory, and releases it as a source-bound chromatic ink afterimage. Use for Starryear-Ink, 星年水墨, 鹅鹅鹅, 摄影印刷水墨转译, or requests for a photo-to-print-to-ink editorial sheet. Do not use for full-frame ink filters, traditional shanshui, generic watercolor posters, or unrelated fantasy collage.
metadata:
  author: "Starryear"
  version: "2.1.0"
  license: "Starryear Personal Use and Attribution License"
---

# Starryear-Ink

Create one finished 1024 × 1536 RGB artwork from the user's actual photograph:

`PHOTOGRAPHIC EVIDENCE → ABSTRACT PRINTED MEMORY → CHROMATIC INK AFTERIMAGE`

The result is one continuous tactile sheet, not three panels and not one filter repeated three times. Recognition decays downward while source relationships remain.

## Before Making the Image

Inspect the source and write down five concrete facts:

1. **Primary evidence** — the subject or spatial relationship that makes this photograph specific.
2. **Count / rhythm** — repeated subjects, intervals, bars, blooms, steps, windows, or gaps.
3. **Directional gesture** — the dominant curve, axis, motion, perspective, or growth direction.
4. **Negative-space shape** — the largest sky, water, wall, shadow, bokeh, or open gap.
5. **Color system** — one dominant accent plus no more than two quieter source-derived supporting hues.

Choose one controlled impossible behavior that transforms real evidence: displacement, detached reflection, folded perspective, continuation, scale contradiction, material migration, or shadow separation. Never add unrelated fantasy objects.

Read [references/art-direction.md](references/art-direction.md) for the material grammar. For subject-specific decisions, read [references/source-translation.md](references/source-translation.md).

When visual calibration would improve the result, read [references/reference-gallery.md](references/reference-gallery.md) and inspect only the examples that match the source's spatial logic. Treat them as compositional evidence, never as images to copy or as permission to reproduce their text, seals, or incidental motifs.

## Three States

### 1. Evidence: immutable source photograph

Use a direct crop of the supplied file across roughly 26–35% of the canvas height. Crop, scale, position, and at most minimally harmonize tone. Do not ask image generation to recreate the visible photograph.

Preserve important subject identity, count, geometry, viewpoint, optical depth, light, shadows, reflections, background accidents, and at least 90% of meaningful evidence. End the band with one continuous irregular fibrous tear and a partial handmade-paper embrace; do not create a clean rectangular mat.

When possible, generate the paper/print/ink field first and then run:

```bash
python3 scripts/lock_evidence.py SOURCE_IMAGE GENERATED_BASE OUTPUT_IMAGE --evidence-ratio 0.30
```

Use `--focal-x` and `--focal-y` when a centered crop would lose the anchor. This deterministic step is required whenever the image tool can only approximate the photograph.

### 2. Printed Memory: dry, fragmented, structurally surreal

Use about three to seven meaningful fragments. Preserve relationships rather than complete depiction:

- count through rhythm;
- subjects through partial silhouettes or voids;
- geometry through axes and interrupted contours;
- depth through overlap;
- movement through displacement;
- color through residue.

Prefer halftone, transfer loss, etching line, graphite residue, broken registration, reduced-color print, and dry pigment. At first glance this should be an abstract printed construction; at second glance the source becomes recoverable. It must not be a smaller illustration of the photograph.

### 3. Ink Afterimage: wet, expanded, chromatic

Use two to five broad pigment masses and only the necessary dry-brush gestures or residual contours. Keep at least half of this region as untouched or nearly untouched warm paper. Make it broader, wetter, lower-frequency, and less literal than the printed memory.

Use transparent granulating versions of source colors. Black and near-black are structural anchors and should stay below roughly 20% of the lower pigment area. Do not default to pale grey ink when the photograph contains useful color.

## Make the States Collide

The middle and bottom may not sit as isolated horizontal illustrations. At least one principal wet ink relationship must rise from the lower field, enter the dry printed construction, change material, and approach the torn photo boundary. Let dots enter washes, contours disappear beneath pigment, or color migrate through fibers. Printed fragments may descend and dissolve.

Only when useful, allow the upward trace to overlap 2–8% of a nonessential part of the photographic band. Never cover the anchor.

This is the core movement:

`PRINTED STRUCTURE → MATERIAL COLLISION → PARTIAL DISSOLUTION → WET RELEASE`

## Generation and Assembly

1. Generate the non-photographic authored sheet using the actual photograph as a reference for structure and color, while reserving the upper evidence area for deterministic compositing.
2. Use the prompt builder in [references/production-prompt.md](references/production-prompt.md); replace every bracketed field with source-specific facts.
3. Composite the real source pixels with `scripts/lock_evidence.py`. Do not deliver an AI approximation in the evidence band.
4. Add exact text deterministically after generation. Default to no title. Add one small exact `Starryear` signature in the quiet lower margin.
5. Inspect at full resolution and thumbnail size using [references/quality-gate.md](references/quality-gate.md). Regenerate the non-photographic field once if a central invariant fails; do not keep iterating decorative details.

## Hard Rejections

Reject or revise any result that has:

- regenerated or visibly altered photographic evidence;
- three equal bands, framed boxes, or empty gaps between states;
- a complete middle redraw or a miniature lower watercolor copy;
- grey-only “safe ink” despite source color;
- unrelated mountains, bamboo, cranes, temples, moons, portals, calligraphy, seals, or mystical symbols;
- synthetic scalloped tearing, dirty antique parchment, glossy mockup depth, or heavy grunge;
- random crosshairs, fake metadata, pseudo-English, pseudo-Asian writing, branding blocks, or dominant typography;
- multiple competing saturated hues or black-dominant lower imagery.

## Authorship and Delivery

Preserve the name **Starryear-Ink** and credit **Starryear**. For a public post, include:

`使用 Starryear-Ink 创作｜作者：Starryear`

Return the final raster, source filename, the five source facts, the controlled surreal event, and a one-sentence description of how print becomes ink. Do not claim source-pixel lock unless the deterministic compositing step was used.

Read [AUTHOR.md](AUTHOR.md) and [LICENSE.md](LICENSE.md) before redistribution or commercial-use guidance.
