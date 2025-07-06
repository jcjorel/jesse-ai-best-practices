#!/usr/bin/env python3
"""
Test for centralized RebuildDecisionEngine fixing scattered decision logic issues.

This test specifically addresses the two issues mentioned:
1. Empty directories (like "image") rebuilding every time with "REBUILDING KB: image - KB file doesn't exist"
2. Missing global summary at project-base level (root_kb.md)
"""

import asyncio
import tempfile
import shutil
from pathlib import Path
from datetime import datetime
from typing import List

# Import the decision engine and models
from jesse_framework_mcp.knowledge_bases.indexing.rebuild_decision_engine import RebuildDecisionEngine
from jesse_framework_mcp.knowledge_bases.models.indexing_config import (
    IndexingConfig, IndexingMode, 
    OutputConfig, ChangeDetectionConfig
)
from jesse_framework_mcp.knowledge_bases.models.knowledge_context import DirectoryContext, FileContext
from jesse_framework_mcp.knowledge_bases.models.rebuild_decisions import DecisionOutcome, DecisionReason


class MockContext:
    """
    [Class intent]
    Simple mock implementation of FastMCP Context for decision engine testing.
    Captures all messages and provides them for test verification and analysis.

    [Design principles]
    Minimal mock preserving essential interface for decision engine testing.
    Message capture enabling verification of decision reasoning and logic.
    Real-time message display for debugging test execution and decision analysis.

    [Implementation details]
    Stores messages in categorized lists for post-processing verification.
    Provides async methods matching FastMCP Context interface requirements.
    Prints messages for real-time debugging during test execution.
    """
    
    def __init__(self):
        """
        [Class method intent]
        Initializes mock context with message storage for decision engine testing.

        [Design principles]
        Simple initialization preparing comprehensive message collection for verification.

        [Implementation details]
        Creates separate lists for different message types supporting detailed verification.
        """
        self.info_messages: List[str] = []
        self.debug_messages: List[str] = []
        self.warning_messages: List[str] = []
        self.error_messages: List[str] = []
    
    async def info(self, message: str) -> None:
        """
        [Class method intent]
        Captures info messages from decision engine for verification and analysis.

        [Design principles]
        Message capture enabling verification of decision engine reasoning and logic.

        [Implementation details]
        Stores message and displays for real-time debugging during test execution.
        """
        self.info_messages.append(message)
        print(f"INFO: {message}")
    
    async def debug(self, message: str) -> None:
        """
        [Class method intent]
        Captures debug messages from decision engine for detailed verification.

        [Design principles]
        Debug message capture supporting comprehensive decision logic verification.

        [Implementation details]
        Stores message in debug collection for post-processing verification.
        """
        self.debug_messages.append(message)
        print(f"DEBUG: {message}")
    
    async def warning(self, message: str) -> None:
        """
        [Class method intent]
        Captures warning messages from decision engine for issue identification.

        [Design principles]
        Warning capture enabling identification of decision logic issues and edge cases.

        [Implementation details]
        Stores warning message and displays for immediate attention during testing.
        """
        self.warning_messages.append(message)
        print(f"WARNING: {message}")
    
    async def error(self, message: str) -> None:
        """
        [Class method intent]
        Captures error messages from decision engine for failure analysis.

        [Design principles]
        Error message capture enabling comprehensive failure analysis and debugging.

        [Implementation details]
        Stores error message and displays prominently for immediate attention.
        """
        self.error_messages.append(message)
        print(f"ERROR: {message}")


