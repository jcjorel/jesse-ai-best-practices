# PDF Knowledge Bases Index

This directory contains knowledge bases extracted from PDF documents that provide context and patterns relevant to the JESSE Framework development.

## Storage Policy
**CRITICAL**: All PDF files are stored **EXCLUSIVELY** in this directory (`<project_root>/.knowledge/pdf-knowledge/`).

- **Single Location Rule**: PDF files must **NEVER** exist anywhere else in the project structure
- **No Exceptions**: This policy has no exceptions - all imported PDFs are stored only in `.knowledge/pdf-knowledge/`
- **Centralized Management**: This ensures consistent knowledge management and prevents scattered document copies
- **Version Control Separation**: Keeps PDF content separate from project codebase through .gitignore rules

## Directory Structure
```
.knowledge/pdf-knowledge/
├── README.md                        # This index file
├── [document-name].pdf              # Actual PDF file (ignored by .gitignore)
├── [document-name]_kb.md           # Knowledge base extracted from PDF (tracked)
└── [another-document]_kb.md        # Additional knowledge bases (tracked)
```

## Available Knowledge Bases

### Amazon Bedrock User Guide
**PDF File**: bedrock-ug.pdf (3,431 pages)
**Purpose**: Comprehensive Amazon Bedrock service documentation for AI/ML development context
**Key Features**: Foundation models, API reference, Agents, Knowledge Bases, Guardrails, Custom models
**Knowledge Base**: [bedrock_ug_kb.md](bedrock_ug/bedrock_ug_kb.md)
**Added**: 2025-06-30T00:09:00Z
**Status**: **IN PROGRESS** - 1 of 172 chunks analyzed
**Next Action**: Continue import in new session with `/jesse_wip_kb_pdf_import`
**Relevance**: Critical reference for Bedrock service integration, MCP server development with Bedrock models, and AI application development patterns

## How to Add PDF Knowledge Bases
Use the PDF Import workflow to add external PDF documents:

```bash
/jesse_wip_kb_pdf_import.md
```

This workflow will:
1. Prompt for PDF file location and focus areas
2. Copy PDF to `.knowledge/pdf-knowledge/[document-name].pdf`
3. Create knowledge base file `[document-name]_kb.md`
4. Extract and structure important content and patterns
5. Update main knowledge base with reference

## .gitignore Protection
When any PDF is added to the knowledge base, the project `.gitignore` file contains these protective rules:

```
# Knowledge Management System - PDF Documents
# Ignore actual PDF files but keep knowledge base files
.knowledge/pdf-knowledge/*.pdf
!.knowledge/pdf-knowledge/*.md
!.knowledge/pdf-knowledge/README.md
```

This ensures that:
- Actual PDF files are ignored and not committed to the project repository
- Knowledge base files (`[document-name]_kb.md`) are preserved and version controlled
- This index file (`README.md`) is maintained in version control
- PDF content remains separate from project codebase

## Large Document Processing
When working with large PDF documents:
1. Check if content is documented in corresponding `[document-name]_kb.md`
2. If not documented and content is extensive:
   - Mark document in `KNOWLEDGE_BASE.md` as requiring processing with priority "**before any other tasks**"
   - Recommend dedicated processing session using `/jesse_wip_task_process_large_file.md`
   - Use systematic extraction approach to capture key insights

## Knowledge Extraction Guidelines
- **Focus on Relevance**: Extract content directly applicable to JESSE Framework development
- **Structure Information**: Organize extracted knowledge in clear, searchable format
- **Intemporal Writing**: Write knowledge in present tense, stating facts rather than referencing document context
- **Cross-Reference**: Link PDF knowledge to relevant git clone knowledge and WIP tasks where applicable
