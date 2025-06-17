#!/usr/bin/env python3
"""
Extract Claude conversations from JSON export to individual markdown files.
"""

import json
import os
import re
from datetime import datetime
from pathlib import Path


def sanitize_filename(name, max_length=50):
    """Convert conversation name to safe filename."""
    # Remove/replace problematic characters
    sanitized = re.sub(r'[<>:"/\\|?*]', '_', name)
    sanitized = re.sub(r'\s+', '_', sanitized)
    sanitized = sanitized.strip('._')
    
    # Limit length
    if len(sanitized) > max_length:
        sanitized = sanitized[:max_length].rstrip('_')
    
    return sanitized or "untitled"


def format_timestamp(timestamp_str):
    """Format ISO timestamp to readable date."""
    try:
        dt = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
        return dt.strftime('%Y-%m-%d %H:%M')
    except:
        return timestamp_str


def extract_message_content(message):
    """Extract text content from message, handling various formats."""
    # Try content array first (more reliable)
    if message.get('content') and len(message['content']) > 0:
        content_item = message['content'][0]
        if content_item.get('text'):
            return content_item['text']
    
    # Fallback to direct text field
    if message.get('text'):
        return message['text']
    
    # Handle attachments if no text content
    attachments = message.get('attachments', [])
    if attachments:
        attachment_text = []
        for att in attachments:
            if att.get('extracted_content'):
                attachment_text.append(f"[Attachment: {att.get('file_name', 'file')}]")
                attachment_text.append(att['extracted_content'])
        if attachment_text:
            return '\n\n'.join(attachment_text)
    
    return "[No content]"


def should_filter_conversation(conv):
    """
    Determines if a conversation should be filtered out based on content quality.
    
    Returns: (bool, str) - (should_filter, reason)
    """
    name = conv.get('name', '')
    messages = conv.get('chat_messages', [])
    message_count = len(messages)
    
    # Count total characters and message types
    total_chars = 0
    human_messages = 0
    assistant_messages = 0
    
    for msg in messages:
        sender = msg.get('sender', '')
        if sender == 'human':
            human_messages += 1
        elif sender == 'assistant':
            assistant_messages += 1
        
        # Count characters from text field
        text_content = msg.get('text', '')
        if text_content and text_content.strip():
            total_chars += len(text_content.strip())
        
        # Count characters from content array
        if 'content' in msg and isinstance(msg['content'], list):
            for content_item in msg['content']:
                if isinstance(content_item, dict) and 'text' in content_item:
                    content_text = content_item.get('text', '')
                    if content_text and content_text.strip():
                        total_chars += len(content_text.strip())
    
    # Filtering rules
    if total_chars == 0:
        return True, "Empty conversation (0 characters)"
    
    if human_messages > 0 and assistant_messages == 0:
        return True, "No assistant response"
    
    if message_count == 0:
        return True, "No messages"
    
    return False, ""


def process_conversation(conv, output_dir):
    """Convert single conversation to markdown file."""
    # Get conversation metadata
    title = conv.get('name', 'Untitled Conversation')
    created_at = conv.get('created_at', '')
    updated_at = conv.get('updated_at', '')
    messages = conv.get('chat_messages', [])
    
    # Create filename
    date_str = ''
    if created_at:
        try:
            dt = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
            date_str = dt.strftime('%Y-%m-%d_')
        except:
            pass
    
    filename = f"{date_str}{sanitize_filename(title)}.md"
    filepath = output_dir / filename
    
    # Build markdown content
    content = []
    content.append(f"# {title}")
    content.append("")
    
    # Metadata section
    if created_at:
        content.append(f"**Created:** {format_timestamp(created_at)}")
    if updated_at and updated_at != created_at:
        content.append(f"**Updated:** {format_timestamp(updated_at)}")
    content.append(f"**Messages:** {len(messages)}")
    content.append("")
    content.append("---")
    content.append("")
    
    # Process messages
    for i, message in enumerate(messages):
        sender = message.get('sender', 'unknown')
        message_content = extract_message_content(message)
        
        # Add sender header
        if sender == 'human':
            content.append("## Human")
        elif sender == 'assistant':
            content.append("## Assistant")
        else:
            content.append(f"## {sender.title()}")
        
        content.append("")
        content.append(message_content)
        content.append("")
    
    # Write file
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('\n'.join(content))
    
    return filepath


def main():
    """Main extraction process."""
    # Input file
    data_dir = Path("Claude Data Jun 17 2025")
    conversations_file = data_dir / "conversations.json"
    
    if not conversations_file.exists():
        print(f"Error: {conversations_file} not found")
        return
    
    # Output directory
    output_dir = Path("conversations")
    output_dir.mkdir(exist_ok=True)
    
    print(f"Loading conversations from {conversations_file}...")
    
    # Load and parse JSON
    with open(conversations_file, 'r', encoding='utf-8') as f:
        conversations = json.load(f)
    
    print(f"Found {len(conversations)} conversations")
    
    # Filter conversations
    filtered_conversations = []
    filtered_count = 0
    for i, conv in enumerate(conversations, 1):
        should_filter, reason = should_filter_conversation(conv)
        if should_filter:
            conv_name = conv.get('name', f'conversation-{i}')
            print(f"  FILTERED {i:2d}/{len(conversations)}: '{conv_name}' - {reason}")
            filtered_count += 1
        else:
            filtered_conversations.append(conv)
    
    print(f"Filtered out {filtered_count} conversations")
    print(f"Processing {len(filtered_conversations)} meaningful conversations...")
    print(f"Extracting to {output_dir}/")
    
    # Process each valid conversation
    success_count = 0
    for i, conv in enumerate(filtered_conversations, 1):
        try:
            filepath = process_conversation(conv, output_dir)
            print(f"  {i:2d}/{len(filtered_conversations)}: {filepath.name}")
            success_count += 1
        except Exception as e:
            conv_name = conv.get('name', f'conversation-{i}')
            print(f"  ERROR processing '{conv_name}': {e}")
    
    print(f"\nCompleted: {success_count}/{len(filtered_conversations)} conversations extracted")
    print(f"Total filtered: {filtered_count}/{len(conversations)} ({filtered_count/len(conversations)*100:.1f}%)")


if __name__ == "__main__":
    main()