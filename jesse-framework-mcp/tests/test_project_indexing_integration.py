#!/usr/bin/env python3
"""
Simple integration test for Knowledge Bases Hierarchical Indexing System.

This test triggers indexing on the actual JESSE Framework project root to verify
the system works with real-world complexity, real files, and real project structures.
Focus is on basic functionality verification and error detection without complex scenarios.
"""

import asyncio
import tempfile
import shutil
from pathlib import Path
from datetime import datetime
from typing import List

# Import the indexing system components
from jesse_framework_mcp.knowledge_bases.indexing.hierarchical_indexer import HierarchicalIndexer
from jesse_framework_mcp.knowledge_bases.models.indexing_config import IndexingConfig, IndexingMode
from jesse_framework_mcp.knowledge_bases.models.knowledge_context import ProcessingStatus
from jesse_framework_mcp.helpers.path_utils import ensure_project_root


class MockContext:
    """
    [Class intent]
    Simple mock implementation of FastMCP Context for integration testing.
    Captures all messages from the indexing process to verify proper operation
    and detect any errors or warnings during real project processing.

    [Design principles]
    Minimal mock preserving essential interface for real project indexing testing.
    Message capture with categorization enabling comprehensive error analysis.
    Real-time message display for monitoring indexing progress during testing.

    [Implementation details]
    Stores messages in categorized lists for post-processing analysis.
    Provides async methods matching FastMCP Context interface requirements.
    Prints messages in real-time for visual monitoring of indexing progress.
    """
    
    def __init__(self):
        """
        [Class method intent]
        Initializes mock context with message storage for integration test verification.

        [Design principles]
        Simple initialization preparing comprehensive message collection for analysis.

        [Implementation details]
        Creates separate lists for different message types supporting detailed analysis.
        """
        self.info_messages: List[str] = []
        self.debug_messages: List[str] = []
        self.warning_messages: List[str] = []
        self.error_messages: List[str] = []
    
    async def info(self, message: str) -> None:
        """
        [Class method intent]
        Captures info messages from indexer for progress monitoring and verification.

        [Design principles]
        Real-time progress reporting enabling visual monitoring during integration testing.

        [Implementation details]
        Stores message and displays immediately for real-time feedback during testing.
        """
        self.info_messages.append(message)
        print(f"INFO: {message}")
    
    async def debug(self, message: str) -> None:
        """
        [Class method intent]
        Captures debug messages from indexer for detailed operation analysis.

        [Design principles]
        Detailed debug information capture supporting comprehensive integration testing.

        [Implementation details]
        Stores message in debug collection for post-processing analysis.
        """
        self.debug_messages.append(message)
        print(f"DEBUG: {message}")
    
    async def warning(self, message: str) -> None:
        """
        [Class method intent]
        Captures warning messages from indexer for issue identification and analysis.

        [Design principles]
        Warning capture enabling identification of non-critical issues during processing.

        [Implementation details]
        Stores warning message and displays for immediate attention during testing.
        """
        self.warning_messages.append(message)
        print(f"WARNING: {message}")
    
    async def error(self, message: str) -> None:
        """
        [Class method intent]
        Captures error messages from indexer for failure analysis and debugging.

        [Design principles]
        Error message capture enabling comprehensive failure analysis and debugging.

        [Implementation details]
        Stores error message and displays prominently for immediate attention.
        """
        self.error_messages.append(message)
        print(f"ERROR: {message}")


