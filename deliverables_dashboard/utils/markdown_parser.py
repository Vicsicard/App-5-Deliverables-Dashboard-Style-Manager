import re
from typing import Dict, List

def extract_sections(markdown_text: str) -> Dict[str, str]:
    """
    Parses the markdown into section titles and content blocks.
    Returns a dictionary: { "Title": "Full content under that header" }
    """
    # Remove YAML frontmatter if present
    markdown_text = re.sub(r'^---\n.*?\n---\n', '', markdown_text, flags=re.DOTALL)
    
    # Remove emoji patterns
    markdown_text = re.sub(r':[a-zA-Z_]+:', '', markdown_text)
    
    # Split text into lines for processing
    lines = markdown_text.split('\n')
    sections: Dict[str, str] = {}
    current_title = None
    current_content = []
    
    for line in lines:
        # Check for header (supports both # and ## formats)
        header_match = re.match(r'^#{1,2}\s+(.+)$', line.strip())
        
        if header_match:
            # If we were building a previous section, save it
            if current_title:
                sections[current_title] = '\n'.join(current_content).strip()
            
            # Start new section
            current_title = header_match.group(1).strip()
            current_content = []
        elif current_title:
            # Add line to current section
            current_content.append(line)
    
    # Save the last section
    if current_title and current_content:
        sections[current_title] = '\n'.join(current_content).strip()
    
    return sections

def extract_speaker_quotes(markdown_text: str) -> List[str]:
    """
    Extracts all lines in blockquote format that begin with '> Speaker 1:'
    Returns a list of quotes.
    """
    # Find all blockquotes that start with Speaker 1:
    quotes = []
    
    # Split into lines and process each line
    lines = markdown_text.split('\n')
    current_quote = []
    
    for line in lines:
        # Check for speaker quote start
        if re.match(r'^>\s*Speaker 1:', line.strip()):
            # If we were building a previous quote, save it
            if current_quote:
                quotes.append('\n'.join(current_quote).strip())
            current_quote = [line.strip()]
        # Continue previous quote if it's a blockquote
        elif line.strip().startswith('>') and current_quote:
            current_quote.append(line.strip())
        # End of quote
        elif current_quote:
            quotes.append('\n'.join(current_quote).strip())
            current_quote = []
    
    # Add last quote if exists
    if current_quote:
        quotes.append('\n'.join(current_quote).strip())
    
    return quotes
