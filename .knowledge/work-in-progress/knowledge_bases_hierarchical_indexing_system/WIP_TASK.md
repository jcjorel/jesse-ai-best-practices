# Task: Knowledge Bases Hierarchical Indexing System

# 🚨 FRAMEWORK-WIDE SESSION INITIALIZATION REQUIREMENT 🚨

## Mandatory Session Initialization Command
**EVERY JESSE FRAMEWORK DEVELOPMENT SESSION MUST START WITH:**
```bash
cd jesse-framework-mcp && uv run python tests/test_project_root.py --dump
```

**REQUIREMENT LEVEL**: 🔒 **HARD BLOCKING** - Development work cannot proceed without this  
**SCOPE**: All JESSE Framework development sessions (framework-wide requirement)  
**ENFORCEMENT**: Manual verification required before any development activity
**CRITICAL**: You MUST run this command once as soon as possible even in PLAN mode

**This requirement is documented in detail in**: `.knowledge/persistent-knowledge/KNOWLEDGE_BASE.md`

---

## Git Integration
- **Branch**: jesse-wip/knowledge_bases_hierarchical_indexing_system
- **Parent Branch**: next-gen-mcp
- **Branch Created**: 2025-07-01T10:29:00Z
- **Branch Status**: Active

## Task Context

### Objective
Create a FastMCP-based knowledge indexing system that implements Hierarchical Semantic Context pattern for the JESSE Framework, enabling automated maintenance of structured knowledge files throughout the .knowledge/ directory hierarchy.

### Scope
- **In Scope**: 
  - Create `jesse-framework-mcp/jesse_framework_mcp/knowledge-bases/` directory structure
  - Implement hierarchical indexing with leaf-first update strategy  
  - Integrate strands_agent_driver for LLM-powered content summarization
  - Build change detection system using filesystem timestamps
  - Create FastMCP tools for manual indexing trigger and search
  - Handle special cases: git-clones (read-only) and project-base (whole codebase)
  - Follow JESSE_CODE_COMMENTS.md standards throughout implementation

- **Out of Scope**: 
  - Query/search feature implementation (future task)
  - Web interface or visualization tools
  - Performance optimization beyond basic requirements
  - Integration with external search engines

### Success Criteria
- [ ] Complete directory structure created with proper module organization
- [ ] HierarchicalIndexer class implemented with leaf-first processing
- [ ] Change detection system working with filesystem timestamps
- [ ] Knowledge file builder integrated with strands_agent_driver
- [ ] Special handlers for git-clones and project-base implemented
- [ ] FastMCP tools created with JESSE standards compliance
- [ ] All code follows JESSE_CODE_COMMENTS.md documentation standards
- [ ] Basic indexing workflow functional end-to-end

### Dependencies
- Existing strands_agent_driver implementation
- FastMCP framework and Context patterns
- JESSE_CODE_COMMENTS.md documentation standards
- Project .knowledge/ directory structure
- Git repository for branch management

### Timeline
- **Started**: 2025-07-01T10:25:00Z
- **Target**: 2025-07-15T00:00:00Z (2 weeks)
- **Milestones**: 
  - Week 1: Core architecture and indexing engine
  - Week 2: Special handlers and FastMCP tools integration

## Comprehensive Design Documentation

### Architecture Overview

#### FastMCP Integration Strategy
- **Resource-First Architecture**: Builds on existing FastMCP resource-first patterns
- **Context Integration**: All operations use FastMCP Context for progress reporting and error handling
- **Tool Integration**: Manual indexing trigger and future search capabilities as FastMCP tools
- **HTTP Formatting**: Consistent HTTP-formatted responses using existing http_formatter patterns

#### Async Design Principles
- **Pure Async Architecture**: All operations are async using FastMCP Context patterns
- **Strands Agent Integration**: Leverage existing strands_agent_driver for LLM operations
- **Error Resilience**: Comprehensive error handling following existing defensive programming patterns
- **Progress Reporting**: Real-time progress updates via FastMCP Context

### Directory Structure Design

