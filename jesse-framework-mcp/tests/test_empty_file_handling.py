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
# Test module for empty file handling in Knowledge Builder system.
# Verifies that empty files (0 bytes) receive standardized analysis content
# instead of triggering infinite rebuild loops through proper cache management.
###############################################################################
# [Source file design principles]
# - Comprehensive testing of empty file detection and analysis generation
# - Cache behavior verification ensuring empty files create stable cache entries
# - Rebuild loop prevention testing validating fix for infinite rebuild scenarios
# - Integration testing ensuring empty file handling works within full system
# - Performance verification checking that empty files avoid unnecessary LLM calls
###############################################################################
# [Source file constraints]
# - Tests must use temporary files and directories for isolation
# - Empty file creation must use filesystem operations for realistic scenarios
# - Cache verification must check actual file system cache entries
# - All test operations must clean up temporary resources properly
###############################################################################
# [Dependencies]
# <codebase>: ..knowledge_bases.indexing.knowledge_builder - KnowledgeBuilder class under test
# <codebase>: ..knowledge_bases.models - IndexingConfig and FileContext models
# <system>: pytest - Testing framework for test execution and assertions
# <system>: tempfile - Temporary file and directory creation for test isolation
# <system>: pathlib - Cross-platform path operations and file creation
###############################################################################
# [GenAI tool change history]
# 2025-07-07T10:18:00Z : Initial empty file handling test creation by CodeAssistant
# * Created comprehensive test suite for empty file detection and analysis generation
# * Added test for standardized empty file analysis content verification
# * Implemented cache behavior testing ensuring empty files create stable cache entries
# * Created rebuild loop prevention test validating infinite rebuild fix
###############################################################################

"""
Test module for empty file handling in Knowledge Builder system.

This module tests the empty file special handling that prevents infinite rebuild loops
by generating standardized analysis content for zero-byte files instead of skipping them.
"""

import pytest
import tempfile
import asyncio
from pathlib import Path
from datetime import datetime

from fastmcp import Context

from jesse_framework_mcp.knowledge_bases.indexing.knowledge_builder import KnowledgeBuilder
from jesse_framework_mcp.knowledge_bases.models import (
    IndexingConfig,
    FileContext,
    ProcessingStatus,
    IndexingMode
)


class MockContext:
    """
    [Class intent]
    Mock FastMCP Context for testing empty file handling without external dependencies.
    Provides logging interface compatible with KnowledgeBuilder requirements
    while capturing log messages for test verification.

    [Design principles]
    Minimal mock implementation focusing only on required KnowledgeBuilder interface.
    Message capture enabling test verification of empty file processing flow.
    Async interface compatibility matching FastMCP Context expectations.

    [Implementation details]
    Implements required async logging methods used by KnowledgeBuilder.
    Captures all log messages in lists for test assertion and verification.
    Provides simple interface for test setup without complex mock frameworks.
    """
    
    def __init__(self):
        """
        [Class method intent]
        Initializes mock context with message capture lists for test verification.
        Sets up storage for different log levels to enable detailed test assertions.

        [Design principles]
        Simple initialization with message capture preparation.
        Separate storage for different log levels enabling granular test verification.

        [Implementation details]
        Creates empty lists for each log level used by KnowledgeBuilder.
        Provides clean state for each test execution.
        """
        self.debug_messages = []
        self.info_messages = []
        self.warning_messages = []
        self.error_messages = []
    
    async def debug(self, message: str):
        """
        [Class method intent]
        Captures debug messages for test verification while providing async interface.
        Records debug-level log messages from KnowledgeBuilder for test assertions.

        [Design principles]
        Message capture without side effects enabling clean test verification.
        Async interface compatibility matching FastMCP Context expectations.

        [Implementation details]
        Appends debug messages to capture list for later test assertion.
        Provides async interface expected by KnowledgeBuilder logging calls.
        """
        self.debug_messages.append(message)
    
    async def info(self, message: str):
        """
        [Class method intent]
        Captures info messages for test verification while providing async interface.
        Records info-level log messages from KnowledgeBuilder for test assertions.

        [Design principles]
        Message capture without side effects enabling clean test verification.
        Async interface compatibility matching FastMCP Context expectations.

        [Implementation details]
        Appends info messages to capture list for later test assertion.
        Provides async interface expected by KnowledgeBuilder logging calls.
        """
        self.info_messages.append(message)
    
    async def warning(self, message: str):
        """
        [Class method intent]
        Captures warning messages for test verification while providing async interface.
        Records warning-level log messages from KnowledgeBuilder for test assertions.

        [Design principles]
        Message capture without side effects enabling clean test verification.
        Async interface compatibility matching FastMCP Context expectations.

        [Implementation details]
        Appends warning messages to capture list for later test assertion.
        Provides async interface expected by KnowledgeBuilder logging calls.
        """
        self.warning_messages.append(message)
    
    async def error(self, message: str):
        """
        [Class method intent]
        Captures error messages for test verification while providing async interface.
        Records error-level log messages from KnowledgeBuilder for test assertions.

        [Design principles]
        Message capture without side effects enabling clean test verification.
        Async interface compatibility matching FastMCP Context expectations.

        [Implementation details]
        Appends error messages to capture list for later test assertion.
        Provides async interface expected by KnowledgeBuilder logging calls.
        """
        self.error_messages.append(message)


