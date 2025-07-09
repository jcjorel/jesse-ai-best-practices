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
# Main orchestrator for clean knowledge bases indexer with two-subphase discovery.
# Coordinates complete indexing workflow from discovery through execution with
# comprehensive monitoring, error handling, and dry-run capabilities.
###############################################################################
# [Source file design principles]
# - Complete workflow orchestration with clear phase separation
# - Two-subphase discovery pattern as originally specified
# - Exception-first error handling with comprehensive monitoring
# - Dry-run support for safe operation validation
# - Simple callback-based progress reporting without FastMCP coupling
###############################################################################
# [Source file constraints]
# - Must implement proper two-subphase discovery pattern
# - No FastMCP dependencies for clean architecture
# - Exception-first error handling - no fallback mechanisms
# - Must support both project-base and git-clone content types
###############################################################################
# [Dependencies]
# <system>:pathlib.Path
# <system>:typing.Optional
# <system>:time.time
# <codebase>:jesse_framework_mcp.knowledge_bases.indexer.models.ProgressCallback
# <codebase>:jesse_framework_mcp.knowledge_bases.indexer.models.ExecutionContext
# <codebase>:jesse_framework_mcp.knowledge_bases.indexer.models.IndexingResult
# <codebase>:jesse_framework_mcp.knowledge_bases.indexer.discovery.DiscoveryEngine
# <codebase>:jesse_framework_mcp.knowledge_bases.indexer.handlers.ProjectHandler
# <codebase>:jesse_framework_mcp.knowledge_bases.indexer.handlers.GitCloneHandler
# <codebase>:jesse_framework_mcp.knowledge_bases.indexer.decisions.DecisionEngine
# <codebase>:jesse_framework_mcp.knowledge_bases.indexer.planning.GenericPlanGenerator
# <codebase>:jesse_framework_mcp.knowledge_bases.indexer.planning.TaskRegistry
# <codebase>:jesse_framework_mcp.knowledge_bases.indexer.execution.GenericExecutor
# <codebase>:jesse_framework_mcp.knowledge_bases.indexer.knowledge.AnalyzeFileTask
# <codebase>:jesse_framework_mcp.knowledge_bases.indexer.knowledge.BuildKnowledgeBaseTask
# <codebase>:jesse_framework_mcp.knowledge_bases.indexer.knowledge.CleanupTask
# <codebase>:jesse_framework_mcp.llm.strands_agent_driver.driver.StrandsAgentDriver
###############################################################################
# [GenAI tool change history]
# 2025-07-09T13:40:00Z : Initial core orchestrator implementation by CodeAssistant
# * Created CoreIndexer with complete workflow orchestration
# * Implemented two-subphase discovery integration
# * Added comprehensive monitoring and error handling
# * Integrated all indexer components with proper task registry
###############################################################################

from pathlib import Path
from typing import Optional
import time

from .models import ProgressCallback, ExecutionContext, IndexingResult, KnowledgeTree
from .discovery import DiscoveryEngine
from .handlers import ProjectHandler, GitCloneHandler
from .decisions import DecisionEngine
from .planning import GenericPlanGenerator, TaskRegistry
from .execution import GenericExecutor
from .knowledge import AnalyzeFileTask, BuildKnowledgeBaseTask, CleanupTask
from ...llm.strands_agent_driver.driver import StrandsClaude4Driver


