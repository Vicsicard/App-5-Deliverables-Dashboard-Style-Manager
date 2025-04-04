from utils.markdown_parser import extract_sections, extract_speaker_quotes

def test_parser():
    # Read test file
    with open('test_markdown.md', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Test section extraction
    print("\nTesting section extraction:")
    sections = extract_sections(content)
    for title, content in sections.items():
        print(f"\n[Section] {title}")
        print("-" * 40)
        print(content)
    
    # Test quote extraction
    print("\nTesting quote extraction:")
    quotes = extract_speaker_quotes(content)
    for quote in quotes:
        print("\n[Quote]")
        print("-" * 40)
        print(quote)

if __name__ == "__main__":
    test_parser()
