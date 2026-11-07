# Cognitive Design Principles

Evidence-based rules for slide design. Every Designer and Reviewer decision should trace to one of these principles.

---

## Miller's Law (Working Memory Capacity)

Human working memory holds **4 ± 1 chunks** in active focus (Cowan, 2001).

- Each Bento Grid card = 1 chunk if visually cohesive
- Max **5 distinct information units** per slide
- Complex topics: one core point per slide, split if needed
- Group related sub-items inside a single card to reduce chunk count

---

## Mayer's Multimedia Learning Principles

| Principle | Rule | Effect Size |
|-----------|------|-------------|
| **Spatial Contiguity** | Place labels/text adjacent to corresponding visuals | 1.10 (highest) |
| **Coherence** | Remove ALL decorative material that doesn't serve the message | 0.86 |
| **Signaling** | Use visual cues (color, size, position) to guide attention to key structures | 0.41 |
| **Segmenting** | Break complex information into digestible chunks across cards/slides | 0.32 |
| **Multimedia** | Use words + graphics together, not words alone | 0.43 |
| **Redundancy** | Don't display identical information in text AND narration simultaneously | -0.20 (harmful) |

**Design implication**: every decoration must justify its existence. "Does this help the audience understand?" — if no, remove it. Grain textures and glow spots are acceptable because they establish atmosphere without competing for attention; a decorative illustration that doesn't relate to content is not.

---

## Gestalt Principles for Slide Layout

| Principle | Slide Application |
|-----------|-------------------|
| **Proximity** | Related cards must be adjacent; separate unrelated groups with whitespace (>= 40px gap vs 20px within-group) |
| **Similarity** | Same-level items share visual treatment (color, size, shape). Don't mix card styles for peers. |
| **Continuity** | Align card edges to grid lines. Eyes follow implied alignment paths — break alignment only intentionally. |
| **Figure-Ground** | Primary content must have sufficient contrast against background. Cards create figure-ground separation. |
| **Common Region** | Use card boundaries to group related information. Items inside one card are perceived as related. |

---

## Cognitive Load Theory (Sweller)

Three types of cognitive load — design controls all three:

| Type | Definition | Design Goal |
|------|-----------|-------------|
| **Intrinsic** | Content complexity itself | Reduce by segmenting and sequencing (simpler concepts first) |
| **Extraneous** | Load imposed by poor design | **Eliminate aggressively** — this is what bad slides create |
| **Germane** | Effort that builds understanding | Maximize — structure, examples, analogies |

**Practical rule**: if a design element doesn't reduce intrinsic load or increase germane load, it's adding extraneous load. Remove it.

---

## Three-Second Test

Validation protocol for every completed slide:

1. Cover the slide, then look at it for **exactly 3 seconds**, then look away.
2. Ask: What did I see **first**? **Second**? **Third**?
3. If the answer doesn't match the intended hierarchy → **redesign** (hierarchy failure)
4. If you can't identify the core message at all → **reduce density** (overload failure)

This test catches the most common failure mode: slides where everything has equal visual weight.

---

## Three-Tier Information Hierarchy

Every slide must have **exactly three** distinguishable visual tiers:

| Tier | Role | Size | Opacity | Whitespace |
|------|------|------|---------|------------|
| **Primary** | Title, hero number, key message | 36-72px | 1.0 | Generous (20px+ margin) |
| **Secondary** | Supporting data, subheads, card titles | 18-24px | 0.8-1.0 | Moderate (12px margin) |
| **Tertiary** | Source citations, footnotes, labels, page numbers | 12-14px | 0.5-0.7 | Minimal |

**Rules**:
- If only 2 tiers are distinguishable → hierarchy is too flat → add contrast
- If 4+ tiers exist → hierarchy is too complex → merge the two closest tiers
- Primary tier: only **one** element per slide (the hero). Two competing primaries = no primary.

---

## Narrative Arc Structure

Structure the deck's emotional progression regardless of logical framework:

| Phase | Proportion | Purpose | Slide Types |
|-------|-----------|---------|-------------|
| **Setup** | ~15% | Establish context, shared understanding | cover, overview, context |
| **Tension** | ~60% | Present problem/opportunity, deepen with evidence, build toward climax | pain points, features, data, comparisons |
| **Resolution** | ~25% | Solution, vision, call to action | summary, CTA, pricing, closing |

**Rules**:
- The **climax slide** (strongest data or most compelling vision) should appear ~75% through the deck
- Build emotional intensity progressively — don't front-load your best evidence
- End on a **forward-looking note** (CTA, next steps, vision), not a summary of past content
- For a 16-slide deck: ~2 setup, ~10 tension, ~4 resolution

---

## Information Density Targets

| Page Type | Target Info Units | Max Key Points | Exceeding Limit |
|-----------|------------------|----------------|-----------------|
| cover / end | 2-3 | 0 | > 3 = Critical |
| section_divider | 1-2 | 0 | > 3 = Critical |
| quote / full_bleed | 1-2 | 0 | > 3 = Critical |
| content | 3-5 | 3 | > 7 = Major |
| data / dashboard | 4-7 | 2 (+2-5 data viz) | > 9 = Major |
| comparison | 4-6 | 2-3 per column | > 8 = Major |
| timeline / process | 3-6 | 3-6 nodes | > 8 = Major |

**What counts as 1 info unit**: a stat card, a bullet group (not individual bullets), a chart, an icon+label pair, a badge group.
