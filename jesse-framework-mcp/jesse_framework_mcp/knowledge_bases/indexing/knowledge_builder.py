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
# 3-phase knowledge file builder implementing token-efficient generation workflow.
# Phase 1: Individual file analysis with factual LLM processing.
# Phase 2: Programmatic content insertion and subdirectory assembly.
# Phase 3: Global summary generation using assembled content for comprehensive synthesis.
###############################################################################
# [Source file design principles]
# - 3-phase generation workflow optimizing token usage and content quality
# - Factual individual file analysis without judgmental language or quality assessments
# - Programmatic content insertion for file analyses and subdirectory summaries
# - Global summary generation leveraging complete assembled content for comprehensive synthesis
# - Standard markdown compatibility through template engine with parseable output structure
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
# 2025-07-04T08:57:00Z : Completed DirectorySummary cleanup for incremental architecture alignment by CodeAssistant
# * Removed all functional DirectorySummary references from method signatures and implementations
# * Simplified _generate_llm_insights() to return only global summary string instead of tuple
# * Updated _finalize_knowledge_file() to remove DirectorySummary parameter and usage
# * Removed complex _generate_directory_analysis() and _collect_subdirectory_summaries() methods
# * Aligned data flow with incremental markdown engine using direct string content
# 2025-07-03T16:16:00Z : Integrated FileAnalysisCache for high-performance file analysis caching by CodeAssistant
# * Added FileAnalysisCache integration with cache-first processing in _process_single_file()
# * Implemented 4-phase cache workflow: cache check, debug replay, fresh analysis, cache storage
# * Enhanced build_file_knowledge() to pass source_root parameter for cache path calculation
# * Added cache initialization in constructor for comprehensive caching support
# 2025-07-03T16:00:00Z : Removed backward compatibility and enforced mandatory project-base/ subdirectory by CodeAssistant
# * Modified _get_knowledge_file_path() to always use project-base/ subdirectory regardless of configuration
# * Removed conditional logic for enable_project_base_indexing flag - now always enforced
# * Simplified implementation by removing backward compatibility with direct structure mirroring
# * Updated documentation to reflect mandatory project-base indexing segregation business rule
# 2025-07-03T15:56:00Z : Implemented project-base indexing business rule with project-base/ subdirectory by CodeAssistant
# * Modified _get_knowledge_file_path() to use project-base/ subdirectory when enable_project_base_indexing=True
# * Added logic to distinguish between project-base and regular indexing modes
# * Implemented directory structure mirroring within project-base/ subdirectory
# * Updated documentation to reflect project-base indexing segregation business rule implementation
# 2025-07-02T23:18:00Z : Simplified LLM output processing to eliminate parsing complexity by CodeAssistant
# * Removed complex _parse_directory_response method - no longer needed with hierarchical prompts
# * Simplified _generate_directory_analysis to use raw LLM output directly without section parsing
# * Enhanced prompts generate structured hierarchical semantic trees that don't require parsing
# * DirectorySummary now stores complete hierarchical content directly in main field
# 2025-07-02T20:28:00Z : Major refactoring - broke down 218-line monster method into focused phase methods by CodeAssistant
# * Replaced build_directory_summary_3_phase() (218 lines) with 6 focused methods for maintainability
# * Added _initialize_and_assemble_content(), _generate_llm_insights(), _finalize_knowledge_file() phase methods
# * Added _generate_global_summary(), _generate_directory_analysis() for focused LLM operations
# * Simplified main build_directory_summary() method with clear 3-phase workflow delegation
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
from ...helpers.path_utils import get_portable_path
from .markdown_template_engine import IncrementalMarkdownEngine
from .enhanced_prompts import EnhancedPrompts
from .debug_handler import DebugHandler
from .file_analysis_cache import FileAnalysisCache

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
        
        # Initialize new architecture components
        self.enhanced_prompts = EnhancedPrompts()
        self.template_engine = IncrementalMarkdownEngine()
        
        # Initialize file analysis cache for performance optimization
        self.analysis_cache = FileAnalysisCache(config)
        
        # Initialize debug handler
        self.debug_handler = DebugHandler(
            debug_enabled=config.debug_mode,
            debug_output_directory=config.debug_output_directory,
            enable_replay=config.enable_llm_replay
        )
        
        # Load existing interactions for replay if enabled
        if config.enable_llm_replay:
            self.debug_handler.load_existing_interactions()
        
        logger.info(f"Initialized KnowledgeBuilder with Claude 4 Sonnet configuration and debug mode: {config.debug_mode}")
    
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
    
    async def build_file_knowledge(self, file_context: FileContext, ctx: Context, source_root: Optional[Path] = None) -> FileContext:
        """
        [Class method intent]
        Generates comprehensive file knowledge using cache-first Claude 4 Sonnet analysis.
        Implements high-performance caching to avoid recomputation of file analyses when source files
        haven't changed, with fallback to LLM analysis for cache misses.

        [Design principles]
        Cache-first processing strategy maximizing performance by avoiding unnecessary LLM calls.
        Single file analysis through Claude 4 Sonnet with comprehensive content understanding.
        Content chunking for large files exceeding LLM context window constraints.
        Full knowledge content generation following established knowledge base format patterns.
        Error handling enabling graceful degradation when LLM processing fails.

        [Implementation details]
        Reads file content and determines if chunking is required based on size limits.
        Uses cache-first approach with FileAnalysisCache for performance optimization.
        Uses appropriate prompt template for file analysis with context-aware instructions.
        Processes content through Claude 4 Sonnet with retry logic for robustness.
        Returns updated FileContext with generated knowledge content and processing status.
        """
        if not self.llm_driver:
            await self.initialize()
        
        processing_start = datetime.now()
        parsed_sections = None
        
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
            
            # Generate summary using cache-first Claude 4 Sonnet processing
            summary = await self._process_single_file(file_context.file_path, file_content, ctx, source_root)
            
            return FileContext(
                file_path=file_context.file_path,
                file_size=file_context.file_size,
                last_modified=file_context.last_modified,
                processing_status=ProcessingStatus.COMPLETED,
                knowledge_content=summary,
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
        Implements 3-phase directory knowledge generation workflow for token efficiency and content quality.
        Phase 1: Initialize structure and insert file/subdirectory content, Phase 2: Generate LLM insights,
        Phase 3: Finalize and write knowledge file.

        [Design principles]
        3-phase generation workflow optimizing token usage through selective LLM usage and programmatic assembly.
        Individual file analysis uses factual LLM processing without judgmental language or quality assessments.
        Programmatic content insertion for file analyses and subdirectory summaries maintaining structural consistency.
        Global summary generation leverages complete assembled content for comprehensive synthesis.

        [Implementation details]
        Breaks down complex workflow into focused phase methods for maintainability.
        Each phase handles specific aspect of knowledge generation with clear separation of concerns.
        Error handling ensures graceful degradation when individual phases encounter issues.
        """
        if not self.llm_driver:
            await self.initialize()
        
        processing_start = datetime.now()
        
        try:
            await ctx.info(f"Building directory knowledge for: {directory_context.directory_path}")
            
            # Phase 1: Initialize and assemble content
            markdown_content = await self._initialize_and_assemble_content(directory_context, ctx)
            
            # Phase 2: Generate LLM insights
            global_summary = await self._generate_llm_insights(directory_context, markdown_content, ctx)
            
            # Phase 3: Finalize knowledge file
            knowledge_file_path = await self._finalize_knowledge_file(
                directory_context, markdown_content, global_summary, source_root, ctx
            )
            
            await ctx.info(f"Directory knowledge generation completed: {knowledge_file_path}")
            
            return DirectoryContext(
                directory_path=directory_context.directory_path,
                file_contexts=directory_context.file_contexts,
                subdirectory_contexts=directory_context.subdirectory_contexts,
                processing_status=ProcessingStatus.COMPLETED,
                knowledge_file_path=knowledge_file_path,
                directory_summary=global_summary,
                processing_start_time=processing_start,
                processing_end_time=datetime.now()
            )
            
        except Exception as e:
            logger.error(f"Directory knowledge generation failed for {directory_context.directory_path}: {e}", exc_info=True)
            
            return DirectoryContext(
                directory_path=directory_context.directory_path,
                file_contexts=directory_context.file_contexts,
                subdirectory_contexts=directory_context.subdirectory_contexts,
                processing_status=ProcessingStatus.FAILED,
                error_message=str(e),
                processing_start_time=processing_start,
                processing_end_time=datetime.now()
            )
    
    async def _initialize_and_assemble_content(self, directory_context: DirectoryContext, ctx: Context) -> str:
        """
        [Class method intent]
        Phase 1: Loads existing knowledge base or creates base structure for incremental updates.
        Uses IncrementalMarkdownEngine to load existing content or create minimal structure
        ready for selective section updates without full regeneration.

        [Design principles]
        Incremental update foundation preserving existing content and enabling selective modifications.
        Load-first approach optimizing for existing knowledge bases with incremental changes.
        Error handling enabling graceful degradation when base structure operations encounter issues.

        [Implementation details]
        Uses load_or_create_base_structure for existing content preservation or minimal creation.
        Returns base markdown content ready for selective section updates in subsequent phases.
        Eliminates complex assembly operations in favor of incremental update approach.
        """
        await ctx.debug("Phase 1: Loading existing or creating base knowledge structure")
        
        # Determine knowledge file path
        knowledge_file_path = self._get_knowledge_file_path(directory_context.directory_path)
        
        # Load existing or create base structure
        markdown_content = self.template_engine.load_or_create_base_structure(knowledge_file_path)
        
        await ctx.debug(f"Phase 1: Base structure ready for incremental updates")
        return markdown_content

    async def _generate_llm_insights(self, directory_context: DirectoryContext, markdown_content: str, ctx: Context) -> str:
        """
        [Class method intent]
        Phase 2: Generates LLM-powered global summary using assembled content.
        Uses Claude 4 Sonnet to analyze assembled content and generate comprehensive
        global summary for the directory using incremental update approach.

        [Design principles]
        LLM insight generation leveraging complete assembled content for comprehensive analysis.
        Simplified approach focusing on global summary generation without complex dataclass creation.
        Debug-aware processing supporting replay functionality for consistent results.
        Error handling ensuring graceful degradation when LLM analysis encounters issues.

        [Implementation details]
        Extracts assembled content and generates global summary using factual analysis prompts.
        Eliminates complex directory analysis workflow in favor of incremental updates.
        Handles debug replay functionality for consistent testing and development.
        Returns global summary string ready for incremental section replacement.
        """
        await ctx.debug("Phase 2: Generating LLM global summary from assembled content")
        
        # Extract assembled content for global summary generation
        assembled_content = self.template_engine.extract_assembled_content(markdown_content)
        
        # Generate global summary
        global_summary = await self._generate_global_summary(directory_context, assembled_content, ctx)
        
        return global_summary

    async def _finalize_knowledge_file(
        self, 
        directory_context: DirectoryContext, 
        markdown_content: str, 
        global_summary: str, 
        source_root: Optional[Path], 
        ctx: Context
    ) -> Path:
        """
        [Class method intent]
        Phase 3: Finalizes knowledge file using incremental updates and writes to filesystem.
        Uses selective section updates to integrate LLM insights without full regeneration,
        then writes complete knowledge file to appropriate location.

        [Design principles]
        Incremental update approach modifying only changed sections without full regeneration.
        Selective updates preserving existing content and maintaining document structure.
        File writing with intelligent path resolution and error handling.
        Validation ensuring generated content meets structural requirements.

        [Implementation details]
        Uses incremental template engine methods for selective section updates.
        Updates file sections, subdirectory sections, global summary, and metadata incrementally.
        Validates final markdown structure before writing to ensure quality.
        Returns knowledge file path for calling context tracking and reporting.
        """
        await ctx.debug("Phase 3: Finalizing knowledge file with incremental updates")
        
        current_markdown = markdown_content
        
        # Update file sections incrementally
        file_contexts = self._collect_file_contexts(directory_context)
        for file_context in file_contexts:
            if file_context.knowledge_content:
                await ctx.debug(f"Updating file section: {file_context.file_path.name}")
                current_markdown = self.template_engine.replace_file_section(
                    current_markdown, 
                    file_context.file_path, 
                    file_context.knowledge_content
                )
        
        # Update subdirectory sections incrementally
        for subdir_context in directory_context.subdirectory_contexts:
            if subdir_context.processing_status == ProcessingStatus.COMPLETED and subdir_context.knowledge_file_path:
                await ctx.debug(f"Updating subdirectory section: {subdir_context.directory_path.name}")
                # Extract content from subdirectory knowledge base
                extracted_content = self.template_engine.extract_subdirectory_summary(subdir_context.knowledge_file_path)
                current_markdown = self.template_engine.replace_subdirectory_section(
                    current_markdown,
                    subdir_context.directory_path,
                    extracted_content
                )
        
        # Update global summary section
        await ctx.debug("Updating global summary section")
        current_markdown = self.template_engine.replace_global_summary_section(current_markdown, global_summary)
        
        # Update footer metadata
        completed_subdirectories = len([subdir for subdir in directory_context.subdirectory_contexts 
                                        if subdir.processing_status == ProcessingStatus.COMPLETED])
        await ctx.debug("Updating footer metadata")
        final_markdown = self.template_engine.update_footer_metadata(
            current_markdown,
            len(file_contexts),
            completed_subdirectories
        )
        
        # Validate final markdown structure
        if not self.template_engine.validate_markdown_structure(final_markdown):
            logger.warning(f"Final markdown structure validation failed for: {directory_context.directory_path}")
        
        # Determine knowledge file path and write
        knowledge_file_path = self._get_knowledge_file_path(directory_context.directory_path, source_root)
        await self._write_knowledge_file(knowledge_file_path, final_markdown)
        
        return knowledge_file_path

    async def _generate_global_summary(self, directory_context: DirectoryContext, assembled_content: str, ctx: Context) -> str:
        """
        [Class method intent]
        Generates global summary using Claude 4 Sonnet analysis of complete assembled content.
        Creates comprehensive directory overview synthesizing all file analyses and
        subdirectory content into cohesive understanding of directory purpose.

        [Design principles]
        Global synthesis leveraging complete assembled content for comprehensive understanding.
        Factual analysis without quality judgments maintaining consistency with file analysis.
        Debug replay support enabling consistent results during development and testing.
        LLM response processing ensuring clean content extraction for template integration.

        [Implementation details]
        Constructs factual analysis prompt using assembled content for comprehensive context.
        Handles debug replay functionality for consistent testing and development workflows.
        Processes LLM response to extract clean content without interfering headers.
        Returns global summary ready for template engine integration and final assembly.
        """
        # Generate global summary prompt using enhanced prompts getter method
        global_summary_prompt = self.enhanced_prompts.get_global_summary_prompt(
            directory_path=directory_context.directory_path,
            assembled_content=assembled_content
        )
        
        # Check for main stage replay response (already reviewed content)
        global_summary_replay = self.debug_handler.get_stage_replay_response(
            stage="stage_5_global_summary",
            directory_path=directory_context.directory_path
        )
        
        if global_summary_replay:
            await ctx.info(f"🔄 REPLAY MODE: Using cached reviewed global summary for {directory_context.directory_path.name}/ (no LLM or reviewer calls)")
            # Return cached reviewed content directly - no need to review again
            return self._extract_content_from_llm_response(global_summary_replay.strip())
        
        # Make fresh LLM call and review it
        conversation_id = f"global_summary_{directory_context.directory_path.name}_{datetime.now().isoformat()}"
        await ctx.info(f"🤖 LLM CALL: Generating global directory summary for {directory_context.directory_path.name}/ using Claude 4 Sonnet")
        response = await self.llm_driver.send_message(global_summary_prompt, conversation_id)
        
        # Capture original interaction
        self.debug_handler.capture_stage_llm_output(
            stage="stage_5_global_summary_original",
            prompt=global_summary_prompt,
            response=response.content,
            directory_path=directory_context.directory_path
        )
        
        # Parse the LLM response to extract only content, not headers
        original_global_summary = self._extract_content_from_llm_response(response.content.strip())
        
        # QUALITY ASSURANCE: Bounded loop reviewer for robust compliance checking
        final_global_summary, iterations_used, was_compliant = await self._review_content_until_compliant(
            content_to_review=original_global_summary,
            reviewer_prompt_func=self.enhanced_prompts.get_global_summary_reviewer_prompt,
            base_conversation_id=conversation_id,
            stage_name="stage_5_global_summary",
            directory_path=directory_context.directory_path,
            ctx=ctx
        )
        
        # Log final compliance status
        if was_compliant:
            await ctx.debug(f"✅ Global summary achieved compliance: {directory_context.directory_path.name}/ (after {iterations_used} iteration(s))")
        else:
            await ctx.info(f"🔧 Global summary using best attempt: {directory_context.directory_path.name}/ (after {iterations_used} iteration(s))")
        
        # Capture the final reviewed version for future replay
        self.debug_handler.capture_stage_llm_output(
            stage="stage_5_global_summary",
            prompt=global_summary_prompt,
            response=final_global_summary,
            directory_path=directory_context.directory_path
        )
        
        return final_global_summary


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
    
    async def _process_single_file(self, file_path: Path, content: str, ctx: Context, source_root: Optional[Path] = None) -> str:
        """
        [Class method intent]
        Processes single file content through cache-first LLM analysis generating raw markdown output.
        Implements high-performance caching to avoid recomputation of file analyses when source files
        haven't changed, with fallback to LLM analysis when cache miss occurs.

        [Design principles]
        Cache-first processing strategy maximizing performance by avoiding unnecessary LLM calls.
        Clean content extraction ensuring no metadata artifacts contaminate knowledge files.
        Simplified LLM processing eliminating complex parsing and structured response handling.
        Raw content storage enabling direct insertion into directory knowledge files.
        Natural markdown generation leveraging LLM's native markdown capabilities.
        Token efficiency through direct content usage without additional processing overhead.

        [Implementation details]
        Checks analysis cache first for existing clean content before LLM processing.
        Uses enhanced prompts with content-type detection for specialized analysis approaches.
        Processes LLM response as raw markdown content without parsing or transformation.
        Caches analysis results with metadata for future retrieval and debugging.
        Returns raw analysis content ready for direct insertion into knowledge files.
        """
        try:
            # PHASE 1: Check cache first for performance optimization
            if source_root:
                cached_analysis = await self.analysis_cache.get_cached_analysis(file_path, source_root)
                if cached_analysis:
                    cache_path = self.analysis_cache.get_cache_path(file_path, source_root)
                    await ctx.info(f"📄 CACHE HIT: Using cached analysis for {file_path.name} from {cache_path}")
                    return cached_analysis
            
            # PHASE 2: Cache miss - check debug replay (existing debug system)
            replay_response = self.debug_handler.get_stage_replay_response(
                stage="stage_1_file_analysis",
                file_path=file_path
            )
            
            if replay_response:
                await ctx.info(f"🔄 REPLAY MODE: Using cached reviewed content for {file_path.name} (no LLM or reviewer calls)")
                await ctx.debug(f"Using final reviewed response from replay: {file_path}")
                # Cache the replay response for future use
                if source_root:
                    await self.analysis_cache.cache_analysis(file_path, replay_response.strip(), source_root)
                return replay_response.strip()
            
            # PHASE 3: No cache/replay - generate fresh analysis
            await ctx.info(f"🤖 CACHE MISS: Generating new analysis for {file_path.name} using Claude 4 Sonnet")
            await ctx.debug(f"Making fresh LLM call for file analysis: {file_path}")
            
            # Generate analysis prompt
            prompt = self.enhanced_prompts.get_file_analysis_prompt(
                file_path=file_path,
                file_content=content,
                file_size=len(content)
            )
            
            # Make LLM call
            normalized_path = self.debug_handler._normalize_path_for_filename(file_path)
            conversation_id = f"file_analysis_{normalized_path}"
            response = await self.llm_driver.send_message(prompt, conversation_id)
            original_response_content = response.content
            
            # Capture original interaction
            self.debug_handler.capture_stage_llm_output(
                stage="stage_1_file_analysis_original",
                prompt=prompt,
                response=original_response_content,
                file_path=file_path
            )
            
            # QUALITY ASSURANCE: Bounded loop reviewer for robust compliance checking
            final_response_content, iterations_used, was_compliant = await self._review_content_until_compliant(
                content_to_review=original_response_content,
                reviewer_prompt_func=self.enhanced_prompts.get_file_analysis_reviewer_prompt,
                base_conversation_id=conversation_id,
                stage_name="stage_1_file_analysis",
                file_path=file_path,
                ctx=ctx
            )
            
            # Log final compliance status
            if was_compliant:
                await ctx.debug(f"✅ File analysis achieved compliance: {file_path.name} (after {iterations_used} iteration(s))")
            else:
                await ctx.info(f"🔧 File analysis using best attempt: {file_path.name} (after {iterations_used} iteration(s))")
            
            # Capture the final reviewed version for future replay
            self.debug_handler.capture_stage_llm_output(
                stage="stage_1_file_analysis",
                prompt=prompt,
                response=final_response_content,
                file_path=file_path
            )
            
            # PHASE 4: Cache the analysis result for future use
            if source_root:
                await self.analysis_cache.cache_analysis(file_path, final_response_content.strip(), source_root)
                await ctx.debug(f"💾 CACHED: Analysis cached for {file_path.name}")
            
            # Return final analysis content
            return final_response_content.strip()
            
        except Exception as e:
            logger.error(f"Cache-first file processing failed for {file_path}: {e}")
            raise
    
    
    
    def _prepare_child_content_summary(self, directory_context: DirectoryContext) -> str:
        """
        [Class method intent]
        Prepares comprehensive child content summary for enhanced directory analysis.
        Aggregates file and subdirectory information into structured format suitable
        for architectural analysis through enhanced prompts.

        [Design principles]
        Structured content organization enabling comprehensive directory analysis.
        Architectural focus emphasizing component relationships and design patterns.
        Comprehensive content aggregation supporting detailed hierarchical understanding.

        [Implementation details]
        Combines file knowledge content and subdirectory summaries into formatted text.
        Includes file metadata and processing status for complete context.
        Returns structured content ready for enhanced directory analysis prompts.
        """
        content_parts = []
        
        # Add file content summary
        if directory_context.file_contexts:
            content_parts.append("## File Content Summary")
            for file_context in directory_context.file_contexts:
                if file_context.is_completed and file_context.knowledge_content:
                    # Extract key insights from file knowledge content
                    content_parts.append(f"### {file_context.file_path.name}")
                    content_parts.append(f"**Status**: Completed")
                    content_parts.append(f"**Size**: {file_context.file_size} bytes")
                    # Include a condensed version of the knowledge content
                    content_parts.append(f"**Content**: {file_context.knowledge_content[:500]}...")
                elif file_context.processing_status == ProcessingStatus.FAILED:
                    content_parts.append(f"### {file_context.file_path.name}")
                    content_parts.append(f"**Status**: Failed - {file_context.error_message}")
                else:
                    content_parts.append(f"### {file_context.file_path.name}")
                    content_parts.append(f"**Status**: {file_context.processing_status.value}")
        
        # Add subdirectory content summary
        if directory_context.subdirectory_contexts:
            content_parts.append("\n## Subdirectory Content Summary")
            for subdir_context in directory_context.subdirectory_contexts:
                content_parts.append(f"### {subdir_context.directory_path.name}")
                if subdir_context.processing_status == ProcessingStatus.COMPLETED and subdir_context.directory_summary:
                    content_parts.append(f"**Status**: Completed")
                    # Include a condensed version of directory summary (now always a string)
                    content_parts.append(f"**Summary**: {str(subdir_context.directory_summary)[:300]}...")
                elif subdir_context.processing_status == ProcessingStatus.FAILED:
                    content_parts.append(f"**Status**: Failed - {subdir_context.error_message}")
                else:
                    content_parts.append(f"**Status**: {subdir_context.processing_status.value}")
        
        return "\n".join(content_parts) if content_parts else "[No child content available]"
    
    def _collect_file_contexts(self, directory_context: DirectoryContext) -> List[FileContext]:
        """
        [Class method intent]
        Collects FileContext objects from completed file contexts for ultra-simplified processing.
        Returns completed FileContext objects directly without any transformation or wrapping
        for direct usage by template engine with exact LLM response preservation.

        [Design principles]
        Zero transformation approach using FileContext objects directly without intermediate wrappers.
        Direct object passing eliminating unnecessary data structure conversions and complexity.
        Raw content preservation maintaining complete LLM response integrity throughout pipeline.
        Error handling ensuring graceful degradation when file content is missing.

        [Implementation details]
        Filters completed file contexts with valid knowledge content for template processing.
        Returns raw FileContext objects ready for direct template engine consumption.
        No data transformation, parsing, or wrapper object creation performed.
        """
        file_contexts = []
        
        for file_context in directory_context.file_contexts:
            if file_context.is_completed and file_context.knowledge_content:
                file_contexts.append(file_context)
                        
        return file_contexts
    
    
    def _get_knowledge_file_path(self, directory_path: Path, source_root: Optional[Path] = None) -> Path:
        """
        [Class method intent]
        Determines appropriate knowledge file path for directory following naming conventions.
        Implements hierarchical semantic context pattern with standardized knowledge file
        naming and location conventions for consistent knowledge base organization.
        Enforces project-base indexing business rule using mandatory project-base/ subdirectory.

        [Design principles]
        Standardized knowledge file naming following hierarchical semantic context patterns.
        Configurable file placement enabling separation between source and knowledge files.
        Hierarchical structure preservation in knowledge output directory mirroring source structure.
        Mandatory project-base indexing segregation using dedicated project-base/ subdirectory.

        [Implementation details]
        Generates knowledge file name using directory name with '_kb.md' suffix.
        Uses knowledge_output_directory from config if specified, preserving relative structure.
        Always uses project-base/ subdirectory with structure mirroring for project-base indexing.
        Calculates relative path from source root and recreates structure in knowledge directory.
        Returns Path object ready for knowledge file writing operations.
        """
        knowledge_filename = f"{directory_path.name}_kb.md"
        
        if self.config.knowledge_output_directory and source_root:
            # Use separate knowledge output directory, preserving relative structure
            try:
                # Calculate relative path from source root to current directory
                relative_path = directory_path.relative_to(source_root)
                
                # Apply project-base indexing business rule - always use project-base/ subdirectory
                knowledge_dir = self.config.knowledge_output_directory / "project-base" / relative_path
                
                return knowledge_dir / knowledge_filename
            except ValueError:
                # Fallback if relative path calculation fails
                return self.config.knowledge_output_directory / "project-base" / knowledge_filename
        elif self.config.knowledge_output_directory:
            # Use separate knowledge output directory, flat structure
            return self.config.knowledge_output_directory / "project-base" / knowledge_filename
        else:
            # Default behavior: place in parent directory with project-base/ subdirectory
            parent_dir = directory_path.parent
            return parent_dir / "project-base" / knowledge_filename
    
    async def _write_knowledge_file(self, file_path: Path, content: str) -> None:
        """
        [Class method intent]
        Writes generated knowledge file content using complete file replacement strategy.
        Provides safe content writing with proper formatting and error handling.

        [Design principles]
        Simplified file writing strategy using complete file replacement for all knowledge files.
        Reliable file writing ensuring consistent knowledge file format and content.
        Robust error handling for reliable knowledge file persistence.

        [Implementation details]
        Creates complete parent directory structure and handles filesystem errors gracefully.
        Uses complete file replacement for all knowledge file writing operations.
        """
        try:
            # Ensure complete parent directory structure exists
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Write knowledge file using complete replacement
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
                
            logger.debug(f"Knowledge file written: {file_path}")
            
        except Exception as e:
            logger.error(f"Failed to write knowledge file {file_path}: {e}")
            raise
    
    
    def _extract_content_from_llm_response(self, llm_response: str) -> str:
        """
        [Class method intent]
        Extracts clean content from LLM response by removing LLM-generated headers.
        Handles cases where LLMs add their own headers/structure to responses that
        would interfere with mistletoe parsing and section extraction.

        [Design principles]
        Robust content extraction handling various LLM response formats and structures.
        Header detection and removal preventing parsing conflicts with expected markdown structure.
        Content preservation ensuring actual response content is retained without LLM formatting artifacts.
        Fallback handling ensuring extraction works even with unexpected LLM response formats.

        [Implementation details]
        Uses mistletoe to parse LLM response and identify LLM-generated headers.
        Extracts paragraph content while filtering out unwanted header structures.
        Handles edge cases like responses with no headers or malformed markdown.
        Returns cleaned content suitable for template engine insertion without parsing conflicts.
        """
        if not llm_response or not llm_response.strip():
            return ""
        
        try:
            # Check if the response already has proper section structure
            # If it contains legitimate section headers (like "## Architecture and Design"), 
            # preserve the original formatting instead of stripping structure
            if self._has_legitimate_section_structure(llm_response):
                logger.debug("Response has legitimate section structure, preserving original formatting")
                return llm_response.strip()
            
            # Parse the LLM response using mistletoe for responses that need header filtering
            doc = self.template_engine.markdown_parser.parse_content(llm_response)
            if not doc:
                logger.warning("Failed to parse LLM response, returning raw content")
                return llm_response.strip()
            
            # Extract content while filtering out LLM-generated headers
            content_parts = []
            
            for token in doc.children:
                # Skip LLM-generated headers (common patterns)
                if hasattr(token, 'level') and hasattr(token, '_children'):
                    # This is a header - check if it's an LLM artifact
                    header_text = self.template_engine.markdown_parser._extract_text_from_token(token)
                    
                    # Skip common LLM header patterns - but be more specific to avoid false positives
                    skip_patterns = [
                        "here's my", "here is my", "my analysis", "based on the", 
                        "looking at the", "examining the", "considering the",
                        "here's what", "here is what", "my response", "my answer"
                    ]
                    
                    if any(pattern in header_text.lower() for pattern in skip_patterns):
                        logger.debug(f"Skipping LLM-generated header: {header_text}")
                        continue
                
                # Extract content from non-header tokens (paragraphs, lists, etc.)
                if not hasattr(token, 'level'):  # Not a header
                    # Render this token back to markdown
                    temp_doc = type(doc)([])
                    temp_doc.children = [token]
                    token_content = self.template_engine.markdown_parser.render_to_markdown(temp_doc)
                    if token_content and token_content.strip():
                        content_parts.append(token_content.strip())
            
            # Join content parts with appropriate spacing
            cleaned_content = "\n\n".join(content_parts)
            
            # If we got no content (all headers were filtered), return original response
            # This handles the edge case where LLM responses contain only headers without actual content
            if not cleaned_content.strip():
                logger.warning("All content was filtered out, returning original response")
                return llm_response.strip()
            
            logger.debug(f"Extracted {len(cleaned_content)} characters from LLM response")
            return cleaned_content.strip()
            
        except Exception as e:
            logger.error(f"Failed to extract content from LLM response: {e}")
            # Fallback: return original response
            return llm_response.strip()
    
    
    def _has_legitimate_section_structure(self, content: str) -> bool:
        """
        [Class method intent]
        Determines if LLM response contains legitimate section structure that should be preserved.
        Identifies properly formatted responses with architectural section headers that should not
        be stripped during content extraction to maintain section formatting and readability.

        [Design principles]
        Structure detection enabling preservation of well-formatted LLM responses with section organization.
        Pattern recognition identifying legitimate architectural and technical section headers.
        Conservative approach favoring structure preservation over aggressive header filtering.

        [Implementation details]
        Checks for common legitimate section headers used in architectural analysis responses.
        Uses pattern matching to identify standard knowledge base section organization patterns.
        Returns boolean indicating whether original formatting should be preserved without header stripping.
        """
        try:
            # Look for legitimate section headers that indicate proper structure
            legitimate_headers = [
                "## Architecture and Design", "## Key Patterns", "## Integration Points",
                "## Technical Details", "## Implementation", "## Dependencies",
                "## Design Patterns", "## Components", "## Structure", "## Overview"
            ]
            
            # Check if any legitimate headers are present
            content_lower = content.lower()
            found_headers = []
            for header in legitimate_headers:
                if header.lower() in content_lower:
                    found_headers.append(header)
                    logger.debug(f"Found legitimate section header: {header}")
            
            if found_headers:
                return True
            
            # Also check for multiple section headers (## pattern) which usually indicates structured content
            section_header_count = content.count("## ")
            
            if section_header_count >= 2:
                logger.debug(f"Found {section_header_count} section headers, preserving structure")
                return True
            
            return False
            
        except Exception as e:
            logger.warning(f"Failed to check section structure: {e}")
            return False  # Default to header filtering if detection fails
    
    async def _review_content_until_compliant(
        self,
        content_to_review: str,
        reviewer_prompt_func: callable,
        base_conversation_id: str,
        stage_name: str,
        file_path: Optional[Path] = None,
        directory_path: Optional[Path] = None,
        ctx: Context = None,
        max_iterations: int = 5
    ) -> tuple[str, int, bool]:
        """
        [Class method intent]
        Executes bounded loop reviewer workflow iterating until compliance is achieved or max iterations reached.
        Provides robust quality assurance by repeatedly applying reviewer prompts to content until
        hierarchical semantic tree compliance is verified or iteration limit is exceeded.

        [Design principles]
        Bounded iteration approach preventing infinite loops while maximizing compliance success rates.
        Progressive improvement strategy applying reviewer corrections iteratively for complex compliance issues.
        Comprehensive debug capture enabling replay and analysis of entire review process.
        Graceful degradation returning best attempt when perfect compliance cannot be achieved within bounds.

        [Implementation details]
        Iterates through reviewer prompts with content updates until "COMPLIANT" response or max iterations.
        Captures each iteration separately in debug system with structured stage naming and iteration tracking.
        Returns final content, iteration count, and compliance status for comprehensive result analysis.
        Handles errors gracefully with fallback to previous iteration's content when reviewer calls fail.

        Args:
            content_to_review: Original content to be reviewed for compliance
            reviewer_prompt_func: Function that generates reviewer prompts (takes content string, returns prompt string)
            base_conversation_id: Base conversation ID for LLM calls with iteration suffixes
            stage_name: Stage name for debug capture with iteration tracking
            file_path: Optional file path for debug capture (file-based reviews)
            directory_path: Optional directory path for debug capture (directory-based reviews)  
            ctx: FastMCP context for progress reporting and logging
            max_iterations: Maximum number of review iterations before giving up (default: 3)

        Returns:
            tuple[str, int, bool]: (final_content, iterations_used, was_compliant)
                - final_content: The final reviewed content (compliant or best attempt)
                - iterations_used: Number of review iterations performed
                - was_compliant: True if final content achieved compliance, False if max iterations reached
        """
        current_content = content_to_review
        iteration = 0
        was_compliant = False
        
        if ctx:
            await ctx.debug(f"🔍 BOUNDED REVIEWER: Starting review process for {stage_name} (max {max_iterations} iterations)")
        
        while iteration < max_iterations:
            iteration += 1
            
            try:
                # Generate reviewer prompt for current content
                reviewer_prompt = reviewer_prompt_func(current_content)
                reviewer_conversation_id = f"{base_conversation_id}_review_iter_{iteration}"
                
                if ctx:
                    await ctx.debug(f"🔍 REVIEWER ITERATION {iteration}/{max_iterations}: Checking compliance for {stage_name}")
                
                # Make reviewer LLM call
                reviewer_response = await self.llm_driver.send_message(reviewer_prompt, reviewer_conversation_id)
                reviewer_response_content = reviewer_response.content.strip()
                
                # Capture iteration in debug system
                iteration_stage_name = f"{stage_name}_review_iter_{iteration}"
                if file_path:
                    self.debug_handler.capture_stage_llm_output(
                        stage=iteration_stage_name,
                        prompt=reviewer_prompt,
                        response=reviewer_response_content,
                        file_path=file_path
                    )
                elif directory_path:
                    self.debug_handler.capture_stage_llm_output(
                        stage=iteration_stage_name,
                        prompt=reviewer_prompt,
                        response=reviewer_response_content,
                        directory_path=directory_path
                    )
                
                # Check if compliance achieved
                if reviewer_response_content == "COMPLIANT":
                    was_compliant = True
                    if ctx:
                        await ctx.info(f"✅ COMPLIANCE ACHIEVED: {stage_name} compliant after {iteration} iteration(s)")
                    break
                else:
                    # Update content with reviewer corrections
                    current_content = reviewer_response_content
                    if ctx:
                        await ctx.debug(f"🔧 REVIEWER ITERATION {iteration}: Applied corrections for {stage_name}")
            
            except Exception as e:
                logger.error(f"Reviewer iteration {iteration} failed for {stage_name}: {e}")
                if ctx:
                    await ctx.warning(f"⚠️ REVIEWER ITERATION {iteration} FAILED: {stage_name} - {e}")
                # Continue with current content on error
                break
        
        if not was_compliant and ctx:
            if iteration >= max_iterations:
                await ctx.warning(f"⚠️ MAX ITERATIONS REACHED: {stage_name} using best attempt after {iteration} iterations")
            else:
                await ctx.warning(f"⚠️ REVIEWER ERROR: {stage_name} using last valid content after {iteration} iterations")
        
        # Capture final reviewed content for replay
        final_stage_name = f"{stage_name}_review_final"
        if file_path:
            self.debug_handler.capture_stage_llm_output(
                stage=final_stage_name,
                prompt="Final reviewed content",
                response=current_content,
                file_path=file_path
            )
        elif directory_path:
            self.debug_handler.capture_stage_llm_output(
                stage=final_stage_name,
                prompt="Final reviewed content",
                response=current_content,
                directory_path=directory_path
            )
        
        logger.debug(f"Bounded reviewer completed for {stage_name}: {iteration} iterations, compliant={was_compliant}")
        return current_content, iteration, was_compliant

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
        
        # Cleanup debug handler
        if self.debug_handler:
            try:
                self.debug_handler.cleanup()
                logger.debug("Debug handler cleanup completed")
            except Exception as e:
                logger.warning(f"Debug handler cleanup error: {e}")
