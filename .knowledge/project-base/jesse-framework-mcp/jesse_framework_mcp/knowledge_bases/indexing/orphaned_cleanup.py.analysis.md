<!-- CACHE_METADATA_START -->
<!-- Source File: {PROJECT_ROOT}/jesse-framework-mcp/jesse_framework_mcp/knowledge_bases/indexing/orphaned_cleanup.py -->
<!-- Cached On: 2025-07-05T13:45:42.820905 -->
<!-- Source Modified: 2025-07-05T13:39:43.540651 -->
<!-- Cache Version: 1.0 -->
<!-- CACHE_METADATA_END -->

#### Functional Intent & Features

This file implements orphaned analysis cleanup management for the Jesse Framework MCP knowledge base system, designed to remove analysis files and knowledge files that no longer have corresponding source files, ensuring knowledge base accuracy and preventing stale artifact accumulation. The module provides comprehensive cleanup capabilities including orphaned `.analysis.md` file removal, orphaned `_kb.md` knowledge file cleanup, and empty directory pruning while maintaining mirror directory structure integrity. Key semantic entities include `OrphanedAnalysisCleanup` class with `cleanup_orphaned_files` method, `CleanupStats` dataclass for metrics tracking, `FileAnalysisCache` integration for path calculations, `FastMCP` context for progress reporting, leaf-first directory traversal with `_collect_directories_leaf_first`, three-phase cleanup strategy, reverse path mapping methods `_get_source_path_from_analysis_file` and `_get_source_directory_from_mirrored_path`, and comprehensive error handling with graceful degradation. The system implements conservative deletion approach only removing confirmed orphaned artifacts while preserving valid knowledge base structure and providing detailed audit trail through statistics and logging.

##### Main Components

The file contains the `OrphanedAnalysisCleanup` class as the primary cleanup orchestrator with key methods including `cleanup_orphaned_files` for comprehensive cleanup workflow, `_collect_directories_leaf_first` for safe traversal ordering, `_cleanup_directory` for per-directory processing, `_cleanup_orphaned_analysis_files` for `.analysis.md` removal, `_cleanup_orphaned_knowledge_files` for `_kb.md` cleanup, and `_cleanup_empty_directory` for directory pruning. The `CleanupStats` dataclass provides comprehensive metrics tracking with properties for `total_files_deleted`, `total_items_deleted`, `cleanup_duration`, and error collection through `add_error` method. Supporting utility methods include `_get_source_path_from_analysis_file` and `_get_source_directory_from_mirrored_path` for reverse path calculation enabling source file verification. The class integrates `FileAnalysisCache` for consistent path calculations and maintains detailed statistics throughout all cleanup operations.

###### Architecture & Design

The architecture implements a three-phase cleanup strategy with clear separation between analysis file cleanup, knowledge file cleanup, and directory pruning operations. The design follows leaf-first processing pattern ensuring child directories are processed before parents, eliminating cleanup dependencies and enabling safe bottom-up directory removal. The system uses conservative deletion approach with explicit source file verification before removing any artifacts, preventing accidental deletion of valid knowledge base components. Key design patterns include the orchestrator pattern for workflow coordination, dataclass-based statistics tracking for comprehensive metrics, integration with existing `FileAnalysisCache` for consistent business logic, and async-first architecture supporting non-blocking operations with `FastMCP` context integration for real-time progress reporting.

####### Implementation Approach

The implementation uses leaf-first directory traversal with `_collect_directories_leaf_first` creating ordered processing queue ensuring safe cleanup dependencies. The system implements three-phase cleanup strategy starting with orphaned analysis file removal, followed by orphaned knowledge file cleanup, and concluding with empty directory pruning. Key algorithms include reverse path calculation mapping cache file paths back to source file locations, directory emptiness verification checking for both files and subdirectories, and mirror structure preservation logic preventing deletion when corresponding source directories exist. The approach integrates comprehensive error handling continuing cleanup operations despite individual failures, detailed statistics tracking with timing and error collection, and conservative deletion verification requiring explicit source file absence before artifact removal.

######## External Dependencies & Integration Points

**→ Inbound:**
- `..models:IndexingConfig` - configuration and path calculation utilities for cleanup behavior
- `.file_analysis_cache:FileAnalysisCache` - cache path calculation and knowledge file location logic
- `fastmcp:Context` - MCP context for progress reporting and user interaction
- `pathlib` (external library) - cross-platform path operations and filesystem interaction
- `logging` (external library) - structured logging for cleanup operations and debugging
- `asyncio` (external library) - async programming patterns for non-blocking operations
- `datetime` (external library) - timing information for performance analysis
- `dataclasses` (external library) - statistics container implementation

