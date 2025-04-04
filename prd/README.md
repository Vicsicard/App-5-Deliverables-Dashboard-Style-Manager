 # App 5: Deliverables Dashboard + Style Manager
Module 5 of 6 in the Self Cast Studios system
App Function: Centralized interface for reviewing, approving, revising, and managing all generated content and narrative style profiles from previous apps (App 1–4).

## 1. PURPOSE
App 5 serves as the client-facing and internal QA interface for managing deliverables and style data. It enables structured review of:

📄 Generated content (blogs, bios, show notes, etc.)

🧠 Narrative style profiles

🎥 Finalized videos (shortform + longform)

🔄 Revision requests per deliverable

🧩 Reference linkage between content and source data (e.g., transcript chunk, question ID, emotion, etc.)

It acts as the final review and approval hub before publishing or handoff to App 6.

## 2. INPUTS
- `output/app3/*.md`: All content files from Content Generator Suite
- `style-profile.md`: Style summary from App 2
- `video_index.json`: Video chunk mapping from App 1
- `video_handoff_status.json`: Finalized video output list from App 4
- `chunk_metadata.json`: Source metadata
- `handoff_status.json`: Draft tracking info (optional)

## 3. OUTPUTS
📁 Final client-approved versions of all content (stored in `/output/app5/`)

📝 Structured revision requests (in `revision_requests.json`)

✅ Approval logs (per content type)

🔗 Linkback index: connects each content section to corresponding transcript chunks, question ID, and emotion tags

📄 `content_status.json`: Status tracking for each file (e.g., draft, approved, revised)

## 4. IMPLEMENTED MODULES

### 📂 FILE LOADER (`dashboard.py`) [✅]
- [✅] Loads all content .md files and style profile
- [✅] Loads video and transcript metadata
- [✅] Proper error handling
- [✅] [LOADER] console output

### 🧠 STYLE PARSER (`style_parser.py`) [✅]
- [✅] Parses all 5 narrative dimensions
- [✅] UTF-8 encoding with fallback
- [✅] Quote extraction
- [✅] Error tolerance

### 📊 FILE REGISTRY (`file_registry.py`) [✅]
- [✅] Scans markdown files
- [✅] Extracts metadata
- [✅] [REGISTRY] output
- [✅] Cross-OS compatibility

### ✍️ REVISION ENGINE (`revision_engine.py`) [✅]
- [✅] Style alignment checking
- [✅] HTML comment annotations
- [✅] Content preservation
- [✅] Format validation

### 📦 HANDOFF WRITER (`handoff_writer.py`) [✅]
- [✅] Writes to `/output/app5/`
- [✅] Creates `handoff_manifest_app5.json`
- [✅] Tracks revision notes
- [✅] [HANDOFF] console output

## 5. SYSTEM CONSTRAINTS
- [✅] No content editing in place
- [✅] Structural feedback storage
- [✅] Markdown preservation
- [✅] No LLM/generation logic

## 6. CLI USAGE
```bash
python dashboard.py --load /output/app3/ --style style-profile.md --video video_handoff_status.json --meta chunk_metadata.json
```

## 7. POSTCONDITIONS
Upon successful completion:
- [✅] All content files are reviewed and stored in `/output/app5/`
- [✅] All structured revision requests saved in `revision_requests.json`
- [✅] Approval metadata exists in `content_status.json`

## 8. CURRENT STATUS
🎯 **Implementation Complete**
- All core modules implemented and tested
- Directory structure verified
- Error handling confirmed
- Console output standardized
- Ready for handoff to App 6

### Test Coverage
- [✅] Unit tests for all modules
- [✅] Integration tests
- [✅] Error case handling
- [✅] File system operations
- [✅] Cross-OS compatibility

### Next Steps
Ready for integration with App 6 for final publishing and distribution.
