from typing import Dict, List, Optional
import re
from utils.markdown_parser import extract_sections

class StyleProfileParser:
    """Parser for style profile markdown files"""
    
    def __init__(self):
        self.required_sections = {
            "Voice": "voice",
            "Themes": "themes", 
            "Values": "values",
            "Emotional Tone": "emotional_tone",
            "Relatability": "relatability"
        }
    
    def parse_style_profile(self, content: str, encoding: str = 'utf-8') -> Dict[str, List[str]]:
        """
        Parse style profile content into structured dictionary
        
        Args:
            content: Raw markdown content
            encoding: File encoding (default: utf-8)
            
        Returns:
            Dictionary with parsed style signals
        """
        try:
            if not isinstance(content, str):
                content = content.decode(encoding)
        except UnicodeDecodeError:
            # Fallback to latin-1 if utf-8 fails
            content = content.decode('latin-1')
            
        # Initialize with empty lists
        style_signals = {
            "voice": [],
            "themes": [],
            "values": [],
            "emotional_tone": [],
            "relatability": []
        }
        
        # Extract sections
        sections = extract_sections(content)
        
        # Parse each section
        for section_title, content in sections.items():
            key = self.required_sections.get(section_title)
            if not key:
                continue
                
            # Extract bullet points and quotes
            signals = self._extract_signals(content)
            style_signals[key] = signals
            
        # Validate all sections present
        self._validate_sections(style_signals)
        
        return style_signals
    
    def _extract_signals(self, content: str) -> List[str]:
        """Extract bullet points and speaker quotes"""
        signals = []
        
        for line in content.split('\n'):
            line = line.strip()
            
            # Skip empty lines
            if not line:
                continue
                
            # Extract bullet points
            if line.startswith(('-', '*')):
                point = line[1:].strip()
                if point:
                    signals.append(point)
                    
            # Extract speaker quotes
            elif line.startswith('Speaker 1:'):
                quote = line[len('Speaker 1:'):].strip()
                # Remove surrounding quotes if present
                quote = re.sub(r'^["\'](.*)["\']$', r'\1', quote)
                if quote:
                    signals.append(quote)
                    
        return signals
    
    def _validate_sections(self, signals: Dict[str, List[str]]) -> None:
        """Ensure all required sections have content"""
        missing = []
        for section, items in signals.items():
            if not items:
                missing.append(section)
                
        if missing:
            raise ValueError(
                f"Missing content in sections: {', '.join(missing)}"
            )
