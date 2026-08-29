# Production Prompt Builder

Use this only after writing the five source facts. Replace every bracketed field; never send placeholders literally.

## Generate the authored paper / print / ink field

```text
Using the supplied photograph solely as structural and chromatic reference, create one 1024 × 1536 RGB vertical Starryear-Ink authored sheet. Reserve the upper [EVIDENCE_PERCENT]% for later deterministic placement of the actual source photograph. Do not invent or redraw photographic content there; make the reserved area compatible with a direct source crop and one irregular torn-paper boundary.

Source facts:
- Primary evidence: [PRIMARY_EVIDENCE]
- Count or rhythm: [COUNT_RHYTHM]
- Directional gesture: [DIRECTIONAL_GESTURE]
- Negative-space shape: [NEGATIVE_SPACE]
- Color system: dominant [DOMINANT_HUE], supported quietly by [SUPPORTING_HUES]

Below the future evidence band, build a warm matte ivory handmade-paper field with restrained fibers, subtle mottling, shallow wrinkles, broad active negative space, and no outer frame.

Create an abstract dry printed memory from three to seven source-derived fragments: [PRINT_FRAGMENTS]. Preserve count through rhythm, subjects through incomplete contours or voids, geometry through axes, depth through overlap, motion through displacement, and color through residue. Use imperfect halftone, transfer loss, etching line, graphite residue, broken registration, reduced-color print, and dry pigment. At first glance it must read as an abstract print construction; at second glance the source relationships become discoverable. Do not make a complete illustration or smaller copy.

Introduce one restrained source-bound impossible behavior: [CONTROLLED_SURREAL_EVENT]. Transform only evidence that exists in the photograph; add no fantasy object.

Release the print toward the bottom into a wet chromatic ink afterimage made from [TWO_TO_FIVE_MASSES] and [ONE_TO_FOUR_GESTURES]. Use transparent granulating versions of the selected source colors, capillary feathering, pigment tide, sediment, diluted mineral wash, and broken dry brush. Keep black subordinate and leave at least half of the lower region as untouched or nearly untouched paper. Preserve the scene through mass, spacing, rhythm, and direction, never literal detail.

Make print and ink physically collide. Let [UPWARD_INK_RELATIONSHIP] grow upward from the lower field, collect or erase halftone, change into broken dry texture, and approach the future torn-photo boundary. Let [DESCENDING_PRINT_RELATIONSHIP] descend and dissolve into pigment. Create no empty horizontal gap and no exact boundary between middle and bottom.

Keep the work quiet but not vacant, experimental but not arbitrary, surreal but not fantastical, and materially handmade. No three equal panels, framed boxes, scrapbook collage, grey-only safe ink, generic watercolor, dirty parchment, glossy mockup, unrelated mountains, bamboo, cranes, temples, moons, portals, calligraphy, seals, mystical marks, decorative icons, fake metadata, illegible text, or commercial advertising.

Reserve a clean lower-margin position for a tiny exact Starryear signature, to be added deterministically later. Render no other text.
```

## Assemble the immutable evidence

After generation, run from the skill folder:

```bash
python3 scripts/lock_evidence.py \
  /absolute/path/source.jpg \
  /absolute/path/generated-base.png \
  /absolute/path/final.png \
  --evidence-ratio 0.30 \
  --focal-x 0.50 \
  --focal-y 0.50 \
  --signature Starryear
```

Change focal coordinates only to preserve the declared primary evidence. Values range from 0 to 1.

Verify the protected upper region:

```bash
python3 scripts/verify_evidence.py \
  /absolute/path/source.jpg \
  /absolute/path/final.png \
  --evidence-ratio 0.30 \
  --focal-x 0.50 \
  --focal-y 0.50
```

The verifier checks the uncontested upper portion, above the irregular tear and material overlaps. It does not replace visual QA.
