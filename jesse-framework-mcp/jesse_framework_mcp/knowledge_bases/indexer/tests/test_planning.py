"""
Test suite for new indexer planning system.

Tests task registry, dependency resolution, concurrency analysis,
and execution plan generation for comprehensive planning functionality.
"""

import pytest
from unittest.mock import Mock, AsyncMock
from pathlib import Path

from ..planning import TaskRegistry, DependencyResolver, ConcurrencyAnalyzer, GenericPlanGenerator
from ..decisions import TaskDecision
from ..models import AtomicTask, ExecutionPlan, TaskResult, ExecutionContext
from .test_models import MockAtomicTask


class TestTaskRegistry:
    """Test TaskRegistry functionality."""
    
    def test_empty_registry_creation(self):
        """Test creating empty task registry."""
        registry = TaskRegistry()
        assert registry.get_registered_types() == []
        assert registry.is_task_type_registered("nonexistent") is False
    
    def test_task_type_registration(self):
        """Test registering task types."""
        registry = TaskRegistry()
        
        registry.register_task_type("mock_task", MockAtomicTask)
        
        assert "mock_task" in registry.get_registered_types()
        assert registry.is_task_type_registered("mock_task") is True
    
    def test_duplicate_registration_raises_error(self):
        """Test that duplicate registration raises error."""
        registry = TaskRegistry()
        
        registry.register_task_type("mock_task", MockAtomicTask)
        
        with pytest.raises(ValueError, match="already registered"):
            registry.register_task_type("mock_task", MockAtomicTask)
    
    def test_invalid_task_class_raises_error(self):
        """Test that invalid task class raises error."""
        registry = TaskRegistry()
        
        class InvalidTask:
            pass
        
        with pytest.raises(ValueError, match="must implement AtomicTask"):
            registry.register_task_type("invalid", InvalidTask)
    
    def test_task_creation_from_decision(self):
        """Test creating tasks from decisions."""
        registry = TaskRegistry()
        registry.register_task_type("mock_task", MockAtomicTask)
        
        decision = Mock()
        decision.task_type = "mock_task"
        decision.task_id = "test_123"
        
        task = registry.create_task(decision)
        
        assert isinstance(task, MockAtomicTask)
        assert task.get_task_type() == "mock_task"
    
    def test_unknown_task_type_raises_error(self):
        """Test that unknown task type raises error."""
        registry = TaskRegistry()
        
        decision = Mock()
        decision.task_type = "unknown_task"
        decision.task_id = "test_123"
        
        with pytest.raises(ValueError, match="Unknown task type"):
            registry.create_task(decision)
    
    def test_task_creation_failure_handling(self):
        """Test handling of task creation failures."""
        registry = TaskRegistry()
        
        class FailingTask(AtomicTask):
            def __init__(self, decision):
                raise RuntimeError("Task creation failed")
            
            def get_task_type(self):
                return "failing"
            
            def get_task_id(self):
                return "fail"
            
            def get_dependencies(self):
                return []
            
            async def execute(self, context):
                pass
            
            def can_run_concurrently_with(self, other):
                return True
            
            def validate_preconditions(self, context):
                return True
        
        registry.register_task_type("failing_task", FailingTask)
        
        decision = Mock()
        decision.task_type = "failing_task"
        decision.task_id = "fail_123"
        
        with pytest.raises(RuntimeError, match="Failed to create task"):
            registry.create_task(decision)


