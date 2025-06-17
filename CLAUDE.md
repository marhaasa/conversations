# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Purpose

This repository contains a conversation extraction system for processing Claude chat exports. It converts JSON conversation data from Claude into organized markdown files suitable for personal note-taking systems.

## Development Commands

**Extract conversations from JSON export:**
```bash
python3 extract_conversations.py
```

**Re-process with new data:**
1. Replace files in `Claude Data Jun 17 2025/` directory with new export
2. Run extraction script
3. Review filtered conversations output

## Architecture Overview

### Data Processing Pipeline

The extraction system follows a three-stage pipeline:

1. **Input Processing**: Reads Claude JSON export from `Claude Data Jun 17 2025/conversations.json`
2. **Content Filtering**: Automatically filters out empty/meaningless conversations using `should_filter_conversation()`
3. **Markdown Generation**: Converts each valid conversation to individual markdown files with metadata

### Key Components

**Filtering Logic (`should_filter_conversation`):**
- Filters conversations with 0 characters of content
- Removes conversations with human messages but no assistant responses
- Excludes conversations with no messages
- Reports filtering statistics and reasons

**Content Extraction (`extract_message_content`):**
- Prioritizes `content[0].text` over direct `text` field (more reliable)
- Handles file attachments and extracted content
- Gracefully handles malformed message structures

**Filename Generation:**
- Format: `YYYY-MM-DD_sanitized-title.md`
- Sanitizes conversation titles for filesystem compatibility
- Limits filename length to 50 characters
- Falls back to "untitled" for empty names

### Output Structure

Generated markdown files include:
- Conversation title as H1 header
- Metadata (creation date, update date, message count)
- Alternating "## Human" and "## Assistant" sections
- Chronological message ordering

### Git Workflow

The `conversations/` directory containing extracted markdown files is tracked in git, but the raw JSON export data in `Claude Data Jun 17 2025/` is excluded from version control to avoid committing large conversation datasets.

## Data Format Notes

**Input JSON Structure:**
- Array of conversation objects with `uuid`, `name`, `created_at`, `chat_messages`
- Messages contain `sender`, `text`, and `content` arrays
- Content may include attachments with `extracted_content`

**Filtering Results:**
- Typical filter rate: ~9-10% of conversations (empty/incomplete)
- Remaining conversations contain meaningful human-assistant exchanges