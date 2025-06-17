# Claude Conversations Extractor

A Python tool to convert Claude chat exports into organized markdown files for personal note-taking.

## Overview

This tool processes JSON conversation exports from Claude and converts them into individual markdown files, automatically filtering out empty conversations and organizing content with metadata.

## Usage

1. **Export your conversations** from Claude and place the JSON files in the `Claude Data Jun 17 2025/` directory

2. **Run the extraction script:**
   ```bash
   python3 extract_conversations.py
   ```

3. **Find your conversations** in the `conversations/` directory as markdown files named by date and title

## Features

- **Automatic filtering** - Removes empty conversations and incomplete exchanges
- **Organized output** - Files named with date prefix for chronological sorting
- **Rich metadata** - Each file includes creation date, message count, and conversation timeline
- **Content preservation** - Handles attachments and various message formats
- **Progress reporting** - Shows filtering statistics and processing status

## Output Format

Generated markdown files include:
- Conversation title as main header
- Metadata section with dates and message count
- Alternating "Human" and "Assistant" sections
- Clean, readable formatting suitable for note-taking apps

## Example

```
conversations/
├── 2024-11-05_Comparing_Data_Across_Tables.md
├── 2025-05-23_Feedback_on_Microsoft_Fabric_CLI_TUI_Application.md
└── 2025-06-17_Italian_Dinner_Party_Drinks.md
```

## Requirements

- Python 3.6+
- No external dependencies (uses only standard library)