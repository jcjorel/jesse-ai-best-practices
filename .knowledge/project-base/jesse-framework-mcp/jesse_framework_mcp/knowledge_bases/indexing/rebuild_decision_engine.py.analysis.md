<!-- CACHE_METADATA_START -->
<!-- Source File: {PROJECT_ROOT}/jesse-framework-mcp/jesse_framework_mcp/knowledge_bases/indexing/rebuild_decision_engine.py -->
<!-- Cached On: 2025-07-07T00:57:12.677311 -->
<!-- Source Modified: 2025-07-07T00:46:11.813017 -->
<!-- Cache Version: 1.0 -->
<!-- CACHE_METADATA_END -->

#### Functional Intent & Features

Centralized decision engine consolidating all rebuild and deletion decision logic for the Jesse Framework MCP knowledge base hierarchical indexing system. Provides single source of truth for processing decisions eliminating scattered logic across multiple components through `RebuildDecisionEngine` class with comprehensive staleness checking via `FileAnalysisCache` integration. Enables developers to make consistent, auditable decisions about file rebuilds, directory processing, and orphaned content cleanup with rich audit trails and performance optimization. Key semantic entities include `RebuildDecisionEngine`, `DecisionReport`, `RebuildDecision`, `DeletionDecision`, `DecisionOutcome`, `DecisionReason`, `FileAnalysisCache`, `ProjectBaseHandler`, `GitCloneHandler`, `DirectoryContext`, `FileContext`, `IndexingConfig`, `fastmcp.Context`, `pathlib.Path`, and `datetime` for comprehensive decision-making operations using file-first optimization approach preventing unnecessary directory rebuilds when only individual files are stale.

##### Main Components

Core `RebuildDecisionEngine` class serving as the primary decision-making component with comprehensive analysis methods including `analyze_hierarchy()` for full directory tree processing, `_analyze_file_rebuild_decisions()` and `_analyze_directory_rebuild_decisions()` for targeted processing, and `_analyze_deletion_decisions()` for orphaned content cleanup. Supporting decision factory methods `_create_rebuild_decision()` and `_create_deletion_decision()` for standardized decision object creation. Consolidated helper methods including `_get_file_timestamp_safe()`, `_is_timestamp_newer()`, `_calculate_cache_path_safe()`, and path mapping utilities for consistent filesystem operations. Public interface methods `should_rebuild_directory()`, `should_cleanup_orphaned_analysis()`, and `is_cache_fresh()` for external component integration.

###### Architecture & Design

Implements centralized decision architecture consolidating scattered logic from multiple components into single authoritative decision point with comprehensive audit trails. Uses file-first optimization approach analyzing individual file staleness before directory-level decisions to prevent unnecessary rebuilds. Integrates with existing `FileAnalysisCache` for performance-optimized staleness checking and special handlers (`ProjectBaseHandler`, `GitCloneHandler`) for scenario-specific processing. Employs selective cascading pattern where content-driven rebuilds automatically trigger ancestor directory rebuilds through `_propagate_cascading_decisions()`. Implements defensive programming with graceful error handling ensuring decision failures don't break overall processing workflow.

####### Implementation Approach

Executes four-phase analysis workflow: Phase 1 analyzes individual file rebuild decisions using cache staleness checking, Phase 2 analyzes directory rebuild decisions considering file-level outcomes, Phase 3 detects orphaned files for deletion decisions, and Phase 4 implements selective cascading propagating rebuild decisions up hierarchy. Uses timestamp-based staleness detection through direct comparison without tolerance for consistent behavior across components. Implements comprehensive path mapping between source files and knowledge base structure using project-base directory mirroring. Employs consolidated helper methods eliminating DRY violations and providing consistent error handling patterns across all decision operations.

######## External Dependencies & Integration Points

