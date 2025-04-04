from utils.style_tools import load_style_signals
import json

def test_style_tools():
    # Read test file
    with open('test_style_profile.md', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Load style signals
    style_signals = load_style_signals(content)
    
    # Print results in a structured way
    print("\nStyle Profile Analysis:")
    print("=" * 50)
    print(json.dumps(style_signals, indent=2))
    
    # Verify all sections are present
    expected_sections = ["voice", "themes", "values", "emotional_tone", "relatability"]
    missing_sections = [section for section in expected_sections if not style_signals.get(section)]
    
    if missing_sections:
        print("\nWARNING: Missing sections:", ", ".join(missing_sections))
    else:
        print("\nSUCCESS: All sections present and parsed")
    
    # Print counts for each section
    print("\nCounts per section:")
    for section, items in style_signals.items():
        print(f"{section}: {len(items)} items")

if __name__ == "__main__":
    test_style_tools()