```
jesse-framework-mcp/jesse_framework_mcp/knowledge-bases/
├── README.md                           # Main documentation
├── __init__.py                         # Package initialization + tool registration
├── tools.py                           # FastMCP tools implementation
├── resources.py                       # FastMCP resources implementation
├── indexing/                          # Indexing subsystem
│   ├── __init__.py
│   ├── hierarchical_indexer.py        # Core indexing engine
│   ├── change_detector.py             # File change detection
│   ├── knowledge_builder.py           # Knowledge file builder
│   └── special_handlers.py            # Git-clone & project-base handlers
└── models/                            # Data models
    ├── __init__.py
    ├── knowledge_context.py           # Hierarchical context models
    └── indexing_config.py             # Configuration models
```

#### Component Responsibilities

**HierarchicalIndexer (`hierarchical_indexer.py`)**
- Main indexing orchestrator implementing leaf-first update strategy
- Coordinates between change detection, knowledge building, and special handlers
- Manages knowledge hierarchy traversal and update sequencing

**ChangeDetector (`change_detector.py`)**
- Detects when knowledge files need updates based on filesystem changes
- Timestamp-based comparison between source files and knowledge files
- Batch change detection for efficient processing

**KnowledgeBuilder (`knowledge_builder.py`)**
- Builds structured knowledge files using strands_agent_driver
- Implements LLM-powered content summarization with context awareness
- Maintains structured knowledge file format consistency

**SpecialHandlers (`special_handlers.py`)**
- GitCloneHandler: Manages read-only git clones with mirrored knowledge structure
- ProjectBaseHandler: Handles whole project codebase indexing (excluding .git, .knowledge, .coding_assistant)

### Knowledge File Format Specification

#### Hierarchical Semantic Context Pattern
Each directory level has a corresponding `<subdirectory_name>_kb.md` file:
- `.knowledge/git-clones/` → `.knowledge/git-clones_kb.md`
- `.knowledge/git-clones/cline/` → `.knowledge/git-clones/cline_kb/` (mirrored structure)
- `.knowledge/project-base/src/components/` → `.knowledge/project-base/src/components_kb.md`

#### Standard Knowledge File Structure
```markdown
# Summary

<Summary of below markdown items>

## Summary section of <subdirectory>/<each_subdirectory_knowledge_files>_kb.md

<Summary section of <subdirectory>/<subdirectories>_kb.md>

## Summary of <subdirectory>/<file>    <!-- For each files in <subdirectory> -->
 
<Summary of <subdirectory>/<file>>

# End of <subdirectory>_kb.md
```

#### Content Generation Principles
- **Intemporal Writing**: All knowledge entries written in present tense, stating facts rather than referencing past implementations
- **Hierarchical Assembly**: Parent knowledge files built from child summaries
- **Context Preservation**: Maintain essential information describing content of respective subdirectories
- **LLM Integration**: Use strands_agent_driver for consistent, high-quality summarization

### Special Handling Requirements

#### Git-Clones Special Case
- **Read-Only Constraint**: Git clones in `.knowledge/git-clones/` must remain untouched
- **Mirrored Knowledge Structure**: Create `<git_clone_name>_kb/` subdirectory with hierarchy mirroring original
- **Knowledge File Location**: Knowledge files created in mirrored structure, not in original git clone
- **Example**: 
  - Original: `.knowledge/git-clones/cline/src/extension.ts`
  - Knowledge: `.knowledge/git-clones/cline_kb/src/extension_kb.md`

#### Project-Base Special Case
- **Whole Codebase Indexing**: Index entire project code base into `.knowledge/project-base/`
- **Exclusion Rules**: Exclude `.git`, `.knowledge`, `.coding_assistant` directories
- **Mirroring Strategy**: Same as git-clones but for project root structure
- **Large File Handling**: Implement chunking for files exceeding size limits

### FastMCP Tools Integration

#### Tools Declaration (JESSE Standards Compliant)
```python
@server.tool("knowledge_bases_index_trigger", description="Manually trigger knowledge base indexing for specified path or entire hierarchy with configurable options")
async def knowledge_bases_index_trigger(ctx: Context, ...):
    # Implementation with three-section documentation pattern

@server.tool("knowledge_bases_search", description="Search across indexed knowledge bases using hierarchical context with natural language queries")  
async def knowledge_bases_search(ctx: Context, ...):
    # Future implementation
```

#### Resources Declaration (JESSE Standards Compliant)
```python
@server.resource("jesse://knowledge-bases/index-status", description="Display current indexing status, statistics, and knowledge hierarchy health")
async def knowledge_bases_index_status(ctx: Context):
    # Implementation with three-section documentation pattern

@server.resource("jesse://knowledge-bases/hierarchy-overview", description="Display knowledge hierarchy structure and metadata for all indexed knowledge bases")
async def knowledge_bases_hierarchy_overview(ctx: Context):
    # Implementation with three-section documentation pattern
```

