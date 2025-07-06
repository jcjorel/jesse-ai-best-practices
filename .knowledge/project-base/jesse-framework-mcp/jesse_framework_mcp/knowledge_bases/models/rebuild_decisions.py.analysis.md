<!-- CACHE_METADATA_START -->
<!-- Source File: {PROJECT_ROOT}/jesse-framework-mcp/jesse_framework_mcp/knowledge_bases/models/rebuild_decisions.py -->
<!-- Cached On: 2025-07-07T01:01:40.569905 -->
<!-- Source Modified: 2025-07-07T00:44:47.912379 -->
<!-- Cache Version: 1.0 -->
<!-- CACHE_METADATA_END -->

#### Functional Intent & Features

Structured decision models providing immutable data structures for rebuild and deletion operations in the Jesse Framework MCP knowledge base hierarchical indexing system. Provides comprehensive decision outcome tracking through `RebuildDecision` and `DeletionDecision` classes with type-safe `DecisionOutcome` and `DecisionReason` enumerations, enabling centralized decision logic with clear audit trails and comprehensive action planning via `DecisionReport` class. Enables developers to create reliable, auditable decision workflows with rich reasoning capture, performance statistics, and execution coordination for all indexing operations. Key semantic entities include `DecisionOutcome`, `DecisionReason`, `RebuildDecision`, `DeletionDecision`, `DecisionReport`, `dataclasses.dataclass`, `dataclasses.field`, `enum.Enum`, `pathlib.Path`, `datetime.datetime`, and `typing` annotations for comprehensive decision modeling using immutable frozen dataclasses ensuring audit trail integrity and preventing post-creation modification.

##### Main Components

Core enumeration classes `DecisionOutcome` defining five possible outcomes (REBUILD, SKIP, DELETE, CREATE, ERROR) and `DecisionReason` providing comprehensive reasoning categories for all decision scenarios including rebuild reasons, skip reasons, delete reasons, create reasons, and error reasons. Immutable decision data classes `RebuildDecision` capturing rebuild outcomes with path, outcome, reason, reasoning text, timestamp, and metadata, and `DeletionDecision` capturing deletion outcomes with additional safety validation through `is_safe_to_delete` and `backup_recommended` flags. Comprehensive reporting class `DecisionReport` containing decision dictionaries, organized action lists, analysis metadata, and error tracking with methods for decision management, statistics calculation, and reasoning analysis.

###### Architecture & Design

Implements immutable decision architecture using frozen dataclasses ensuring audit trail integrity and preventing modification after creation. Uses type-safe enumeration design with `DecisionOutcome` and `DecisionReason` preventing ambiguous decision interpretation and enabling clear outcome validation. Employs comprehensive action planning through `DecisionReport` with separate decision dictionaries and organized action lists enabling targeted execution and error handling. Implements rich metadata capture with optional metadata dictionaries, timestamp tracking, and performance statistics collection supporting debugging and optimization requirements. Uses property-based decision validation with convenience properties like `should_rebuild`, `should_skip`, and `is_error` simplifying decision logic and conditional processing.

####### Implementation Approach

Uses frozen dataclass pattern with `@dataclass(frozen=True)` ensuring immutability and audit trail integrity while providing automatic initialization and field validation. Implements default factory pattern with `field(default_factory=datetime.now)` and `field(default_factory=dict)` for timestamp generation and metadata initialization. Employs dictionary-based decision storage with `Dict[Path, RebuildDecision]` and `Dict[Path, DeletionDecision]` enabling efficient path-based decision lookup and deduplication. Uses set-based action lists with `Set[Path]` for files_to_rebuild, files_to_delete, directories_to_create, and directories_to_delete ensuring unique operations and preventing duplicate actions. Implements comprehensive statistics calculation through decision counting and categorization with structured dictionary returns for monitoring integration.

######## External Dependencies & Integration Points

**→ Inbound:**
- `dataclasses` (external library) - Immutable decision object creation with automatic initialization and field validation
- `datetime` (external library) - Timestamp tracking for decision timing and audit trail construction
- `enum` (external library) - Type-safe decision outcome and reasoning enumeration with clear value definitions
- `pathlib.Path` (external library) - Cross-platform path operations and file system entity identification
- `typing` (external library) - Type annotations for decision object integrity and IDE support

