# Claude Conversations Extractor

A Python tool to convert Claude chat exports into organized markdown files for personal note-taking.

## Overview

This tool processes JSON conversation exports from Claude and converts them into individual markdown files, automatically filtering out empty conversations and organizing content with metadata.

## Usage

### Basic Usage

1. **Export your conversations** from Claude and place the JSON files in a directory (e.g., `Claude Data/`)

2. **Run the extraction script:**
   ```bash
   python3 extract_conversations.py --data-dir "Claude Data"
   ```

3. **Find your conversations** in the `conversations/` directory as markdown files named by date and title

### Advanced Usage

**Extract from custom data directory:**
```bash
python3 extract_conversations.py --data-dir "Claude Data Dec 15 2025"
```

**Extract to custom output directory:**
```bash
python3 extract_conversations.py --output-dir "my_notes"
```

**Combine both options:**
```bash
python3 extract_conversations.py --data-dir "Claude Export" --output-dir "processed_conversations"
```

**View help:**
```bash
python3 extract_conversations.py --help
```

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

## Example Output

After processing your Claude export, you'll get organized markdown files:

```
conversations/
├── 2024-12-03_Building_REST_API_with_FastAPI.md
├── 2025-02-14_Explaining_Machine_Learning_Concepts.md
├── 2025-04-08_JavaScript_Debugging_Techniques.md
├── 2025-05-20_Career_Advice_for_Software_Engineers.md
└── 2025-06-15_Database_Schema_Design_Tips.md
```

Each markdown file contains:
```markdown
# Building REST API with FastAPI

**Created:** 2024-12-03 09:15:33  
**Updated:** 2024-12-03 10:42:18  
**Messages:** 8

## Human

What's the best way to structure a FastAPI project for a medium-sized application?

## Assistant

For a medium-sized FastAPI application, I recommend following a structured approach...
```

## Adding Semantic Tags

For semantic tagging of your extracted conversations, use the companion tool [sage](https://github.com/marhaasa/sage) - an intelligent markdown tagger that analyzes content and adds relevant tags.

## Requirements

- Python 3.6+
- No external dependencies (uses only standard library)