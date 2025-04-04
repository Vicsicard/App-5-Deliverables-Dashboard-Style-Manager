from pathlib import Path
from typing import Dict

def finalize_and_write(content: str, output_path: str, status: str, approvals: Dict[str, bool]) -> None:
    """
    Write revised content to disk only if approved.
    
    Args:
        content: The revised markdown content to write
        output_path: Path to write the content to
        status: Current revision status ("approved", "pending", "rejected")
        approvals: Dictionary of approval flags, e.g. {"style": True, "content": True}
        
    Raises:
        ValueError: If status or approvals are invalid
        OSError: If file writing fails
    """
    # Check status
    if status != "approved":
        print("[OUTPUT] ❌ Content not approved. Skipping write.")
        return
    
    # Check approvals
    if not all(approvals.values()):
        print("[OUTPUT] ❌ Rejected by client. Skipping write.")
        return
    
    # Convert to Path object
    output_file = Path(output_path)
    
    # Verify parent directory exists (don't create it)
    if not output_file.parent.exists():
        raise OSError(f"Directory does not exist: {output_file.parent}")
    
    try:
        # Write content with UTF-8 encoding
        output_file.write_text(content, encoding='utf-8')
        print(f"[OUTPUT] ✅ File saved to: {output_path}")
    except OSError as e:
        raise OSError(f"Failed to write to {output_path}: {str(e)}")