@pytest.fixture
def temp_dir():
    """
    [Function intent]
    Creates temporary directory for test file operations with automatic cleanup.
    Provides isolated filesystem environment for empty file creation and testing.

    [Design principles]
    Temporary resource management with automatic cleanup preventing test pollution.
    Isolated test environment ensuring tests don't interfere with each other.

    [Implementation details]
    Uses tempfile.TemporaryDirectory for automatic cleanup on test completion.
    Returns Path object for convenient file operations in tests.
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        yield Path(temp_dir)


@pytest.fixture
def mock_config(temp_dir):
    """
    [Function intent]
    Creates mock IndexingConfig for testing with temporary directory setup.
    Provides minimal configuration required for KnowledgeBuilder testing.

    [Design principles]
    Minimal configuration focusing only on requirements for empty file testing.
    Temporary directory usage ensuring test isolation and cleanup.

    [Implementation details]
    Creates IndexingConfig with incremental mode to enable caching behavior.
    Uses temporary directory for knowledge output ensuring test isolation.
    Sets minimal required parameters for KnowledgeBuilder initialization.
    """
    return IndexingConfig(
        source_directories=[temp_dir],
        knowledge_output_directory=temp_dir / ".knowledge",
        indexing_mode=IndexingMode.INCREMENTAL,
        llm_model="claude-3-5-sonnet-20241022",
        temperature=0.1,
        max_tokens=8192,
        timestamp_tolerance_seconds=1,
        debug_mode=False,
        enable_llm_replay=False
    )


@pytest.mark.asyncio
async def test_empty_file_detection():
    """
    [Function intent]
    Tests empty file detection functionality using filesystem operations.
    Verifies that KnowledgeBuilder correctly identifies zero-byte files
    and returns True for empty files, False for non-empty files.

    [Design principles]
    Direct filesystem testing using actual empty and non-empty files.
    Clear verification of detection logic with realistic file scenarios.

    [Implementation details]
    Creates actual empty file using Path.touch() for realistic zero-byte file.
    Creates non-empty file with content for comparison testing.
    Tests both positive and negative cases for comprehensive coverage.
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Create mock config with hierarchical structure
        from jesse_framework_mcp.knowledge_bases.models.indexing_config import (
            OutputConfig, ChangeDetectionConfig, LLMConfig, DebugConfig
        )
        
        config = IndexingConfig(
            output_config=OutputConfig(knowledge_output_directory=temp_path / ".knowledge"),
            change_detection=ChangeDetectionConfig(
                indexing_mode=IndexingMode.INCREMENTAL,
                timestamp_tolerance_seconds=1
            ),
            llm_config=LLMConfig(
                llm_model="claude-3-5-sonnet-20241022",
                temperature=0.1,
                max_tokens=8192
            ),
            debug_config=DebugConfig(
                debug_mode=False,
                enable_llm_replay=False
            )
        )
        
        # Create KnowledgeBuilder
        builder = KnowledgeBuilder(config)
        
        # Test empty file detection
        empty_file = temp_path / "empty.md"
        empty_file.touch()  # Creates 0-byte file
        
        non_empty_file = temp_path / "content.md"
        non_empty_file.write_text("Some content")
        
        # Test detection
        assert builder._is_empty_file(empty_file) == True
        assert builder._is_empty_file(non_empty_file) == False