### Technical Implementation Details

#### Indexing Workflow Algorithm
1. **Discovery Phase**: Scan knowledge hierarchy for existing structure
2. **Change Detection**: Identify stale knowledge files using timestamp comparison
3. **Leaf-First Processing**: Update knowledge files starting from deepest directories
4. **Content Generation**: Use strands_agent_driver to generate summaries
5. **Hierarchical Assembly**: Build parent knowledge files from child summaries

#### Strands Agent Driver Integration
- **LLM Operations**: All content summarization through existing strands_agent_driver
- **Context Awareness**: Pass hierarchical context to LLM for better summarization
- **Error Handling**: Robust error handling for LLM failures with fallback strategies
- **Batch Processing**: Efficient batching for multiple file processing

#### Change Detection Strategy
- **Timestamp Comparison**: Compare file modification times with knowledge file timestamps
- **Dependency Tracking**: Track which knowledge files depend on which source files
- **Incremental Updates**: Only update knowledge files when source content changes
- **Batch Processing**: Group related changes for efficient processing

#### Error Handling & Recovery
- **Defensive Programming**: Comprehensive error handling following existing patterns
- **Partial Failure Recovery**: Handle individual file failures without stopping entire process
- **Progress Reporting**: Detailed progress updates through FastMCP Context
- **Rollback Capability**: Ability to rollback partial changes on critical failures

### Configuration & Models

#### IndexingConfig Model
```python
@dataclass
class IndexingConfig:
    max_file_size: int = 1024 * 1024  # 1MB max per file
    excluded_extensions: Set[str] = {'.pyc', '.git', '__pycache__'}
    llm_model: str = "claude-3-5-sonnet"
    chunk_size: int = 4000  # For large files
    batch_size: int = 10   # Files per batch
    enable_git_clone_indexing: bool = True
    enable_project_base_indexing: bool = True
```

#### Knowledge Context Models
- **DirectoryContext**: Represents directory structure and metadata
- **FileContext**: Represents individual file context and summary
- **ChangeInfo**: Tracks file changes and update requirements
- **IndexingStatus**: Overall indexing operation status and statistics

## Task Learnings

### Key Discoveries
- **Claude 4 Sonnet Model ID**: Must use `"us.anthropic.claude-sonnet-4-20250514-v1:0"` as defined in `llm/strands_agent_driver/models.py`
- **Hierarchical Processing Constraint**: Leaf-first, bottom-up ONLY - parent summaries built FROM child summaries, never parent context passed to child processing
- **Implementation Priority**: Core indexing engine first (HierarchicalIndexer → ChangeDetector → KnowledgeBuilder), then special handlers

### Patterns Identified
- **Bottom-Up Assembly Pattern**: Process files in deepest directories independently, then build parent summaries from completed child summaries
- **Aggregative Hierarchy**: Each directory level aggregates information from its children without passing context downward
- **Independent Processing**: Each file/directory processes in isolation before contributing to parent summary

### Challenges & Solutions
- **Context Flow Direction**: Corrected understanding that hierarchy is purely aggregative (child → parent), not contextual (parent → child)
- **Model Configuration**: Use strands_agent_driver's Claude4SonnetConfig.create_optimized_for_analysis() for consistent summarization
- **Processing Algorithm**: Depth-first discovery, leaf processing, child-to-parent assembly pattern

## Task Resources

### External Links
- [FastMCP Documentation](https://fastmcp.readthedocs.io/)
- [Strands Agent SDK](https://github.com/strands-agents/sdk-python)
- [JESSE Framework Documentation](../../../README.md)

### Reference Materials
- `jesse-framework-mcp/jesse_framework_mcp/embedded_content/JESSE_CODE_COMMENTS.md`
- `jesse-framework-mcp/llm/strands_agent_driver/`
- `jesse-framework-mcp/jesse_framework_mcp/helpers/`
- `.knowledge/git-clones/fastmcp_kb.md`

### Tools & APIs
- FastMCP Framework for MCP server integration
- Strands Agent Driver for LLM operations
- Python pathlib for cross-platform file operations
- Python asyncio for async programming patterns
