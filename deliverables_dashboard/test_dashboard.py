import json
from pathlib import Path
import pytest
from dashboard import DashboardLoader

def test_dashboard_loader(tmp_path):
    """Test dashboard file loading functionality"""
    
    # Create test files and directories
    data_dir = tmp_path / "data"
    app3_dir = tmp_path / "output" / "app3"
    data_dir.mkdir()
    app3_dir.mkdir(parents=True)
    
    # Create style profile
    style_profile = """# Voice
- Professional
- Clear

# Themes
- Technology
- Innovation

# Values
- Integrity
- Excellence

# Emotional Tone
- Optimistic
- Confident

# Relatability
- Examples
- Insights
"""
    style_file = data_dir / "style-profile.md"
    style_file.write_text(style_profile)
    
    # Create draft files
    drafts = [
        ("blog.md", "# Blog Post\nContent here"),
        ("social.md", "# Social Post\nMore content")
    ]
    
    for filename, content in drafts:
        draft_file = app3_dir / filename
        draft_file.write_text(content)
    
    # Create metadata files
    chunk_metadata = {
        "chunks": ["chunk1", "chunk2"]
    }
    chunk_file = data_dir / "chunk_metadata.json"
    chunk_file.write_text(json.dumps(chunk_metadata))
    
    video_status = {
        "status": "ready"
    }
    video_file = data_dir / "video_status.json"
    video_file.write_text(json.dumps(video_status))
    
    # Test case 1: Successful loading
    loader = DashboardLoader()
    success = loader.load_input_files(
        style_profile_path=str(style_file),
        app3_output_dir=str(app3_dir),
        chunk_metadata_path=str(chunk_file),
        video_status_path=str(video_file)
    )
    
    assert success
    assert len(loader.get_draft_files()) == 2
    assert len(loader.get_style_signals()) == 5
    
    # Test case 2: Missing style profile
    bad_loader = DashboardLoader()
    success = bad_loader.load_input_files(
        style_profile_path="nonexistent.md",
        app3_output_dir=str(app3_dir)
    )
    
    assert not success
    
    # Test case 3: Invalid style profile
    invalid_style = data_dir / "invalid.txt"
    invalid_style.write_text("Not markdown")
    
    bad_loader = DashboardLoader()
    success = bad_loader.load_input_files(
        style_profile_path=str(invalid_style),
        app3_output_dir=str(app3_dir)
    )
    
    assert not success
    
    # Test case 4: Missing App 3 directory
    bad_loader = DashboardLoader()
    success = bad_loader.load_input_files(
        style_profile_path=str(style_file),
        app3_output_dir="nonexistent"
    )
    
    assert not success
    
    # Test case 5: Empty App 3 directory
    empty_dir = tmp_path / "empty"
    empty_dir.mkdir()
    
    bad_loader = DashboardLoader()
    success = bad_loader.load_input_files(
        style_profile_path=str(style_file),
        app3_output_dir=str(empty_dir)
    )
    
    assert not success

if __name__ == "__main__":
    pytest.main([__file__])