async def test_empty_directory_decision():
    """
    [Function intent]
    Tests that empty directories are properly handled with SKIP decision instead of infinite rebuilds.
    Addresses the "REBUILDING KB: image - KB file doesn't exist" issue by verifying
    empty directories get SKIP decisions with EMPTY_DIRECTORY reasoning.

    [Design principles]
    KISS approach testing core empty directory handling functionality.
    Single test scenario focused on the specific reported issue with empty directories.
    Clear verification of decision outcome and reasoning for empty directory scenarios.
    Comprehensive error monitoring enabling clear success/failure determination.

    [Implementation details]
    Creates empty directory context simulating problematic "image" directory scenario.
    Uses RebuildDecisionEngine to make directory decision with comprehensive verification.
    Verifies decision outcome is SKIP with EMPTY_DIRECTORY reasoning preventing infinite loops.
    Checks for proper messaging indicating empty directory detection and handling.
    """
    print("=== Testing Empty Directory Decision (Issue #1) ===")
    
    # Create test configuration
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Create empty directory scenario (like "image" directory)
        empty_dir = temp_path / "image"
        empty_dir.mkdir()
        
        config = IndexingConfig(
            output_config=OutputConfig(knowledge_output_directory=temp_path / ".knowledge"),
            change_detection=ChangeDetectionConfig(
                indexing_mode=IndexingMode.INCREMENTAL,
                timestamp_tolerance_seconds=1.0
            )
        )
        
        # Create empty directory context (no files, no subdirectories)
        empty_directory_context = DirectoryContext(
            directory_path=empty_dir,
            file_contexts=[],  # No files
            subdirectory_contexts=[]  # No subdirectories
        )
        
        # Create decision engine and mock context
        decision_engine = RebuildDecisionEngine(config)
        ctx = MockContext()
        
        try:
            # Make decision for empty directory
            decision = await decision_engine.should_rebuild_directory(
                empty_directory_context, temp_path, ctx
            )
            
            # Verify decision outcome
            print(f"Decision outcome: {decision.outcome.value}")
            print(f"Decision reason: {decision.reason.value}")
            print(f"Decision reasoning: {decision.reasoning_text}")
            
            # Test assertions
            assert decision.outcome == DecisionOutcome.SKIP, f"Expected SKIP, got {decision.outcome.value}"
            assert decision.reason == DecisionReason.EMPTY_DIRECTORY, f"Expected EMPTY_DIRECTORY, got {decision.reason.value}"
            assert "no processable" in decision.reasoning_text.lower(), f"Expected empty directory reasoning, got: {decision.reasoning_text}"
            
            # Verify debug messages indicate empty directory detection
            empty_messages = [msg for msg in ctx.debug_messages if "📁 EMPTY" in msg]
            assert len(empty_messages) > 0, "Expected '📁 EMPTY' debug message indicating empty directory detection"
            
            print("✅ PASS: Empty directory correctly identified and skipped")
            print("✅ PASS: No infinite rebuild loop for empty directories")
            return True
            
        except Exception as e:
            print(f"❌ FAIL: Empty directory test failed: {e}")
            return False


