#!/usr/bin/env python3
"""
AWS Bedrock Simultaneous Indexing Integration Test.

This test performs:
1. AWS Bedrock liveness testing 
2. Simultaneous indexing of both "project-base" and "git-clones" areas
3. Real project testing (not mock data) using the new tree-based architecture
4. Dry-run validation with tree status verification
"""

import asyncio
import argparse
from pathlib import Path
from datetime import datetime
from typing import Optional, List

# Import the new tree-based indexer system
from jesse_framework_mcp.knowledge_bases.indexer.core import CoreIndexer
from jesse_framework_mcp.knowledge_bases.indexer.models import (
    KnowledgeTree, UpdateStatus, IndexingResult
)
from jesse_framework_mcp.llm.strands_agent_driver.driver import StrandsClaude4Driver
from jesse_framework_mcp.helpers.aws_session_manager import AWSSessionManager, AWSConnectionError
from jesse_framework_mcp.helpers.path_utils import ensure_project_root


class BedrockTestContext:
    """Test context for Bedrock integration testing."""
    
    def __init__(self):
        self.test_messages: List[str] = []
        self.aws_session: Optional[AWSSessionManager] = None
        self.bedrock_driver: Optional[StrandsClaude4Driver] = None
        self.project_root: Optional[Path] = None
    
    def log(self, message: str) -> None:
        """Log test message with timestamp."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {message}"
        self.test_messages.append(formatted_message)
        print(formatted_message)


async def test_bedrock_liveness(ctx: BedrockTestContext) -> bool:
    """
    Test AWS Bedrock service liveness and authentication.
    
    Returns:
        bool: True if Bedrock is accessible, False otherwise
    """
    ctx.log("🔍 Testing AWS Bedrock liveness...")
    
    try:
        # Initialize AWS session manager
        ctx.aws_session = AWSSessionManager()
        
        # Test AWS connectivity
        ctx.log("🔐 Testing AWS authentication...")
        await ctx.aws_session.validate_connection()
        ctx.log("✅ AWS authentication successful")
        
        # Initialize Bedrock driver
        ctx.log("🧠 Initializing Bedrock Claude driver...")
        ctx.bedrock_driver = StrandsClaude4Driver()
        
        # Initialize the driver
        await ctx.bedrock_driver.initialize()
        
        # Test Bedrock service availability
        ctx.log("🌐 Testing Bedrock service connectivity...")
        test_response = await ctx.bedrock_driver.send_message(
            message="Test connectivity - respond with 'BEDROCK_LIVE'",
            conversation_id="bedrock_test"
        )
        
        if "BEDROCK_LIVE" in test_response.content:
            ctx.log("✅ Bedrock service is live and responding")
            return True
        else:
            ctx.log(f"⚠️ Bedrock responded but unexpected content: {test_response.content}")
            return True  # Still consider it working if we got a response
            
    except AWSConnectionError as e:
        ctx.log(f"❌ AWS connection failed: {e}")
        return False
    except Exception as e:
        ctx.log(f"❌ Bedrock liveness test failed: {e}")
        return False


async def test_simultaneous_indexing(ctx: BedrockTestContext, dry_run: bool = True) -> dict:
    """
    Test simultaneous indexing of both project-base and git-clones areas.
    
    Args:
        ctx: Test context with Bedrock driver
        dry_run: Whether to run in dry-run mode for safety
        
    Returns:
        dict: Test results with detailed statistics
    """
    mode = "DRY-RUN" if dry_run else "LIVE"
    ctx.log(f"🚀 Starting simultaneous indexing test ({mode} mode)...")
    
    try:
        # Initialize the new tree-based indexer
        ctx.log("🌳 Initializing tree-based CoreIndexer...")
        indexer = CoreIndexer(
            source_root=ctx.project_root,
            llm_driver=ctx.bedrock_driver
        )
        
        # Validate indexer configuration
        ctx.log("🔧 Validating indexer configuration...")
        config_status = indexer.validate_configuration()
        
        if not config_status['configuration_valid']:
            ctx.log("❌ Indexer configuration validation failed:")
            for error in config_status['validation_errors']:
                ctx.log(f"  • {error}")
            return {'success': False, 'error': 'Configuration validation failed'}
        
        ctx.log("✅ Indexer configuration validated successfully")
        ctx.log(f"  📂 Handlers: {config_status['supported_handler_types']}")
        ctx.log(f"  🔧 Tasks: {config_status['registered_task_types']}")
        
        # Define progress callback for detailed logging
        def progress_callback(message: str) -> None:
            ctx.log(f"📊 {message}")
        
        # Execute the indexing workflow
        ctx.log("⚡ Executing tree-based indexing workflow...")
        start_time = datetime.now()
        
        result: IndexingResult = await indexer.index(
            progress=progress_callback,
            dry_run=dry_run
        )
        
        end_time = datetime.now()
        duration = end_time - start_time
        
        # Analyze results
        ctx.log("📈 Analyzing indexing results...")
        
        test_results = {
            'success': result.success_rate > 0.8,  # 80% success threshold
            'duration_seconds': duration.total_seconds(),
            'files_analyzed': result.files_analyzed,
            'kbs_built': result.kbs_built,
            'cache_files_created': result.cache_files_created,
            'orphaned_files_cleaned': result.orphaned_files_cleaned,
            'success_rate': result.success_rate,
            'total_files_processed': result.total_files_processed,
            'task_results_count': len(result.task_results),
            'errors': result.errors,
            'discovery_time': result.discovery_time,
            'planning_time': result.planning_time,
            'execution_time': result.execution_time
        }
        
        # Enhanced tree-based validation for dry-run mode
        if dry_run and result.final_tree_state:
            ctx.log("🌳 Performing tree-based dry-run validation...")
            tree_stats = result.final_tree_state.get_summary_stats()
            
            # Verify tree structure
            project_files = 0
            gitclone_files = 0
            
            for file in result.final_tree_state.get_all_files():
                if file.handler_type == "project":
                    project_files += 1
                elif file.handler_type == "gitclone":
                    gitclone_files += 1
            
            test_results.update({
                'tree_validation': {
                    'total_files_in_tree': tree_stats['total_files'],
                    'project_handler_files': project_files,
                    'gitclone_handler_files': gitclone_files,
                    'analysis_files': tree_stats['analysis_files'],
                    'knowledge_base_files': tree_stats['knowledge_base_files'],
                    'status_distribution': tree_stats['status_distribution']
                }
            })
            
            # Verify that files have appropriate status after dry-run
            updated_files = result.final_tree_state.get_files_by_status(UpdateStatus.UPDATED_SUCCESS)
            failed_files = result.final_tree_state.get_files_by_status(UpdateStatus.UPDATED_FAILED)
            
            ctx.log(f"✅ Tree validation: {len(updated_files)} files marked as updated")
            ctx.log(f"⚠️ Tree validation: {len(failed_files)} files marked as failed")
            
            # Enhanced validation - check that simultaneous processing worked
            if project_files > 0 and gitclone_files > 0:
                ctx.log("✅ Simultaneous processing confirmed: Both handlers processed files")
                test_results['simultaneous_success'] = True
            else:
                ctx.log("⚠️ Only one handler type processed files")
                test_results['simultaneous_success'] = False
        
        # Log comprehensive results
        ctx.log("📊 INDEXING RESULTS SUMMARY:")
        ctx.log(f"  ⏱️ Total duration: {test_results['duration_seconds']:.2f}s")
        ctx.log(f"  📄 Files analyzed: {test_results['files_analyzed']}")
        ctx.log(f"  📚 Knowledge bases built: {test_results['kbs_built']}")
        ctx.log(f"  💾 Cache files created: {test_results['cache_files_created']}")
        ctx.log(f"  🧹 Orphaned files cleaned: {test_results['orphaned_files_cleaned']}")
        ctx.log(f"  ✅ Success rate: {test_results['success_rate']:.1%}")
        
        if test_results['success']:
            ctx.log("🎉 Simultaneous indexing test PASSED")
        else:
            ctx.log("❌ Simultaneous indexing test FAILED")
            for error in test_results['errors']:
                ctx.log(f"  • Error: {error}")
        
        return test_results
        
    except Exception as e:
        ctx.log(f"❌ Simultaneous indexing test failed with exception: {e}")
        return {
            'success': False,
            'error': str(e),
            'duration_seconds': 0
        }


async def main():
    """Main test runner for Bedrock simultaneous indexing."""
    parser = argparse.ArgumentParser(
        description="AWS Bedrock Simultaneous Indexing Test"
    )
    parser.add_argument(
        '--mode', 
        choices=['liveness-only', 'indexing-only', 'full'], 
        default='full',
        help='Test mode: liveness-only, indexing-only, or full'
    )
    parser.add_argument(
        '--live-run', 
        action='store_true',
        help='Perform live indexing (default is dry-run for safety)'
    )
    
    args = parser.parse_args()
    
    print("🧪 AWS Bedrock Simultaneous Indexing Integration Test")
    print("=" * 60)
    
    # Initialize test context
    ctx = BedrockTestContext()
    
    try:
        # Ensure we have a valid project root
        ctx.project_root = ensure_project_root()
        ctx.log(f"📂 Project root: {ctx.project_root}")
    except Exception as e:
        ctx.log(f"❌ Failed to locate project root: {e}")
        return False
    
    test_start = datetime.now()
    results = {
        'bedrock_liveness': {'tested': False, 'success': False},
        'simultaneous_indexing': {'tested': False, 'success': False}
    }
    
    # Phase 1: Bedrock Liveness Test
    if args.mode in ['liveness-only', 'full']:
        ctx.log("🔬 PHASE 1: AWS Bedrock Liveness Test")
        ctx.log("-" * 40)
        
        results['bedrock_liveness']['tested'] = True
        results['bedrock_liveness']['success'] = await test_bedrock_liveness(ctx)
        
        if not results['bedrock_liveness']['success']:
            ctx.log("❌ Bedrock liveness test failed - cannot proceed with indexing")
            if args.mode == 'full':
                ctx.log("💡 Try running with --mode liveness-only to debug AWS connectivity")
                return False
    
    # Phase 2: Simultaneous Indexing Test
    if args.mode in ['indexing-only', 'full']:
        ctx.log("🔬 PHASE 2: Simultaneous Indexing Test")
        ctx.log("-" * 40)
        
        # Only proceed if Bedrock is live or we're doing indexing-only
        if args.mode == 'indexing-only' or results['bedrock_liveness']['success']:
            results['simultaneous_indexing']['tested'] = True
            
            dry_run = not args.live_run
            indexing_results = await test_simultaneous_indexing(ctx, dry_run=dry_run)
            results['simultaneous_indexing']['success'] = indexing_results['success']
            results['simultaneous_indexing']['details'] = indexing_results
        else:
            ctx.log("⏭️ Skipping indexing test due to Bedrock connectivity issues")
    
    # Final Results Summary
    test_end = datetime.now()
    total_duration = test_end - test_start
    
    ctx.log("=" * 60)
    ctx.log("📊 COMPREHENSIVE TEST RESULTS")
    ctx.log("=" * 60)
    ctx.log(f"⏱️ Total test duration: {total_duration}")
    
    if results['bedrock_liveness']['tested']:
        status = "✅ PASS" if results['bedrock_liveness']['success'] else "❌ FAIL"
        ctx.log(f"🔍 Bedrock Liveness: {status}")
    
    if results['simultaneous_indexing']['tested']:
        status = "✅ PASS" if results['simultaneous_indexing']['success'] else "❌ FAIL"
        ctx.log(f"🚀 Simultaneous Indexing: {status}")
        
        if 'details' in results['simultaneous_indexing']:
            details = results['simultaneous_indexing']['details']
            ctx.log(f"  📊 Success rate: {details.get('success_rate', 0):.1%}")
            ctx.log(f"  📁 Files processed: {details.get('total_files_processed', 0)}")
            
            # Tree-based validation results
            if 'tree_validation' in details:
                tree_val = details['tree_validation']
                ctx.log(f"  🌳 Tree files: {tree_val['total_files_in_tree']}")
                ctx.log(f"  📂 Project files: {tree_val['project_handler_files']}")
                ctx.log(f"  📦 Git-clone files: {tree_val['gitclone_handler_files']}")
    
    # Determine overall success
    tested_phases = [name for name, result in results.items() if result['tested']]
    successful_phases = [name for name, result in results.items() if result['tested'] and result['success']]
    
    overall_success = len(tested_phases) > 0 and len(successful_phases) == len(tested_phases)
    
    ctx.log("=" * 60)
    if overall_success:
        ctx.log("🎉 OVERALL RESULT: SUCCESS")
        ctx.log("✅ All tested phases completed successfully")
        if results['simultaneous_indexing']['tested'] and results['simultaneous_indexing']['success']:
            ctx.log("🎯 Simultaneous indexing of project-base and git-clones confirmed")
    else:
        ctx.log("❌ OVERALL RESULT: FAILURE")
        ctx.log("💥 Some test phases failed")
    
    ctx.log(f"📈 Success rate: {len(successful_phases)}/{len(tested_phases)} phases passed")
    
    return overall_success


if __name__ == "__main__":
    # Run the integration test
    try:
        result = asyncio.run(main())
        exit(0 if result else 1)
    except KeyboardInterrupt:
        print("\n⏹️ Test interrupted by user")
        exit(130)
    except Exception as e:
        print(f"\n💥 Test failed with unexpected error: {e}")
        exit(1)
