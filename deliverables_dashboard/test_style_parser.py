import pytest
from style_parser import StyleProfileParser

def test_style_profile_parser():
    """Test style profile parsing functionality"""
    
    parser = StyleProfileParser()
    
    # Test content with all sections
    content = """# Voice
- Professional but approachable
- Clear and concise
Speaker 1: "Keep it friendly but authoritative"

# Themes
- Technology impact
- Future of work
* Innovation mindset

# Values
- Integrity
- Excellence
- Innovation

# Emotional Tone
- Optimistic
- Inspiring
- Confident
Speaker 1: "We want to energize readers"

# Relatability
- Industry examples
- Real-world applications
- Practical insights
"""

    # Test successful parsing
    signals = parser.parse_style_profile(content)
    
    # Verify all sections present
    assert all(key in signals for key in [
        "voice", "themes", "values", 
        "emotional_tone", "relatability"
    ])
    
    # Verify bullet points parsed
    assert "Professional but approachable" in signals["voice"]
    assert "Technology impact" in signals["themes"]
    assert "Innovation" in signals["values"]
    
    # Verify speaker quotes parsed
    assert "Keep it friendly but authoritative" in signals["voice"]
    assert "We want to energize readers" in signals["emotional_tone"]
    
    # Test UTF-8 content
    utf8_content = content.encode('utf-8')
    signals = parser.parse_style_profile(utf8_content)
    assert signals["voice"] == [
        "Professional but approachable",
        "Clear and concise",
        "Keep it friendly but authoritative"
    ]
    
    # Test missing sections
    incomplete = """# Voice
- Clear voice
"""
    with pytest.raises(ValueError) as exc:
        parser.parse_style_profile(incomplete)
    assert "Missing content in sections" in str(exc.value)
    
    # Test malformed content
    malformed = "No sections here"
    with pytest.raises(ValueError) as exc:
        parser.parse_style_profile(malformed)
    assert "Missing content in sections" in str(exc.value)

if __name__ == "__main__":
    pytest.main([__file__])
