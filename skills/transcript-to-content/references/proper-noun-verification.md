# Proper Noun Verification for Transcripts

Transcripts (voice-to-text) have extremely high error rates for proper nouns due to mishearing. This step is MANDATORY before writing any content from transcript input.

## Common Error Types

- Sound-alike confusions: Plot/Plaud, Cloud/Plaud, Luki/Looki
- Homophone substitutions: characters that sound similar in Chinese
- Company/product/person name mishearing

## Workflow

### 1. Extract ALL proper nouns from transcript

- People names (founders, executives, experts mentioned)
- Company names (startups, corporations)
- Product names (apps, hardware, services)
- Use Grep to find capitalized words and potential names

### 2. Verify EACH proper noun BEFORE writing content

- Use Bash curl or web search to verify correct spelling
- For Chinese names: verify both pinyin and characters
- For products: check official website/announcement
- **Create a replacement list**: Incorrect -> Correct

### 3. Verification priority rules

- If name appears 3+ times in transcript, it's important -> MUST verify
- If you're not 100% certain of spelling -> MUST verify
- If name sounds like common word (Cloud, Plot) -> MUST verify
- Chinese names/terms -> ALWAYS verify

### 4. Apply corrections

- Use Edit tool with replace_all=true for consistent names
- Do this BEFORE writing any content pieces
- Verify the count: "Replaced 5 instances of 'Plot' with 'Plaud'"

## Example Workflow

```
1. Grep for "Plot|Luki" in transcript
2. Search "Plaud AI recorder" -> Confirm it's "Plaud"
3. Search "Looki AI camera" -> Confirm it's "Looki"
4. Search founder name -> Confirm correct characters
5. Edit transcript: Replace all "Plot" -> "Plaud"
6. Now safe to write content
```

## Why This Step is Critical

- You cannot fix errors after writing 10+ pieces of content
- Users will catch these errors immediately (damages credibility)
- Voice-to-text errors are systematic, not random
- Prevention costs 5 minutes, correction costs 30+ minutes

## Skip this step ONLY if:

- Input is written text (not transcript)
- Input has no proper nouns
