from pathlib import Path
import pytest
import shutil

def test_output_structure():
    """Test and create output directory structure"""
    
    # Get project root
    root = Path(__file__).parent
    
    # Define required paths
    output_dir = root / "output"
    app5_dir = output_dir / "app5"
    
    # Create output/app5 if missing
    app5_dir.mkdir(parents=True, exist_ok=True)
    
    # Verify structure
    assert output_dir.exists() and output_dir.is_dir()
    assert app5_dir.exists() and app5_dir.is_dir()
    
    # Test write permissions
    test_file = app5_dir / "test.txt"
    try:
        test_file.write_text("test")
        assert test_file.exists()
        test_file.unlink()
    except Exception as e:
        pytest.fail(f"Failed to write to output/app5: {e}")
        
    print("[SETUP] ✅ output/app5 directory verified")

if __name__ == "__main__":
    pytest.main([__file__])
