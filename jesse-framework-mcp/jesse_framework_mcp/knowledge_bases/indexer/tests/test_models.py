"""
Test suite for new indexer data models.

Tests all data classes, enums, and abstract interfaces to ensure proper
validation, serialization, and behavior according to specification.
"""

import pytest
from pathlib import Path
from unittest.mock import Mock, patch
import tempfile

from ..models import (
    KnowledgeFile,
    ValidationResult,
    ExecutionContext,
    TaskResult,
    AtomicTask,
    ExecutionPlan,
    IndexingResult,
    TaskStatus,
    ProgressCallback
)


class TestKnowledgeFile:
    """Test KnowledgeFile data class functionality."""
    
    def test_valid_knowledge_file_creation(self):
        """Test creating valid KnowledgeFile instances."""
        kb_file = KnowledgeFile(
            path=Path("/test/kb.md"),
            handler_type="project",
            file_type="knowledge"
        )
        
        assert kb_file.path == Path("/test/kb.md")
        assert kb_file.handler_type == "project"
        assert kb_file.file_type == "knowledge"
        assert kb_file.is_orphaned is True  # Default orphaned state
        assert kb_file.source_path is None
        assert kb_file.is_stale is False
    
    def test_invalid_handler_type_raises_error(self):
        """Test that invalid handler types raise ValueError."""
        with pytest.raises(ValueError, match="Invalid handler_type"):
            KnowledgeFile(
                path=Path("/test/kb.md"),
                handler_type="invalid_type",
                file_type="knowledge"
            )
    
    def test_invalid_file_type_raises_error(self):
        """Test that invalid file types raise ValueError."""
        with pytest.raises(ValueError, match="Invalid file_type"):
            KnowledgeFile(
                path=Path("/test/kb.md"),
                handler_type="project", 
                file_type="invalid_type"
            )
    
    def test_valid_handler_types(self):
        """Test all valid handler types work."""
        for handler_type in ["project", "gitclone"]:
            kb_file = KnowledgeFile(
                path=Path("/test/kb.md"),
                handler_type=handler_type,
                file_type="knowledge"
            )
            assert kb_file.handler_type == handler_type
    
    def test_valid_file_types(self):
        """Test all valid file types work."""
        for file_type in ["knowledge", "cache"]:
            kb_file = KnowledgeFile(
                path=Path("/test/file"),
                handler_type="project",
                file_type=file_type
            )
            assert kb_file.file_type == file_type
    
    @patch('pathlib.Path.exists')
    @patch('pathlib.Path.stat')
    def test_metadata_population_for_existing_files(self, mock_stat, mock_exists):
        """Test metadata is populated for existing files."""
        mock_exists.return_value = True
        mock_stat.return_value = Mock(st_mtime=1234567890.0, st_size=1024)
        
        kb_file = KnowledgeFile(
            path=Path("/test/existing.md"),
            handler_type="project",
            file_type="knowledge"
        )
        
        assert kb_file.last_modified == 1234567890.0
        assert kb_file.file_size == 1024


class TestValidationResult:
    """Test ValidationResult data class."""
    
    def test_valid_source_exists(self):
        """Test validation result with existing source."""
        result = ValidationResult(
            source_exists=True,
            source_path=Path("/source/file.py"),
            is_stale=False,
            validation_reason="Source file found and up to date"
        )
        
        assert result.source_exists is True
        assert result.source_path == Path("/source/file.py")
        assert result.is_stale is False
        assert "up to date" in result.validation_reason
    
    def test_missing_source(self):
        """Test validation result with missing source."""
        result = ValidationResult(
            source_exists=False,
            source_path=None,
            is_stale=True,
            validation_reason="Source file not found"
        )
        
        assert result.source_exists is False
        assert result.source_path is None
        assert result.is_stale is True
        assert "not found" in result.validation_reason


