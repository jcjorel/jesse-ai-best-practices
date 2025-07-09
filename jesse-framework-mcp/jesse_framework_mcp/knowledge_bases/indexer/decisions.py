###############################################################################
# IMPORTANT: This header comment is designed for GenAI code review and maintenance
# Any GenAI tool working with this file MUST preserve and update this header
###############################################################################
# [GenAI coding tool directive]
# - Maintain this header with all modifications
# - Update History section with each change
# - Keep only the 4 most recent records in the history section. Sort from newer to older.
# - Preserve Intent, Design, and Constraints sections
# - Use this header as context for code reviews and modifications
# - Ensure all changes align with the design principles
# - Respect system prompt directives at all times
###############################################################################
# [Source file intent]
# Clean decision engine for converting discovery results into execution tasks.
# Analyzes knowledge file status (orphaned, stale, fresh) and generates
# appropriate atomic tasks for analysis, synthesis, and cleanup operations.
###############################################################################
# [Source file design principles]
# - Clear status-to-task conversion logic
# - Single responsibility decision making
# - Fail-fast validation with comprehensive error reporting
# - Task dependency analysis for proper execution ordering
# - Extensible decision rules for different scenarios
###############################################################################
# [Source file constraints]
# - Must generate tasks based on discovery outcomes only
# - No FastMCP dependencies for clean architecture
# - Exception-first error handling - no fallback mechanisms
# - Must support both project-base and git-clone content types
###############################################################################
# [Dependencies]
# <system>:pathlib.Path
# <system>:typing.List
# <system>:typing.Dict
# <system>:typing.Optional
# <system>:dataclasses.dataclass
# <system>:dataclasses.field
# <codebase>:jesse_framework_mcp.knowledge_bases.indexer.models.KnowledgeFile
# <codebase>:jesse_framework_mcp.knowledge_bases.indexer.models.ProgressCallback
###############################################################################
# [GenAI tool change history]
# 2025-07-09T13:31:00Z : Initial decision engine implementation by CodeAssistant
# * Created TaskDecision dataclass for decision outcomes
# * Implemented DecisionEngine for status-to-task conversion
# * Added StalenessAnalyzer for detailed staleness assessment
# * Implemented OrphanDetector for cleanup task generation
###############################################################################

from pathlib import Path
from typing import List, Dict, Optional
from dataclasses import dataclass, field

from .models import KnowledgeTree, BaseIndexedFile, AnalysisFile, KnowledgeBaseFile, ProgressCallback


@dataclass
class TaskDecision:
    """
    [Class intent]
    Represents a decision to create a specific task based on knowledge file analysis.
    Contains task type, priority, and all necessary parameters for task creation.

    [Design principles]
    Single decision outcome with clear task specification.
    Priority-based task ordering for execution planning.
    Complete parameter specification for task creation.

    [Implementation details]
    task_type corresponds to AtomicTask implementation types.
    priority enables dependency-aware execution ordering.
    parameters contain all data needed for task execution.
    """
    task_type: str
    task_id: str
    priority: int  # Lower numbers = higher priority
    source_path: Optional[Path] = None
    knowledge_path: Optional[Path] = None
    cache_path: Optional[Path] = None
    parameters: Dict[str, any] = field(default_factory=dict)
    dependencies: List[str] = field(default_factory=list)
    reason: str = ""