async def test_project_root_decision():
    """
    [Function intent]
    Tests that project root directories get REBUILD decision ensuring root_kb.md generation.
    Addresses the missing global summary issue by verifying project root always processes
    with PROJECT_ROOT_FORCED reasoning regardless of change detection.

    [Design principles]
    KISS approach testing core project root handling functionality.
    Single test scenario focused on the specific reported issue with missing root_kb.md.
    Clear verification of decision outcome and reasoning for project root scenarios.
    Comprehensive error monitoring enabling clear success/failure determination.

    [Implementation details]
    Creates project root directory context simulating the missing root_kb.md scenario.
    Uses RebuildDecisionEngine to make directory decision with comprehensive verification.
    Verifies decision outcome is REBUILD with PROJECT_ROOT_FORCED reasoning ensuring generation.
    Checks for proper messaging indicating project root detection and forced processing.
    """
    print("=== Testing Project Root Decision (Issue #2) ===")
    
    # Create test configuration
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Create project root scenario with some content
        project_file = temp_path / "README.md"
        project_file.write_text("# Test Project")
        
        config = IndexingConfig(
            output_config=OutputConfig(knowledge_output_directory=temp_path / ".knowledge"),
            change_detection=ChangeDetectionConfig(
                indexing_mode=IndexingMode.INCREMENTAL,
                timestamp_tolerance_seconds=1.0
            )
        )
        
        # Create project root directory context (with some content)
        project_root_context = DirectoryContext(
            directory_path=temp_path,
            file_contexts=[
                FileContext(
                    file_path=project_file,
                    file_size=project_file.stat().st_size,
                    last_modified=datetime.fromtimestamp(project_file.stat().st_mtime)
                )
            ],
            subdirectory_contexts=[]
        )
        
        # Create decision engine and mock context
        decision_engine = RebuildDecisionEngine(config)
        ctx = MockContext()
        
        try:
            # Make decision for project root (source_root = temp_path)
            decision = await decision_engine.should_rebuild_directory(
                project_root_context, temp_path, ctx  # source_root = temp_path makes this project root
            )
            
            # Verify decision outcome
            print(f"Decision outcome: {decision.outcome.value}")
            print(f"Decision reason: {decision.reason.value}")
            print(f"Decision reasoning: {decision.reasoning_text}")
            
            # Test assertions
            assert decision.outcome == DecisionOutcome.REBUILD, f"Expected REBUILD, got {decision.outcome.value}"
            assert decision.reason == DecisionReason.PROJECT_ROOT_FORCED, f"Expected PROJECT_ROOT_FORCED, got {decision.reason.value}"
            assert "project root" in decision.reasoning_text.lower(), f"Expected project root reasoning, got: {decision.reasoning_text}"
            assert "root_kb.md" in decision.reasoning_text, f"Expected root_kb.md mention, got: {decision.reasoning_text}"
            
            # Verify debug messages indicate project root detection
            root_messages = [msg for msg in ctx.debug_messages if "🏗️ PROJECT ROOT" in msg]
            assert len(root_messages) > 0, "Expected '🏗️ PROJECT ROOT' debug message indicating project root detection"
            
            print("✅ PASS: Project root correctly identified for forced processing")
            print("✅ PASS: root_kb.md generation ensured for project root")
            return True
            
        except Exception as e:
            print(f"❌ FAIL: Project root test failed: {e}")
            return False


async def test_regular_directory_decision():
    """
    [Function intent]
    Tests that regular directories with content get proper staleness-based decisions.
    Verifies the decision engine correctly handles normal directories using comprehensive
    staleness checking without the special case handling of empty dirs or project root.

    [Design principles]
    KISS approach testing normal directory decision logic functionality.
    Single test scenario verifying standard directory processing behavior.
    Clear verification that regular directories get staleness-based decision making.
    Comprehensive error monitoring enabling clear success/failure determination.

    [Implementation details]
    Creates regular directory context with processable content for normal decision testing.
    Uses RebuildDecisionEngine to make directory decision using standard staleness logic.
    Verifies decision outcome uses COMPREHENSIVE_STALENESS reasoning for normal directories.
    Checks that regular directories don't get special case handling inappropriately.
    """
    print("=== Testing Regular Directory Decision (Normal Case) ===")
    
    # Create test configuration
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Create regular directory with content
        regular_dir = temp_path / "src"
        regular_dir.mkdir()
        source_file = regular_dir / "main.py"
        source_file.write_text("print('Hello, World!')")
        
        config = IndexingConfig(
            output_config=OutputConfig(knowledge_output_directory=temp_path / ".knowledge"),
            change_detection=ChangeDetectionConfig(
                indexing_mode=IndexingMode.INCREMENTAL,
                timestamp_tolerance_seconds=1.0
            )
        )
        
        # Create regular directory context (with content)
        regular_directory_context = DirectoryContext(
            directory_path=regular_dir,
            file_contexts=[
                FileContext(
                    file_path=source_file,
                    file_size=source_file.stat().st_size,
                    last_modified=datetime.fromtimestamp(source_file.stat().st_mtime)
                )
            ],
            subdirectory_contexts=[]
        )
        
        # Create decision engine and mock context
        decision_engine = RebuildDecisionEngine(config)
        ctx = MockContext()
        
        try:
            # Make decision for regular directory (not project root, has content)
            decision = await decision_engine.should_rebuild_directory(
                regular_directory_context, temp_path, ctx
            )
            
            # Verify decision outcome
            print(f"Decision outcome: {decision.outcome.value}")
            print(f"Decision reason: {decision.reason.value}")
            print(f"Decision reasoning: {decision.reasoning_text}")
            
            # Test assertions - should use staleness-based logic
            assert decision.outcome in [DecisionOutcome.REBUILD, DecisionOutcome.SKIP], f"Expected REBUILD or SKIP, got {decision.outcome.value}"
            
            # Should NOT be empty directory or project root reasons
            assert decision.reason != DecisionReason.EMPTY_DIRECTORY, "Regular directory should not get EMPTY_DIRECTORY reason"
            assert decision.reason != DecisionReason.PROJECT_ROOT_FORCED, "Regular directory should not get PROJECT_ROOT_FORCED reason"
            
            # Should use comprehensive staleness logic
            expected_reasons = [DecisionReason.COMPREHENSIVE_STALENESS, DecisionReason.UP_TO_DATE]
            assert decision.reason in expected_reasons, f"Expected staleness-based reason, got {decision.reason.value}"
            
            print("✅ PASS: Regular directory uses staleness-based decision logic")
            print("✅ PASS: No inappropriate special case handling for regular directories")
            return True
            
        except Exception as e:
            print(f"❌ FAIL: Regular directory test failed: {e}")
            return False


