from pathlib import Path
from typing import List, Dict
import re

def _extract_title(content: str) -> str:
    """Extract the first # heading from markdown content"""
    title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    return title_match.group(1).strip() if title_match else "Untitled"

def _infer_type(filename: str) -> str:
    """Infer content type from filename"""
    filename = filename.lower()
    if 'blog' in filename:
        return 'blog'
    elif 'newsletter' in filename:
        return 'newsletter'
    elif 'notes' in filename:
        return 'notes'
    elif 'bio' in filename:
        return 'bio'
    elif 'ad' in filename:
        return 'ad_copy'
    return 'other'

def _count_words(content: str) -> int:
    """Count words in markdown content, excluding headers and metadata"""
    # Remove YAML frontmatter if present
    content = re.sub(r'^---\n.*?\n---\n', '', content, flags=re.DOTALL)
    
    # Remove markdown headers and formatting
    content = re.sub(r'^#.*$', '', content, flags=re.MULTILINE)
    content = re.sub(r'[#*_>`\[\]]', '', content)
    content = re.sub(r'\(.*?\)', '', content)  # Remove URL contents
    
    # Split and count non-empty words
    words = [word for word in content.split() if word.strip()]
    return len(words)

def scan_drafts(directory_path: str) -> List[Dict]:
    """
    Scan a directory for markdown files and extract metadata.
    
    Args:
        directory_path: Path to directory containing markdown files
        
    Returns:
        List of dictionaries containing file metadata:
        {
            "filename": str,
            "title": str,
            "type": str,
            "word_count": int,
            "has_quotes": bool
        }
    """
    drafts = []
    dir_path = Path(directory_path)
    
    if not dir_path.exists() or not dir_path.is_dir():
        return drafts
    
    # Scan only visible .md files
    for file_path in dir_path.glob("*.md"):
        # Skip hidden files
        if file_path.name.startswith('.'):
            continue
            
        try:
            # Read file content with UTF-8 encoding
            content = file_path.read_text(encoding='utf-8')
            
            # Extract metadata
            draft_info = {
                "filename": file_path.name,
                "title": _extract_title(content),
                "type": _infer_type(file_path.name),
                "word_count": _count_words(content),
                "has_quotes": bool(re.search(r'^>\s*Speaker 1:', content, re.MULTILINE))
            }
            
            drafts.append(draft_info)
            
        except UnicodeDecodeError:
            # Try alternative encoding if UTF-8 fails
            try:
                content = file_path.read_text(encoding='utf-8-sig')
                draft_info = {
                    "filename": file_path.name,
                    "title": _extract_title(content),
                    "type": _infer_type(file_path.name),
                    "word_count": _count_words(content),
                    "has_quotes": bool(re.search(r'^>\s*Speaker 1:', content, re.MULTILINE))
                }
                drafts.append(draft_info)
            except Exception:
                continue
        except Exception:
            continue
    
    return drafts