@pytest.mark.asyncio
async def test_empty_file_analysis_generation():
    """
    [Function intent]
    Tests standardized analysis content generation for empty files.
    Verifies that generated content contains expected sections and information
    while maintaining consistency with standard analysis format.

    [Design principles]
    Content verification ensuring standardized empty file analysis quality.
    Format consistency checking with expected markdown structure and sections.

    [Implementation details]
    Creates realistic empty file with filesystem operations.
    Generates analysis content using KnowledgeBuilder method.
    Verifies presence of required sections and technical details.
    Checks for present tense writing and informative content.
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Create mock config with hierarchical structure
        from jesse_framework_mcp.knowledge_bases.models.indexing_config import (
            OutputConfig, ChangeDetectionConfig, LLMConfig, DebugConfig
        )
        
        config = IndexingConfig(
            output_config=OutputConfig(knowledge_output_directory=temp_path / ".knowledge"),
            change_detection=ChangeDetectionConfig(
                indexing_mode=IndexingMode.INCREMENTAL,
                timestamp_tolerance_seconds=1
            ),
            llm_config=LLMConfig(
                llm_model="claude-3-5-sonnet-20241022",
                temperature=0.1,
                max_tokens=8192
            ),
            debug_config=DebugConfig(
                debug_mode=False,
                enable_llm_replay=False
            )
        )
        
        # Create KnowledgeBuilder
        builder = KnowledgeBuilder(config)
        
        # Create empty file
        empty_file = temp_path / "working_backwards_stages.md"
        empty_file.touch()
        
        # Generate analysis
        analysis = builder._generate_empty_file_analysis(empty_file)
        
        # Verify analysis content
        assert "# File Analysis: working_backwards_stages.md" in analysis
        assert "## Summary" in analysis
        assert "This is an empty file with no content to analyze" in analysis
        assert "## Content Analysis" in analysis
        assert "**File Size**: 0 bytes" in analysis
        assert "## Technical Details" in analysis
        assert "## Empty File Characteristics" in analysis
        assert "--END OF LLM OUTPUT--" in analysis
        
        # Verify present tense writing
        assert "contains no data" in analysis or "exists but contains no data" in analysis
        
        # Verify file type detection
        assert ".md file" in analysis or "md file" in analysis


@pytest.mark.asyncio
async def test_empty_file_processing_flow():
    """
    [Function intent]
    Tests complete empty file processing flow through build_file_knowledge method.
    Verifies that empty files receive standardized analysis without LLM calls
    and return completed FileContext with proper status and content.

    [Design principles]
    End-to-end testing of empty file processing through main KnowledgeBuilder interface.
    Integration testing ensuring empty file handling works within complete system flow.

    [Implementation details]
    Creates realistic empty file and FileContext for processing.
    Calls build_file_knowledge method to test complete processing flow.
    Verifies returned FileContext has completed status and standardized content.
    Confirms no LLM driver initialization occurs for empty file processing.
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Create mock config with hierarchical structure
        from jesse_framework_mcp.knowledge_bases.models.indexing_config import (
            OutputConfig, ChangeDetectionConfig, LLMConfig, DebugConfig
        )
        
        config = IndexingConfig(
            output_config=OutputConfig(knowledge_output_directory=temp_path / ".knowledge"),
            change_detection=ChangeDetectionConfig(
                indexing_mode=IndexingMode.INCREMENTAL,
                timestamp_tolerance_seconds=1
            ),
            llm_config=LLMConfig(
                llm_model="claude-3-5-sonnet-20241022",
                temperature=0.1,
                max_tokens=8192
            ),
            debug_config=DebugConfig(
                debug_mode=False,
                enable_llm_replay=False
            )
        )
        
        # Create KnowledgeBuilder
        builder = KnowledgeBuilder(config)
        
        # Create empty file
        empty_file = temp_path / "empty_stages.md"
        empty_file.touch()
        
        # Create FileContext
        file_stats = empty_file.stat()
        file_context = FileContext(
            file_path=empty_file,
            file_size=file_stats.st_size,
            last_modified=datetime.fromtimestamp(file_stats.st_mtime)
        )
        
        # Create mock context
        ctx = MockContext()
        
        # Process empty file
        result = await builder.build_file_knowledge(file_context, ctx, temp_path)
        
        # Verify results
        assert result is not None
        assert result.processing_status == ProcessingStatus.COMPLETED
        assert result.knowledge_content is not None
        assert "This is an empty file with no content to analyze" in result.knowledge_content
        assert "--END OF LLM OUTPUT--" in result.knowledge_content
        
        # Verify logging
        empty_file_messages = [msg for msg in ctx.info_messages if "EMPTY FILE" in msg]
        assert len(empty_file_messages) > 0
        
        # Verify no LLM driver was initialized (empty files should skip LLM processing)
        assert builder.llm_driver is None