**← Outbound:**
- `hierarchical_indexer.py:HierarchicalIndexer` - integrated as Phase 1.7 in indexing workflow
- Knowledge base maintenance workflows - cleanup operations for stale artifact removal
- MCP server cleanup operations - maintenance functionality for knowledge base integrity

**⚡ System role and ecosystem integration:**
- **System Role**: Specialized maintenance component within Jesse Framework MCP knowledge base indexing pipeline, ensuring knowledge base accuracy by removing orphaned artifacts
- **Ecosystem Position**: Auxiliary component providing critical maintenance functionality integrated into the hierarchical indexing workflow as Phase 1.7 cleanup operation
- **Integration Pattern**: Invoked by `HierarchicalIndexer` during indexing workflow phases, with direct integration to `FileAnalysisCache` for consistent path calculation and business rule enforcement

######### Edge Cases & Error Handling

The system handles comprehensive error scenarios including filesystem access failures during directory traversal with graceful skipping and continued processing, individual file deletion failures with detailed error tracking and statistics updates, and path calculation errors returning `None` for safety in reverse mapping operations. Error handling includes permission errors during file and directory operations with comprehensive logging, concurrent access scenarios during cleanup operations, and malformed directory structures with defensive programming approaches. The implementation provides configurable error behavior through comprehensive error collection in `CleanupStats.errors`, detailed logging with `exc_info=True` for debugging support, and graceful degradation ensuring partial cleanup completion when individual operations fail. Special handling includes project-base root directory protection preventing structural damage, mirror structure preservation when source directories exist, and conservative deletion approach requiring explicit verification before artifact removal.

########## Internal Implementation Details

Internal mechanics include leaf-first directory collection using recursive depth-first traversal with `collect_recursive` nested function, three-phase cleanup processing with separate methods for each cleanup type, and reverse path calculation algorithms mapping cache paths back to source locations. The implementation uses `FileAnalysisCache.get_knowledge_file_path()` for consistent knowledge file location logic, comprehensive statistics tracking with timing information and error collection, and defensive programming with extensive try-catch blocks preventing cascading failures. Key internal patterns include project-base relative path calculation for mirror structure mapping, directory emptiness verification checking both files and subdirectories, and source directory existence verification for mirror structure preservation. The system maintains detailed audit trail through structured logging and statistics collection, handles component lifecycle through proper initialization and error recovery, and provides comprehensive metrics through `CleanupStats.to_dict()` for reporting and analysis.

########### Code Usage Examples

Basic orphaned analysis cleanup integration within indexing workflow:

```python
# Initialize and execute orphaned analysis cleanup as part of indexing workflow
from jesse_framework_mcp.knowledge_bases.indexing.orphaned_cleanup import OrphanedAnalysisCleanup
from jesse_framework_mcp.knowledge_bases.models import IndexingConfig
from fastmcp import Context

# Create cleanup component with configuration
config = IndexingConfig(knowledge_output_directory=Path("./knowledge"))
cleanup = OrphanedAnalysisCleanup(config)

# Execute comprehensive cleanup with progress reporting
async with Context() as ctx:
    stats = await cleanup.cleanup_orphaned_files(
        knowledge_root=Path("./knowledge"),
        source_root=Path("./source"),
        ctx=ctx
    )
    print(f"Cleanup completed: {stats.total_items_deleted} items removed in {stats.cleanup_duration:.2f}s")
```

Advanced cleanup statistics analysis and error handling pattern:

```python
# Execute cleanup with comprehensive statistics analysis and error reporting
cleanup = OrphanedAnalysisCleanup(config)

try:
    stats = await cleanup.cleanup_orphaned_files(knowledge_root, source_root, ctx)
    
    # Analyze cleanup results
    cleanup_report = stats.to_dict()
    print(f"Analysis files deleted: {stats.analysis_files_deleted}")
    print(f"Knowledge files deleted: {stats.knowledge_files_deleted}")
    print(f"Directories deleted: {stats.directories_deleted}")
    
    if len(stats.errors) > 0:
        print(f"Cleanup completed with {len(stats.errors)} errors:")
        for error in stats.errors[:5]:  # Show first 5 errors
            print(f"  - {error}")
            
except Exception as e:
    print(f"Cleanup operation failed: {e}")
```