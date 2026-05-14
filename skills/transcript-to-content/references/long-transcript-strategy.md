# Long Transcript Processing Strategies

Memory is lossy compression, verification must be real-time. Choose strategy by transcript length:

## Short transcripts (<1000 lines / <30 min)

- **Strategy**: Single-pass with light verification
- **Workflow**:
  - Read full transcript once (fits comfortably in context)
  - Extract all potential content points while reading
  - Write content pieces from working memory
  - Verify only critical data points (numbers, names) using Grep
- **Why**: Short content can be held in working memory with minimal loss
- **Risk**: Low fabrication risk

## Medium transcripts (1000-3000 lines / 30-90 min)

- **Strategy**: Chunked reading with targeted verification
- **Workflow**:
  - Read transcript in 2-3 logical chunks (by topic/section)
  - After each chunk, extract content points and write immediately
  - Use Grep to verify any uncertain details before finalizing each piece
  - Cross-reference between chunks if needed
- **Why**: Balance between speed and accuracy; chunks prevent memory overflow
- **Risk**: Medium - verify cross-chunk connections carefully

## Long transcripts (>3000 lines / >90 min)

- **Strategy**: Two-pass index-retrieval (MANDATORY)
- **Workflow**:
  - **Pass 1 - Build index (15-20 min):**
    - **Option A (Recommended)**: Use Agent tool with Explore subagent (subagent_type=Explore, thoroughness="medium")
      - Agent will scan full transcript and build topic structure automatically
      - Returns organized list of topics with key points and approximate line ranges
      - Faster and more comprehensive than manual scanning
    - **Option B**: Quick scan with Grep to identify all major topics/keywords
      - Grep for high-level keywords to map topic distribution
      - Create sparse index: Topic -> Keywords -> Approximate line ranges
  - **Pass 2 - Extract and verify immediately (per topic):**
    - For each topic in index:
      1. Grep search relevant keywords
      2. Read 20-50 lines of surrounding context
      3. Verify exact wording, data, logical connections
      4. Write content piece immediately
      5. Move to next topic (do NOT batch write later)
- **Why**: This is an index-retrieval problem, not full-text processing. Memory is unreliable beyond 3000 lines.
- **Risk**: High fabrication risk if you deviate from this workflow

## Verification Workflow for All Lengths

When dealing with transcripts >1000 lines, follow this rigorous verification workflow:

1. **DO NOT rely on memory** - Don't write content from impression after reading the full transcript
2. **Extract and verify immediately:**
   - Use Grep to find relevant sections BEFORE writing each content piece
   - Read surrounding context (20-50 lines) to verify accuracy
   - Confirm exact wording, data points, and logical connections
3. **Common error patterns to avoid:**
   - **Fabricating data**: Don't add numbers/metrics that "feel right" but aren't in transcript
   - **False connections**: Don't connect two unrelated sections just because they seem related
   - **Over-generalization**: Don't change specific statements to broad generalizations
   - **Misunderstanding context**: Don't create A->B logic when transcript only contains A and B separately
4. **Verification checklist for each piece:**
   - [ ] Grep searched the relevant section
   - [ ] Read 20-50 lines of context around the key points
   - [ ] All data points confirmed in original text
   - [ ] Logical connections verified (not assumed)
   - [ ] No generalizations beyond what transcript states

**Example of WRONG process:**
- Read full 5000-line transcript -> Remember key points -> Write all content from memory
- Result: Fabricated data, wrongly connected points, over-generalizations

**Example of CORRECT process:**
- Identify topic -> Grep for relevant keywords -> Read lines with context -> Verify exact wording -> Write content -> Move to next topic