@pytest.mark.asyncio
async def test_empty_file_cache_behavior():
    """
    [Function intent]
    Tests cache behavior for empty files ensuring stable cache entries are created.
    Verifies that empty file analysis is properly cached and subsequent reads
    return cached content without regeneration, preventing rebuild loops.

    [Design principles]
    Cache behavior verification ensuring empty files create stable, reusable cache entries.
    Rebuild loop prevention testing validating that cached empty file analysis prevents repeated processing.

    [Implementation details]
    Creates empty file and processes it with caching enabled.
    Verifies cache file is created with expected standardized content.
    Tests cache hit behavior on subsequent processing attempts.
    Confirms cache freshness prevents unnecessary reprocessing.
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Create mock config with caching enabled and hierarchical structure
        from jesse_framework_mcp.knowledge_bases.models.indexing_config import (
            OutputConfig, ChangeDetectionConfig, LLMConfig, DebugConfig
        )
        
        config = IndexingConfig(
            output_config=OutputConfig(knowledge_output_directory=temp_path / ".knowledge"),
            change_detection=ChangeDetectionConfig(
                indexing_mode=IndexingMode.INCREMENTAL,  # Enables caching
                timestamp_tolerance_seconds=1
            ),
            llm_config=LLMConfig(
                llm_model="claude-3-5-sonnet-20241022",
                temperature=0.1,
                max_tokens=8192
            ),
            debug_config=DebugConfig(
                debug_mode=False,
                enable_llm_replay=False
            )
        )
        
        # Create KnowledgeBuilder
        builder = KnowledgeBuilder(config)
        
        # Create empty file
        empty_file = temp_path / "test_empty.md"
        empty_file.touch()
        
        # Create FileContext
        file_stats = empty_file.stat()
        file_context = FileContext(
            file_path=empty_file,
            file_size=file_stats.st_size,
            last_modified=datetime.fromtimestamp(file_stats.st_mtime)
        )
        
        # Create mock context
        ctx = MockContext()
        
        # First processing - should create cache
        result1 = await builder.build_file_knowledge(file_context, ctx, temp_path)
        
        # Verify cache was created
        cache_path = builder.analysis_cache.get_cache_path(empty_file, temp_path)
        assert cache_path.exists()
        
        # Verify cache content
        cached_content = await builder.analysis_cache.get_cached_analysis(empty_file, temp_path)
        assert cached_content is not None
        assert "This is an empty file with no content to analyze" in cached_content
        
        # Second processing - should use cache
        ctx2 = MockContext()
        result2 = await builder.build_file_knowledge(file_context, ctx2, temp_path)
        
        # Verify results are identical (cache hit)
        assert result1.knowledge_content == result2.knowledge_content
        
        # Verify cache hit was logged
        cache_hit_messages = [msg for msg in ctx2.info_messages if "CACHE HIT" in msg]
        assert len(cache_hit_messages) > 0


if __name__ == "__main__":
    # Run tests directly if script is executed
    pytest.main([__file__, "-v"])