class TestExecutionContext:
    """Test ExecutionContext data class."""
    
    def test_basic_execution_context(self):
        """Test basic execution context creation."""
        progress_callback = Mock()
        context = ExecutionContext(
            source_root=Path("/project"),
            progress_callback=progress_callback
        )
        
        assert context.source_root == Path("/project")
        assert context.progress_callback == progress_callback
        assert context.llm_driver is None
        assert context.shared_data == {}
        assert context.dry_run is False
    
    def test_full_execution_context(self):
        """Test execution context with all parameters."""
        progress_callback = Mock()
        llm_driver = Mock()
        shared_data = {"key": "value"}
        
        context = ExecutionContext(
            source_root=Path("/project"),
            progress_callback=progress_callback,
            llm_driver=llm_driver,
            shared_data=shared_data,
            dry_run=True
        )
        
        assert context.source_root == Path("/project")
        assert context.progress_callback == progress_callback
        assert context.llm_driver == llm_driver
        assert context.shared_data == shared_data
        assert context.dry_run is True


class TestTaskResult:
    """Test TaskResult data class."""
    
    def test_successful_task_result(self):
        """Test successful task result creation."""
        result = TaskResult(
            success=True,
            task_type="analyze_file",
            task_id="task_123",
            files_processed=1,
            output_files=[Path("/output/analysis.md")]
        )
        
        assert result.success is True
        assert result.task_type == "analyze_file"
        assert result.task_id == "task_123"
        assert result.error_message is None
        assert result.files_processed == 1
        assert result.output_files == [Path("/output/analysis.md")]
        assert result.metadata == {}
    
    def test_failed_task_result(self):
        """Test failed task result creation."""
        result = TaskResult(
            success=False,
            task_type="build_kb",
            task_id="task_456",
            error_message="LLM driver not available",
            execution_time=2.5
        )
        
        assert result.success is False
        assert result.task_type == "build_kb"
        assert result.task_id == "task_456"
        assert result.error_message == "LLM driver not available"
        assert result.execution_time == 2.5
        assert result.files_processed == 0
        assert result.output_files == []


class TestTaskStatus:
    """Test TaskStatus enum."""
    
    def test_all_status_values(self):
        """Test all status enum values are available."""
        assert TaskStatus.PENDING.value == "pending"
        assert TaskStatus.RUNNING.value == "running"
        assert TaskStatus.COMPLETED.value == "completed"
        assert TaskStatus.FAILED.value == "failed" 
        assert TaskStatus.SKIPPED.value == "skipped"


class MockAtomicTask(AtomicTask):
    """Mock implementation of AtomicTask for testing."""
    
    def __init__(self, task_id="mock_task", task_type="mock", dependencies=None):
        self.task_id = task_id
        self.task_type = task_type
        self.dependencies = dependencies or []
    
    def get_task_type(self):
        return self.task_type
    
    def get_task_id(self):
        return self.task_id
    
    def get_dependencies(self):
        return self.dependencies
    
    async def execute(self, context):
        return TaskResult(
            success=True,
            task_type=self.task_type,
            task_id=self.task_id
        )
    
    def can_run_concurrently_with(self, other):
        return self.task_id != other.get_task_id()
    
    def validate_preconditions(self, context):
        return True


class TestAtomicTask:
    """Test AtomicTask abstract interface."""
    
    def test_cannot_instantiate_abstract_task(self):
        """Test that AtomicTask cannot be instantiated directly."""
        with pytest.raises(TypeError):
            AtomicTask()
    
    def test_mock_task_implementation(self):
        """Test mock task implementation works correctly."""
        task = MockAtomicTask("test_123", "analyze", ["dep_1", "dep_2"])
        
        assert task.get_task_type() == "analyze"
        assert task.get_task_id() == "test_123"
        assert task.get_dependencies() == ["dep_1", "dep_2"]
        assert task.validate_preconditions(Mock()) is True
    
    @pytest.mark.asyncio
    async def test_mock_task_execution(self):
        """Test mock task execution."""
        task = MockAtomicTask("test_456", "build")
        context = Mock()
        
        result = await task.execute(context)
        
        assert result.success is True
        assert result.task_type == "build"
        assert result.task_id == "test_456"
    
    def test_task_concurrency_rules(self):
        """Test task concurrency compatibility."""
        task1 = MockAtomicTask("task_1")
        task2 = MockAtomicTask("task_2") 
        task1_duplicate = MockAtomicTask("task_1")
        
        # Different tasks can run concurrently
        assert task1.can_run_concurrently_with(task2) is True
        assert task2.can_run_concurrently_with(task1) is True
        
        # Same task ID cannot run concurrently
        assert task1.can_run_concurrently_with(task1_duplicate) is False


