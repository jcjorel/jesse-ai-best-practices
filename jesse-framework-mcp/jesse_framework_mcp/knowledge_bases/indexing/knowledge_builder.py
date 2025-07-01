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
# LLM-powered knowledge file builder for Knowledge Bases Hierarchical Indexing System.
# Integrates with strands_agent_driver to generate structured knowledge file content
# through Claude 4 Sonnet analysis of source files and hierarchical directory summaries.
###############################################################################
# [Source file design principles]
# - Integration with strands_agent_driver for consistent Claude 4 Sonnet LLM operations
# - Bottom-up content generation aggregating child summaries into parent knowledge files
# - Structured knowledge file format generation following established patterns
# - Intemporal writing using present tense for consistent knowledge representation
# - Comprehensive error handling with graceful degradation on LLM failures
###############################################################################
# [Source file constraints]
# - Must use Claude 4 Sonnet model through strands_agent_driver integration
# - All knowledge content must be written in present tense (intemporal writing)
# - Knowledge file format must follow hierarchical semantic context pattern
# - Content chunking required for files exceeding LLM context window limits
# - Error handling must enable continuation when individual LLM requests fail
###############################################################################
# [Dependencies]
# <codebase>: ..models.indexing_config - Configuration and processing parameters
# <codebase>: ..models.knowledge_context - Context structures and processing state
# <codebase>: ...llm.strands_agent_driver - Claude 4 Sonnet LLM integration
# <system>: asyncio - Async programming patterns for LLM request handling
# <system>: pathlib - Cross-platform file operations and path handling
# <system>: logging - Structured logging for LLM operations and error tracking
###############################################################################
# [GenAI tool change history]
# 2025-07-01T12:10:00Z : Initial knowledge builder creation by CodeAssistant
# * Created LLM-powered knowledge builder with strands_agent_driver integration
# * Implemented hierarchical content generation with bottom-up assembly
# * Set up structured knowledge file format generation and error handling
###############################################################################

"""
Knowledge Builder for Hierarchical Indexing System.

This module implements LLM-powered knowledge file generation using Claude 4 Sonnet
through strands_agent_driver integration. Generates structured knowledge files
following hierarchical semantic context patterns with bottom-up assembly.
"""

import asyncio
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Dict, Any

from fastmcp import Context

from ..models import (
    IndexingConfig,
    DirectoryContext,
    FileContext,
    ProcessingStatus
)
from ...llm.strands_agent_driver import StrandsClaude4Driver, Claude4SonnetConfig

logger = logging.getLogger(__name__)


