from pathlib import Path
import json
from typing import Dict

def load_markdown_files(directory: str) -> Dict[str, str]:
    """
    Load all .md files from the specified directory and return a dict:
    {filename (no path): content (string)}
    """
    markdown_files = {}
    try:
        dir_path = Path(directory)
        if not dir_path.exists():
            return markdown_files

        for file_path in dir_path.glob("*.md"):
            try:
                content = file_path.read_text(encoding='utf-8')
                markdown_files[file_path.name] = content
            except UnicodeDecodeError:
                # Try with a different encoding if UTF-8 fails
                try:
                    content = file_path.read_text(encoding='utf-8-sig')
                    markdown_files[file_path.name] = content
                except Exception:
                    continue
            except Exception:
                continue

        return markdown_files
    except Exception:
        return markdown_files

def load_json_file(path: str) -> Dict:
    """
    Load and return a JSON file from a given path.
    """
    try:
        file_path = Path(path)
        if not file_path.exists():
            return {}

        content = file_path.read_text(encoding='utf-8')
        return json.loads(content)
    except json.JSONDecodeError:
        return {}
    except Exception:
        return {}

def save_json_file(path: str, data: Dict) -> None:
    """
    Save dictionary as JSON to the given path.
    """
    try:
        file_path = Path(path)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        file_path.write_text(json.dumps(data, indent=4), encoding='utf-8')
    except Exception:
        pass
