#!/usr/bin/env python3
"""
Batch tag conversations using Claude Code SDK.
Analyzes conversation content and adds relevant tags while validating format.
"""

import os
import subprocess
import sys
import re
from pathlib import Path

class ConversationTagger:
    def __init__(self, conversations_dir="conversations"):
        self.conversations_dir = Path(conversations_dir)
        self.claude_prompt = """Analyze this conversation and suggest 2-5 relevant one word tags that describe the topic, technology, or type of discussion. 

Requirements:
- Tags must be single words only (no spaces)
- Tags must be lowercase
- Tags should be relevant and descriptive
- Examples: python, debugging, react, tutorial, planning

Open the conversation file and at the end of the file add these tags. Each tag should be on a new line surrounded by [[]] like [[tag]]. Do not remove the existing [[claude]] tag if it exists."""
        
        self.allowed_tools = "Read,Write,Edit"
    
    def get_conversation_files(self):
        """Get all markdown files in conversations directory."""
        if not self.conversations_dir.exists():
            print(f"Error: Directory {self.conversations_dir} does not exist")
            return []
        
        md_files = list(self.conversations_dir.glob("*.md"))
        print(f"Found {len(md_files)} conversation files")
        return md_files
    
    def validate_tags(self, text):
        """Validate that tags follow the required format."""
        # Find all tags in the text
        tag_pattern = r'\[\[([^\]]+)\]\]'
        tags = re.findall(tag_pattern, text)
        
        issues = []
        for tag in tags:
            if tag == "claude":  # Skip the claude tag
                continue
                
            # Check for spaces
            if ' ' in tag:
                issues.append(f"Tag '{tag}' contains spaces")
            
            # Check for uppercase
            if tag != tag.lower():
                issues.append(f"Tag '{tag}' contains uppercase letters")
            
            # Check for special characters (allow only letters, numbers, hyphens)
            if not re.match(r'^[a-z0-9-]+$', tag):
                issues.append(f"Tag '{tag}' contains invalid characters (only lowercase letters, numbers, and hyphens allowed)")
        
        return issues
    
    def check_already_tagged(self, file_path):
        """Check if conversation already has tags (excluding [[claude]])."""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find all tags
        tag_pattern = r'\[\[([^\]]+)\]\]'
        tags = re.findall(tag_pattern, content)
        
        # Filter out 'claude' tag
        non_claude_tags = [tag for tag in tags if tag != "claude"]
        
        return len(non_claude_tags) > 0, non_claude_tags
    
    def verify_content_unchanged(self, original_content, updated_content):
        """Verify that only tags were added, not conversation content changed."""
        # Remove all tags from both versions for comparison
        tag_pattern = r'\[\[([^\]]+)\]\]'
        original_no_tags = re.sub(tag_pattern, '', original_content).strip()
        updated_no_tags = re.sub(tag_pattern, '', updated_content).strip()
        
        return original_no_tags == updated_no_tags
    
    def process_file(self, file_path, force=False):
        """Process a single conversation file."""
        print(f"\nProcessing: {file_path.name}")
        
        # Check if already tagged
        already_tagged, existing_tags = self.check_already_tagged(file_path)
        if already_tagged and not force:
            print(f"  ✓ Already tagged with: {existing_tags}")
            return True
        
        try:
            # Store original content for verification
            with open(file_path, 'r', encoding='utf-8') as f:
                original_content = f.read()
            
            # Run claude command
            cmd = [
                "claude", 
                "-p", self.claude_prompt,
                f"--allowedTools={self.allowed_tools}"
            ]
            
            result = subprocess.run(
                cmd,
                input=original_content,
                text=True,
                capture_output=True,
                timeout=60
            )
            
            if result.returncode != 0:
                print(f"  ❌ Error processing file: {result.stderr}")
                return False
            
            # Read updated content and verify integrity
            with open(file_path, 'r', encoding='utf-8') as f:
                updated_content = f.read()
            
            # Verify original content wasn't altered
            if not self.verify_content_unchanged(original_content, updated_content):
                print(f"  ❌ Content verification failed - original conversation was modified!")
                # Restore original content
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(original_content)
                print(f"  🔄 Original content restored")
                return False
            
            # Validate tags in the updated file
            tag_issues = self.validate_tags(updated_content)
            if tag_issues:
                print(f"  ⚠️  Tag validation issues:")
                for issue in tag_issues:
                    print(f"    - {issue}")
            else:
                print(f"  ✓ Successfully tagged")
            
            return True
            
        except subprocess.TimeoutExpired:
            print(f"  ❌ Timeout processing file")
            return False
        except Exception as e:
            print(f"  ❌ Error: {e}")
            return False
    
    def run(self, force=False, limit=None):
        """Run the batch tagging process."""
        files = self.get_conversation_files()
        if not files:
            return
        
        if limit:
            files = files[:limit]
            print(f"Processing first {limit} files only")
        
        print(f"\nStarting batch tagging process...")
        print(f"Force retag: {force}")
        
        success_count = 0
        error_count = 0
        
        for file_path in files:
            if self.process_file(file_path, force=force):
                success_count += 1
            else:
                error_count += 1
        
        print(f"\n=== Summary ===")
        print(f"Successfully processed: {success_count}")
        print(f"Errors: {error_count}")
        print(f"Total files: {len(files)}")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Batch tag conversations using Claude")
    parser.add_argument("--conversations-dir", default="conversations", 
                       help="Directory containing conversation files")
    parser.add_argument("--force", action="store_true", 
                       help="Retag files that already have tags")
    parser.add_argument("--limit", type=int, 
                       help="Limit number of files to process (for testing)")
    
    args = parser.parse_args()
    
    tagger = ConversationTagger(args.conversations_dir)
    tagger.run(force=args.force, limit=args.limit)

if __name__ == "__main__":
    main()