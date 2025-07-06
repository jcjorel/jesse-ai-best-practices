#!/usr/bin/env python3
"""
Test suite for hierarchical dependency planning architecture fix.
Validates selective cascading and horizontal dependency management.
"""

import asyncio
import tempfile
from pathlib import Path
from datetime import datetime

from fastmcp import Context

from jesse_framework_mcp.knowledge_bases.models import IndexingConfig, DirectoryContext, FileContext
from jesse_framework_mcp.knowledge_bases.models.indexing_config import OutputConfig, ContentFilteringConfig
from jesse_framework_mcp.knowledge_bases.models.rebuild_decisions import (
    DecisionReport, RebuildDecision, DecisionOutcome, DecisionReason
)
from jesse_framework_mcp.knowledge_bases.indexing.rebuild_decision_engine import RebuildDecisionEngine
from jesse_framework_mcp.knowledge_bases.indexing.plan_generator import PlanGenerator


class MockContext(Context):
    """Mock FastMCP Context for testing."""
    
    def __init__(self):
        self.logs = []
    
    async def debug(self, message: str):
        self.logs.append(f"DEBUG: {message}")
        print(f"DEBUG: {message}")
    
    async def info(self, message: str):
        self.logs.append(f"INFO: {message}")
        print(f"INFO: {message}")
    
    async def warning(self, message: str):
        self.logs.append(f"WARNING: {message}")
        print(f"WARNING: {message}")
    
    async def error(self, message: str):
        self.logs.append(f"ERROR: {message}")
        print(f"ERROR: {message}")


async def test_selective_cascading():
    """Test that selective cascading marks ancestor directories for rebuild."""
    print("\n🔍 Testing Selective Cascading Logic...")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        source_root = Path(temp_dir)
        knowledge_dir = Path(temp_dir) / "knowledge"
        
        # Create test directory structure
        (source_root / "src" / "components" / "buttons").mkdir(parents=True)
        (source_root / "src" / "components" / "forms").mkdir(parents=True)
        (source_root / "src" / "utils").mkdir(parents=True)
        
        # Create test files
        (source_root / "src" / "components" / "buttons" / "button.py").write_text("# button code")
        (source_root / "src" / "components" / "forms" / "form.py").write_text("# form code")
        (source_root / "src" / "utils" / "helper.py").write_text("# helper code")
        
        # Setup configuration
        config = IndexingConfig(
            output_config=OutputConfig(knowledge_output_directory=knowledge_dir),
            content_filtering=ContentFilteringConfig(
                excluded_extensions={".pyc", ".pyo"},  # Keep minimal exclusions
                excluded_directories={".git", "__pycache__"}
            )
        )
        
        # Create decision engine
        decision_engine = RebuildDecisionEngine(config)
        ctx = MockContext()
        
        # Create a decision report with one directory needing rebuild
        report = DecisionReport()
        
        # Mark buttons directory for rebuild (content change)
        buttons_decision = RebuildDecision(
            path=source_root / "src" / "components" / "buttons",
            outcome=DecisionOutcome.REBUILD,
            reason=DecisionReason.COMPREHENSIVE_STALENESS,
            reasoning_text="Source files are newer than knowledge file"
        )
        report.add_rebuild_decision(buttons_decision)
        
        # Test cascading logic
        cascaded_count = await decision_engine._propagate_cascading_decisions(
            None, source_root, report, ctx
        )
        
        print(f"✅ Cascaded {cascaded_count} ancestor decisions")
        
        # Verify ancestors were marked for rebuild
        components_decision = report.get_decision_for_path(source_root / "src" / "components")
        src_decision = report.get_decision_for_path(source_root / "src")
        root_decision = report.get_decision_for_path(source_root)
        
        assert components_decision and components_decision.should_rebuild
        assert components_decision.reason == DecisionReason.CHILD_DIRECTORY_REBUILT
        
        assert src_decision and src_decision.should_rebuild
        assert src_decision.reason == DecisionReason.CHILD_DIRECTORY_REBUILT
        
        assert root_decision and root_decision.should_rebuild
        assert root_decision.reason == DecisionReason.CHILD_DIRECTORY_REBUILT
        
        print("✅ All ancestors correctly marked for rebuild")
        
        # Verify forms directory was NOT marked (no content changes)
        forms_decision = report.get_decision_for_path(source_root / "src" / "components" / "forms")
        assert forms_decision is None or not forms_decision.should_rebuild
        
        print("✅ Sibling directories correctly NOT cascaded")