async def test_real_project_indexing():
    """
    [Function intent]
    Simple integration test triggering indexing on actual JESSE Framework project root.
    Verifies the system works with real-world complexity without getting distracted by
    complex test scenarios. Focus on basic functionality and error detection.

    [Design principles]
    KISS approach testing core functionality with real project complexity.
    Single test scenario avoiding unnecessary complexity for first integration test.
    Real project structure providing authentic testing conditions and edge cases.
    Comprehensive error monitoring enabling clear success/failure determination.

    [Implementation details]
    Targets actual project root for realistic integration testing conditions.
    Uses incremental mode with project-base indexing for comprehensive coverage.
    Creates debug output directory for detailed analysis of any processing issues.
    Monitors all message types to identify errors, warnings, and success indicators.
    Reports clear success/failure determination with detailed statistics.
    """
    print("=== JESSE Framework Project Root Integration Test ===")
    print("Testing real project indexing with actual complexity and file structures")
    
    # Define project root - use ensure_project_root() for dynamic detection with error handling
    try:
        project_root = ensure_project_root()
        print(f"Target project root: {project_root}")
        print(f"✅ Project root verified: {project_root}")
    except ValueError as e:
        print(f"❌ PROJECT ROOT NOT FOUND: {e}")
        print("This test must be run from the JESSE Framework project environment")
        return False
    except Exception as e:
        print(f"❌ PROJECT ROOT ERROR: {e}")
        print("Unexpected error during project root detection")
        return False
    
    # Create debug directory for detailed analysis
    debug_dir = Path("/tmp/jesse_project_indexing_integration_test")
    if debug_dir.exists():
        shutil.rmtree(debug_dir)
    debug_dir.mkdir(parents=True)
    print(f"Debug output directory: {debug_dir}")
    
    try:
        # Create integration test configuration
        config = IndexingConfig(
            indexing_mode=IndexingMode.INCREMENTAL,  # Safer than FULL for first test
            enable_project_base_indexing=True,       # Index actual project content
            enable_git_clone_indexing=False,         # Focus on project content only
            debug_mode=True,                         # Capture debug info for errors
            debug_output_directory=debug_dir,        # Store debug files for analysis
            enable_llm_replay=False,                 # Force fresh LLM calls
            max_file_size=2 * 1024 * 1024,          # 2MB limit
            batch_size=5,                            # Moderate batch size for stability
            max_concurrent_operations=1,             # Conservative concurrency
            continue_on_file_errors=True,            # Don't stop on individual file failures
            enable_progress_reporting=True           # Monitor progress
        )
        print(f"Configuration: {config.indexing_mode.value} mode, project-base enabled")
        
        # Show what files/directories will be processed
        print("\n=== PROJECT STRUCTURE ANALYSIS ===")
        total_files = 0
        processable_files = 0
        excluded_dirs = 0
        
        for item in project_root.iterdir():
            if item.is_dir():
                if config.should_process_directory(item):
                    dir_files = list(item.rglob("*"))
                    total_in_dir = len([f for f in dir_files if f.is_file()])
                    processable_in_dir = len([f for f in dir_files if f.is_file() and config.should_process_file(f)])
                    print(f"  📁 {item.name}/: {processable_in_dir}/{total_in_dir} processable files")
                    total_files += total_in_dir
                    processable_files += processable_in_dir
                else:
                    excluded_dirs += 1
                    print(f"  🚫 {item.name}/: excluded directory")
            elif item.is_file():
                total_files += 1
                if config.should_process_file(item):
                    processable_files += 1
                    print(f"  📄 {item.name}: processable")
                else:
                    print(f"  🚫 {item.name}: excluded")
        
        print(f"\nSUMMARY: {processable_files}/{total_files} files processable, {excluded_dirs} directories excluded")
        
        # Create mock context for message capture
        ctx = MockContext()
        
        # Create hierarchical indexer
        print("\n=== INDEXING EXECUTION ===")
        print("Creating HierarchicalIndexer...")
        indexer = HierarchicalIndexer(config)
        print("✅ HierarchicalIndexer created successfully")
        
        # Record start time
        start_time = datetime.now()
        print(f"Starting indexing at: {start_time}")
        
        # Execute indexing operation on the real project root
        print("🚀 Starting real project indexing...")
        try:
            result = await indexer.index_hierarchy(project_root, ctx)
            end_time = datetime.now()
            duration = end_time - start_time
            
            print(f"✅ Indexing completed in {duration}")
            
            # Analyze results
            print(f"\n=== INDEXING RESULTS ===")
            print(f"Overall Status: {result.overall_status}")
            print(f"Current Operation: {result.current_operation}")
            print(f"Completion Percentage: {result.completion_percentage:.2f}%")
            
            # Print processing statistics
            stats = result.processing_stats
            print(f"\nProcessing Statistics:")
            print(f"  Files Discovered: {stats.total_files_discovered}")
            print(f"  Files Processed: {stats.files_processed}")
            print(f"  Files Completed: {stats.files_completed}")
            print(f"  Files Failed: {stats.files_failed}")
            print(f"  Files Skipped: {stats.files_skipped}")
            print(f"  Directories Discovered: {stats.total_directories_discovered}")
            print(f"  Directories Completed: {stats.directories_completed}")
            
            # Print context message summary
            print(f"\nContext Messages:")
            print(f"  Info Messages: {len(ctx.info_messages)}")
            print(f"  Debug Messages: {len(ctx.debug_messages)}")
            print(f"  Warning Messages: {len(ctx.warning_messages)}")
            print(f"  Error Messages: {len(ctx.error_messages)}")
            
            # Show critical errors if any
            if ctx.error_messages:
                print(f"\n🚨 CRITICAL ERRORS DETECTED:")
                for i, error in enumerate(ctx.error_messages[:5]):  # Show first 5 errors
                    print(f"  {i+1}. {error}")
                if len(ctx.error_messages) > 5:
                    print(f"  ... and {len(ctx.error_messages) - 5} more errors")
            
            # Show warnings if any
            if ctx.warning_messages:
                print(f"\n⚠️ WARNINGS DETECTED:")
                for i, warning in enumerate(ctx.warning_messages[:3]):  # Show first 3 warnings
                    print(f"  {i+1}. {warning}")
                if len(ctx.warning_messages) > 3:
                    print(f"  ... and {len(ctx.warning_messages) - 3} more warnings")
            
            # Verify debug files were created
            debug_files = list(debug_dir.rglob("*")) if debug_dir.exists() else []
            print(f"\nDebug Files Created: {len(debug_files)}")
            if debug_files:
                print("Debug directory structure:")
                for debug_file in sorted(debug_files)[:10]:  # Show first 10 debug files
                    relative_path = debug_file.relative_to(debug_dir)
                    file_type = "DIR" if debug_file.is_dir() else "FILE"
                    print(f"  {file_type}: {relative_path}")
                if len(debug_files) > 10:
                    print(f"  ... and {len(debug_files) - 10} more debug files")
            
            # Determine overall success
            success_criteria = {
                "Indexing completed": result.overall_status == ProcessingStatus.COMPLETED,
                "Files discovered": stats.total_files_discovered > 0,
                "Some files processed": stats.files_processed > 0,
                "Progress messages": len(ctx.info_messages) > 0,
                "No critical failure": len(ctx.error_messages) < stats.total_files_discovered,  # Some errors OK
                "Debug files generated": len(debug_files) > 0
            }
            
            print(f"\n=== SUCCESS CRITERIA ANALYSIS ===")
            all_criteria_met = True
            for criterion, met in success_criteria.items():
                status = "✅ PASS" if met else "❌ FAIL"
                print(f"{status}: {criterion}")
                if not met:
                    all_criteria_met = False
            
            # Calculate success percentage
            files_success_rate = (stats.files_completed / max(stats.total_files_discovered, 1)) * 100
            print(f"\nFile Processing Success Rate: {files_success_rate:.1f}%")
            
            # Final determination
            integration_success = all_criteria_met and files_success_rate > 50  # Allow some failures
            
            print(f"\n=== FINAL RESULT ===")
            if integration_success:
                print("🎉 INTEGRATION TEST PASSED")
                print("✅ Real project indexing works correctly")
                print("✅ System handles real-world complexity")
                print("✅ No critical system failures detected")
            else:
                print("❌ INTEGRATION TEST FAILED")
                print("💥 Issues detected that need investigation")
                print("🔍 Check debug files and error messages above")
            
            return integration_success
            
        except Exception as e:
            end_time = datetime.now()
            duration = end_time - start_time
            
            print(f"💥 INDEXING FAILED after {duration}")
            print(f"Exception: {type(e).__name__}: {str(e)}")
            
            # Still try to analyze what was captured
            print(f"\nMessage Summary (before failure):")
            print(f"  Info Messages: {len(ctx.info_messages)}")
            print(f"  Debug Messages: {len(ctx.debug_messages)}")
            print(f"  Warning Messages: {len(ctx.warning_messages)}")
            print(f"  Error Messages: {len(ctx.error_messages)}")
            
            if ctx.error_messages:
                print(f"\nLast few error messages:")
                for error in ctx.error_messages[-3:]:
                    print(f"  💥 {error}")
            
            print(f"\n=== INTEGRATION TEST FAILED ===")
            print("❌ System could not complete real project indexing")
            print("🔍 Exception details above indicate the failure point")
            
            import traceback
            traceback.print_exc()
            
            return False
            
    except Exception as e:
        print(f"🚨 TEST SETUP FAILED: {e}")
        print("Could not initialize indexing system for integration test")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        # Preserve debug directory for analysis
        print(f"\n🔧 DEBUG ARTIFACTS PRESERVED: {debug_dir}")
        print("📁 Examine debug files for detailed analysis if issues occurred")


async def main():
    """
    [Function intent]
    Main test runner for real project indexing integration test.
    Executes comprehensive integration testing and provides clear pass/fail determination.

    [Design principles]
    Single comprehensive integration test focusing on real-world project complexity.
    Clear result reporting enabling easy assessment of system functionality.
    Preservation of debug artifacts for detailed analysis when needed.

    [Implementation details]
    Executes real project indexing test with comprehensive error monitoring.
    Reports final success/failure status with detailed analysis information.
    Preserves all debug output for post-test analysis and troubleshooting.
    """
    print("JESSE Framework - Project Root Indexing Integration Test")
    print("=" * 60)
    
    try:
        success = await test_real_project_indexing()
        
        print("\n" + "=" * 60)
        if success:
            print("🎉 INTEGRATION TEST RESULT: SUCCESS")
            print("✅ Real project indexing system verified working")
        else:
            print("❌ INTEGRATION TEST RESULT: FAILURE")
            print("💥 Issues detected - system needs investigation")
        
        return success
        
    except Exception as e:
        print(f"🚨 INTEGRATION TEST EXECUTION FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    # Run the integration test
    result = asyncio.run(main())
    exit(0 if result else 1)
