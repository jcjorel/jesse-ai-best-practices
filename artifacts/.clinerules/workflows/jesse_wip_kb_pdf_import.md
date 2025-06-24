# WIP KB PDF Import Workflow

## Workflow Purpose
Import and index PDF documents into the knowledge base system using LLM-based visual understanding. This workflow creates searchable knowledge bases with chunked PDFs optimized for LLM reading, eliminating the need for external OCR tools or text extraction utilities. The workflow is designed to be restartable across multiple Cline sessions to handle very large PDFs that may exceed context window limits.

## Session Initialization Override
**CRITICAL**: When this workflow is executed as the first prompt of a new Cline session, it automatically disables WIP task loading to prevent interference with PDF processing operations.

### WIP Task Disable Protocol
If this is the first prompt of a session:
1. **Automatic Disable**: WIP task auto-loading is disabled for this session only
2. **Session Scope**: This setting applies only to the current session and does not persist
3. **Clean Context**: Provides clean context focused solely on PDF import operations
4. **User Notification**: User is informed that WIP task loading has been disabled for this session

### Session State Confirmation
Display to user when WIP task is disabled:
```
✓ WIP task auto-loading DISABLED for this PDF import session
- Reason: Clean context required for PDF processing operations
- Scope: Current session only (will re-enable in new sessions)
- Focus: PDF import workflow execution without WIP task interference
```

## Execution Steps

### 1. Check for Existing Import Session
Before starting a new import, check if there's an ongoing import:
- Look for `.knowledge/pdf-knowledge/<snake_case_pdf_name>/import_progress.json`
- If found, offer to resume the import from where it left off
- Display progress information: chunks processed, chunks remaining

### 2. Gather PDF Information
For new imports, prompt user for the following information:
- **PDF File Path**: Full path to the PDF file to import
- **PDF Purpose**: Why this PDF is valuable for the project
- **Key Topics**: Main subjects covered in the PDF
- **Content Type**: Technical manual, research paper, documentation, etc.
- **Processing Priority**: Which sections are most important if partial processing is needed

### 3. Validate PDF File
Perform initial validation checks:
- Verify file exists and is readable
- Confirm PDF format validity using PyPDF2
- Check file size and page count
- Assess if file size requires multi-session handling (>500 pages)
- Create initial progress tracking file

### 4. Initialize Import Session
Create import session tracking:
```json
{
  "pdf_path": "/path/to/original.pdf",
  "snake_case_name": "pdf_name",
  "total_pages": 1000,
  "total_chunks": 50,
  "chunks_processed": 0,
  "chunks_analyzed": 0,
  "session_started": "2025-06-20T08:00:00Z",
  "last_updated": "2025-06-20T08:00:00Z",
  "status": "chunking|analyzing|completed",
  "file_hash": "sha256_hash",
  "metadata": {
    "purpose": "...",
    "key_topics": ["..."],
    "content_type": "..."
  }
}
```

### 5. Generate Directory Structure
Create standardized directory names and structure:
- Sanitize PDF filename to snake_case format
- Create base directory: `.knowledge/pdf-knowledge/<snake_case_pdf_name>/`
- Create subdirectories: `pdf_chunks/`, `temp/`
- Save progress file: `import_progress.json`

### 6. Copy Original PDF (if not already done)
Copy the original PDF to knowledge base:
- Check if original already exists (resume scenario)
- Copy file to `.knowledge/pdf-knowledge/<snake_case_pdf_name>/<original_pdf_name>.pdf`
- Verify copy integrity using file hash
- Update progress file

### 7. Execute PDF Chunking
Run the embedded Python chunking script:

```python
#!/usr/bin/env python3
"""
PDF Chunking Script for Knowledge Base Import
Supports resumable chunking for large PDFs
Requires: PyPDF2 (install with: pip install PyPDF2)
"""

import os
import sys
import re
import json
from pathlib import Path
from typing import List, Tuple, Dict
from PyPDF2 import PdfReader, PdfWriter
from datetime import datetime
import hashlib

def load_progress(progress_file: str) -> Dict:
    """Load existing progress or create new."""
    if os.path.exists(progress_file):
        with open(progress_file, 'r') as f:
            return json.load(f)
    return {}

def save_progress(progress_file: str, progress: Dict):
    """Save progress to file."""
    progress['last_updated'] = datetime.now().isoformat()
    with open(progress_file, 'w') as f:
        json.dump(progress, f, indent=2)

def sanitize_filename(filename: str) -> str:
    """Convert filename to snake_case format."""
    name = os.path.splitext(filename)[0]
    name = re.sub(r'[^\w\s-]', '', name)
    name = re.sub(r'[-\s]+', '_', name)
    return name.lower()

def get_existing_chunks(chunks_dir: str) -> List[str]:
    """Get list of already created chunks."""
    if not os.path.exists(chunks_dir):
        return []
    return sorted([f for f in os.listdir(chunks_dir) if f.endswith('.pdf')])

def chunk_pdf_resumable(input_path: str, output_base: str, chunk_size: int = 20) -> Tuple[List[Tuple[str, int, int]], Dict]:
    """Split PDF into chunks with resume capability."""
    chunks_dir = os.path.join(output_base, "pdf_chunks")
    os.makedirs(chunks_dir, exist_ok=True)
    
    progress_file = os.path.join(output_base, "import_progress.json")
    progress = load_progress(progress_file)
    
    # Get existing chunks
    existing_chunks = get_existing_chunks(chunks_dir)
    existing_count = len(existing_chunks)
    
    chunks_created = []
    
    try:
        with open(input_path, 'rb') as file:
            reader = PdfReader(file)
            total_pages = len(reader.pages)
            base_name = sanitize_filename(os.path.basename(input_path))
            
            # Calculate total expected chunks
            total_chunks = (total_pages + chunk_size - 1) // chunk_size
            
            # Update progress
            progress['total_pages'] = total_pages
            progress['total_chunks'] = total_chunks
            progress['chunks_processed'] = existing_count
            
            print(f"PDF has {total_pages} pages, will create {total_chunks} chunks")
            if existing_count > 0:
                print(f"Resuming: {existing_count} chunks already exist")
            
            # Start from where we left off
            start_chunk = existing_count
            
            for chunk_idx in range(start_chunk, total_chunks):
                start_page = chunk_idx * chunk_size
                end_page = min(start_page + chunk_size, total_pages)
                
                writer = PdfWriter()
                
                for page_num in range(start_page, end_page):
                    writer.add_page(reader.pages[page_num])
                
                chunk_filename = f"{base_name}_pages_{start_page+1:03d}_{end_page:03d}.pdf"
                chunk_path = os.path.join(chunks_dir, chunk_filename)
                
                with open(chunk_path, 'wb') as output_file:
                    writer.write(output_file)
                
                chunks_created.append((chunk_filename, start_page + 1, end_page))
                progress['chunks_processed'] = existing_count + len(chunks_created)
                
                # Save progress after each chunk
                save_progress(progress_file, progress)
                
                print(f"Progress: {progress['chunks_processed']}/{total_chunks} chunks ({progress['chunks_processed']/total_chunks*100:.1f}%)")
            
            # Add existing chunks to the list
            for chunk_file in existing_chunks:
                # Parse page numbers from filename
                match = re.search(r'pages_(\d+)_(\d+)\.pdf$', chunk_file)
                if match:
                    start, end = int(match.group(1)), int(match.group(2))
                    chunks_created.insert(0, (chunk_file, start, end))
            
            progress['status'] = 'chunking_complete'
            save_progress(progress_file, progress)
            
            return chunks_created, progress
            
    except Exception as e:
        print(f"Error during chunking: {str(e)}")
        progress['error'] = str(e)
        save_progress(progress_file, progress)
        raise

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python chunk_pdf.py <input_pdf_path> <output_base_directory>")
        sys.exit(1)
    
    input_pdf = sys.argv[1]
    output_dir = sys.argv[2]
    
    if not os.path.exists(input_pdf):
        print(f"Error: Input PDF not found: {input_pdf}")
        sys.exit(1)
    
    chunks, progress = chunk_pdf_resumable(input_pdf, output_dir)
    
    print(f"\nChunking complete: {len(chunks)} total chunks")
    print(f"Progress saved to: {os.path.join(output_dir, 'import_progress.json')}")
```

Execute the script:
- Save script to temporary file
- Run with Python 3.11+
- Script will automatically resume if interrupted
- Progress is saved after each chunk creation

### 8. Initialize or Load Knowledge Base File
Check for existing knowledge base file:
- If exists: Load current state and analyzed chunks list
- If new: Create initial structure at `.knowledge/pdf-knowledge/<snake_case_pdf_name>/<snake_case_pdf_name>_kb.md`

### 9. Process Chunks with LLM (Resumable)
For each chunk that hasn't been analyzed yet:

#### 9.1 Check Context Window Usage
Before processing each chunk:
- Monitor current context window usage
- If usage > 80%, prepare for session handoff:
  - Save current progress
  - Update knowledge base with analyzed chunks
  - Create session handoff notes
  - Inform user to start new session with `/wip_kb_pdf_import` to resume