async def test_comprehensive_decision_analysis():
    """
    [Function intent]
    Tests the comprehensive hierarchy decision analysis providing complete action planning.
    Verifies the decision engine can analyze entire directory hierarchies and provide
    structured decision reports with rebuild and deletion decisions.

    [Design principles]
    KISS approach testing comprehensive decision analysis functionality.
    Mixed scenario testing with empty directories, regular directories, and project root.
    Clear verification of comprehensive decision reporting and action planning.
    Error monitoring enabling verification of complete decision analysis capability.

    [Implementation details]
    Creates mixed directory hierarchy with empty dirs, regular dirs, and project root.
    Uses RebuildDecisionEngine.analyze_hierarchy for comprehensive decision analysis.
    Verifies DecisionReport contains proper decisions for all directory types.
    Checks decision statistics and reasoning for comprehensive analysis coverage.
    """
    print("=== Testing Comprehensive Decision Analysis ===")
    
    # Create test configuration
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Create mixed hierarchy
        # Project root (should get REBUILD with PROJECT_ROOT_FORCED)
        root_file = temp_path / "README.md"
        root_file.write_text("# Test Project")
        
        # Regular directory with content (should get staleness-based decision)
        src_dir = temp_path / "src"
        src_dir.mkdir()
        src_file = src_dir / "main.py"
        src_file.write_text("print('Hello')")
        
        # Empty directory (should get SKIP with EMPTY_DIRECTORY)
        empty_dir = temp_path / "image"
        empty_dir.mkdir()
        
        config = IndexingConfig(
            output_config=OutputConfig(knowledge_output_directory=temp_path / ".knowledge"),
            change_detection=ChangeDetectionConfig(
                indexing_mode=IndexingMode.INCREMENTAL,
                timestamp_tolerance_seconds=1.0
            )
        )
        
        # Build directory hierarchy
        empty_dir_context = DirectoryContext(
            directory_path=empty_dir,
            file_contexts=[],
            subdirectory_contexts=[]
        )
        
        src_dir_context = DirectoryContext(
            directory_path=src_dir,
            file_contexts=[
                FileContext(
                    file_path=src_file,
                    file_size=src_file.stat().st_size,
                    last_modified=datetime.fromtimestamp(src_file.stat().st_mtime)
                )
            ],
            subdirectory_contexts=[]
        )
        
        root_context = DirectoryContext(
            directory_path=temp_path,
            file_contexts=[
                FileContext(
                    file_path=root_file,
                    file_size=root_file.stat().st_size,
                    last_modified=datetime.fromtimestamp(root_file.stat().st_mtime)
                )
            ],
            subdirectory_contexts=[src_dir_context, empty_dir_context]
        )
        
        # Create decision engine and mock context
        decision_engine = RebuildDecisionEngine(config)
        ctx = MockContext()
        
        try:
            # Perform comprehensive analysis
            report = await decision_engine.analyze_hierarchy(root_context, temp_path, ctx)
            
            # Verify report structure
            print(f"Total decisions: {report.total_decisions}")
            print(f"Files to rebuild: {len(report.files_to_rebuild)}")
            print(f"Files to delete: {len(report.files_to_delete)}")
            
            # Get summary statistics
            stats = report.get_summary_statistics()
            print(f"Summary statistics: {stats}")
            
            # Verify expected decisions were made
            assert report.total_decisions >= 3, f"Expected at least 3 decisions (root, src, image), got {report.total_decisions}"
            
            # Check for specific decision outcomes
            root_decision = report.get_decision_for_path(temp_path)
            assert root_decision is not None, "Expected decision for project root"
            
            empty_decision = report.get_decision_for_path(empty_dir)
            assert empty_decision is not None, "Expected decision for empty directory"
            
            src_decision = report.get_decision_for_path(src_dir)
            assert src_decision is not None, "Expected decision for src directory"
            
            print("✅ PASS: Comprehensive decision analysis completed")
            print("✅ PASS: Decision report contains expected decisions")
            print("✅ PASS: Mixed directory hierarchy handled correctly")
            return True
            
        except Exception as e:
            print(f"❌ FAIL: Comprehensive analysis test failed: {e}")
            import traceback
            traceback.print_exc()
            return False