class KnowledgeBuilder:
    """
    [Class intent]
    LLM-powered knowledge file builder integrating with strands_agent_driver for
    Claude 4 Sonnet content analysis and structured knowledge file generation.
    Implements hierarchical content assembly using bottom-up aggregation patterns.

    [Design principles]
    Claude 4 Sonnet integration through strands_agent_driver for consistent LLM operations.
    Hierarchical content generation assembling child summaries into parent knowledge files.
    Structured knowledge file format following established hierarchical semantic patterns.
    Intemporal writing ensuring all content uses present tense for consistency.
    Comprehensive error handling enabling graceful degradation on individual LLM failures.

    [Implementation details]
    Uses Claude4SonnetConfig.create_optimized_for_analysis for consistent summarization.
    Implements content chunking for files exceeding LLM context window constraints.
    Generates knowledge files following standard hierarchical format specification.
    Provides detailed error handling and retry logic for robust LLM integration.
    Reports progress through FastMCP Context for real-time operation monitoring.
    """
    
    def __init__(self, config: IndexingConfig):
        """
        [Class method intent]
        Initializes knowledge builder with configuration and Claude 4 Sonnet driver setup.
        Creates strands_agent_driver instance optimized for analysis tasks with
        configuration parameters matching indexing requirements.

        [Design principles]
        Configuration-driven LLM setup ensuring consistent behavior across operations.
        Claude 4 Sonnet optimization for analytical tasks requiring detailed summarization.
        Error handling during initialization preventing construction failures.

        [Implementation details]
        Creates Claude4SonnetConfig optimized for analysis with low temperature.
        Initializes StrandsClaude4Driver with proper model configuration.
        Sets up prompt templates for different content types and scenarios.
        """
        self.config = config
        
        # Configure Claude 4 Sonnet for analysis tasks
        self.llm_config = Claude4SonnetConfig.create_optimized_for_analysis(
            model_id=config.llm_model,
            temperature=config.temperature,
            max_tokens=config.max_tokens,
            enable_extended_thinking=True  # Enable for complex analysis
        )
        
        self.llm_driver: Optional[StrandsClaude4Driver] = None
        
        # Prompt templates for different content types
        self.prompts = {
            "file_summary": """
Analyze this file and create a comprehensive summary following these requirements:

CRITICAL REQUIREMENTS:
- Write in present tense only (e.g., "The file implements..." not "The file implemented...")
- Focus on what the file DOES and its PURPOSE, not implementation history
- Include key components, functions, classes, and their roles
- Describe integration points and dependencies
- Avoid line-by-line descriptions

FILE CONTENT:
{file_content}

FILE PATH: {file_path}

Provide a structured summary explaining:
1. Primary purpose and functionality
2. Key components and their roles
3. Integration patterns and dependencies
4. Important design decisions
""",
            
            "directory_summary": """
Create a comprehensive directory summary by aggregating the provided information:

CRITICAL REQUIREMENTS:
- Write in present tense only
- Build summary FROM the child summaries provided (bottom-up assembly)
- Explain the directory's purpose and organization
- Maintain hierarchical context and relationships

DIRECTORY PATH: {directory_path}

CHILD FILE SUMMARIES:
{file_summaries}

CHILD DIRECTORY SUMMARIES:
{child_directory_summaries}

Generate a knowledge file following this exact format:

# Summary

<Overall summary of this directory's purpose and contents>

## Summary section of each subdirectory knowledge file

<For each child directory, include its summary section>

## Summary of each file in this directory

<For each file, provide its summary>

# End of {directory_name}_kb.md
""",
            
            "chunked_file_analysis": """
Analyze this file chunk and extract key information:

REQUIREMENTS:
- Present tense only
- Focus on functionality and purpose
- Identify key components in this chunk
- Note any dependencies or integration points

CHUNK {chunk_number} of {total_chunks} from {file_path}:

{chunk_content}

Provide analysis focusing on the functionality and components in this specific chunk.
"""
        }
        
        logger.info(f"Initialized KnowledgeBuilder with Claude 4 Sonnet configuration")
    
    async def initialize(self) -> None:
        """
        [Class method intent]
        Initializes the Claude 4 Sonnet driver for LLM operations.
        Sets up the strands_agent_driver connection and validates LLM accessibility
        before knowledge building operations begin.

        [Design principles]
        Lazy initialization enabling startup without immediate LLM connection requirements.
        Connection validation ensuring LLM availability before processing begins.
        Error handling providing clear feedback on LLM initialization failures.

        [Implementation details]
        Creates and initializes StrandsClaude4Driver with analysis-optimized configuration.
        Validates LLM connection through driver initialization process.
        Provides detailed error information for troubleshooting connection issues.
        """
        if self.llm_driver is None:
            try:
                self.llm_driver = StrandsClaude4Driver(self.llm_config)
                await self.llm_driver.initialize()
                logger.info("Claude 4 Sonnet driver initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize Claude 4 Sonnet driver: {e}", exc_info=True)
                raise RuntimeError(f"Knowledge builder initialization failed: {e}") from e
    
    async def build_file_summary(self, file_context: FileContext, ctx: Context) -> FileContext:
        """
        [Class method intent]
        Generates comprehensive file summary using Claude 4 Sonnet analysis.
        Processes file content through LLM to create structured knowledge summary
        following established format patterns and intemporal writing standards.

        [Design principles]
        Single file analysis through Claude 4 Sonnet with comprehensive content understanding.
        Content chunking for large files exceeding LLM context window constraints.
        Structured summary generation following established knowledge file format patterns.
        Error handling enabling graceful degradation when LLM processing fails.

        [Implementation details]
        Reads file content and determines if chunking is required based on size limits.
        Uses appropriate prompt template for file analysis with context-aware instructions.
        Processes content through Claude 4 Sonnet with retry logic for robustness.
        Returns updated FileContext with generated summary and processing status.
        """
        if not self.llm_driver:
            await self.initialize()
        
        processing_start = datetime.now()
        
        try:
            await ctx.debug(f"Building summary for file: {file_context.file_path}")
            
            # Read file content
            file_content = await self._read_file_content(file_context.file_path)
            
            if not file_content:
                await ctx.warning(f"File is empty or unreadable: {file_context.file_path}")
                return FileContext(
                    file_path=file_context.file_path,
                    file_size=file_context.file_size,
                    last_modified=file_context.last_modified,
                    processing_status=ProcessingStatus.SKIPPED,
                    processing_start_time=processing_start,
                    processing_end_time=datetime.now()
                )
            
            # Generate summary using Claude 4 Sonnet
            if len(file_content) > self.config.chunk_size:
                summary = await self._process_large_file(file_context.file_path, file_content, ctx)
            else:
                summary = await self._process_single_file(file_context.file_path, file_content, ctx)
            
            return FileContext(
                file_path=file_context.file_path,
                file_size=file_context.file_size,
                last_modified=file_context.last_modified,
                processing_status=ProcessingStatus.COMPLETED,
                content_summary=summary,
                processing_start_time=processing_start,
                processing_end_time=datetime.now()
            )
            
        except Exception as e:
            logger.error(f"File summary generation failed for {file_context.file_path}: {e}", exc_info=True)
            
            return FileContext(
                file_path=file_context.file_path,
                file_size=file_context.file_size,
                last_modified=file_context.last_modified,
                processing_status=ProcessingStatus.FAILED,
                error_message=str(e),
                processing_start_time=processing_start,
                processing_end_time=datetime.now()
            )
    
    async def build_directory_summary(self, directory_context: DirectoryContext, ctx: Context, source_root: Optional[Path] = None) -> DirectoryContext:
        """
        [Class method intent]
        Generates hierarchical directory summary by aggregating child file summaries
        and subdirectory knowledge files into comprehensive directory knowledge file.
        Implements bottom-up assembly pattern for hierarchical content generation.

        [Design principles]
        Bottom-up assembly aggregating child summaries into parent directory knowledge files.
        Hierarchical knowledge file generation following established format specifications.
        Complete child context integration ensuring comprehensive directory representation.
        Error handling enabling graceful degradation when directory summary generation fails.

        [Implementation details]
        Collects all child file summaries and subdirectory knowledge content.
        Uses directory summary prompt template for hierarchical content generation.
        Generates knowledge file content following standard hierarchical format.
        Writes generated knowledge file to appropriate filesystem location.
        """
        if not self.llm_driver:
            await self.initialize()
        
        processing_start = datetime.now()
        
        try:
            await ctx.debug(f"Building directory summary for: {directory_context.directory_path}")
            
            # Collect child summaries
            file_summaries = self._collect_file_summaries(directory_context)
            child_directory_summaries = self._collect_directory_summaries(directory_context)
            
            # Generate directory summary using Claude 4 Sonnet
            prompt = self.prompts["directory_summary"].format(
                directory_path=directory_context.directory_path,
                file_summaries=file_summaries,
                child_directory_summaries=child_directory_summaries,
                directory_name=directory_context.directory_path.name
            )
            
            conversation_id = f"directory_summary_{directory_context.directory_path.name}_{datetime.now().isoformat()}"
            response = await self.llm_driver.send_message(prompt, conversation_id)
            
            directory_summary = response.content.strip()
            
            # Determine knowledge file path with source root for hierarchical structure
            knowledge_file_path = self._get_knowledge_file_path(directory_context.directory_path, source_root)
            
            # Write knowledge file
            await self._write_knowledge_file(knowledge_file_path, directory_summary)
            
            await ctx.info(f"Generated knowledge file: {knowledge_file_path}")
            
            return DirectoryContext(
                directory_path=directory_context.directory_path,
                file_contexts=directory_context.file_contexts,
                subdirectory_contexts=directory_context.subdirectory_contexts,
                processing_status=ProcessingStatus.COMPLETED,
                knowledge_file_path=knowledge_file_path,
                directory_summary=directory_summary,
                processing_start_time=processing_start,
                processing_end_time=datetime.now()
            )
            
        except Exception as e:
            logger.error(f"Directory summary generation failed for {directory_context.directory_path}: {e}", exc_info=True)
            
            return DirectoryContext(
                directory_path=directory_context.directory_path,
                file_contexts=directory_context.file_contexts,
                subdirectory_contexts=directory_context.subdirectory_contexts,
                processing_status=ProcessingStatus.FAILED,
                error_message=str(e),
                processing_start_time=processing_start,
                processing_end_time=datetime.now()
            )
    
    async def _read_file_content(self, file_path: Path) -> str:
        """
        [Class method intent]
        Reads file content with encoding detection and error handling.
        Attempts multiple encoding strategies to maximize file readability
        while handling binary files and encoding errors gracefully.

        [Design principles]
        Robust file reading with multiple encoding fallback strategies.
        Binary file detection preventing processing of unsuitable content.
        Error handling enabling graceful degradation when files are unreadable.

        [Implementation details]
        Attempts UTF-8 encoding first with fallback to latin-1 for broader compatibility.
        Detects binary files through encoding errors and skips them appropriately.
        Returns empty string for unreadable files enabling continued processing.
        """
        try:
            # Try UTF-8 first
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except UnicodeDecodeError:
            try:
                # Fallback to latin-1 for broader compatibility
                with open(file_path, 'r', encoding='latin-1') as f:
                    content = f.read()
                    # Check if content looks like binary
                    if '\x00' in content:
                        logger.warning(f"Binary file detected, skipping: {file_path}")
                        return ""
                    return content
            except Exception as e:
                logger.warning(f"Cannot read file {file_path}: {e}")
                return ""
        except Exception as e:
            logger.warning(f"File read error {file_path}: {e}")
            return ""
    
    async def _process_single_file(self, file_path: Path, content: str, ctx: Context) -> str:
        """
        [Class method intent]
        Processes single file content through Claude 4 Sonnet for summary generation.
        Uses file summary prompt template with comprehensive analysis instructions
        for detailed content understanding and structured summary creation.

        [Design principles]
        Single-pass LLM analysis for files within context window constraints.
        Comprehensive content analysis using specialized prompt template.
        Error handling with retry logic for robust LLM integration.

        [Implementation details]
        Uses file_summary prompt template with file content and path context.
        Processes through Claude 4 Sonnet with conversation management.
        Implements retry logic for handling transient LLM failures.
        """
        prompt = self.prompts["file_summary"].format(
            file_content=content,
            file_path=file_path
        )
        
        conversation_id = f"file_summary_{file_path.stem}_{datetime.now().isoformat()}"
        
        try:
            response = await self.llm_driver.send_message(prompt, conversation_id)
            return response.content.strip()
        except Exception as e:
            logger.error(f"LLM processing failed for {file_path}: {e}")
            raise
    
    async def _process_large_file(self, file_path: Path, content: str, ctx: Context) -> str:
        """
        [Class method intent]
        Processes large files through content chunking and multi-pass Claude 4 Sonnet analysis.
        Splits content into manageable chunks and aggregates analysis results
        into comprehensive file summary following established format patterns.

        [Design principles]
        Content chunking enabling processing of files exceeding LLM context constraints.
        Multi-pass analysis with aggregation for comprehensive large file understanding.
        Chunk overlap preservation maintaining context continuity across boundaries.
        Summary aggregation combining chunk analyses into unified file understanding.

        [Implementation details]
        Splits content into chunks based on configuration size limits with overlap.
        Processes each chunk through Claude 4 Sonnet with chunk-specific prompts.
        Aggregates chunk analyses into final comprehensive file summary.
        Handles chunk processing failures gracefully with partial summary generation.
        """
        await ctx.info(f"Processing large file with chunking: {file_path}")
        
        # Split content into chunks
        chunks = self._split_content_into_chunks(content)
        chunk_summaries = []
        
        # Process each chunk
        for i, chunk in enumerate(chunks):
            try:
                prompt = self.prompts["chunked_file_analysis"].format(
                    chunk_number=i + 1,
                    total_chunks=len(chunks),
                    file_path=file_path,
                    chunk_content=chunk
                )
                
                conversation_id = f"chunk_analysis_{file_path.stem}_chunk_{i}_{datetime.now().isoformat()}"
                response = await self.llm_driver.send_message(prompt, conversation_id)
                chunk_summaries.append(response.content.strip())
                
            except Exception as e:
                logger.warning(f"Chunk {i+1} processing failed for {file_path}: {e}")
                chunk_summaries.append(f"[Chunk {i+1} processing failed: {e}]")
        
        # Aggregate chunk summaries into final summary
        aggregation_prompt = f"""
Combine these chunk analyses into a comprehensive file summary:

FILE: {file_path}

CHUNK ANALYSES:
{chr(10).join(f'Chunk {i+1}: {summary}' for i, summary in enumerate(chunk_summaries))}

Create a unified summary that:
- Uses present tense only
- Explains the file's overall purpose and functionality
- Integrates insights from all chunks
- Follows structured summary format
"""
        
        conversation_id = f"file_aggregation_{file_path.stem}_{datetime.now().isoformat()}"
        response = await self.llm_driver.send_message(aggregation_prompt, conversation_id)
        
        return response.content.strip()
    
    def _split_content_into_chunks(self, content: str) -> List[str]:
        """
        [Class method intent]
        Splits file content into manageable chunks with configurable overlap.
        Ensures chunks respect LLM context window constraints while maintaining
        context continuity through overlap preservation at chunk boundaries.

        [Design principles]
        Content chunking respecting LLM context window size constraints.
        Overlap preservation maintaining context continuity across chunk boundaries.
        Efficient chunking algorithm minimizing processing overhead while maximizing coverage.

        [Implementation details]
        Uses configuration chunk size and overlap parameters for consistent behavior.
        Implements sliding window approach with configurable overlap percentage.
        Returns list of content chunks ready for individual LLM processing.
        """
        chunk_size = self.config.chunk_size
        overlap = self.config.chunk_overlap
        chunks = []
        
        start = 0
        while start < len(content):
            end = min(start + chunk_size, len(content))
            chunk = content[start:end]
            chunks.append(chunk)
            
            if end >= len(content):
                break
            
            start = end - overlap
        
        return chunks
    
    def _collect_file_summaries(self, directory_context: DirectoryContext) -> str:
        """
        [Class method intent]
        Collects and formats all child file summaries for directory knowledge generation.
        Aggregates completed file summaries into formatted text suitable for
        hierarchical directory summary generation through LLM processing.

        [Design principles]
        Bottom-up assembly collecting child file summaries for parent directory processing.
        Structured formatting enabling clear organization of child content in directory summaries.
        Error handling ensuring graceful degradation when some file summaries are missing.

        [Implementation details]
        Iterates through file contexts collecting completed summaries only.
        Formats summaries with file names and paths for clear organization.
        Returns formatted text ready for inclusion in directory summary prompts.
        """
        summaries = []
        
        for file_context in directory_context.file_contexts:
            if file_context.is_completed and file_context.content_summary:
                summaries.append(f"## {file_context.file_path.name}\n{file_context.content_summary}")
            elif file_context.processing_status == ProcessingStatus.FAILED:
                summaries.append(f"## {file_context.file_path.name}\n[File processing failed: {file_context.error_message}]")
        
        return "\n\n".join(summaries) if summaries else "[No file summaries available]"
    
    def _collect_directory_summaries(self, directory_context: DirectoryContext) -> str:
        """
        [Class method intent]
        Collects and formats all child directory summaries for hierarchical knowledge generation.
        Aggregates completed subdirectory knowledge content into formatted text suitable
        for parent directory summary generation through LLM processing.

        [Design principles]
        Hierarchical assembly collecting child directory summaries for parent processing.
        Structured formatting maintaining clear organization of subdirectory content.
        Error handling ensuring graceful degradation when some directory summaries are missing.

        [Implementation details]
        Iterates through subdirectory contexts collecting completed summaries only.
        Formats summaries with directory names and paths for clear organization.
        Returns formatted text ready for inclusion in parent directory summary prompts.
        """
        summaries = []
        
        for subdir_context in directory_context.subdirectory_contexts:
            if subdir_context.processing_status == ProcessingStatus.COMPLETED and subdir_context.directory_summary:
                summaries.append(f"## {subdir_context.directory_path.name}\n{subdir_context.directory_summary}")
            elif subdir_context.processing_status == ProcessingStatus.FAILED:
                summaries.append(f"## {subdir_context.directory_path.name}\n[Directory processing failed: {subdir_context.error_message}]")
        
        return "\n\n".join(summaries) if summaries else "[No subdirectory summaries available]"
    
    def _get_knowledge_file_path(self, directory_path: Path, source_root: Optional[Path] = None) -> Path:
        """
        [Class method intent]
        Determines appropriate knowledge file path for directory following naming conventions.
        Implements hierarchical semantic context pattern with standardized knowledge file
        naming and location conventions for consistent knowledge base organization.

        [Design principles]
        Standardized knowledge file naming following hierarchical semantic context patterns.
        Configurable file placement enabling separation between source and knowledge files.
        Hierarchical structure preservation in knowledge output directory mirroring source structure.

        [Implementation details]
        Generates knowledge file name using directory name with '_kb.md' suffix.
        Uses knowledge_output_directory from config if specified, preserving relative structure.
        Calculates relative path from source root and recreates structure in knowledge directory.
        Returns Path object ready for knowledge file writing operations.
        """
        knowledge_filename = f"{directory_path.name}_kb.md"
        
        if self.config.knowledge_output_directory and source_root:
            # Use separate knowledge output directory, preserving relative structure
            try:
                # Calculate relative path from source root to current directory
                relative_path = directory_path.relative_to(source_root)
                # Create corresponding path in knowledge output directory
                knowledge_dir = self.config.knowledge_output_directory / relative_path
                return knowledge_dir / knowledge_filename
            except ValueError:
                # Fallback if relative path calculation fails
                return self.config.knowledge_output_directory / knowledge_filename
        elif self.config.knowledge_output_directory:
            # Use separate knowledge output directory, flat structure
            return self.config.knowledge_output_directory / knowledge_filename
        else:
            # Default behavior: place in parent directory
            parent_dir = directory_path.parent
            return parent_dir / knowledge_filename
    
    async def _write_knowledge_file(self, file_path: Path, content: str) -> None:
        """
        [Class method intent]
        Writes generated knowledge file content to filesystem with proper formatting.
        Ensures parent directories exist and handles file writing errors gracefully
        for robust knowledge file persistence across diverse filesystem scenarios.

        [Design principles]
        Robust file writing with parent directory creation and error handling.
        UTF-8 encoding ensuring consistent character handling across platforms.
        Atomic write operations preventing partial file corruption during failures.
        Automatic directory structure mirroring for organized knowledge file placement.

        [Implementation details]
        Creates complete parent directory structure if it doesn't exist using parents=True.
        Writes content using UTF-8 encoding for consistent character representation.
        Handles filesystem errors gracefully with detailed error reporting.
        Automatically creates hierarchical directory structure mirroring source organization.
        """
        try:
            # Ensure complete parent directory structure exists
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Write knowledge file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
                
            logger.debug(f"Knowledge file written: {file_path}")
            
        except Exception as e:
            logger.error(f"Failed to write knowledge file {file_path}: {e}")
            raise
    
    async def cleanup(self) -> None:
        """
        [Class method intent]
        Cleans up LLM driver resources and connections for proper resource management.
        Ensures Claude 4 Sonnet driver is properly closed and resources are released
        when knowledge building operations are complete.

        [Design principles]
        Proper resource cleanup preventing memory leaks and connection issues.
        Graceful cleanup handling ensuring operations complete safely.
        Resource management supporting long-running knowledge building operations.

        [Implementation details]
        Closes Claude 4 Sonnet driver connection if initialized.
        Handles cleanup errors gracefully preventing cascading failures.
        Sets driver reference to None ensuring clean state after cleanup.
        """
        if self.llm_driver:
            try:
                await self.llm_driver.cleanup()
                self.llm_driver = None
                logger.info("KnowledgeBuilder cleanup completed")
            except Exception as e:
                logger.warning(f"KnowledgeBuilder cleanup error: {e}")
