# Deck Instructions

## Source
- **File:** [your-outline.md]
- **Theme:** electric-dark

## Meta (all optional -- Claude infers from outline if not provided)
- **Title:**
- **Subtitle:**
- **Presenter:**
- **Date:**
- **Audience:**
- **Duration:**

## Content guidance

Build a complete Reveal.js deck from the raw outline above. The outline contains slide titles with raw notes -- some sparse, some overly long. Use your judgment:

- **Too long for one slide?** Tighten the language first. If it's still too dense, break it across 2-3 slides. Don't lose key information -- condense, don't cut.
- **Too sparse?** Flesh it out with relevant detail the audience would benefit from. Don't pad -- add substance.
- **Topic breaks** -- when the subject shifts, insert a section divider slide to orient the audience before continuing.
- **Missing topics** -- if there's an obvious gap or related idea the outline doesn't cover but should, add a slide for it. Flag these with a speaker note so I can review.
- **Display choices** -- pick the right component for the content: bullet lists for sequences, panels/boxes for grouped concepts, pull quotes for key takeaways, code blocks for commands/syntax, comparison layouts for before/after or good/bad, flow diagrams for processes. Don't default to bullet lists when a visual would be stronger.
- **External resources** -- include links where they add value (docs, tools, references).
- **Graphics** -- use inline SVG for diagrams, charts, or visuals where they reinforce the content. Don't force visuals where text is clearer.

## Workflow

### Step 1 -- Interview (before building)

After reading the outline, ask a short round of targeted questions (3-5 max). Only ask what you actually need to know -- skip anything obvious from the outline itself. Examples:

- What's the audience and their familiarity with the topic?
- Any preferred theme, or should I default to `electric-dark`?
- Any slides you already know need special treatment (heavy visuals, specific layout)?
- Tone -- technical deep-dive, casual overview, persuasive pitch?
- Anything in the notes that's unclear or seems incomplete?

Don't ask generic questions the outline already answers. Don't turn this into a long survey -- read the material first, then ask only what's ambiguous.

After reading the outline, also note 2-4 concrete suggestions:
- Topics the audience would expect but aren't covered
- A missing intro, summary, or closing
- Opportunities for a comparison, demo, or example
- Sections that might flow better rearranged

Frame as proposals, not demands. I'll accept, reject, or modify before you build.

### Step 2 -- Full draft

After the interview, generate all slides in one pass:

- It's okay to add slides beyond what the outline specifies.
- Every content slide gets a `{NNN}` slug for easy reference during iteration.
- Flag any slides you added (not in the original outline) with a speaker note.

### Step 3 -- Title slide meta (automatic)

After generating the draft, update the title slide with:

- **Slide count** -- total number of content slides (excluding the title slide itself)
- **Estimated duration** -- calculated from slide complexity:
  - Section dividers / title cards: ~30 seconds each
  - Standard content slides: ~1 minute each
  - Dense slides (code, comparisons, detailed diagrams): ~1.5 minutes each
- Display both on the title slide (e.g. "15 slides / ~18 min")

Recalculate and update these values after every editing pass so they stay current.

### Step 4 -- Iterate

After the draft, I'll iterate by referencing specific slides: "tighten {003}", "split {007}", "drop {011}", etc.