class DecisionEngine:
    """
    [Class intent]
    Main decision engine for converting discovery results into execution tasks.
    Analyzes knowledge file status and generates appropriate atomic task decisions
    for analysis, synthesis, and cleanup operations.

    [Design principles]
    Clear status-to-task conversion with comprehensive decision logic.
    Priority-based task generation for execution planning.
    Extensible decision rules for different content scenarios.

    [Implementation details]
    Uses StalenessAnalyzer and OrphanDetector for detailed analysis.
    Generates TaskDecision objects for each required operation.
    Provides comprehensive progress reporting for decision process.
    """
    
    def __init__(self):
        """
        [Class method intent]
        Initialize decision engine for tree-based decision making.

        [Design principles]
        Simple initialization for clean tree-based architecture.

        [Implementation details]
        No additional components needed - tree provides all status information.
        """
        pass
    
    async def make_decisions(
        self, 
        knowledge_tree: KnowledgeTree, 
        progress: Optional[ProgressCallback] = None
    ) -> List[TaskDecision]:
        """
        [Class method intent]
        Analyze knowledge tree and generate task decisions for execution.

        [Design principles]
        Comprehensive decision making covering all file states.
        Priority-based task generation for proper execution ordering.
        Clear progress reporting for long-running analysis.

        [Implementation details]
        Processes each knowledge file in tree through staleness analysis.
        Generates appropriate task decisions based on file status.
        Combines all decisions with proper priority ordering.
        """
        if progress:
            progress("🤔 Starting tree-based decision making process...")
        
        all_decisions = []
        
        # Get all files from the knowledge tree
        all_files = list(knowledge_tree.get_all_files())
        
        # Generate decisions for each knowledge file
        for i, indexed_file in enumerate(all_files):
            if progress and i % 20 == 0:  # Progress every 20 files
                file_type_desc = "analysis files" if isinstance(indexed_file, AnalysisFile) else "knowledge base files"
                progress(f"🔬 Analyzing {file_type_desc}: {i+1}/{len(all_files)}")
            
            try:
                # Generate task decisions based on file status
                file_decisions = self._generate_tree_task_decisions(indexed_file)
                all_decisions.extend(file_decisions)
                
            except Exception as e:
                error_msg = f"Failed to analyze indexed file {indexed_file.path}: {str(e)}"
                if progress:
                    progress(f"ERROR: {error_msg}")
                raise RuntimeError(error_msg) from e
        
        # Generate cleanup decisions for orphaned files
        if progress:
            progress("🧹 Detecting orphaned files for cleanup...")
        
        cleanup_decisions = self._detect_tree_orphans(all_files)
        all_decisions.extend(cleanup_decisions)
        
        # Sort decisions by priority
        all_decisions.sort(key=lambda d: d.priority)
        
        # Count decision types for reporting
        decision_counts = {}
        for decision in all_decisions:
            decision_counts[decision.task_type] = decision_counts.get(decision.task_type, 0) + 1
        
        if progress:
            progress(f"✅ Decision making complete: {len(all_decisions)} tasks generated")
            for task_type, count in decision_counts.items():
                progress(f"  📋 {task_type}: {count} tasks")
        
        return all_decisions
    
    def _generate_tree_task_decisions(self, indexed_file: BaseIndexedFile) -> List[TaskDecision]:
        """
        [Class method intent]
        Generate task decisions based on tree-based indexed file status.

        [Design principles] 
        Tree-based decision making using file status and staleness.
        Direct status evaluation without additional analysis layers.

        [Implementation details]
        Uses file's built-in status and staleness methods.
        Generates appropriate tasks based on UpdateStatus and file type.
        """
        decisions = []
        
        # Skip fresh files that don't need updates
        if indexed_file.update_status.value in ['fresh', 'updated_success']:
            return decisions
        
        # Generate cleanup tasks for orphaned files
        if indexed_file.update_status.value == 'orphaned':
            task_id = f"cleanup_{indexed_file.handler_type}_{indexed_file.path.name}_{id(indexed_file)}"
            
            decision = TaskDecision(
                task_type="cleanup",
                task_id=task_id,
                priority=90,  # Low priority - cleanup after other tasks
                knowledge_path=indexed_file.path,
                parameters={
                    'handler_type': indexed_file.handler_type,
                    'orphan_reason': 'File marked as orphaned during discovery'
                },
                dependencies=[],
                reason=f"Cleanup orphaned file: {indexed_file.path}"
            )
            decisions.append(decision)
            
        # Generate tasks for stale or missing files
        elif indexed_file.update_status.value in ['stale', 'missing']:
            if isinstance(indexed_file, AnalysisFile):
                # Generate file analysis task
                task_id = f"analyze_file_{indexed_file.handler_type}_{indexed_file.path.stem}_{id(indexed_file)}"
                
                decision = TaskDecision(
                    task_type="analyze_file",
                    task_id=task_id,
                    priority=10,  # High priority - analyze files first
                    source_path=indexed_file.source_file,
                    cache_path=indexed_file.path,
                    parameters={
                        'handler_type': indexed_file.handler_type,
                        'analysis_reason': f'Analysis file is {indexed_file.update_status.value}'
                    },
                    dependencies=[],
                    reason=f"Analyze {indexed_file.update_status.value} source file: {indexed_file.source_file}"
                )
                decisions.append(decision)
                
            elif isinstance(indexed_file, KnowledgeBaseFile):
                # Generate knowledge base build task
                task_id = f"build_kb_{indexed_file.handler_type}_{indexed_file.path.stem}_{id(indexed_file)}"
                
                decision = TaskDecision(
                    task_type="build_knowledge_base",
                    task_id=task_id,
                    priority=50,  # Medium priority - after file analysis
                    source_path=indexed_file.source_directory,
                    knowledge_path=indexed_file.path,
                    parameters={
                        'handler_type': indexed_file.handler_type,
                        'rebuild_reason': f'Knowledge base is {indexed_file.update_status.value}'
                    },
                    dependencies=[],
                    reason=f"Build {indexed_file.update_status.value} knowledge base: {indexed_file.path}"
                )
                decisions.append(decision)
        
        return decisions
    
    def _detect_tree_orphans(self, all_files: List[BaseIndexedFile]) -> List[TaskDecision]:
        """
        [Class method intent]
        Detect orphaned files in the knowledge tree and generate cleanup tasks.

        [Design principles]
        Conservative orphan detection using tree status.
        Clear cleanup task generation with proper priorities.

        [Implementation details]
        Filters files by orphaned status from the tree.
        Generates cleanup tasks for confirmed orphans.
        """
        cleanup_decisions = []
        orphaned_files = [f for f in all_files if f.update_status.value == 'orphaned']
        
        for orphaned_file in orphaned_files:
            task_id = f"cleanup_orphan_{orphaned_file.handler_type}_{orphaned_file.path.name}_{id(orphaned_file)}"
            
            decision = TaskDecision(
                task_type="cleanup",
                task_id=task_id,
                priority=95,  # Very low priority - cleanup after everything else
                knowledge_path=orphaned_file.path,
                parameters={
                    'handler_type': orphaned_file.handler_type,
                    'orphan_reason': 'File has no corresponding source (detected in tree)'
                },
                dependencies=[],
                reason=f"Cleanup orphaned file: {orphaned_file.path}"
            )
            cleanup_decisions.append(decision)
        
        return cleanup_decisions
    
    
    def get_decision_summary(self, decisions: List[TaskDecision]) -> Dict[str, any]:
        """
        [Class method intent]
        Generate summary statistics for decision outcomes.

        [Design principles]
        Clear reporting of decision results for monitoring.

        [Implementation details]
        Counts decisions by type, priority, and handler.
        Provides comprehensive decision analysis summary.
        """
        summary = {
            'total_decisions': len(decisions),
            'by_task_type': {},
            'by_priority': {},
            'by_handler_type': {},
            'dependency_count': 0
        }
        
        for decision in decisions:
            # Count by task type
            task_type = decision.task_type
            summary['by_task_type'][task_type] = summary['by_task_type'].get(task_type, 0) + 1
            
            # Count by priority
            priority = decision.priority
            summary['by_priority'][priority] = summary['by_priority'].get(priority, 0) + 1
            
            # Count by handler type
            handler_type = decision.parameters.get('handler_type', 'unknown')
            summary['by_handler_type'][handler_type] = summary['by_handler_type'].get(handler_type, 0) + 1
            
            # Count dependencies
            summary['dependency_count'] += len(decision.dependencies)
        
        return summary
