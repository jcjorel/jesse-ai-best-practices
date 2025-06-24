# Project Knowledge Base
*Last Updated: 2025-06-24T17:48:00Z*

## Session-Specific Knowledge Loading Strategy
**LAZY LOADING APPROACH**: Knowledge bases related to the current session task are loaded on-demand when specifically needed, rather than automatically at session initialization. This approach:

- **Reduces Context Window Usage**: Only loads relevant knowledge bases for the current task
- **Improves Performance**: Avoids loading unnecessary external repository content
- **Maintains Focus**: Keeps session context aligned with current work objectives
- **Enables Selective Access**: Allows targeted knowledge base consultation when specific expertise is required

**Loading Triggers**: Knowledge bases are loaded when:
- User explicitly requests information from a specific repository or PDF
- Current task requires specific external API or framework knowledge
- Implementation needs reference patterns from external sources
- Debugging requires consultation of external documentation

**Available Knowledge Sources**:
- Git Clone Knowledge Bases: `.knowledge/git-clones/[repo-name]_kb.md`
- PDF Knowledge Bases: `.knowledge/pdf-knowledge/[source-name]/[source-name]_kb.md`
- Essential Knowledge Base: Always loaded (this file)

## PDF Knowledge Usage Requirements
**CRITICAL**: When using knowledge from imported PDF knowledge bases, you MUST also open and read the associated PDF chunk files to get full clarity and complete context about the knowledge. PDF chunk files are always located in `.knowledge/pdf-knowledge/[source-name]/pdf_chunks/<PDF-chunk-filename>`.

**Mandatory Process**:
1. **Reference PDF Knowledge Base**: First consult `.knowledge/pdf-knowledge/[source-name]/[source-name]_kb.md` for indexed knowledge
2. **Access Original Chunks**: Always open and read the corresponding PDF chunk files referenced in the knowledge base entry
3. **Verify Context**: Cross-reference the chunk content with the summarized knowledge to ensure complete understanding
4. **Use Complete Information**: Base decisions and implementations on the full context from both the knowledge base summary and the original PDF chunks

**PDF Chunk Naming Convention**: PDF chunks are stored with specific naming pattern:
- **Location**: `<project_root>/.knowledge/pdf-knowledge/<imported_pdf_name>/pdf_chunks/`
- **Naming Format**: `<imported_pdf_name>_pages_<page_number_start>_<page_number_end>.pdf`
- **Example**: `.knowledge/pdf-knowledge/user_manual/pdf_chunks/user_manual_pages_001_020.pdf`

**Locating PDF Chunks**: To find the correct PDF chunk(s) to read:
1. Identify the imported PDF name from the knowledge base entry
2. Navigate to `<project_root>/.knowledge/pdf-knowledge/<imported_pdf_name>/pdf_chunks/`
3. Look for files matching pattern `<imported_pdf_name>_pages_<start>_<end>.pdf`
4. Select chunks based on the page range containing the information you need

**Why This Is Required**:
- Knowledge base entries are summaries and may not contain all critical details
- PDF chunks contain the complete original context and nuanced information
- Implementation decisions require full understanding of the source material
- Error prevention through comprehensive information access

## Knowledge Entry Requirements
**MANDATORY**: All knowledge entries must include one or more trust sources to enable deep-dive verification and validation. Trust sources can be:
- Complete relative file paths to codebase files (e.g., `src/services/api_service.py`)
- Git cloned repository references (e.g., `.knowledge/git-clones/framework-docs_kb.md`)
- Web URLs with specific sections (e.g., `https://docs.example.com/api/v1/authentication.html`)
- Documentation file references (e.g., `doc/DESIGN.md#architecture-overview`)

**Format**: Each knowledge entry must end with:
```
**Trust Sources**:
- [Source Type]: [Complete path/URL/reference]
- [Source Type]: [Complete path/URL/reference]
```