class TestDependencyResolver:
    """Test DependencyResolver functionality."""
    
    def test_empty_task_list(self):
        """Test dependency resolution with empty task list."""
        resolver = DependencyResolver()
        
        resolved = resolver.resolve_dependencies([])
        assert resolved == []
    
    def test_single_task_no_dependencies(self):
        """Test single task with no dependencies."""
        resolver = DependencyResolver()
        task = MockAtomicTask("task_1", "analyze", [])
        
        resolved = resolver.resolve_dependencies([task])
        assert len(resolved) == 1
        assert resolved[0] == task
    
    def test_simple_dependency_chain(self):
        """Test simple dependency chain resolution."""
        resolver = DependencyResolver()
        
        # Task B depends on Task A
        task_a = MockAtomicTask("task_a", "analyze", [])
        task_b = MockAtomicTask("task_b", "build", ["task_a"])
        
        resolved = resolver.resolve_dependencies([task_b, task_a])
        
        # Should be ordered: A first, then B
        assert len(resolved) == 2
        assert resolved[0].get_task_id() == "task_a"
        assert resolved[1].get_task_id() == "task_b"
    
    def test_complex_dependency_resolution(self):
        """Test complex dependency graph resolution."""
        resolver = DependencyResolver()
        
        # Complex dependency: D depends on [B, C], B depends on A, C depends on A
        task_a = MockAtomicTask("task_a", "analyze", [])
        task_b = MockAtomicTask("task_b", "analyze", ["task_a"])
        task_c = MockAtomicTask("task_c", "analyze", ["task_a"])
        task_d = MockAtomicTask("task_d", "build", ["task_b", "task_c"])
        
        resolved = resolver.resolve_dependencies([task_d, task_c, task_b, task_a])
        
        # Should be ordered properly
        task_ids = [task.get_task_id() for task in resolved]
        
        assert task_ids.index("task_a") < task_ids.index("task_b")
        assert task_ids.index("task_a") < task_ids.index("task_c")
        assert task_ids.index("task_b") < task_ids.index("task_d")
        assert task_ids.index("task_c") < task_ids.index("task_d")
    
    def test_circular_dependency_detection(self):
        """Test circular dependency detection."""
        resolver = DependencyResolver()
        
        # Create circular dependency: A -> B -> A
        task_a = MockAtomicTask("task_a", "analyze", ["task_b"])
        task_b = MockAtomicTask("task_b", "analyze", ["task_a"])
        
        with pytest.raises(RuntimeError, match="Dependency cycles detected"):
            resolver.resolve_dependencies([task_a, task_b])
    
    def test_self_dependency_detection(self):
        """Test self-dependency detection."""
        resolver = DependencyResolver()
        
        # Task depends on itself
        task_a = MockAtomicTask("task_a", "analyze", ["task_a"])
        
        with pytest.raises(RuntimeError, match="Dependency cycles detected"):
            resolver.resolve_dependencies([task_a])
    
    def test_complex_cycle_detection(self):
        """Test complex cycle detection."""
        resolver = DependencyResolver()
        
        # Create complex cycle: A -> B -> C -> A
        task_a = MockAtomicTask("task_a", "analyze", ["task_c"])
        task_b = MockAtomicTask("task_b", "analyze", ["task_a"])
        task_c = MockAtomicTask("task_c", "analyze", ["task_b"])
        
        with pytest.raises(RuntimeError, match="Dependency cycles detected"):
            resolver.resolve_dependencies([task_a, task_b, task_c])


class TestConcurrencyAnalyzer:
    """Test ConcurrencyAnalyzer functionality."""
    
    def test_empty_task_list(self):
        """Test concurrency analysis with empty task list."""
        analyzer = ConcurrencyAnalyzer()
        
        groups = analyzer.analyze_concurrency([])
        assert groups == []
    
    def test_single_task(self):
        """Test concurrency analysis with single task."""
        analyzer = ConcurrencyAnalyzer()
        task = MockAtomicTask("task_1")
        
        groups = analyzer.analyze_concurrency([task])
        assert len(groups) == 1
        assert groups[0] == ["task_1"]
    
    def test_compatible_tasks(self):
        """Test tasks that can run concurrently."""
        analyzer = ConcurrencyAnalyzer()
        
        # Different tasks can run concurrently (MockAtomicTask allows this by default)
        task_a = MockAtomicTask("task_a")
        task_b = MockAtomicTask("task_b")
        task_c = MockAtomicTask("task_c")
        
        groups = analyzer.analyze_concurrency([task_a, task_b, task_c])
        
        # All should be in same group since they're compatible
        assert len(groups) == 1
        assert set(groups[0]) == {"task_a", "task_b", "task_c"}
    
    def test_incompatible_tasks(self):
        """Test tasks that cannot run concurrently."""
        analyzer = ConcurrencyAnalyzer()
        
        class IncompatibleTask(MockAtomicTask):
            def can_run_concurrently_with(self, other):
                return False  # Cannot run with any other task
        
        task_a = IncompatibleTask("task_a")
        task_b = IncompatibleTask("task_b")
        
        groups = analyzer.analyze_concurrency([task_a, task_b])
        
        # Should be in separate groups
        assert len(groups) == 2
        assert groups[0] == ["task_a"]
        assert groups[1] == ["task_b"]
    
    def test_mixed_compatibility(self):
        """Test mixed compatibility scenarios."""
        analyzer = ConcurrencyAnalyzer()
        
        class SelectiveTask(MockAtomicTask):
            def __init__(self, task_id, compatible_with=None):
                super().__init__(task_id)
                self.compatible_with = compatible_with or set()
            
            def can_run_concurrently_with(self, other):
                return other.get_task_id() in self.compatible_with
        
        # A is compatible with B, B is compatible with A, C is compatible with none
        task_a = SelectiveTask("task_a", {"task_b"})
        task_b = SelectiveTask("task_b", {"task_a"})
        task_c = SelectiveTask("task_c", set())
        
        groups = analyzer.analyze_concurrency([task_a, task_b, task_c])
        
        # A and B should be together, C should be separate
        assert len(groups) == 2
        assert set(groups[0]) == {"task_a", "task_b"} or set(groups[1]) == {"task_a", "task_b"}
        assert ["task_c"] in groups