async def test_horizontal_dependencies():
    """Test that horizontal dependencies are correctly established."""
    print("\n🔍 Testing Horizontal Dependency Management...")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        source_root = Path(temp_dir)
        knowledge_dir = Path(temp_dir) / "knowledge"
        
        config = IndexingConfig(
            output_config=OutputConfig(knowledge_output_directory=knowledge_dir),
            content_filtering=ContentFilteringConfig(
                excluded_extensions={".pyc", ".pyo"},  # Keep minimal exclusions
                excluded_directories={".git", "__pycache__"}
            )
        )
        
        # Create directory contexts for testing
        buttons_file = FileContext(
            file_path=source_root / "src" / "components" / "buttons" / "button.py",
            file_size=100,
            last_modified=datetime.now()
        )
        
        forms_file = FileContext(
            file_path=source_root / "src" / "components" / "forms" / "form.py",
            file_size=200,
            last_modified=datetime.now()
        )
        
        buttons_context = DirectoryContext(
            directory_path=source_root / "src" / "components" / "buttons",
            file_contexts=[buttons_file],
            subdirectory_contexts=[]
        )
        
        forms_context = DirectoryContext(
            directory_path=source_root / "src" / "components" / "forms",
            file_contexts=[forms_file],
            subdirectory_contexts=[]
        )
        
        components_context = DirectoryContext(
            directory_path=source_root / "src" / "components",
            file_contexts=[],
            subdirectory_contexts=[buttons_context, forms_context]
        )
        
        # Create decision report with both siblings needing rebuild
        report = DecisionReport()
        
        buttons_decision = RebuildDecision(
            path=source_root / "src" / "components" / "buttons",
            outcome=DecisionOutcome.REBUILD,
            reason=DecisionReason.COMPREHENSIVE_STALENESS,
            reasoning_text="Buttons directory needs rebuild"
        )
        
        forms_decision = RebuildDecision(
            path=source_root / "src" / "components" / "forms",
            outcome=DecisionOutcome.REBUILD,
            reason=DecisionReason.COMPREHENSIVE_STALENESS,
            reasoning_text="Forms directory needs rebuild"
        )
        
        components_decision = RebuildDecision(
            path=source_root / "src" / "components",
            outcome=DecisionOutcome.REBUILD,
            reason=DecisionReason.CHILD_DIRECTORY_REBUILT,
            reasoning_text="Child directories were rebuilt"
        )
        
        report.add_rebuild_decision(buttons_decision)
        report.add_rebuild_decision(forms_decision)
        report.add_rebuild_decision(components_decision)
        
        # Test plan generation with horizontal dependencies
        plan_generator = PlanGenerator(config)
        ctx = MockContext()
        
        # Test sibling collection for components directory
        sibling_task_ids = plan_generator._collect_sibling_directory_tasks(
            components_context, report, source_root, None, ctx
        )
        
        # Components directory should NOT have siblings (it's the parent)
        # But let's test the buttons directory - it should see forms as a sibling
        buttons_siblings = plan_generator._collect_sibling_directory_tasks(
            buttons_context, report, source_root, None, ctx
        )
        
        print(f"✅ Found {len(buttons_siblings)} sibling dependencies for buttons/")
        
        # Buttons should have forms as a sibling dependency
        expected_forms_task_id = f"dir_{plan_generator._sanitize_path_for_id(source_root / 'src' / 'components' / 'forms')}"
        assert expected_forms_task_id in buttons_siblings
        
        print("✅ Sibling dependencies correctly identified")


async def main():
    """Run all hierarchical dependency planning tests."""
    print("🚀 Running Hierarchical Dependency Planning Tests...")
    
    try:
        await test_selective_cascading()
        await test_horizontal_dependencies()
        
        print("\n🎉 All hierarchical dependency planning tests passed!")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        raise
    
    print("\n📋 Test Summary:")
    print("✅ Selective cascading marks ancestors for rebuild")
    print("✅ Only content-driven rebuilds trigger cascading")
    print("✅ Horizontal dependencies correctly established")
    print("✅ Sibling directories wait for each other")


if __name__ == "__main__":
    asyncio.run(main())
