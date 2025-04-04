from pathlib import Path
from typing import Dict, List, Optional
from utils.file_loader import load_markdown_files, load_json_file
from utils.markdown_parser import extract_sections
from style_parser import StyleProfileParser

class DashboardLoader:
    """Handles loading and validation of input files"""
    
    def __init__(self):
        self.root_dir = Path(__file__).resolve().parent
        self.style_parser = StyleProfileParser()
        
    def load_input_files(
        self,
        style_profile_path: str,
        app3_output_dir: str,
        chunk_metadata_path: Optional[str] = None,
        video_status_path: Optional[str] = None
    ) -> bool:
        """
        Load and validate all input files
        
        Args:
            style_profile_path: Path to style-profile.md
            app3_output_dir: Path to /output/app3/ directory
            chunk_metadata_path: Optional path to chunk_metadata.json
            video_status_path: Optional path to video_handoff_status.json
            
        Returns:
            True if all required files loaded successfully
        """
        try:
            # Load style profile
            style_file = Path(style_profile_path)
            if not style_file.exists():
                print(f"[LOADER] ❌ Style profile not found: {style_profile_path}")
                return False
                
            if style_file.suffix.lower() != '.md':
                print(f"[LOADER] ❌ Invalid style profile format: {style_file.suffix}")
                return False
                
            try:
                style_content = style_file.read_text(encoding='utf-8')
                self.style_signals = self.style_parser.parse_style_profile(style_content)
                print("[LOADER] ✅ Style profile loaded successfully")
            except Exception as e:
                print(f"[LOADER] ❌ Failed to parse style profile: {str(e)}")
                return False
            
            # Load App 3 drafts
            app3_dir = Path(app3_output_dir)
            if not app3_dir.exists() or not app3_dir.is_dir():
                print(f"[LOADER] ❌ App 3 output directory not found: {app3_output_dir}")
                return False
                
            markdown_files = list(app3_dir.glob("*.md"))
            if not markdown_files:
                print("[LOADER] ❌ No markdown files found in App 3 output")
                return False
                
            self.draft_files = markdown_files
            print(f"[LOADER] ✅ Found {len(markdown_files)} draft files")
            
            # Load optional metadata
            if chunk_metadata_path:
                try:
                    chunk_file = Path(chunk_metadata_path)
                    if chunk_file.exists():
                        self.chunk_metadata = load_json_file(str(chunk_file))
                        print("[LOADER] ✅ Chunk metadata loaded")
                    else:
                        print(f"[LOADER] ⚠️ Chunk metadata not found: {chunk_metadata_path}")
                except Exception as e:
                    print(f"[LOADER] ⚠️ Failed to load chunk metadata: {str(e)}")
            
            if video_status_path:
                try:
                    video_file = Path(video_status_path)
                    if video_file.exists():
                        self.video_status = load_json_file(str(video_file))
                        print("[LOADER] ✅ Video status loaded")
                    else:
                        print(f"[LOADER] ⚠️ Video status not found: {video_status_path}")
                except Exception as e:
                    print(f"[LOADER] ⚠️ Failed to load video status: {str(e)}")
            
            print("[LOADER] ✅ All required files loaded successfully")
            return True
            
        except Exception as e:
            print(f"[LOADER] ❌ Unexpected error: {str(e)}")
            return False
            
    def get_style_signals(self) -> Dict[str, List[str]]:
        """Get parsed style signals"""
        return self.style_signals
        
    def get_draft_files(self) -> List[Path]:
        """Get list of draft files"""
        return self.draft_files

if __name__ == "__main__":
    # Test file loading
    loader = DashboardLoader()
    success = loader.load_input_files(
        style_profile_path="data/style-profile.md",
        app3_output_dir="output/app3",
        chunk_metadata_path="data/chunk_metadata.json",
        video_status_path="data/video_handoff_status.json"
    )
    
    if success:
        print("\nLoaded Files Summary:")
        print(f"Style Signals: {len(loader.get_style_signals())} dimensions")
        print(f"Draft Files: {len(loader.get_draft_files())} files")