class TestGenericPlanGenerator:
    """Test GenericPlanGenerator functionality."""
    
    def test_empty_decisions_list(self):
        """Test plan generation with empty decisions."""
        registry = TaskRegistry()
        generator = GenericPlanGenerator(registry)
        
        plan = asyncio.run(generator.generate_plan([]))
        
        assert isinstance(plan, ExecutionPlan)
        assert plan.tasks == []
        assert plan.concurrent_groups == []
        assert plan.is_valid is True
    
    @pytest.mark.asyncio
    async def test_simple_plan_generation(self):
        """Test simple plan generation."""
        registry = TaskRegistry()
        registry.register_task_type("mock_task", MockAtomicTask)
        
        generator = GenericPlanGenerator(registry)
        
        # Create simple decisions
        decision = Mock()
        decision.task_type = "mock_task"
        decision.task_id = "test_123"
        decision.dependencies = []
        
        plan = await generator.generate_plan([decision])
        
        assert plan.is_valid is True
        assert len(plan.tasks) == 1
        assert plan.tasks[0].get_task_id() == "test_123"
        assert len(plan.concurrent_groups) == 1
        assert plan.concurrent_groups[0] == ["test_123"]
    
    @pytest.mark.asyncio
    async def test_plan_with_dependencies(self):
        """Test plan generation with dependencies."""
        registry = TaskRegistry()
        registry.register_task_type("mock_task", MockAtomicTask)
        
        generator = GenericPlanGenerator(registry)
        
        # Create decisions with dependencies
        decision_a = Mock()
        decision_a.task_type = "mock_task"
        decision_a.task_id = "task_a"
        decision_a.dependencies = []
        
        decision_b = Mock()
        decision_b.task_type = "mock_task"
        decision_b.task_id = "task_b"
        decision_b.dependencies = ["task_a"]
        
        plan = await generator.generate_plan([decision_b, decision_a])
        
        assert plan.is_valid is True
        assert len(plan.tasks) == 2
        
        # Check dependency order
        task_ids = [task.get_task_id() for task in plan.tasks]
        assert task_ids.index("task_a") < task_ids.index("task_b")
    
    @pytest.mark.asyncio
    async def test_plan_validation_errors(self):
        """Test plan generation with validation errors."""
        registry = TaskRegistry()
        generator = GenericPlanGenerator(registry)
        
        # Create decision for unregistered task type
        decision = Mock()
        decision.task_type = "unregistered_task"
        decision.task_id = "test_123"
        decision.dependencies = []
        
        plan = await generator.generate_plan([decision])
        
        assert plan.is_valid is False
        assert len(plan.validation_errors) > 0
        assert len(plan.tasks) == 0
    
    @pytest.mark.asyncio
    async def test_progress_callback_integration(self):
        """Test progress callback integration."""
        registry = TaskRegistry()
        registry.register_task_type("mock_task", MockAtomicTask)
        
        generator = GenericPlanGenerator(registry)
        
        progress_messages = []
        def progress_callback(message):
            progress_messages.append(message)
        
        decision = Mock()
        decision.task_type = "mock_task"
        decision.task_id = "test_123"
        decision.dependencies = []
        
        plan = await generator.generate_plan([decision], progress_callback)
        
        assert len(progress_messages) > 0
        assert any("Starting execution plan generation" in msg for msg in progress_messages)
        assert any("successfully" in msg for msg in progress_messages)
    
    @pytest.mark.asyncio
    async def test_dependency_population(self):
        """Test automatic dependency population."""
        registry = TaskRegistry()
        registry.register_task_type("analyze_file", MockAtomicTask)
        registry.register_task_type("build_knowledge_base", MockAtomicTask)
        
        generator = GenericPlanGenerator(registry)
        
        # Create decisions that should have dependencies populated
        analyze_decision = Mock()
        analyze_decision.task_type = "analyze_file"
        analyze_decision.task_id = "analyze_src_file"
        analyze_decision.source_path = Path("/project/src/file.py")
        analyze_decision.dependencies = []
        
        kb_decision = Mock()
        kb_decision.task_type = "build_knowledge_base"
        kb_decision.task_id = "build_src_kb"
        kb_decision.source_path = Path("/project/src")
        kb_decision.dependencies = []
        
        plan = await generator.generate_plan([kb_decision, analyze_decision])
        
        assert plan.is_valid is True
        assert len(plan.tasks) == 2
        
        # KB task should depend on analyze task
        kb_task = next(task for task in plan.tasks if "build" in task.get_task_id())
        assert "analyze_src_file" in kb_task.get_dependencies()
    
    def test_plan_summary_generation(self):
        """Test plan summary generation."""
        registry = TaskRegistry()
        registry.register_task_type("mock_task", MockAtomicTask)
        
        generator = GenericPlanGenerator(registry)
        
        # Create mock plan
        task1 = MockAtomicTask("task_1", "analyze")
        task2 = MockAtomicTask("task_2", "build")
        
        plan = ExecutionPlan(
            tasks=[task1, task2],
            concurrent_groups=[["task_1"], ["task_2"]]
        )
        
        summary = generator.get_plan_summary(plan)
        
        assert summary['total_tasks'] == 2
        assert summary['concurrent_groups'] == 2
        assert summary['is_valid'] is True
        assert summary['task_types']['analyze'] == 1
        assert summary['task_types']['build'] == 1
        assert summary['max_concurrent_tasks'] == 1