## Project Purpose
[Replace this section with your project's purpose and description]

**Example Template**:
```
[Project Name] is a [type of application] that [main functionality] to provide [key value proposition]. The project features [key technical components] with [deployment/infrastructure details].

**Trust Sources**:
- Codebase: `README.md`
- Codebase: `documentation/ARCHITECTURE.md`
```

## Perplexity Query Results
*No Perplexity queries recorded yet*

## Web Resources  
*No web resources captured yet*

## PDF Large Files Requiring Processing
*No large PDF files marked for processing*

## Patterns and Solutions

### [Pattern Name Template]
**Pattern**: [Brief description of the pattern or solution]
**Context**: [When and why this pattern is useful]
**Implementation**:
- [Key implementation detail 1]
- [Key implementation detail 2]
- [Key implementation detail 3]
**Benefits**: [Advantages of using this pattern]

**Trust Sources**:
- [Source Type]: [Complete path/URL/reference]

*Add your project-specific patterns and solutions here using the template above*

## Development Environment
### Virtual Environment
**Location**: [Path to virtual environment, e.g., `venv/` or `project-name/venv`]
**Usage**: Must be activated before executing any commands in the project
**Activation Command**: `source [path-to-venv]/bin/activate`
**Purpose**: Isolates project dependencies from system environment

**Trust Sources**:
- Codebase: `README.md`
- Codebase: `requirements.txt` or `package.json`

### [Additional Environment Setup]
*Add additional development environment details as needed*

## External APIs
### [API Name Template]
**Purpose**: [What this API provides]
**Key Endpoints**: [Main endpoints or services used]
**Authentication**: [Authentication method]
**Usage Notes**: [Important implementation notes]

**Trust Sources**:
- Codebase: [Path to service integration code]
- Documentation: [Path to API documentation]

*Add your project's external API integrations here*

## Project PR/FAQ Documents

### Press Release & FAQ
**Status**: ⚠️ **NOT YET CREATED**

**🚀 ACTION REQUIRED**: No PR/FAQ document exists for this project yet.

**To create your project's PR/FAQ document**:
1. Use the Amazon PR/FAQ Coach: `/jesse_amazon_prfaq_coach.md`  
2. The coach will guide you through Amazon's authentic Working Backwards methodology
3. Complete press release and FAQ will be automatically added to this knowledge base

**What you'll get**:
- Professional press release using Amazon's 7-paragraph structure
- Comprehensive FAQ with customer-facing and internal questions
- Working Backwards methodology completion with 5 Customer Questions
- Integration with this knowledge base for future reference

**Trust Sources**:
- Coach Workflow: `.clinerules/workflows/jesse_amazon_prfaq_coach.md`
- Working Backwards Directory: `working_backwards/`

### Working Backwards Summary

**Status**: ⚠️ **NOT YET COMPLETED**

**🚀 ACTION REQUIRED**: Project Working Backwards analysis not yet completed.

**The 5 Customer Questions Framework**:
```
❓ WHO is the customer?     → [Not yet answered - use PR/FAQ coach]
❓ WHAT is the problem?     → [Not yet answered - use PR/FAQ coach]  
❓ WHAT is the solution?    → [Not yet answered - use PR/FAQ coach]
❓ WHAT is the experience?  → [Not yet answered - use PR/FAQ coach]
❓ HOW measure success?     → [Not yet answered - use PR/FAQ coach]
```

**To complete your Working Backwards analysis**:
1. Launch the Amazon PR/FAQ Coach: `/jesse_amazon_prfaq_coach.md`
2. The coach provides authentic Amazon methodology with real examples
3. Your completed analysis will automatically populate this section

**Trust Sources**:
- Coach Workflow: `/jesse_amazon_prfaq_coach.md`
- Amazon Examples: Real internal Amazon PR/FAQ examples included in coach
- Working Backwards Directory: `working_backwards/current/` and `working_backwards/archive/`

## Available Knowledge Sources (Lazy Loading)
**Note**: These knowledge bases are loaded on-demand when specifically needed for the current session task, following the lazy loading strategy described above.

### Git Clone Knowledge Bases
*No git clone knowledge bases configured yet*

**To add a git clone knowledge base**:
1. Use the Git Clone Import workflow: `/jesse_wip_kb_git_clone_import.md`
2. The workflow will clone the repository and create the knowledge base
3. Git clones are stored in `.knowledge/git-clones/[repo-name]/`
4. Knowledge bases are created as `.knowledge/git-clones/[repo-name]_kb.md`

### PDF Knowledge Bases
*No PDF knowledge bases imported yet*

**To import a PDF knowledge base**:
1. Use the PDF Import workflow: `/jesse_wip_kb_pdf_import.md`
2. The workflow will process the PDF and create indexed knowledge base
3. PDFs are stored in `.knowledge/pdf-knowledge/[pdf-name]/`
4. Knowledge bases are created as `.knowledge/pdf-knowledge/[pdf-name]/[pdf-name]_kb.md`
5. PDF chunks are stored in `.knowledge/pdf-knowledge/[pdf-name]/pdf_chunks/`
