# Turn Recordings into Posts & Articles

A Claude Code skill that transforms raw transcripts, conversations, and notes into ready-to-publish content — either **multiple social posts** or a **single long-form article**.

## Two Modes

| Mode | Input | Output |
|---|---|---|
| **Social Posts** (default) | Any transcript/notes | 2-15 ready-to-publish posts, sorted by quality |
| **Long-form Article** | Structured talk/interview | One cohesive article (3000-10000+ chars), written section-by-section |

The skill auto-detects which mode to use based on your request, or you can specify explicitly.

## Key Features

- **Persistent style profile**: Analyze your reference posts once, auto-load every time. No need to re-upload style references per session.
- **Style learning**: Saves both analysis summary + full sample posts for accurate voice matching
- **Rigorous fact-checking**: Verifies all proper nouns, data points, and logical connections
- **Multi-source ASR handling**: Cross-verifies multiple transcripts, user dictionary has highest authority
- **Long transcript handling**: Tested up to 5500+ lines / 90+ min — uses index-retrieval strategy to prevent fabrication
- **Pre-delivery QA**: Mandatory self-review (fact-check, dedup, ASR residue, unsourced content) before output
- **Version management**: Every revision saved as `_vN.md` for traceability
- **Article heading logic**: 4-6 first-level headings for narrative arcs, sub-headings for specific topics
- **Quality over quantity**: Strict 4 Iron Rules for insights; "Delete Until Impossible" for every sentence

## Usage

Provide a transcript — style is auto-loaded from your saved profile:

```
/transcript-to-content
```

### First-time setup: Save your style

Provide 2-5 reference posts and tell Claude "保存风格":

```
保存风格

[paste 2-5 of your published posts here]
```

Claude will analyze and save your style profile. All future runs auto-load it.

### Multiple style profiles

```
保存为 formal 风格    # Save a named profile
用 formal 风格        # Use a specific profile
更新风格              # Update default profile with new references
```

## File Structure

```
transcript-to-content/
├── SKILL.md                                  # Main skill prompt
├── README.md                                 # This file
├── references/
│   ├── golden-sentence-standards.md          # Quality standards for insights
│   ├── writing-checklist.md                  # Writing checklist (both modes)
│   ├── long-transcript-strategy.md           # Processing strategy by length
│   ├── paragraph-rhythm.md                   # Paragraph rhythm guidelines
│   ├── proper-noun-verification.md           # Transcript name verification
│   └── troubleshooting.md                    # Technical edge cases
└── style-profiles/                           # Persistent style profiles
    └── README.md                             # Profile format documentation
```

## Use Cases

**Social Posts**: Podcast recordings, meeting notes, brainstorming sessions -> Twitter threads, LinkedIn posts, blog posts

**Articles**: Sharing sessions, interview transcripts, panel discussions, lecture recordings -> Deep-dive articles, narrative long-reads, educational content