#### 9.2 Read and Analyze Chunk
For each unprocessed chunk:
- Load the chunk PDF file
- Use LLM vision to read and understand content
- Extract key information:
  - Main topics and concepts
  - Visual elements (diagrams, charts, tables)
  - Code snippets or technical content
  - Important definitions or procedures
  - Cross-references to other sections

#### 9.3 Update Knowledge Base
Add chunk analysis to knowledge base file:
- Summary of chunk content
- Key concepts and their locations
- Visual element descriptions
- Notable findings
- **MANDATORY**: When referencing any page number or range, immediately include the corresponding PDF chunk file name(s) in parentheses for precise retrieval
- Mark chunk as analyzed in progress file

**Page Reference Enforcement Rule**: 
Every mention of page numbers (e.g., "page 45", "pages 23-27", "see page 156") MUST be immediately followed by the corresponding chunk file name(s) in this format: `(chunk: filename.pdf)` or `(chunks: file1.pdf, file2.pdf)` for ranges spanning multiple chunks.

**Examples**:
- "The authentication process on page 45 (chunk: manual_pages_041_060.pdf) describes..."
- "Security guidelines on pages 23-27 (chunks: manual_pages_021_040.pdf) outline..."
- "Configuration details spanning pages 156-162 (chunks: manual_pages_141_160.pdf, manual_pages_161_180.pdf) provide..."

#### 9.4 Save Progress
After each chunk:
- Update `import_progress.json` with chunks_analyzed count
- Save knowledge base file with new content
- Commit progress to ensure resumability

### 10. Generate Cross-References (Final Phase)
Once all chunks are analyzed:
- Review all chunk summaries
- Identify topics that span multiple chunks
- Create topic-based navigation index
- Generate visual content catalog
- Add usage patterns and reading guidance

### 11. Finalize Import
Complete the import process:
- Update Essential Knowledge Base with PDF entry
- Mark import as completed in progress file
- Generate import summary report
- Clean up temporary files
- Display final statistics

## Knowledge Base Template Structure

```markdown
# PDF Knowledge Base: [PDF Title]
*Last Updated: [ISO timestamp]*
*Original File: [original_filename.pdf]*
*Total Pages: [page_count]*
*Chunks Created: [chunk_count]*
*File Hash**: [SHA256 hash]*
*Import Status**: [In Progress: X/Y chunks analyzed | Completed]

## Document Overview
**Subject**: [Main subject/topic of the PDF]
**Type**: [Technical Manual/Research Paper/Documentation/etc.]
**Key Topics**: [List of main topics covered]
**Target Audience**: [Who this document is for]
**Visual Content**: [Notable diagrams/charts/images present]
**Processing Notes**: [Any special considerations for LLM reading]

## Import Progress
- **Session Started**: [ISO timestamp]
- **Last Updated**: [ISO timestamp]
- **Chunks Analyzed**: [X] of [Y]
- **Estimated Sessions Remaining**: [Based on context usage]

## Page Reference Enforcement
**CRITICAL RULE**: Every page number or range mentioned in this knowledge base MUST be immediately followed by the corresponding PDF chunk file name(s) in parentheses using this format:
- Single page: `page X (chunk: filename.pdf)`
- Page range: `pages X-Y (chunks: file1.pdf, file2.pdf)`
- Multiple ranges: `pages X-Y, Z-W (chunks: file1.pdf, file2.pdf, file3.pdf)`

This ensures precise retrieval of PDF chunks for complete understanding of referenced content.

## Chunk File Mapping
[Auto-generated mapping table showing page ranges and corresponding chunk files]
| Page Range | Chunk File | Content Summary |
|------------|------------|-----------------|
| 1-20       | [name]_pages_001_020.pdf | [Brief description] |
| 21-40      | [name]_pages_021_040.pdf | [Brief description] |
| ...        | ...        | ... |

## Semantic Content Index

[Content added incrementally as chunks are processed...]
```

## Session Handoff Protocol

When context window limit is approached:

### 1. Create Handoff Summary
```markdown
## Session Handoff - [ISO timestamp]
**Progress**: Analyzed [X] of [Y] chunks
**Last Chunk Processed**: [chunk_filename]
**Next Chunk**: [chunk_filename]
**Context Window Used**: [percentage]

### Key Findings So Far
- [Important discovery 1 with page references and chunk names]
- [Important discovery 2 with page references and chunk names]

### Resume Instructions
1. Run `/wip_kb_pdf_import` workflow
2. Select "Resume existing import"
3. Import will continue from chunk [X+1]

### Page Reference Compliance Check
**MANDATORY**: Before session handoff, verify that ALL page references in the knowledge base include corresponding chunk file names. Any missing chunk references must be added before proceeding to next session.
```