**→ Inbound:**
- `fastmcp.Context` - FastMCP framework context interface for async logging and progress reporting
- `jesse_framework_mcp.knowledge_bases.models:IndexingConfig` - Configuration object providing filtering rules and output directory settings
- `jesse_framework_mcp.knowledge_bases.models:DirectoryContext` - Directory structure representation with file and subdirectory contexts
- `jesse_framework_mcp.knowledge_bases.models:FileContext` - Individual file metadata including path, size, and modification timestamps
- `jesse_framework_mcp.knowledge_bases.models.rebuild_decisions` - Decision model classes for structured outcomes and reasoning
- `jesse_framework_mcp.knowledge_bases.indexing.file_analysis_cache:FileAnalysisCache` - Cache staleness checking and performance optimization
- `jesse_framework_mcp.knowledge_bases.indexing.special_handlers` - Project-base and git-clone scenario handlers
- `pathlib.Path` (external library) - Cross-platform path operations and filesystem metadata access
- `datetime` (external library) - Timestamp comparison and decision timing calculations
- `asyncio` (external library) - Async execution framework for concurrent decision processing

**← Outbound:**
- `jesse_framework_mcp.knowledge_bases.indexing.plan_generator:PlanGenerator` - Consumes decision reports for execution planning
- `jesse_framework_mcp.knowledge_bases.indexing.hierarchical_indexer:HierarchicalIndexer` - Uses rebuild decisions for processing coordination
- Knowledge base processing pipeline - Receives structured decision reports with rebuild and deletion instructions
- Monitoring and logging systems - Consumes performance statistics and decision audit trails

**⚡ System role and ecosystem integration:**
- **System Role**: Core decision-making component serving as single source of truth for all rebuild and deletion decisions within the Jesse Framework MCP knowledge base indexing system
- **Ecosystem Position**: Central component eliminating scattered decision logic across multiple indexing components while providing comprehensive audit trails and performance optimization
- **Integration Pattern**: Used by hierarchical indexer and plan generator for coordinated processing decisions, with results feeding into execution planning and monitoring systems

######### Edge Cases & Error Handling

Handles empty directories by detecting contentless directories and skipping knowledge file generation to prevent infinite rebuild loops through `_is_directory_empty_of_processable_content()`. Manages project root specially ensuring `root_kb.md` generation follows business rules while applying standard staleness checking. Implements graceful filesystem error handling with conservative fallback decisions when file access fails or path calculations encounter errors. Provides comprehensive orphaned file detection with safety validation preventing accidental deletion of valid content. Uses consolidated error handling patterns through `_handle_decision_error()` creating standardized error decisions with detailed context information for debugging and recovery.

########## Internal Implementation Details

Maintains performance tracking through `_decisions_made`, `_filesystem_operations`, and `_decision_start_time` counters for optimization monitoring. Uses cached `_project_base_root` path for performance optimization in repeated path calculations. Implements consolidated helper methods eliminating DRY violations including timestamp retrieval, path calculation, and decision creation patterns. Employs direct timestamp comparison without tolerance aligning with `FileAnalysisCache` behavior for consistent staleness detection. Tracks cascading decisions through ancestor path calculation using `_get_ancestor_directories()` with safety limits preventing infinite traversal loops.

########### Code Usage Examples

Essential decision engine initialization and hierarchy analysis pattern:

```python
# Initialize decision engine with configuration for centralized decision making
config = IndexingConfig(output_config=OutputConfig(knowledge_output_directory=knowledge_dir))
decision_engine = RebuildDecisionEngine(config)

# Perform comprehensive hierarchy analysis with file-first optimization
report = await decision_engine.analyze_hierarchy(root_context, source_root, ctx)

# Access structured decision results for execution planning
stats = report.get_summary_statistics()
rebuild_decisions = report.rebuild_decisions
deletion_decisions = report.deletion_decisions
```

Individual decision making for external component integration:

```python
# Make single directory rebuild decision for targeted processing
directory_decision = await decision_engine.should_rebuild_directory(
    directory_context, source_root, ctx
)

# Check cache freshness for individual file processing optimization
is_fresh, reason = decision_engine.is_cache_fresh(file_path, source_root)

# Determine orphaned file cleanup status for maintenance operations
cleanup_outcome, cleanup_reason = await decision_engine.should_cleanup_orphaned_analysis(
    analysis_file_path, source_root, ctx
)
```