async def main():
    """
    [Function intent]
    Main test runner for centralized decision engine addressing scattered logic issues.
    Executes all decision engine tests and provides comprehensive pass/fail reporting.

    [Design principles]
    Comprehensive test execution covering both specific reported issues and general functionality.
    Clear result reporting enabling easy assessment of decision engine functionality.
    Error isolation preventing individual test failures from stopping overall test execution.

    [Implementation details]
    Executes all decision engine tests with individual error handling.
    Reports final success/failure status with detailed test results.
    Provides clear indication of whether reported issues have been resolved.
    """
    print("Centralized Decision Engine Tests - Addressing Scattered Logic Issues")
    print("=" * 70)
    
    test_results = []
    
    try:
        # Test Issue #1: Empty directories rebuilding infinitely
        result1 = await test_empty_directory_decision()
        test_results.append(("Empty Directory Handling", result1))
        
        print("\n" + "-" * 50 + "\n")
        
        # Test Issue #2: Missing project root summary generation
        result2 = await test_project_root_decision()
        test_results.append(("Project Root Handling", result2))
        
        print("\n" + "-" * 50 + "\n")
        
        # Test normal directory decision logic
        result3 = await test_regular_directory_decision()
        test_results.append(("Regular Directory Handling", result3))
        
        print("\n" + "-" * 50 + "\n")
        
        # Test comprehensive decision analysis
        result4 = await test_comprehensive_decision_analysis()
        test_results.append(("Comprehensive Decision Analysis", result4))
        
        # Report final results
        print("\n" + "=" * 70)
        print("FINAL TEST RESULTS:")
        
        all_passed = True
        for test_name, result in test_results:
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"{status}: {test_name}")
            if not result:
                all_passed = False
        
        print("\n" + "=" * 70)
        if all_passed:
            print("🎉 ALL TESTS PASSED")
            print("✅ Empty directory infinite rebuild issue RESOLVED")
            print("✅ Missing project root summary issue RESOLVED")
            print("✅ Centralized decision engine working correctly")
        else:
            print("❌ SOME TESTS FAILED")
            print("💥 Issues may not be fully resolved")
        
        return all_passed
        
    except Exception as e:
        print(f"🚨 TEST EXECUTION FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    # Run the centralized decision engine tests
    result = asyncio.run(main())
    exit(0 if result else 1)
