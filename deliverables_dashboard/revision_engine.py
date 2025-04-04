from dataclasses import dataclass
from typing import Dict, List
import re

@dataclass
class StyleProfile:
    """Style guidelines for content revision"""
    voice: List[str]
    themes: List[str]
    values: List[str]
    emotional_tone: List[str]
    relatability: List[str]

@dataclass
class ContentSection:
    """A section of content to be analyzed"""
    content: str
    header: str = ""

@dataclass
class RevisionRequest:
    """Request for content revision"""
    content: str
    style_profile: StyleProfile

def apply_revision_guidelines(content: str, style_profile: Dict[str, List[str]]) -> str:
    """
    Apply style guidelines to content and return annotated markdown.
    No file I/O, rendering, or LLM integration.
    
    Args:
        content: Raw markdown draft content
        style_profile: Dictionary of style dimensions and their traits
        
    Returns:
        Annotated markdown with HTML comments for style misalignments
    """
    # Split content into sections (preserve headers and paragraphs)
    sections = re.split(r'(^#{1,3}\s+.*$)', content, flags=re.MULTILINE)
    sections = [s.strip() for s in sections if s.strip()]
    
    # Process each section
    annotated_sections = []
    
    for section in sections:
        if section.startswith('#'):
            # Preserve headers as-is
            annotated_sections.append(section)
            continue
        
        # Initialize misalignments list
        misalignments = []
        
        # Check voice alignment
        voice_matches = False
        for voice in style_profile.get('voice', []):
            if voice.lower() in section.lower():
                voice_matches = True
                break
        if not voice_matches and style_profile.get('voice'):
            misalignments.append("Voice - review tone and style")
        
        # Check theme alignment
        theme_matches = False
        for theme in style_profile.get('themes', []):
            if theme.lower() in section.lower():
                theme_matches = True
                break
        if not theme_matches and style_profile.get('themes'):
            misalignments.append("Theme - align with core topics")
        
        # Check values alignment
        value_matches = False
        for value in style_profile.get('values', []):
            if value.lower() in section.lower():
                value_matches = True
                break
        if not value_matches and style_profile.get('values'):
            misalignments.append("Values - incorporate key principles")
        
        # Check emotional tone
        tone_matches = False
        for tone in style_profile.get('emotional_tone', []):
            if tone.lower() in section.lower():
                tone_matches = True
                break
        if not tone_matches and style_profile.get('emotional_tone'):
            misalignments.append("Tone - adjust emotional resonance")
        
        # Check relatability
        rel_matches = False
        for rel in style_profile.get('relatability', []):
            if rel.lower() in section.lower():
                rel_matches = True
                break
        if not rel_matches and style_profile.get('relatability'):
            misalignments.append("Relatability - add personal connection")
        
        # Add misalignment comments if any found
        if misalignments:
            comments = '\n'.join(f"<!-- MISALIGNMENT: {note} -->" 
                               for note in misalignments)
            annotated_sections.append(f"{comments}\n{section}")
        else:
            # No misalignments - keep section as-is
            annotated_sections.append(section)
    
    # Return annotated markdown string (no file I/O)
    return '\n\n'.join(annotated_sections)
