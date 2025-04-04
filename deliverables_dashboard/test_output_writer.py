import os
from pathlib import Path
import pytest
from output_writer import finalize_and_write

def test_finalize_and_write(tmp_path):
    """Test the finalize_and_write function"""
    
    # Test content
    content = """# Test Content
    
This is a test markdown file.
With multiple lines.
"""
    
    # Create test directory
    test_dir = tmp_path / "test_dir"
    test_dir.mkdir()
    output_file = test_dir / "test_output.md"
    
    # Test case 1: Successful write
    approvals = {"style": True, "content": True}
    finalize_and_write(content, str(output_file), "approved", approvals)
    
    # Verify file was written
    assert output_file.exists()
    assert output_file.read_text() == content
    
    # Test case 2: Not approved status
    if output_file.exists():
        output_file.unlink()  # Remove file if exists
    finalize_and_write(content, str(output_file), "pending", approvals)
    
    # Verify file was not written
    assert not output_file.exists()
    
    # Test case 3: Client rejection
    if output_file.exists():
        output_file.unlink()  # Remove file if exists
    bad_approvals = {"style": True, "content": False}
    finalize_and_write(content, str(output_file), "approved", bad_approvals)
    
    # Verify file was not written
    assert not output_file.exists()
    
    # Test case 4: Missing directory
    missing_dir = tmp_path / "missing" / "test.md"
    with pytest.raises(OSError) as exc:
        finalize_and_write(content, str(missing_dir), "approved", approvals)
    assert "Directory does not exist" in str(exc.value)

if __name__ == "__main__":
    pytest.main([__file__])