**← Outbound:**
- `jesse_framework_mcp.knowledge_bases.indexing.rebuild_decision_engine:RebuildDecisionEngine` - Consumes decision models for centralized decision logic implementation
- `jesse_framework_mcp.knowledge_bases.indexing.plan_generator:PlanGenerator` - Uses decision reports for execution plan generation and task creation
- `jesse_framework_mcp.knowledge_bases.indexing.hierarchical_indexer:HierarchicalIndexer` - Receives decision reports for coordinated processing execution
- Monitoring and logging systems - Consume decision statistics and reasoning summaries for analysis and debugging
- Audit trail systems - Use immutable decision objects for compliance and troubleshooting requirements

**⚡ System role and ecosystem integration:**
- **System Role**: Foundational data model layer providing structured decision representation for all rebuild and deletion operations within the Jesse Framework MCP knowledge base indexing system
- **Ecosystem Position**: Core infrastructure component enabling centralized decision logic by providing immutable, type-safe decision objects with comprehensive audit trails and action planning capabilities
- **Integration Pattern**: Used by decision engines and execution planners as primary data structures for decision communication, with decision reports serving as comprehensive action plans for coordinated processing workflows

######### Edge Cases & Error Handling

Handles missing decisions through `get_decision_for_path()` returning `None` when no decision exists for specified path, enabling graceful handling of incomplete decision scenarios. Manages decision errors through dedicated `DecisionOutcome.ERROR` and error-specific `DecisionReason` values like `FILESYSTEM_ERROR`, `ACCESS_DENIED`, and `DECISION_ERROR` with comprehensive error tracking in `decision_errors` list. Provides safety validation for deletion decisions through `is_safe_to_delete` boolean flag and `backup_recommended` flag preventing accidental data loss and supporting rollback scenarios. Implements comprehensive error detection through `has_errors()` method checking both decision_errors list and individual decision outcomes for error conditions. Uses immutable design preventing accidental modification of decision objects after creation, ensuring audit trail integrity even in error scenarios.

########## Internal Implementation Details

Uses frozen dataclass implementation with automatic `__init__`, `__repr__`, and `__eq__` generation while preventing attribute modification through `frozen=True` parameter. Implements default factory pattern for mutable default values using `field(default_factory=dict)` and `field(default_factory=set)` preventing shared mutable defaults across instances. Maintains decision consistency through automatic action list updates in `add_rebuild_decision()` and `add_deletion_decision()` methods ensuring decision records match execution lists. Uses path-based dictionary keys enabling efficient O(1) decision lookup and preventing duplicate decisions for same paths. Implements comprehensive statistics calculation through list comprehensions and filtering operations providing real-time decision analysis and monitoring capabilities.

########### Code Usage Examples

Essential decision creation and management pattern for rebuild operations. This pattern demonstrates how to create immutable decision objects and integrate them with comprehensive reporting systems for coordinated processing workflows.

```python
# Create immutable rebuild decision with comprehensive metadata and reasoning
rebuild_decision = RebuildDecision(
    path=Path("src/components/button.py"),
    outcome=DecisionOutcome.REBUILD,
    reason=DecisionReason.CACHE_STALE,
    reasoning_text="Source file is newer than analysis cache",
    metadata={"file_size": 1024, "cache_age": 3600}
)

# Add decision to report for comprehensive action planning
report = DecisionReport()
report.add_rebuild_decision(rebuild_decision)

# Access decision properties for conditional processing
if rebuild_decision.should_rebuild:
    print(f"Rebuilding {rebuild_decision.path}")
```

Comprehensive decision reporting and analysis for monitoring and debugging. This approach enables detailed decision analysis and execution coordination through structured reporting and statistics generation.

```python
# Create deletion decision with safety validation and backup recommendation
deletion_decision = DeletionDecision(
    path=Path("cache/orphaned_file.md"),
    outcome=DecisionOutcome.DELETE,
    reason=DecisionReason.ORPHANED_ANALYSIS_CACHE,
    reasoning_text="Analysis cache has no corresponding source file",
    is_safe_to_delete=True,
    backup_recommended=False
)

# Generate comprehensive statistics and reasoning analysis
stats = report.get_summary_statistics()
reasoning_summary = report.get_reasoning_summary()
has_errors = report.has_errors()

# Access organized action lists for execution coordination
files_to_rebuild = report.files_to_rebuild
files_to_delete = report.files_to_delete
```