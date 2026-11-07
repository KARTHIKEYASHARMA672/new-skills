# Book Editor — Claude Code Skill

A Claude Code skill for professional book and manuscript editing using Word track changes. Point Claude at a `.docx` manuscript and get multi-pass editing with proper tracked changes the author can accept or reject in Word.

## What it does

1. Calibrates editing approach on a small sample, gets author feedback
2. Establishes a style guide for consistency across the manuscript
3. Works through the document in multi-pass editing (structural, line, copy, polish)
4. Produces a `.docx` with Word-native track changes and comments

Works with books, academic papers, reports, long-form articles — anything in `.docx` format.

## How it works

The skill unpacks `.docx` files (which are ZIP archives of XML), edits the XML to insert proper track change markup (`<w:ins>`, `<w:del>`) and comments, then repacks. The result opens in Word/LibreOffice with full Track Changes support — the author sees insertions, deletions, and margin comments exactly as if a human editor used Review mode.

## Installation

Copy the skill folder to your Claude Code skills directory:

```bash
# Clone the repo (or download just this folder)
git clone https://github.com/lfurze/claude-skills.git

# Copy the skill into place
cp -r claude-skills/book-editor ~/.claude/skills/book-editor
```

Or symlink:

```bash
ln -s "$(pwd)/claude-skills/book-editor" ~/.claude/skills/book-editor
```

After installation:

```
~/.claude/skills/
  book-editor/
    SKILL.md
    references/
      editing-examples.md
      style-guide-template.md
```

## Usage

Once installed, Claude Code will automatically detect the skill. Just ask:

- "Edit this manuscript"
- "Proofread my book"
- "Do a copy edit on this document"
- "Line edit chapter 3"
- "SPAG check this manuscript"

## Editing passes

The skill uses a four-pass approach, each focused on a different level:

| Pass | Focus | Output |
|------|-------|--------|
| 1. Structural | Organization, flow, gaps, pacing | Comments only |
| 2. Line editing | Sentence clarity, tightening prose | Track changes + comments |
| 3. Copy editing | SPAG, consistency, fact-checking | Primarily track changes |
| 4. Final polish | Catch remaining issues | Light track changes |

## Chunking

For long manuscripts, the skill works in chunks (3,000-5,000 words, preferring chapter boundaries) and maintains a style guide for consistency across chunks.

## Reference files

- `references/style-guide-template.md` — Template for the per-manuscript style guide (spelling, terminology, capitalisation, punctuation, formatting decisions)
- `references/editing-examples.md` — Examples of appropriate edits at each pass level, showing when to use track changes vs comments

## License

MIT
