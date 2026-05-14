# Technical Troubleshooting

## Reading files with special characters in filename

- If filename contains quotes ("), colons (:), or other special characters
- Use bash workaround: `cd "directory" && cat "$(ls | grep 'partial_name' | head -1)"`
- Example: File named `AI Product Strategy: Quotes"Example.md`
  - Don't use Read tool directly with full path (will fail)
  - Use: `cd "/path/to/dir/" && cat "$(ls | grep 'AI Product' | head -1)"`

## Handling large output files

- If Bash output exceeds ~100KB, it will be saved to persisted-output file
- Tool result will show: "Output too large (XXX KB). Full output saved to: /path/to/file"
- Use Read tool to read the persisted-output file path
- This commonly happens with long transcripts (>3000 lines)

## File not found errors

- If Read tool fails with "File does not exist" but Glob shows the file exists
- Likely cause: special characters in path or filename
- Solution: Use Bash with proper quoting or the ls workaround above

## Memory management for long transcripts

- Don't try to load entire 5000+ line transcript into single context
- Use index-retrieval strategy (Agent tool for indexing + Grep for spot verification)
- Process topic-by-topic rather than trying to remember everything
