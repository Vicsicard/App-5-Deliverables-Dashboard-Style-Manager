import json
from pathlib import Path
import pytest
from handoff_writer import prepare_handoff, write_handoff_manifest, finalize_handoff

def test_handoff_writer(tmp_path):
    """Test the handoff writer functionality"""
    
    # Create test content files
    files = [
        ("blog_post.md", """# Blog Post
<!-- MISALIGNMENT: Voice - too formal -->
Content here
<!-- MISALIGNMENT: Values - missing key point -->
More content"""),
        
        ("social_kit.md", """# Social Media Kit
<!-- MISALIGNMENT: Tone - too casual -->
Content for social
<!-- MISALIGNMENT: Theme - off message -->
<!-- MISALIGNMENT: Voice - inconsistent -->
More social content""")
    ]
    
    source_dir = tmp_path / "source"
    source_dir.mkdir()
    
    source_files = []
    for filename, content in files:
        file_path = source_dir / filename
        file_path.write_text(content)
        source_files.append(str(file_path))
    
    # Create output directory
    output_dir = tmp_path / "output"
    output_dir.mkdir()
    
    # Test case 1: Successful handoff preparation
    metadata = prepare_handoff(
        source_files,
        project_id="TEST-001",
        user_id="user123",
        output_dir=str(output_dir)
    )
    
    # Verify metadata
    assert metadata is not None
    assert metadata.project_id == "TEST-001"
    assert metadata.user_id == "user123"
    assert len(metadata.filenames) == 2
    assert metadata.revision_notes["blog_post.md"] == 2
    assert metadata.revision_notes["social_kit.md"] == 3
    
    # Test case 2: Write manifest
    manifest_path = write_handoff_manifest(metadata, str(output_dir))
    manifest_file = Path(manifest_path)
    
    # Verify manifest exists
    assert manifest_file.exists()
    
    # Verify manifest content
    manifest = json.loads(manifest_file.read_text())
    assert manifest["project_id"] == "TEST-001"
    assert manifest["user_id"] == "user123"
    assert len(manifest["files"]) == 2
    assert manifest["revision_notes"]["blog_post.md"] == 2
    
    # Test case 3: Full handoff process
    finalize_handoff(
        source_files,
        project_id="TEST-002",
        user_id="user456",
        output_dir=str(output_dir)
    )
    
    # Verify output structure
    output_path = output_dir / "app5"
    assert output_path.exists()
    assert (output_path / "blog_post.md").exists()
    assert (output_path / "social_kit.md").exists()
    assert (output_path / "handoff_manifest_app5.json").exists()
    
    # Test case 4: Missing file
    with pytest.raises(FileNotFoundError):
        finalize_handoff(
            ["nonexistent.md"],
            project_id="TEST-003",
            user_id="user789",
            output_dir=str(output_dir)
        )
    
    # Test case 5: Non-markdown file
    txt_file = source_dir / "test.txt"
    txt_file.write_text("Not markdown")
    with pytest.raises(ValueError):
        finalize_handoff(
            [str(txt_file)],
            project_id="TEST-004",
            user_id="user101",
            output_dir=str(output_dir)
        )

if __name__ == "__main__":
    pytest.main([__file__])