class TestExecutionPlan:
    """Test ExecutionPlan data class."""
    
    def test_empty_execution_plan(self):
        """Test empty execution plan creation."""
        plan = ExecutionPlan()
        
        assert plan.tasks == []
        assert plan.concurrent_groups == []
        assert plan.validation_errors == []
        assert plan.estimated_duration is None
        assert plan.is_valid is True
        assert plan.task_count == 0
    
    def test_execution_plan_with_tasks(self):
        """Test execution plan with tasks."""
        task1 = MockAtomicTask("task_1")
        task2 = MockAtomicTask("task_2")
        
        plan = ExecutionPlan(
            tasks=[task1, task2],
            concurrent_groups=[["task_1"], ["task_2"]],
            estimated_duration=30.0
        )
        
        assert len(plan.tasks) == 2
        assert plan.concurrent_groups == [["task_1"], ["task_2"]]
        assert plan.estimated_duration == 30.0
        assert plan.is_valid is True
        assert plan.task_count == 2
    
    def test_invalid_execution_plan(self):
        """Test execution plan with validation errors."""
        plan = ExecutionPlan(
            tasks=[MockAtomicTask("task_1")],
            validation_errors=["Missing dependency", "Invalid configuration"]
        )
        
        assert plan.is_valid is False
        assert len(plan.validation_errors) == 2
        assert "Missing dependency" in plan.validation_errors


class TestIndexingResult:
    """Test IndexingResult data class."""
    
    def test_empty_indexing_result(self):
        """Test empty indexing result."""
        result = IndexingResult()
        
        assert result.files_analyzed == 0
        assert result.kbs_built == 0
        assert result.cache_files_created == 0
        assert result.orphaned_files_cleaned == 0
        assert result.task_results == []
        assert result.errors == []
        assert result.success_rate == 1.0  # Perfect success for empty result
        assert result.total_files_processed == 0
    
    def test_successful_indexing_result(self):
        """Test successful indexing result with task results."""
        task_results = [
            TaskResult(True, "analyze", "task_1", files_processed=1),
            TaskResult(True, "build_kb", "task_2", files_processed=2),
            TaskResult(True, "cleanup", "task_3", files_processed=1)
        ]
        
        result = IndexingResult(
            files_analyzed=5,
            kbs_built=2,
            cache_files_created=3,
            task_results=task_results,
            execution_time=45.0
        )
        
        assert result.files_analyzed == 5
        assert result.kbs_built == 2
        assert result.cache_files_created == 3
        assert result.success_rate == 1.0  # All tasks successful
        assert result.total_files_processed == 4  # Sum of files_processed
        assert result.execution_time == 45.0
    
    def test_partial_failure_indexing_result(self):
        """Test indexing result with some failures."""
        task_results = [
            TaskResult(True, "analyze", "task_1", files_processed=1),
            TaskResult(False, "build_kb", "task_2", error_message="LLM failed"),
            TaskResult(True, "cleanup", "task_3", files_processed=1)
        ]
        
        result = IndexingResult(
            files_analyzed=2,
            task_results=task_results,
            errors=["LLM connection timeout"]
        )
        
        assert result.success_rate == 2/3  # 2 out of 3 tasks successful
        assert len(result.errors) == 1
        assert result.total_files_processed == 2


