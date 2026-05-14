---
name: transcript-to-content
description: Transform transcripts, conversations, or raw notes into shareable content — either multiple social posts OR a single long-form article. Learns style from user's published content. Handles transcripts of any length (tested up to 5500+ lines / 90+ min). Use when user: (1) provides transcript/conversation/recording and wants social content, (2) asks to "turn recording/notes into posts", (3) mentions generating content from recordings/notes, (4) needs multiple publishable pieces from single source, (5) asks to write an article from a transcript — e.g. "写成文章/长文", "整理成一篇文章", "write up this session", "turn this talk into a blog post", "深度文章". Social mode outputs 2-15 ready-to-publish pieces. Article mode outputs a structured long-form piece (3000-10000+ chars) written section-by-section.
---

# Transcript to Content Generator

Transform raw content (transcripts, conversations, notes) into ready-to-publish content — social posts or long-form articles.

## Step 0: Determine Mode

Before doing anything else, decide which mode to use:

- **Article Mode** — if user says "写成文章/长文/article/write up/blog post", OR the transcript is a structured talk/sharing/interview with a clear narrative arc. Jump to [Long-form Article Mode](#long-form-article-mode).
- **Social Post Mode** — for everything else (extracting multiple standalone posts). Continue with Step 1 below.

If unclear, ask the user: "Do you want multiple social posts, or one cohesive article?"

---

## Social Post Mode

### Step 1: Receive Input

Accept two inputs:
- **Required**: Raw content (transcript, conversation, notes)
- **Style**: Auto-loaded from saved profile, OR provided by user

**Style resolution order (IMPORTANT — check before asking user):**

1. **Check for saved style profile first**: Read `style-profiles/default.md` AND `style-profiles/default-samples.md` (relative to this skill's directory). If they exist, load both silently — the summary for rules, the samples for voice and rhythm. Do NOT ask user for reference content.
2. **User provides new reference content in this session**: Analyze it (see below) and offer to save/update the profile.
3. **User specifies a named profile**: e.g. "用 formal 风格" → load `style-profiles/formal.md`
4. **No profile exists AND no reference provided**: Ask user: "Do you have 2-5 examples of content you've published that you like? This helps me match your style. I'll save it so you won't need to provide it again."
5. **User declines**: Use neutral professional tone with clear structure.

**When analyzing reference content (new or for saving), extract:**
- Information density (data-heavy / case-heavy / opinion-heavy)
- Language style (formal / casual / sharp / moderate)
- **Structure observation** (CRITICAL):
  - Does it use bold subheadings? How many?
  - Does it use numbered lists (1. 2. 3.)?
  - Average paragraph length (1-2 lines / 3-4 lines / longer)?
  - Opening style (direct statement / data / story / question)?
  - Use of emojis, formatting, links?
- Attitude markers (explicit judgment / emotional words / teaching tone)
- Platform conventions (Twitter threads, LinkedIn posts, blog-style, etc.)

### Step 2: Extract All Possible Content

Identify content at 4 levels:

1. **Short insights (20-150 characters)** - Standalone observations or quotes
2. **Phenomenon posts (150-300 characters)** - Interesting observations with brief analysis
3. **Medium posts (300-600 characters)** - Complete logical argument with 3-4 supporting points
4. **Deep analysis (600-1000 characters)** - Complex multi-dimensional analysis

List all possibilities without filtering yet.

**For transcripts >1000 lines**: Follow the length-based processing strategy in [references/long-transcript-strategy.md](references/long-transcript-strategy.md). The core principle: memory is lossy compression — verify facts in real-time using Grep, don't write from memory. For transcripts >3000 lines, the two-pass index-retrieval workflow is MANDATORY.

### Step 3: Deduplicate and Prioritize

**Deduplication rules:**
- If a point can expand into a full post, don't make it a standalone insight
- Use each point only once - don't repeat in both long post and short insight
- Same material can appear in different posts, but with different roles

**Prioritization criteria:**
- Counter-intuitive insights > common observations
- Specific data with comparisons > abstract descriptions
- Complete material > needs supplementing
- Universal insights > niche/insider-only content

**Determine output quantity based on content richness:**
- Rich content (90+ min, multiple topics): 10-15 total posts
- Medium content (30-90 min, 2-3 topics): 6-10 total posts
- Light content (<30 min, 1 topic): 2-4 total posts

These are guidelines, not hard caps. Better to extract comprehensively upfront than in multiple rounds.

**Output structure:**
- Sort ALL content by quality (highest first)
- Write FULL content for all posts, not just outlines
- Let user decide what to publish

**Insights (short standalone pieces) quantity is NOT predetermined:**
- Apply strict 4 Iron Rules filtering to ALL candidates
- Output as many as pass the standard (could be 0, 1, 5, or 10)
- Quality standard is fixed, quantity is the natural result

If content is too personal or lacks universal value, tell user honestly.

### Step 3.5: Verify All Proper Nouns (MANDATORY for transcripts)

If input is a transcript (voice-to-text), verify all proper nouns BEFORE writing any content. Transcripts have extremely high error rates for names due to mishearing.

See [references/proper-noun-verification.md](references/proper-noun-verification.md) for the full workflow. Key steps:
1. Extract all proper nouns (people, companies, products)
2. Verify each via web search before writing content
3. Create a replacement list and apply corrections with `replace_all=true`
4. Skip only if input is written text (not transcript) or has no proper nouns

### Step 4: Write Content

**For each piece:**

1. **Choose appropriate length** based on topic complexity

2. **Match user's style from saved profile or reference content:**
   - If style profile is loaded (saved or session-provided), mirror their paragraph length, formatting, opening style, and tone
   - If no style available: mobile-first, short paragraphs (2-4 lines), lead with most compelling point

3. **"Delete Until Impossible" Execution:**

   **First pass - Delete structural fluff:**
   - Delete unnecessary formatting (unless user's style uses it)
   - Delete transition sentences between sections
   - Delete summary conclusions that just repeat what was said

   **Second pass - Test each sentence:**
   - Ask: "If I delete this sentence, does the logic break?"
   - If logic doesn't break -> DELETE
   - If it's just repeating the previous point -> DELETE
   - If it's an obvious statement everyone knows -> DELETE

   **Third pass - Check structure:**
   - Does structure feel natural or forced?
   - If it reads like a PowerPoint -> REWRITE without visible structure
   - Logic should flow through content, not through formatting

4. **Follow core principles:**
   - One theme per piece - don't try to cover everything
   - Logic > case studies - use cases only as evidence
   - Match user's style if reference provided
   - Have attitude - make clear judgments, don't hedge excessively

5. **For short insights (STRICT FILTERING):**
   - **4 Iron Rules - ALL must pass:**
     - Independence: Can be understood without context (max 1-2 sentences setup)
     - Completeness: Full meaning, not half a sentence
     - Impact: Data/contrast/counter-intuitive/emotional resonance
     - Non-duplication: Not already covered in a longer post
   - If none pass all 4 tests -> Output "No suitable standalone insights found"
   - See [references/golden-sentence-standards.md](references/golden-sentence-standards.md) for examples

6. **Check against quality standards:**
   - See [references/writing-checklist.md](references/writing-checklist.md) for complete checklist

7. **Verify data points (CRITICAL):**
   - Proper nouns should already be verified in Step 3.5
   - For ALL data points (revenue, valuation, dates, percentages): search to confirm if surprising
   - For long transcripts: don't assume you remember correctly - Grep and re-read the section
   - Better to remove questionable details than publish incorrect information

### Step 5: Batch Output

Output format:

```
Extracted X pieces of shareable content from your transcript, sorted by quality:

---

## Content 1 | Title

[Complete content - ready to publish]

---

## Content 2 | Title

[Complete content]

---

[Continue with all content...]
```

**IMPORTANT:**
- NO category headers or labels
- Sort ALL content by quality (highest first), regardless of type or length
- Clean markdown only - each piece separated by `---`
- Each piece header format: `## Content X | Title` (concise title summarizing the topic)
- DO NOT include meta-information (priority, engagement predictions, recommendations)
- Output should be CLEAN and READY-TO-PUBLISH

After output, ask: "How do these look? Need any adjustments?"

---

## Long-form Article Mode

When the transcript is a structured talk, interview, or sharing session with a clear narrative arc, the user may want a **single deep article** instead of multiple social posts. This mode produces a cohesive long-form piece (3000-10000+ characters) written section-by-section into a markdown file.

### When to Use This Mode

- User says "写成文章" / "写成长文" / "整理成一篇文章" / "turn into an article" / "write up this session"
- Transcript is a structured talk/sharing/interview (not casual chat)
- Content has a clear narrative arc (why -> how -> what happened)

### Article Workflow

#### Phase 1: Read, Compress, Outline

1. **Read all source material** — transcript + any supplementary notes/references mentioned

   **Multi-source ASR handling (CRITICAL when multiple transcripts are provided):**

   当同时提供多份转录文档时（例如：原始录音转录稿 + 聊天总结），两份都可能含有 ASR 识别错误。处理原则：

   | 来源 | 权重 | 用途 |
   |------|------|------|
   | **用户词典** | 最高 | 专有名词、产品名、术语的唯一权威 |
   | **两份文档互相印证** | 高 | 两份都提到的内容，可信度高 |
   | **上下文语义逻辑** | 主要判断依据 | 某个词/说法放在上下文里是否合理 |
   | **单一文档的独立说法** | 需核查 | 只在一份文档出现、另一份没有，需靠上下文验证 |

   **不能做的事：**
   - 不能因为是"原始转录"就自动高于"总结"——两份都是 ASR，都可能有错
   - 不能因为总结里写了某个说法就直接采用——总结同样可能听错
   - 不能凭大模型自身知识补充"背景信息"写入正文——只有对话里出现的内容才能进正文；模型自行补充的公司数据、行业数据等，只能进附录并标注"来源非对话"

   **常见判断案例：**
   - 两份都写"o1模型"但上下文语境是在讲某个开源项目 → 结合用户词典查是否有对应词条，再看上下文
   - 总结写"OpenAI Completions API"，原文写"opengl"（明显 ASR 错误）→ 用词典 + 上下文判断实际指什么
   - 两份均无该词条，上下文语义不通 → 标注存疑，或在附录说明

2. **Compress into structured notes** — Write a `notes.md` file in the same directory as the article. This is the critical intermediate step that prevents quality decay in later sections. For each major topic in the transcript, capture:
   - **Core argument** (1-2 sentences)
   - **Key facts** (specific data, names, examples)
   - **Quotable lines** (vivid/emotional/opinionated — pre-select 2-3 per topic)
   - **Source type** (structured presentation / Q&A discussion / personal story) — this directly feeds Phase 2.5's rewrite intensity

   The notes file replaces the raw transcript as the primary writing source. Subsequent sections are written from notes, with Grep used only to verify specific details. This is why it matters: writing from a 39-page transcript relies on lossy memory; writing from 2-3 pages of structured notes keeps every section equally grounded.

3. **Generate a structured outline** with heading hierarchy (see Heading Structure below)
4. **Present outline to user for confirmation** — do NOT start writing until approved
5. **User may restructure** — e.g. "too many first-level headings, merge into fewer with sub-headings"

#### Phase 2: Section-by-Section Writing

1. **Write into a .md file incrementally** — one section at a time, appending via Edit tool
2. **Each section should be self-contained** — complete before moving to next
3. **Verify facts per section** — Grep the transcript for exact quotes and details before writing each section
4. **Mark completed sections** — use TodoWrite to track progress across sections
5. **Classify source material before writing each section** — see Quality Control below

**Why section-by-section?**
- Prevents context overflow on long articles
- Lets user review and adjust tone/style early (after first 1-2 sections)
- Avoids losing all work if a single large write fails
- User can make corrections mid-stream that inform subsequent sections
- **Prevents tail-end quality decay** — when multiple sections are written in a single generation, the last sections degrade to near-transcription. Strict one-section-per-Edit avoids this.

#### Phase 2.5: Quality Control Per Section

Before writing each section, classify its source material:

| Source type | Rewrite intensity | What to do |
|---|---|---|
| Structured presentation (tool walkthrough, step-by-step demo) | Light — has natural logic skeleton | Tighten language, remove filler, preserve structure |
| Q&A / open discussion (opinions, philosophy, audience questions) | Heavy — oral, scattered, repetitive | Extract core argument first, then write from the argument, not from the transcript |
| Anecdotes / personal stories | Medium — vivid but rambling | Keep emotional texture, cut circular narration |

**Q&A and discussion sections are the #1 source of quality decay.** They sound coherent when spoken but read terribly when transcribed. For these sections:

1. **Don't write from the transcript directly.** First distill the speaker's argument into 2-3 bullet points.
2. **Then write the section from those bullets**, pulling in specific quotes only for texture.
3. **Grep-verify** every claim — don't trust your memory of what was said.

**Oral residue self-check:** After writing a section, scan for filler words: "就是/然后/其实/可能/的话/对吧". If a single paragraph contains 3+ of these, the passage hasn't been sufficiently rewritten — it's still transcript, not article. Rewrite it.

#### Phase 3: Polish

- Apply user's style corrections across the full article
- Global find-and-replace for naming conventions (e.g. real name -> nickname)
- Remove meta-commentary fluff (see Content Principles below)
- **Terminology normalization:** Replace jargon abbreviations with full terms (e.g. RD→研发, PM→产品经理). Align repeated terms to one consistent form throughout (e.g. if both "Web Coding" and "Vibe Coding" appear, pick the industry-standard term and use it everywhere)
- **ASR homophone sweep (MANDATORY for transcripts):** Beyond proper nouns, scan for common ASR mishearings — homophones (市值→价值, 支出→直出), word-boundary errors (可以呀用→可以用), and phonetic transliterations of English terms (e.g. "Figma妹"→"Figma Make"). Read suspicious words in context and Grep-verify against nearby sentences
- **De-date:** Prefer relative time references (周三, 上周, 之前) over specific calendar dates (2026年3月11日) unless the date itself is newsworthy. Specific dates age the article and add no value

#### Phase 4: Pre-delivery QA (MANDATORY before sending to user)

在发出任何版本之前，必须自己通读一遍全文，检查以下四项：

1. **事实核查**：每一个具体的归因（"张奕麟说"、"Kenny分析"）是否和源文档对得上？有没有把某人的话错误地归到另一个人？
2. **重复内容**：同一个故事/案例/观点有没有在多个章节重复出现？（常见：产品演进故事 → 方法论章节 → 行业洞察章节，三处都在讲同一个案例）
3. **ASR 残留**：有没有语义不通的句子？把每段引号内的话读一遍，看是否像一个真实的人说的话
4. **无来源内容**：有没有大模型自行补充的背景知识（公司融资数据、行业统计、产品参数）被写进了正文？有则移至附录并标注"来源非对话"

通读后再进行版本归档。

#### Version Management (MANDATORY)

**每一轮修改完成后**，把当前状态存为带版本号的文件。版本号标在文件名里，用户拿到任何文件都能从名字判断版本。

**Rules:**
- Initial draft from subagents = `_v1.md`
- After each round of corrections: increment version → `_v2.md`, `_v3.md`, etc.
- The no-suffix file is a **working draft only** — never send it to the user; always send a versioned file
- The highest version number = the latest version

**Naming convention:**
```
{basename}_v{N}.md
```
Example: `张奕麟_Kuse深度访谈_20260321_v1.md` → `_v2.md` → `_v5.md`

**When to create a new version (AFTER edits complete):**
- After user's correction round is fully applied
- After any global find-and-replace or restructuring
- Before sending a file to the user — always send a versioned copy

**Implementation:** After finishing a round of edits, save with the next version number:
```bash
cp outputs/article.md outputs/article_v2.md
```
Send `article_v2.md` to the user, continue editing `article.md` for next round.

### Heading Structure Logic

**First-level headings (##) = Major narrative arcs, limit to 4-6 max.**

If your outline has 8-10 major topics, you have too many first-level headings. Consolidate:

| Raw topics | -> | Structured headings |
|---|---|---|
| 8-10 topics at same level | -> | 4-5 first-level (##) with 2-3 second-level (###) each |

**Decision rules:**

- **Use ## (first-level)** for distinct phases of the narrative — e.g. "Why change", "How to change", "What happened after"
- **Use ### (second-level)** for specific topics within a phase — e.g. under "How to change": tool choice, workflow steps, design system tips
- **Intro and conclusion** are ## level but typically have NO sub-headings
- **Middle sections** (the meaty parts) should have 2-3 ### sub-headings each
- **If a section has only 1 sub-heading**, it doesn't need sub-headings — just write it as a single section

**Heading format:** ## headings use descriptive phrases only (NO Chinese numbering like 一、二、三). ### headings use Arabic numbering (1. 2. 3.), restarting within each ## section.

**Example structure:**
```
## 开篇 (no sub-headings)
## 为什么要变 (narrative arc 1)
  ### 1. 工具进化
  ### 2. 流程痛点
  ### 3. 转折
## 怎么变 (narrative arc 2)
  ### 1. 工具选择
  ### 2. 实战工作流
  ### 3. 设计系统
## 变了之后 (narrative arc 3)
  ### 1. 协作模式
  ### 2. 审美
  ### 3. 角色未来
## 行动建议 (short, no sub-headings)
## 结语 (short, no sub-headings)
```

### Content Principles for Long-form Articles

**1. Content over meta-commentary.**

The article's value is the IDEAS, not who said them during the session. Remove:
- "在分享的问答环节，一位叫XX的产品经理提了一个问题：..."
- "我自己也在分享中补充了我的观察。"
- "分享中有一个观众问了一个很有代表性的问题"

Replace with direct content: present the question/topic directly, weave observations naturally.

**2. Consistent naming.**

- Use the speaker's preferred name/nickname throughout (not alternating real name and nickname)
- Establish the name once in the intro, then use it consistently
- Apply via `replace_all=true` if user requests a name change

**3. Narrator perspective and attribution thinning.**

- The article has a narrator (usually the host/organizer) writing in first person
- The main speaker's content is presented in third person with direct quotes
- When narrator shares their own experience, use first person naturally
- **Attribution thinning (CRITICAL):** "瑜子说/瑜子认为/她觉得" should appear at most 2-3 times per major section, NOT at every paragraph start. When the context already makes clear who is speaking, drop the attribution entirely. Bad: "瑜子认为找参考是每个设计师都可以做的事". Good: "找参考是每个设计师都可以做的事". After writing, do a sweep: if 3+ consecutive paragraphs start with speaker attribution, thin them out

**4. Direct quotes for texture.**

- Use `> "quoted text"` for the speaker's most vivid, personal statements
- These should be moments of genuine voice — emotional, funny, or deeply opinionated
- Don't quote mundane statements — only quote what adds texture
- 2-3 direct quotes per major section is a good rhythm

**5. Tool/product descriptions — compress, don't transcribe.**

- When the transcript walks through a tool or website feature-by-feature, do NOT transcribe the walkthrough. Distill to 1-2 sentences capturing the core value proposition
- Bad: "它不仅仅只是呈现一个视觉的设计方案，它其实会有很多子功能——比如你可以去按照登录流程具体是怎么做的去查看，它会有一些框图显示出来。它还有一个叫Flows的Tab..." (transcribing the demo)
- Good: "它不仅呈现设计方案，还可以按流程具体操作体验，甚至把关键动线元素圈出来分析设计思路。" (core value in one sentence)
- This applies to: tool recommendations, website intros, feature walkthroughs, skill descriptions

**6. Supplementary references.**

- If the transcript mentions websites, tools, or resources, fetch them for additional context
- Use WebFetch to get the actual content from URLs mentioned
- This enriches the article with details the speaker may have glossed over verbally

---

## Style Profile Management

Style profiles are saved in `style-profiles/` (relative to this skill's directory) and persist across sessions.

### Saving a Style Profile

When user provides reference content (or says "保存风格" / "save my style"):

1. Analyze the reference content using the style extraction dimensions from Step 1
2. Save TWO files:

**File 1: `style-profiles/default.md`** — Style analysis summary

```markdown
# Style Profile: [Name]

Saved: [date]
Source: [brief description of reference content, e.g. "3 Jike posts about tech/AI"]

## Information Density
[data-heavy / case-heavy / opinion-heavy — with specifics]

## Language Style
[formal / casual / sharp / moderate — with vocabulary examples from the original posts]

## Structure
- Bold subheadings: [yes/no, frequency]
- Numbered lists: [yes/no, when used]
- Paragraph length: [1-2 lines / 3-4 lines / longer]
- Opening style: [direct statement / data / story / question]
- Emojis/formatting: [usage pattern]

## Attitude & Tone
[explicit judgment / restrained / humorous / analytical — with examples]

## Platform
[Jike / Twitter / LinkedIn / WeChat / blog — conventions observed]

## Key Patterns
[2-5 specific patterns unique to this user's writing, e.g. "ends posts with a provocative question", "uses 「」for emphasis instead of bold", "inserts English terms naturally in Chinese text"]
```

**File 2: `style-profiles/default-samples.md`** — 2-3 complete original posts

```markdown
# Style Samples

These are the user's actual published posts. Read them every time to internalize the voice, rhythm, and word choices — not just the rules.

---

## Sample 1

[Full text of the post, unmodified]

---

## Sample 2

[Full text of the post, unmodified]

---

## Sample 3 (optional)

[Full text of the post, unmodified]
```

**Why both files?** The summary captures rules (paragraph length, structure, tone). But rules alone produce mechanical imitation. The samples provide the actual voice — sentence rhythm, word choices, how transitions land, specific humor or sharpness. Read both every time.

3. Confirm to user: "风格档案已保存（分析总结 + 原文范例）。以后每次运行会自动加载，不用再提供参考了。"

### Updating a Profile

User says "更新风格" / "update my style" + provides new reference content → overwrite both `default.md` and `default-samples.md`.

### Multiple Profiles

User can maintain multiple profiles:
- "保存为 formal 风格" → saves to `style-profiles/formal.md` + `formal-samples.md`
- "用 formal 风格" → loads `style-profiles/formal.md` + `formal-samples.md` instead of default
- "切换风格" / "switch style" → list available profiles and let user choose

### Deleting a Profile

User says "删除风格" / "reset my style" → delete the profile file, revert to asking for references.

---

## Common Adjustments

If user says:
- "Too long" -> Condense to target length
- "Can't understand this" -> Add simple background context
- "Wrong style/tone" -> Adjust to match their preference
- "Want more" -> Extract additional angles from transcript
- "Not enough short insights" -> Find more (but maintain quality standards)

## Key Principles

1. **Always batch output** - Write all qualified content upfront, don't ask which to write first
2. **Quality > quantity** - Don't force output if material is weak
3. **Clean output only** - No meta-information in final output
4. **Fact check everything** - Verify names, data, and facts before outputting (transcripts have errors)
5. **Match user's style** - Learn from reference content if provided
6. **Strict insight filtering** - Quality standard is fixed, quantity is natural result (see [golden-sentence-standards.md](references/golden-sentence-standards.md))
7. **Delete until impossible** - Every sentence must advance the logic
8. **No teaching tone** - Provide frameworks, don't preach
9. **No anxiety farming** - Provide insights, don't manufacture panic
10. **Have attitude** - Make clear judgments, don't hedge excessively

## Reference Files

| Topic | File |
|---|---|
| Insight quality standards | [references/golden-sentence-standards.md](references/golden-sentence-standards.md) |
| Writing checklist | [references/writing-checklist.md](references/writing-checklist.md) |
| Long transcript processing | [references/long-transcript-strategy.md](references/long-transcript-strategy.md) |
| Proper noun verification | [references/proper-noun-verification.md](references/proper-noun-verification.md) |
| Technical troubleshooting | [references/troubleshooting.md](references/troubleshooting.md) |
| Style profiles (persistent) | [style-profiles/](style-profiles/) |
