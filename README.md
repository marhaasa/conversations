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
├── 2024-11-05_Comparing_Data_Across_Tables.md
├── 2025-01-15_Python_Code_Review_and_Optimization.md
├── 2025-03-22_Setting_Up_Docker_Development_Environment.md
├── 2025-05-23_Feedback_on_Microsoft_Fabric_CLI_TUI_Application.md
└── 2025-06-17_Italian_Dinner_Party_Drinks.md
```

Each markdown file contains:
```markdown
# Python Code Review and Optimization

**Created:** 2025-01-15 14:30:22  
**Updated:** 2025-01-15 15:45:10  
**Messages:** 12

## Human

Can you help me optimize this Python function for better performance?

## Assistant

I'd be happy to help optimize your Python function! To provide the best...
```

## Requirements

- Python 3.6+
- No external dependencies (uses only standard library)