class CoreIndexer:
    """
    [Class intent]
    Main orchestrator for clean knowledge bases indexer workflow.
    Coordinates complete indexing process from two-subphase discovery through
    execution with comprehensive monitoring and error handling.

    [Design principles]
    Complete workflow orchestration with clear phase separation.
    Two-subphase discovery pattern as originally specified.
    Exception-first error handling with comprehensive monitoring.
    Clean architecture without FastMCP dependencies.

    [Implementation details]
    Coordinates discovery engine, decision engine, plan generator, and executor.
    Provides unified interface for complete indexing operations.
    Supports both dry-run and actual execution modes.
    """
    
    def __init__(self, source_root: Path, llm_driver: Optional[StrandsClaude4Driver] = None):
        """
        [Class method intent]
        Initialize core indexer with source root and optional LLM driver.

        [Design principles]
        Clear initialization with required and optional dependencies.
        Handler registration for extensible content type support.

        [Implementation details]
        Creates all workflow components with proper handler registration.
        Initializes task registry with concrete task implementations.
        """
        self.source_root = source_root
        self.llm_driver = llm_driver
        
        # Initialize handlers for different content types
        self.handlers = [
            ProjectHandler(),
            GitCloneHandler()
        ]
        
        # Initialize workflow components
        self.discovery_engine = DiscoveryEngine(self.handlers)
        self.decision_engine = DecisionEngine()
        
        # Initialize task registry and register concrete task types
        self.task_registry = TaskRegistry()
        self._register_task_types()
        
        # Initialize plan generator and executor
        self.plan_generator = GenericPlanGenerator(self.task_registry)
        self.executor = GenericExecutor()
    
    def _register_task_types(self):
        """
        [Class method intent]
        Register all concrete task types in the task registry.

        [Design principles]
        Explicit registration for type safety and extensibility.
        All task types registered during initialization.

        [Implementation details]
        Registers AnalyzeFileTask, BuildKnowledgeBaseTask, and CleanupTask.
        """
        self.task_registry.register_task_type("analyze_file", AnalyzeFileTask)
        self.task_registry.register_task_type("build_knowledge_base", BuildKnowledgeBaseTask)
        self.task_registry.register_task_type("cleanup", CleanupTask)
    
    async def index(
        self, 
        progress: Optional[ProgressCallback] = None,
        dry_run: bool = False
    ) -> IndexingResult:
        """
        [Class method intent]
        Execute complete indexing workflow with comprehensive monitoring.

        [Design principles]
        Complete workflow orchestration with clear phase separation.
        Two-subphase discovery followed by decision, planning, and execution.
        Comprehensive timing and error monitoring.

        [Implementation details]
        Phase 1: Two-subphase discovery (knowledge-first)
        Phase 2: Decision making (status-to-task conversion)
        Phase 3: Plan generation (dependency resolution)
        Phase 4: Execution (with dry-run support)
        """
        if progress:
            mode = "DRY-RUN" if dry_run else "INDEXING"
            progress("=" * 80)
            progress(f"🚀 Starting {mode} workflow for {self.source_root}")
            progress("=" * 80)
        
        # Track timing for performance analysis
        total_start_time = time.time()
        discovery_time = 0.0
        planning_time = 0.0
        execution_time = 0.0
        
        try:
            # Phase 1: Two-subphase discovery
            if progress:
                progress("📡 Phase 1: Starting two-subphase discovery...")
            
            discovery_start = time.time()
            knowledge_tree = await self.discovery_engine.discover(self.source_root, progress)
            discovery_time = time.time() - discovery_start
            
            # Phase 1 Summary
            if progress:
                stats = knowledge_tree.get_summary_stats()
                progress("")
                progress("─" * 80)
                progress("📊 PHASE 1 SUMMARY - Tree-based Discovery")
                progress("─" * 80)
                progress(f"📄 Analysis files discovered: {stats['analysis_files']}")
                progress(f"📚 Knowledge base files discovered: {stats['knowledge_base_files']}")
                progress(f"📁 Total files discovered: {stats['total_files']}")
                progress(f"⏱️ Discovery time: {discovery_time:.2f}s")
                progress("─" * 80)
                progress("")
            
            # Phase 2: Decision making
            if progress:
                progress("🧠 Phase 2: Making indexing decisions...")
            
            decisions = await self.decision_engine.make_decisions(knowledge_tree, progress)
            
            # Phase 2 Summary
            if progress:
                progress("")
                progress("─" * 80)
                progress("📊 PHASE 2 SUMMARY - Decision Making")
                progress("─" * 80)
                decision_counts = {}
                for decision in decisions:
                    decision_counts[decision.task_type] = decision_counts.get(decision.task_type, 0) + 1
                
                for task_type, count in decision_counts.items():
                    progress(f"🔧 {task_type}: {count} tasks")
                progress(f"📋 Total decisions generated: {len(decisions)}")
                progress("─" * 80)
                progress("")
            
            # Phase 3: Plan generation
            if progress:
                progress("📋 Phase 3: Generating execution plan...")
            
            planning_start = time.time()
            execution_plan = await self.plan_generator.generate_plan(decisions, progress)
            planning_time = time.time() - planning_start
            
            if not execution_plan.is_valid:
                error_msg = f"Invalid execution plan: {'; '.join(execution_plan.validation_errors)}"
                if progress:
                    progress(f"❌ ERROR: {error_msg}")
                raise RuntimeError(error_msg)
            
            # Phase 3 Summary
            if progress:
                progress("")
                progress("─" * 80)
                progress("📊 PHASE 3 SUMMARY - Plan Generation")
                progress("─" * 80)
                progress(f"📋 Total tasks planned: {execution_plan.task_count}")
                progress(f"🔗 Concurrent groups: {len(execution_plan.concurrent_groups)}")
                progress(f"⏱️ Planning time: {planning_time:.2f}s")
                progress(f"✅ Plan validation: {'PASSED' if execution_plan.is_valid else 'FAILED'}")
                progress("─" * 80)
                progress("")
            
            # Phase 4: Execution
            if progress:
                phase_name = "⚡ Phase 4: Dry-run execution..." if dry_run else "⚡ Phase 4: Executing plan..."
                progress(phase_name)
            
            execution_start = time.time()
            
            # Create execution context with knowledge tree
            execution_context = ExecutionContext(
                source_root=self.source_root,
                progress_callback=progress,
                knowledge_tree=knowledge_tree,  # NEW: Tree access for tasks
                llm_driver=self.llm_driver,
                dry_run=dry_run
            )
            
            # Execute the plan
            result = await self.executor.execute_plan(execution_plan, execution_context)
            execution_time = time.time() - execution_start
            
            # Update result with timing information and final tree state
            result.discovery_time = discovery_time
            result.planning_time = planning_time
            result.execution_time = execution_time
            result.final_tree_state = knowledge_tree  # NEW: Tree state for validation
            
            # Report final results
            if progress:
                total_time = time.time() - total_start_time
                success_rate = result.success_rate * 100
                mode_completed = "DRY-RUN COMPLETED" if dry_run else "INDEXING COMPLETED"
                progress(f"✅ {mode_completed}: {success_rate:.1f}% success rate, {total_time:.2f}s total time")
            
            return result
            
        except Exception as e:
            total_time = time.time() - total_start_time
            error_msg = f"Indexing workflow failed after {total_time:.2f}s: {str(e)}"
            if progress:
                progress(f"❌ ERROR: {error_msg}")
            
            # Return failed result with timing information
            return IndexingResult(
                files_analyzed=0,
                kbs_built=0,
                cache_files_created=0,
                orphaned_files_cleaned=0,
                errors=[error_msg],
                execution_time=execution_time,
                discovery_time=discovery_time,
                planning_time=planning_time
            )
    
    def get_supported_handler_types(self) -> list[str]:
        """
        [Class method intent]
        Return list of supported handler types for discovery.

        [Design principles]
        Introspection capability for debugging and reporting.

        [Implementation details]
        Returns handler type strings from discovery engine.
        """
        return self.discovery_engine.get_supported_types()
    
    def get_registered_task_types(self) -> list[str]:
        """
        [Class method intent]
        Return list of registered task types for execution.

        [Design principles]
        Introspection capability for debugging and validation.

        [Implementation details]
        Returns task type strings from task registry.
        """
        return self.task_registry.get_registered_types()
    
    def validate_configuration(self) -> dict[str, any]:
        """
        [Class method intent]
        Validate indexer configuration and return status information.

        [Design principles]
        Comprehensive configuration validation for debugging.
        Clear status reporting for troubleshooting.

        [Implementation details]
        Validates source root, handlers, and task registry configuration.
        Returns detailed configuration status.
        """
        validation_result = {
            'source_root_exists': self.source_root.exists(),
            'source_root_readable': self.source_root.is_dir() if self.source_root.exists() else False,
            'handlers_registered': len(self.handlers),
            'supported_handler_types': self.get_supported_handler_types(),
            'tasks_registered': len(self.task_registry.get_registered_types()),
            'registered_task_types': self.get_registered_task_types(),
            'llm_driver_available': self.llm_driver is not None,
            'configuration_valid': True,
            'validation_errors': []
        }
        
        # Validate source root
        if not validation_result['source_root_exists']:
            validation_result['configuration_valid'] = False
            validation_result['validation_errors'].append(f"Source root does not exist: {self.source_root}")
        elif not validation_result['source_root_readable']:
            validation_result['configuration_valid'] = False
            validation_result['validation_errors'].append(f"Source root is not a readable directory: {self.source_root}")
        
        # Validate handlers
        if validation_result['handlers_registered'] == 0:
            validation_result['configuration_valid'] = False
            validation_result['validation_errors'].append("No handlers registered")
        
        # Validate task registry
        if validation_result['tasks_registered'] == 0:
            validation_result['configuration_valid'] = False
            validation_result['validation_errors'].append("No task types registered")
        
        return validation_result


# Convenience function for simple indexing operations
async def index_project(
    source_root: Path, 
    llm_driver: Optional[StrandsClaude4Driver] = None,
    progress: Optional[ProgressCallback] = None,
    dry_run: bool = False
) -> IndexingResult:
    """
    [Function intent]
    Convenience function for simple project indexing operations.

    [Design principles]
    Simple interface for common indexing use cases.
    Encapsulates CoreIndexer creation and execution.

    [Implementation details]
    Creates CoreIndexer instance and executes indexing workflow.
    Returns IndexingResult with comprehensive outcome information.
    """
    indexer = CoreIndexer(source_root, llm_driver)
    return await indexer.index(progress, dry_run)


# Convenience function for configuration validation
def validate_indexer_setup(source_root: Path, llm_driver: Optional[StrandsClaude4Driver] = None) -> dict[str, any]:
    """
    [Function intent]
    Convenience function for validating indexer configuration.

    [Design principles]
    Simple validation interface for troubleshooting.
    No actual indexing performed - configuration check only.

    [Implementation details]
    Creates CoreIndexer instance and validates configuration.
    Returns detailed validation status for debugging.
    """
    indexer = CoreIndexer(source_root, llm_driver)
    return indexer.validate_configuration()
