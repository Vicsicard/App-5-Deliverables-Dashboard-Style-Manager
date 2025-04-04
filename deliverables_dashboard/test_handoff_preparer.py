import json
from pathlib import Path
import pytest
from handoff_preparer import prepare_handoff, write_handoff_package, prepare_app6_handoff

def test_handoff_preparation(tmp_path):
    """Test the handoff preparation process"""
    
    # Create test content file
    content = """# Test Content
    
This is approved content ready for handoff.
"""
    content_file = tmp_path / "test_content.md"
    content_file.write_text(content)
    
    # Test case 1: Successful handoff preparation
    approvals = {"style": True, "content": True}
    metadata = prepare_handoff(
        content_path=str(content_file),
        content_id="TEST-001",
        approvals=approvals,
        style_profile="default_style",
        revision_count=3
    )
    
    # Verify metadata
    assert metadata is not None
    assert metadata.content_id == "TEST-001"
    assert metadata.status == "approved"
    assert metadata.approvals == approvals
    assert metadata.style_profile_used == "default_style"
    assert metadata.revision_count == 3
    
    # Test case 2: Missing approvals
    bad_approvals = {"style": True, "content": False}
    metadata = prepare_handoff(
        content_path=str(content_file),
        content_id="TEST-002",
        approvals=bad_approvals,
        style_profile="default_style",
        revision_count=1
    )
    
    # Verify no metadata returned
    assert metadata is None
    
    # Test case 3: Missing content file
    with pytest.raises(FileNotFoundError):
        prepare_handoff(
            content_path="nonexistent.md",
            content_id="TEST-003",
            approvals=approvals,
            style_profile="default_style",
            revision_count=1
        )

def test_handoff_package_creation(tmp_path):
    """Test the handoff package creation"""
    
    # Create test content
    content = "# Approved Content"
    content_file = tmp_path / "approved.md"
    content_file.write_text(content)
    
    # Create test output directory
    output_dir = tmp_path / "output"
    output_dir.mkdir()
    
    # Prepare metadata
    metadata = prepare_handoff(
        content_path=str(content_file),
        content_id="TEST-004",
        approvals={"style": True, "content": True},
        style_profile="default_style",
        revision_count=2
    )
    
    # Create handoff package
    package_dir = write_handoff_package(metadata, str(output_dir))
    package_path = Path(package_dir)
    
    # Verify package structure
    assert package_path.exists()
    assert (package_path / "metadata.json").exists()
    assert (package_path / "TEST-004.md").exists()
    
    # Verify metadata content
    metadata_file = package_path / "metadata.json"
    metadata_content = json.loads(metadata_file.read_text())
    assert metadata_content["content_id"] == "TEST-004"
    assert metadata_content["status"] == "approved"
    
    # Verify content file
    content_file = package_path / "TEST-004.md"
    assert content_file.read_text() == content
    
    # Test case 2: Missing output directory
    missing_dir = tmp_path / "missing"
    with pytest.raises(OSError):
        write_handoff_package(metadata, str(missing_dir))

def test_app6_handoff_preparation(tmp_path):
    """Test the App 6 handoff preparation"""
    
    # Create test files
    files = [
        ("blog_post.md", "# Blog Post\nContent here"),
        ("social_kit.md", "# Social Media Kit\nMore content")
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
    
    # Test case 1: Successful handoff
    prepare_app6_handoff(source_files, str(output_dir))
    
    # Verify handoff directory
    handoff_dir = output_dir / "for_app6"
    assert handoff_dir.exists()
    
    # Verify copied files
    for filename, content in files:
        copied_file = handoff_dir / filename
        assert copied_file.exists()
        assert copied_file.read_text() == content
    
    # Verify manifest
    manifest_file = handoff_dir / "handoff_manifest.json"
    assert manifest_file.exists()
    
    manifest = json.loads(manifest_file.read_text())
    assert manifest["status"] == "ready"
    assert len(manifest["files"]) == len(files)
    
    # Test case 2: Missing file
    bad_files = [str(source_dir / "nonexistent.md")]
    with pytest.raises(FileNotFoundError):
        prepare_app6_handoff(bad_files, str(output_dir))
    
    # Test case 3: Non-markdown file
    txt_file = source_dir / "test.txt"
    txt_file.write_text("Not markdown")
    with pytest.raises(ValueError):
        prepare_app6_handoff([str(txt_file)], str(output_dir))

if __name__ == "__main__":
    pytest.main([__file__])
