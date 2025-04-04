from pathlib import Path
import re
from revision_engine import apply_revision_guidelines

def verify_markdown_validity(content: str) -> bool:
    """
    Verify that the content follows markdown rules:
    1. Headers start with #
    2. Paragraphs are separated by blank lines
    3. No malformed markdown syntax
    """
    lines = content.split('\n')
    for i, line in enumerate(lines):
        # Check header format
        if line.strip().startswith('#'):
            if not re.match(r'^#{1,6}\s+\w+', line):
                print(f"Invalid header format at line {i+1}: {line}")
                return False
        
        # Check HTML comments format
        if '<!--' in line:
            if not re.match(r'<!--\s+MISALIGNMENT:\s+\w+\s+-\s+.*\s+-->', line):
                print(f"Invalid comment format at line {i+1}: {line}")
                return False
    
    return True

def verify_content_preserved(original: str, annotated: str) -> bool:
    """
    Verify that all original content is preserved:
    1. All original lines exist in annotated version
    2. Order is maintained
    3. Only HTML comments are added
    """
    # Remove HTML comments from annotated version
    clean_annotated = re.sub(r'<!--.*?-->\n?', '', annotated)
    
    # Remove empty lines and whitespace for comparison
    orig_lines = [l.strip() for l in original.split('\n') if l.strip()]
    annot_lines = [l.strip() for l in clean_annotated.split('\n') if l.strip()]
    
    # Check if all original lines exist in order
    orig_idx = 0
    for line in annot_lines:
        if orig_idx >= len(orig_lines):
            break
        if line == orig_lines[orig_idx]:
            orig_idx += 1
    
    return orig_idx == len(orig_lines)

def test_revision_guidelines():
    """Test the apply_revision_guidelines function"""
    
    # Sample style profile
    style_profile = {
        "voice": ["storytelling", "conversational"],
        "themes": ["innovation", "technology"],
        "values": ["authenticity", "creativity"],
        "emotional_tone": ["inspiring", "optimistic"],
        "relatability": ["personal experience", "shared journey"]
    }
    
    # Sample content with various style elements
    content = """# The Future of AI Development

In my journey exploring AI technology, I've discovered something incredible.
This storytelling approach helps convey complex ideas simply.

## Innovation in Practice

The authentic way we approach creativity in AI development
leads to inspiring breakthroughs. Our shared journey in
technology continues to evolve.

## Technical Details

The system architecture consists of multiple components
that work together efficiently."""

    # Apply revision guidelines
    annotated = apply_revision_guidelines(content, style_profile)
    
    print("\nAnnotated Content:")
    print("=" * 50)
    print(annotated)
    
    # Verify output rules
    print("\nOutput Validation:")
    print("=" * 50)
    
    # 1. Verify markdown validity
    is_valid_md = verify_markdown_validity(annotated)
    print(f"Valid markdown format: {'[OK]' if is_valid_md else '[FAIL]'}")
    
    # 2. Verify content preservation
    is_preserved = verify_content_preserved(content, annotated)
    print(f"Original content preserved: {'[OK]' if is_preserved else '[FAIL]'}")
    
    # 3. Verify only HTML comments added
    comments = re.findall(r'<!--.*?-->', annotated, re.DOTALL)
    all_valid = all('MISALIGNMENT:' in c for c in comments)
    print(f"Only valid comments added: {'[OK]' if all_valid else '[FAIL]'}")
    
    # 4. Verify comment format
    comment_format = re.compile(r'<!--\s+MISALIGNMENT:\s+\w+\s+-\s+[^>]+\s+-->')
    all_formatted = all(bool(comment_format.match(c)) for c in comments)
    print(f"Comment format correct: {'[OK]' if all_formatted else '[FAIL]'}")
    
    # Additional stats
    print(f"\nTotal comments: {len(comments)}")
    print("Comment types:")
    for c in sorted(set(re.findall(r'MISALIGNMENT:\s+(\w+)', annotated))):
        print(f"- {c}")

if __name__ == "__main__":
    test_revision_guidelines()
