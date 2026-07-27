# Sync Cursor Commands

You are helping me sync shared Cursor commands from my canonical commands repository into this project's `.cursor/commands` directory.

## Goal

Run the centralized sync script so this project gets the latest shared command markdown files without overwriting this command file.

## Steps

1. Resolve canonical root:
   - Use `$CURSOR_COMMANDS_HOME` if set
   - Otherwise use `/Users/jcraycraft/Documents/Projects/cursor-commands`
2. Build paths:
   - Script path: `<canonical-root>/scripts/sync-cursor-commands.sh`
   - Destination path: `<current-project>/.cursor/commands`
3. Validate script exists and is executable. If not, stop and report the missing path.
4. Run dry-run first:
   - `"<script-path>" --dry-run "<destination-path>"`
5. Show dry-run results and ask for confirmation before copying.
6. If I confirm, run apply mode:
   - `"<script-path>" --apply "<destination-path>"`
7. Report:
   - resolved source/destination
   - files copied/skipped
   - confirmation that `sync-cursor-commands.md` was not overwritten

## Output

- Sync status summary
- Commands executed
- Files copied/skipped
- Any follow-up action needed

## Important Rules

- Be concise
- Always run dry-run before apply
- Never overwrite `sync-cursor-commands.md`
- Sync only markdown command source files
- Ask if unsure
