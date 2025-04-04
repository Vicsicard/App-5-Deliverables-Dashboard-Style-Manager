from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import json
import re
import shutil

@dataclass
class HandoffMetadata:
    """Metadata for content handoff to App 6"""
    project_id: str
    user_id: str
    filenames: List[str]
    timestamp: str
    revision_notes: Dict[str, int]  # filename -> note count

def count_revision_notes(content: str) -> int:
    """Count revision notes (HTML comments) in content"""
    return len(re.findall(r'<!--\s*MISALIGNMENT:', content))

def prepare_handoff(
    content_files: List[str],
    project_id: str,
    user_id: str,
    output_dir: str
) -> Optional[HandoffMetadata]:
    """
    Prepare content and metadata for handoff to App 6.
    
    Args:
        content_files: List of paths to approved markdown files
        project_id: Project identifier
        user_id: User identifier
        output_dir: Base output directory
        
    Returns:
        HandoffMetadata if successful
        
    Raises:
        FileNotFoundError: If content file doesn't exist
        ValueError: If metadata is invalid
    """
    # Create output directory
    output_path = Path(output_dir) / "app5"
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Track revision notes per file
    revision_notes = {}
    copied_files = []
    
    # Process each file
    for file_path in content_files:
        source_file = Path(file_path)
        
        # Verify file exists and is markdown
        if not source_file.exists():
            raise FileNotFoundError(f"Content file not found: {file_path}")
            
        if source_file.suffix.lower() != '.md':
            raise ValueError(f"Not a markdown file: {file_path}")
            
        # Read content and count revision notes
        content = source_file.read_text(encoding='utf-8')
        note_count = count_revision_notes(content)
        
        # Copy to output directory
        target_file = output_path / source_file.name
        shutil.copy2(source_file, target_file)
        
        # Track metadata
        copied_files.append(source_file.name)
        revision_notes[source_file.name] = note_count
    
    # Create metadata
    metadata = HandoffMetadata(
        project_id=project_id,
        user_id=user_id,
        filenames=copied_files,
        timestamp=datetime.now().isoformat(),
        revision_notes=revision_notes
    )
    
    print(f"[HANDOFF] ✅ {len(copied_files)} files prepared")
    return metadata

def write_handoff_manifest(metadata: HandoffMetadata, output_dir: str) -> str:
    """
    Write handoff manifest for App 6.
    
    Args:
        metadata: HandoffMetadata for approved content
        output_dir: Directory to write manifest
        
    Returns:
        Path to created manifest file
        
    Raises:
        OSError: If directory creation or file writing fails
    """
    # Create output directory
    output_path = Path(output_dir) / "app5"
    if not output_path.exists():
        raise OSError(f"Output directory does not exist: {output_path}")
    
    try:
        # Create manifest
        manifest = {
            "project_id": metadata.project_id,
            "user_id": metadata.user_id,
            "files": metadata.filenames,
            "timestamp": metadata.timestamp,
            "revision_notes": metadata.revision_notes
        }
        
        # Write manifest
        manifest_path = output_path / "handoff_manifest_app5.json"
        manifest_path.write_text(
            json.dumps(manifest, indent=2),
            encoding='utf-8'
        )
        
        print(f"[HANDOFF] ✅ Manifest created: {manifest_path}")
        return str(manifest_path)
        
    except Exception as e:
        raise OSError(f"Failed to create manifest: {str(e)}")

def finalize_handoff(
    content_files: List[str],
    project_id: str,
    user_id: str,
    output_dir: str
) -> None:
    """
    Finalize content handoff to App 6.
    
    Args:
        content_files: List of paths to approved markdown files
        project_id: Project identifier
        user_id: User identifier
        output_dir: Base output directory
        
    Raises:
        FileNotFoundError: If content file doesn't exist
        ValueError: If metadata is invalid
        OSError: If directory creation or file writing fails
    """
    # Prepare content and get metadata
    metadata = prepare_handoff(content_files, project_id, user_id, output_dir)
    if not metadata:
        raise ValueError("Failed to prepare content for handoff")
        
    # Write manifest
    write_handoff_manifest(metadata, output_dir)
    print("[HANDOFF] ✅ Handoff completed successfully")