### 2. Save All Progress
- Update import_progress.json
- Save knowledge base file
- Commit any temporary analysis

### 3. Inform User
Display clear message:
```
PDF import requires session handoff due to context window limits.
Progress saved: [X] of [Y] chunks analyzed.
To continue: Start a new Cline session and run /wip_kb_pdf_import to resume.
```

## Error Handling

### Resumable Errors
- **Context window limit**: Save progress and resume in new session
- **Chunk read failure**: Skip chunk, mark as failed, continue with next
- **Temporary LLM errors**: Retry chunk analysis up to 3 times

### Critical Errors
- **PDF corruption**: Stop import, preserve any completed analysis
- **Disk space issues**: Pause import, request user intervention
- **Invalid PDF structure**: Report specific issue, attempt partial import

## Multi-Session Coordination

### Session State Management
- All state stored in `import_progress.json`
- Knowledge base file updated incrementally
- No in-memory state required between sessions

### Progress Tracking
```json
{
  "sessions": [
    {
      "session_id": "2025-06-20T08:00:00Z",
      "chunks_processed": [0, 1, 2, 3, 4],
      "context_usage_at_end": "78%"
    },
    {
      "session_id": "2025-06-20T09:00:00Z",
      "chunks_processed": [5, 6, 7, 8],
      "context_usage_at_end": "82%"
    }
  ]
}
```

### Optimization Strategies
- Process smaller chunks if context fills quickly
- Prioritize important sections first
- Skip redundant content if identified

## Usage Examples

### Starting New Import
```
User: /wip_kb_pdf_import
Assistant: Starting PDF import workflow...
[Workflow proceeds with new import]
```

### Resuming Existing Import
```
User: /wip_kb_pdf_import
Assistant: Found existing import for "technical_manual.pdf"
Progress: 25 of 50 chunks analyzed (50%)
Would you like to resume this import? [Yes/No]
```

### Handling Large PDFs
```
Assistant: This PDF has 2000 pages (100 chunks).
Estimated sessions needed: 4-5 (based on typical context usage)
Proceed with import? [Yes/No]
```

## Best Practices

### For Optimal Processing
1. Start imports at beginning of Cline session
2. Monitor context usage regularly
3. Process high-priority sections first
4. Use descriptive PDF names for easy identification
5. **ENFORCE PAGE REFERENCE RULE**: Always include chunk file names when mentioning page numbers

### For Large PDFs (1000+ pages)
1. Consider splitting PDF into logical sections first
2. Import most important sections as separate PDFs
3. Plan for multiple sessions upfront
4. Review partial results between sessions
5. **MAINTAIN CHUNK MAPPING**: Keep accurate page-to-chunk mapping table updated

### Page Reference Quality Control
1. **Pre-Analysis**: Generate chunk file mapping table before content analysis
2. **During Analysis**: Immediately add chunk references when writing page numbers
3. **Post-Analysis**: Verify all page references include chunk file names
4. **Session Handoff**: Check compliance before ending session
5. **Resume Verification**: Confirm existing content follows chunk reference rules

## Integration with Knowledge System

### Automatic Updates
- Essential Knowledge Base updated after each session
- Progress visible in knowledge base file
- Partial imports are usable immediately

### Search Integration
- Analyzed chunks immediately searchable
- Partial imports included in knowledge queries
- Progress indicators in search results

## Completion Verification

### Import Considered Complete When
1. All chunks have been analyzed
2. Cross-references have been generated
3. Knowledge base file is finalized
4. Essential Knowledge Base is updated
5. Progress file shows "completed" status

### Post-Completion Actions
- Archive progress file to `.completed/`
- Generate import statistics report
- **FINAL COMPLIANCE CHECK**: Verify ALL page references include chunk file names
- Suggest related PDFs for import
- Offer to create topic-specific extracts

### Quality Assurance Verification
Before marking import as complete:
1. **Scan entire knowledge base** for page number mentions
2. **Verify each page reference** includes corresponding chunk file name(s)
3. **Update any missing chunk references** immediately
4. **Generate compliance report** showing 100% chunk reference coverage
5. **Mark as compliant** only when all page references include chunk names

**ENFORCEMENT**: No PDF import can be marked as "completed" until 100% of page references include corresponding chunk file names.
