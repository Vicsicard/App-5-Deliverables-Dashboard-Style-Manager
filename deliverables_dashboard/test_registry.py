from pathlib import Path
from file_registry import scan_drafts

def create_test_files():
    """Create sample markdown files for testing"""
    output_dir = Path(__file__).parent / "output" / "app3"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Test blog post
    blog_content = """# The Future of AI Development
    
This is a blog post about AI.
It has multiple paragraphs.

> Speaker 1: AI is transforming everything
> And this quote continues

## Key Points
- Point 1
- Point 2"""

    # Test newsletter
    newsletter_content = """# Weekly Tech Update
    
This week in tech news.
No quotes in this one.

## Headlines
1. First item
2. Second item"""

    # Test ad copy
    ad_content = """# Product Launch Ad
    
Short and impactful ad copy.
No quotes here."""

    # Write test files
    (output_dir / "output_blog.md").write_text(blog_content, encoding='utf-8')
    (output_dir / "output_newsletter.md").write_text(newsletter_content, encoding='utf-8')
    (output_dir / "output_ad.md").write_text(ad_content, encoding='utf-8')
    
    # Create a hidden file to test filtering
    (output_dir / ".temp.md").write_text("Hidden file", encoding='utf-8')

def print_registry_table(drafts, directory):
    """Print registry in table format"""
    try:
        print(f"\n[REGISTRY] 🗂️ {len(drafts)} Drafts Found in {directory}/\n")
        
        for draft in drafts:
            quotes = "✅" if draft["has_quotes"] else "❌"
            print(f"📄 {draft['filename']} — "
                  f"Type: {draft['type']} — "
                  f"{draft['word_count']} words — "
                  f"Quotes: {quotes}")
    except UnicodeEncodeError:
        # Fallback to ASCII if Unicode fails
        print(f"\n[REGISTRY] {len(drafts)} Drafts Found in {directory}/\n")
        
        for draft in drafts:
            quotes = "[YES]" if draft["has_quotes"] else "[NO]"
            print(f"* {draft['filename']} - "
                  f"Type: {draft['type']} - "
                  f"{draft['word_count']} words - "
                  f"Quotes: {quotes}")

def test_scan_drafts():
    """Test the scan_drafts function"""
    # Ensure test files exist
    create_test_files()
    
    # Scan the directory
    output_dir = Path(__file__).parent / "output" / "app3"
    drafts = scan_drafts(str(output_dir))
    
    # Print formatted table
    print_registry_table(drafts, "/output/app3")
    
    # Verify all required fields are present
    required_fields = ["filename", "title", "type", "word_count", "has_quotes"]
    for draft in drafts:
        assert all(field in draft for field in required_fields), f"Missing fields in {draft['filename']}"
        assert isinstance(draft["word_count"], int), "word_count must be an integer"
        assert isinstance(draft["has_quotes"], bool), "has_quotes must be a boolean"

if __name__ == "__main__":
    test_scan_drafts()