class TestPlanningIntegration:
    """Test integration between planning components."""
    
    @pytest.mark.asyncio
    async def test_end_to_end_planning_workflow(self):
        """Test complete planning workflow."""
        # Set up registry with task types
        registry = TaskRegistry()
        registry.register_task_type("analyze_file", MockAtomicTask)
        registry.register_task_type("build_knowledge_base", MockAtomicTask)
        registry.register_task_type("cleanup", MockAtomicTask)
        
        generator = GenericPlanGenerator(registry)
        
        # Create comprehensive decision set
        decisions = []
        
        # File analysis decisions
        for i in range(3):
            decision = Mock()
            decision.task_type = "analyze_file"
            decision.task_id = f"analyze_{i}"
            decision.source_path = Path(f"/project/src/file_{i}.py")
            decision.dependencies = []
            decisions.append(decision)
        
        # KB building decisions
        kb_decision = Mock()
        kb_decision.task_type = "build_knowledge_base"
        kb_decision.task_id = "build_kb"
        kb_decision.source_path = Path("/project/src")
        kb_decision.dependencies = []
        decisions.append(kb_decision)
        
        # Cleanup decision
        cleanup_decision = Mock()
        cleanup_decision.task_type = "cleanup"
        cleanup_decision.task_id = "cleanup_orphans"
        cleanup_decision.dependencies = []
        decisions.append(cleanup_decision)
        
        # Generate plan
        plan = await generator.generate_plan(decisions)
        
        # Validate plan
        assert plan.is_valid is True
        assert len(plan.tasks) == 5
        assert len(plan.concurrent_groups) > 0
        
        # Check that dependencies are properly resolved
        kb_task = next(task for task in plan.tasks if "build" in task.get_task_id())
        kb_deps = kb_task.get_dependencies()
        
        # KB should depend on analyze tasks
        analyze_ids = [f"analyze_{i}" for i in range(3)]
        assert all(dep in analyze_ids for dep in kb_deps)
    
    def test_planning_error_handling(self):
        """Test error handling in planning workflow."""
        registry = TaskRegistry()
        generator = GenericPlanGenerator(registry)
        
        # Test with invalid decisions
        invalid_decision = Mock()
        invalid_decision.task_type = "nonexistent_task"
        invalid_decision.task_id = "invalid_123"
        invalid_decision.dependencies = []
        
        # Should handle gracefully
        plan = asyncio.run(generator.generate_plan([invalid_decision]))
        assert plan.is_valid is False
        assert len(plan.validation_errors) > 0
    
    def test_planning_performance_characteristics(self):
        """Test planning performance with larger task sets."""
        import time
        
        registry = TaskRegistry()
        registry.register_task_type("mock_task", MockAtomicTask)
        
        generator = GenericPlanGenerator(registry)
        
        # Create large decision set
        decisions = []
        for i in range(100):
            decision = Mock()
            decision.task_type = "mock_task"
            decision.task_id = f"task_{i}"
            decision.source_path = Path(f"/project/file_{i}.py")
            decision.dependencies = []
            decisions.append(decision)
        
        # Time planning operation
        start_time = time.time()
        plan = asyncio.run(generator.generate_plan(decisions))
        planning_time = time.time() - start_time
        
        # Should complete quickly
        assert planning_time < 5.0, f"Planning too slow: {planning_time}s"
        assert plan.is_valid is True
        assert len(plan.tasks) == 100


# Integration with pytest-asyncio for async tests
import asyncio

if __name__ == "__main__":
    pytest.main([__file__])