class TestProgressCallback:
    """Test ProgressCallback type alias functionality."""
    
    def test_progress_callback_signature(self):
        """Test progress callback can be called with string message."""
        messages = []
        
        def progress_callback(message: str) -> None:
            messages.append(message)
        
        # Test callback matches ProgressCallback type
        callback: ProgressCallback = progress_callback
        
        callback("Starting analysis...")
        callback("Processing file 1 of 10")
        callback("Analysis complete")
        
        assert len(messages) == 3
        assert messages[0] == "Starting analysis..."
        assert messages[1] == "Processing file 1 of 10"
        assert messages[2] == "Analysis complete"


# Integration tests for data model interactions
class TestModelIntegration:
    """Test integration between different data models."""
    
    def test_knowledge_file_to_validation_result_flow(self):
        """Test flow from KnowledgeFile discovery to ValidationResult."""
        # Discovered knowledge file (orphaned by default)
        kb_file = KnowledgeFile(
            path=Path("/project/.knowledge/module_kb.md"),
            handler_type="project",
            file_type="knowledge"
        )
        
        assert kb_file.is_orphaned is True
        
        # Validation determines source exists
        validation = ValidationResult(
            source_exists=True,
            source_path=Path("/project/module.py"),
            is_stale=False,
            validation_reason="Source file found and newer than KB"
        )
        
        # After validation, knowledge file would be updated
        kb_file.is_orphaned = not validation.source_exists
        kb_file.source_path = validation.source_path
        kb_file.is_stale = validation.is_stale
        
        assert kb_file.is_orphaned is False
        assert kb_file.source_path == Path("/project/module.py")
        assert kb_file.is_stale is False
    
    def test_execution_context_to_task_result_flow(self):
        """Test flow from ExecutionContext to TaskResult."""
        # Create execution context
        messages = []
        context = ExecutionContext(
            source_root=Path("/project"),
            progress_callback=lambda msg: messages.append(msg),
            dry_run=False
        )
        
        # Mock task execution using context
        task = MockAtomicTask("integration_test", "analyze")
        
        # Validate preconditions
        assert task.validate_preconditions(context) is True
        
        # Execute task (mock would use context.progress_callback)
        context.progress_callback("Starting file analysis...")
        result = TaskResult(
            success=True,
            task_type=task.get_task_type(),
            task_id=task.get_task_id(),
            files_processed=1,
            metadata={"source_root": str(context.source_root)}
        )
        
        assert len(messages) == 1
        assert messages[0] == "Starting file analysis..."
        assert result.metadata["source_root"] == "/project"
    
    def test_task_results_to_indexing_result_aggregation(self):
        """Test aggregating TaskResults into IndexingResult."""
        # Create various task results
        analyze_results = [
            TaskResult(True, "analyze_file", "analyze_1", files_processed=1),
            TaskResult(True, "analyze_file", "analyze_2", files_processed=1),
            TaskResult(False, "analyze_file", "analyze_3", error_message="File not found")
        ]
        
        kb_results = [
            TaskResult(True, "build_knowledge_base", "kb_1", files_processed=2),
            TaskResult(True, "build_knowledge_base", "kb_2", files_processed=3)
        ]
        
        cleanup_results = [
            TaskResult(True, "cleanup", "cleanup_1", files_processed=1)
        ]
        
        all_results = analyze_results + kb_results + cleanup_results
        
        # Aggregate into IndexingResult
        result = IndexingResult(
            files_analyzed=len([r for r in analyze_results if r.success]),
            kbs_built=len([r for r in kb_results if r.success]),
            orphaned_files_cleaned=len([r for r in cleanup_results if r.success]),
            task_results=all_results,
            errors=[r.error_message for r in all_results if not r.success and r.error_message]
        )
        
        assert result.files_analyzed == 2  # 2 successful analysis tasks
        assert result.kbs_built == 2  # 2 successful KB tasks
        assert result.orphaned_files_cleaned == 1  # 1 successful cleanup task
        assert result.success_rate == 5/6  # 5 out of 6 tasks successful
        assert result.total_files_processed == 8  # Sum of all files_processed
        assert len(result.errors) == 1
        assert result.errors[0] == "File not found"
