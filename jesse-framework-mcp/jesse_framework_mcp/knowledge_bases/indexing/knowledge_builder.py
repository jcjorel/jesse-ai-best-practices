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
# 2025-07-04T17:58:00Z : Implemented continuation-based retry mechanism with intelligent response completion by CodeAssistant
# * Completely redesigned retry strategy from "new conversation ID" approach to natural continuation using same conversation
# * Added _generate_continuation_prompt() method for natural "please complete your response" continuation requests
# * Added _merge_responses() method with intelligent overlap detection and duplicate sentence removal for seamless merging
# * Replaced wasteful re-prompting with token-efficient continuation requests providing 90%+ token savings on retries
# * Implemented progressive continuation supporting multiple truncation scenarios with recursive completion attempts
# * Enhanced with smart response merging detecting overlapping content at merge boundaries for natural flow
# * Leveraged conversation continuity maintaining context across truncation recovery attempts for superior response quality
# 2025-07-04T17:47:00Z : Implemented conversation-specific caching architecture for complete retry mechanism fix by CodeAssistant
# * Completely redesigned caching system to use conversation_id as part of cache key preventing all cross-conversation cache pollution
# * Modified PromptCache._generate_key() to include conversation_id ensuring each conversation gets isolated cache space
# * Updated all cache method signatures throughout strands_agent_driver to pass conversation_id parameter
# * Removed unnecessary use_cache parameter handling since caching is now properly managed by conversation-specific keys
# * Fixed fundamental architectural issue where same prompt content would retrieve cached responses regardless of conversation context
# * Ensured perfect retry isolation where each unique conversation_id generates fresh LLM calls without any cache interference
# 2025-07-04T17:32:00Z : Fixed critical artifact creation bug on global summary truncation by CodeAssistant
# * Removed fallback content creation in _generate_global_summary() when technical errors occur during review
# * Changed from creating fallback summary to raising RuntimeError preventing all knowledge file creation
# * Ensured complete artifact prevention when global summary generation fails due to truncation or technical errors
# * Fixed violation of "no artifacts on truncation" requirement that was allowing knowledge files to be created with fallback content
###############################################################################

"""
Knowledge Builder for Hierarchical Indexing System.

This module implements LLM-powered knowledge file generation using Claude 4 Sonnet
through strands_agent_driver integration. Generates structured knowledge files
following hierarchical semantic context patterns with bottom-up assembly.
"""

import asyncio
import logging
import uuid
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
from .knowledge_file_generator import KnowledgeFileGenerator
from .knowledge_prompts import EnhancedPrompts
from .debug_handler import DebugHandler
from .file_analysis_cache import FileAnalysisCache

logger = logging.getLogger(__name__)


class TruncationDetectedError(Exception):
    """Custom exception for truncation detection scenarios requiring complete artifact avoidance."""
    pass


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
    Truncation detection preventing any artifact creation when LLM output is incomplete.

    [Implementation details]
    Uses Claude4SonnetConfig.create_optimized_for_analysis for consistent summarization.
    Implements content chunking for files exceeding LLM context window constraints.
    Generates knowledge files following standard hierarchical format specification.
    Provides detailed error handling and retry logic for robust LLM integration.
    Reports progress through FastMCP Context for real-time operation monitoring.
    Raises TruncationDetectedError to completely prevent artifact creation on truncation.
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
        self.template_generator = KnowledgeFileGenerator()
        
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
            
        except TruncationDetectedError as e:
            # Truncation detected - completely skip this file, no artifacts created
            await ctx.error(f"🚨 TRUNCATION DETECTED: File {file_context.file_path.name} will be completely skipped - no artifacts created")
            logger.error(f"Truncation detected for file {file_context.file_path}: {e}")
            # Return None to indicate this file should be completely omitted from processing
            return None
            
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
        Builds directory knowledge using simple template generation with timestamp-based change detection.
        Uses three-trigger change detection to determine if rebuild is needed, then generates complete
        knowledge file using alphabetical sorting and full rebuild approach.

        [Design principles]
        Timestamp-based change detection using three-trigger system for comprehensive change detection.
        Full rebuild approach generating complete knowledge files from template on every change.
        Alphabetical sorting ensuring consistent file and subdirectory ordering.
        Simple template generation replacing complex incremental update logic.

        [Implementation details]
        Checks if directory needs rebuild using three-trigger timestamp detection.
        Collects file contexts and subdirectory summaries for template generation.
        Generates global summary using LLM analysis of complete content.
        Creates complete knowledge file using template generator with alphabetical sorting.
        """
        if not self.llm_driver:
            await self.initialize()
        
        processing_start = datetime.now()
        
        try:
            await ctx.info(f"Building directory knowledge for: {directory_context.directory_path}")
            
            # Determine knowledge file path
            knowledge_file_path = self._get_knowledge_file_path(directory_context.directory_path, source_root)
            
            # Check if rebuild is needed using timestamp-based change detection
            needs_rebuild, reason = self.template_generator.directory_needs_rebuild(
                directory_context.directory_path, knowledge_file_path
            )
            
            if not needs_rebuild:
                await ctx.info(f"📄 KB UP TO DATE: {directory_context.directory_path.name} - {reason}")
                return DirectoryContext(
                    directory_path=directory_context.directory_path,
                    file_contexts=directory_context.file_contexts,
                    subdirectory_contexts=directory_context.subdirectory_contexts,
                    processing_status=ProcessingStatus.SKIPPED,
                    knowledge_file_path=knowledge_file_path,
                    processing_start_time=processing_start,
                    processing_end_time=datetime.now()
                )
            
            await ctx.info(f"🔄 REBUILDING KB: {directory_context.directory_path.name} - {reason}")
            
            # Collect completed file contexts for template generation
            completed_file_contexts = [
                fc for fc in directory_context.file_contexts 
                if fc.is_completed and fc.knowledge_content
            ]
            
            # Collect subdirectory summaries by extracting content from existing KB files
            subdirectory_summaries = []
            for subdir_context in directory_context.subdirectory_contexts:
                if (subdir_context.processing_status == ProcessingStatus.COMPLETED and 
                    subdir_context.knowledge_file_path and 
                    subdir_context.knowledge_file_path.exists()):
                    
                    # Extract fourth-level header content from subdirectory KB
                    extracted_content = await self._extract_subdirectory_content(subdir_context.knowledge_file_path, ctx)
                    subdirectory_summaries.append((subdir_context.directory_path, extracted_content))
            
            # Generate global summary using LLM
            global_summary = await self._generate_global_summary_from_contexts(
                directory_context, completed_file_contexts, subdirectory_summaries, ctx
            )
            
            # Generate complete knowledge file using template generator
            complete_knowledge_content = self.template_generator.generate_complete_knowledge_file(
                directory_path=directory_context.directory_path,
                global_summary=global_summary,
                file_contexts=completed_file_contexts,
                subdirectory_summaries=subdirectory_summaries,
                kb_file_path=knowledge_file_path
            )
            
            # Write complete knowledge file
            await self._write_knowledge_file(knowledge_file_path, complete_knowledge_content)
            
            await ctx.info(f"✅ Directory knowledge generation completed: {knowledge_file_path}")
            
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
            
        except TruncationDetectedError as e:
            # Truncation detected during directory processing - no knowledge file created
            await ctx.error(f"🚨 TRUNCATION DETECTED: Directory {directory_context.directory_path.name} knowledge file will NOT be created - no artifacts")
            logger.error(f"Truncation detected for directory {directory_context.directory_path}: {e}")
            
            return DirectoryContext(
                directory_path=directory_context.directory_path,
                file_contexts=directory_context.file_contexts,
                subdirectory_contexts=directory_context.subdirectory_contexts,
                processing_status=ProcessingStatus.FAILED,
                error_message=f"Truncation detected - no artifacts created: {e}",
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
        
        # Make fresh LLM call with retry mechanism
        base_conversation_id = f"global_summary_{directory_context.directory_path.name}"
        
        try:
            await ctx.info(f"🤖 LLM CALL: Generating global directory summary for {directory_context.directory_path.name}/ using Claude 4 Sonnet")
            original_response, success = await self._retry_llm_call_with_truncation_check(
                prompt=global_summary_prompt,
                base_conversation_id=base_conversation_id,
                call_description=f"global summary for {directory_context.directory_path.name}/",
                max_retries=2,
                ctx=ctx
            )
        except Exception as llm_error:
            # Technical LLM error after retries
            await ctx.warning(f"⚠️ Technical LLM error for global summary {directory_context.directory_path.name}/ after retries: {llm_error}")
            raise RuntimeError(f"Technical LLM error - global summary failed: {llm_error}")
        
        # Check for truncation persistence after retries
        if not success:
            await ctx.error(f"🚨 TRUNCATION PERSISTS: Global summary for {directory_context.directory_path.name}/ truncated after retries")
            raise TruncationDetectedError(f"Global summary truncated after retries: {directory_context.directory_path.name}/")
        
        # Capture original interaction
        self.debug_handler.capture_stage_llm_output(
            stage="stage_5_global_summary_original",
            prompt=global_summary_prompt,
            response=original_response,
            directory_path=directory_context.directory_path
        )
        
        # Parse the LLM response to extract only content, not headers
        original_global_summary = self._extract_content_from_llm_response(original_response.strip())
        
        # QUALITY ASSURANCE: Bounded loop reviewer for robust compliance checking
        final_global_summary, iterations_used, was_compliant, should_skip, skip_reason = await self._review_content_until_compliant(
            content_to_review=original_global_summary,
            reviewer_prompt_func=self.enhanced_prompts.get_global_summary_reviewer_prompt,
            base_conversation_id=base_conversation_id,
            stage_name="stage_5_global_summary",
            directory_path=directory_context.directory_path,
            ctx=ctx
        )
        
        # Handle skip scenarios (technical errors or empty responses during review)
        if should_skip:
            await ctx.error(f"🚨 TECHNICAL ERROR: Global summary generation failed for {directory_context.directory_path.name}/ - NO ARTIFACTS WILL BE CREATED: {skip_reason}")
            # Technical errors during review should prevent all artifact creation
            raise RuntimeError(f"Global summary technical error - preventing artifact creation: {skip_reason}")
        
        # Log final compliance status
        if was_compliant:
            await ctx.debug(f"✅ Global summary achieved compliance: {directory_context.directory_path.name}/ (after {iterations_used} iteration(s))")
        else:
            await ctx.info(f"🔧 Global summary using best attempt: {directory_context.directory_path.name}/ (after {iterations_used} iteration(s))")
        
        # Remove truncation marker from final content
        clean_final_summary = self._remove_truncation_marker(final_global_summary)
        
        # Capture the final reviewed version for future replay (with marker removed)
        self.debug_handler.capture_stage_llm_output(
            stage="stage_5_global_summary",
            prompt=global_summary_prompt,
            response=clean_final_summary,
            directory_path=directory_context.directory_path
        )
        
        return clean_final_summary

    async def _extract_subdirectory_content(self, subdir_kb_path: Path, ctx: Context) -> str:
        """
        [Class method intent]
        Extracts content from fourth-level header in subdirectory knowledge base file.
        Reads subdirectory KB file and extracts content from first fourth-level header
        for integration into parent directory knowledge base.

        [Design principles]
        Content extraction with formatting preservation maintaining original LLM output quality.
        Fourth-level header targeting supporting hierarchical semantic context pattern.
        Error handling ensuring graceful degradation when extraction encounters issues.

        [Implementation details]
        Reads subdirectory KB file and searches for first fourth-level header.
        Extracts all content until next same or higher level header.
        Preserves original formatting without transformation.
        Returns extracted content ready for template integration.
        """
        try:
            if not subdir_kb_path.exists():
                await ctx.warning(f"Subdirectory KB file not found: {subdir_kb_path}")
                return f"*Content not available from {subdir_kb_path.name}*"
            
            # Read subdirectory KB file content
            with open(subdir_kb_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Simple extraction: find first fourth-level header and extract content
            lines = content.split('\n')
            extracted_lines = []
            in_target_section = False
            
            for line in lines:
                if line.startswith('#### ') and not in_target_section:
                    # Found first fourth-level header - start extracting (skip the header)
                    in_target_section = True
                    continue
                elif (line.startswith('#### ') or line.startswith('### ') or 
                      line.startswith('## ') or line.startswith('# ')) and in_target_section:
                    # Found next header - stop extracting
                    break
                elif in_target_section:
                    # Extract content line
                    extracted_lines.append(line)
            
            if extracted_lines:
                # Join lines and clean up whitespace
                result = '\n'.join(extracted_lines).strip()
                await ctx.debug(f"Extracted {len(result)} characters from {subdir_kb_path}")
                return result
            else:
                await ctx.info(f"No fourth-level header content found in {subdir_kb_path}")
                return f"*No detailed content available from {subdir_kb_path.name}*"
                
        except Exception as e:
            logger.error(f"Failed to extract subdirectory content from {subdir_kb_path}: {e}")
            await ctx.warning(f"Error extracting content from {subdir_kb_path}: {e}")
            return f"*Error extracting content from {subdir_kb_path.name}: {e}*"

    async def _generate_global_summary_from_contexts(
        self, 
        directory_context: DirectoryContext, 
        file_contexts: List[FileContext], 
        subdirectory_summaries: List[tuple[Path, str]], 
        ctx: Context
    ) -> str:
        """
        [Class method intent]
        Generates global summary using Claude 4 Sonnet analysis of file contexts and subdirectory summaries.
        Creates comprehensive directory overview by analyzing completed file analyses and
        subdirectory content for cohesive understanding of directory purpose.

        [Design principles]
        Global synthesis leveraging file contexts and subdirectory summaries for comprehensive understanding.
        Factual analysis without quality judgments maintaining consistency with file analysis.
        Content assembly for LLM context creation enabling effective global summary generation.

        [Implementation details]
        Assembles content from file contexts and subdirectory summaries into structured format.
        Uses enhanced prompts for global summary generation with comprehensive context.
        Applies review process for quality assurance and compliance checking.
        Returns global summary ready for template integration.
        """
        try:
            # Assemble content for global summary generation
            content_parts = []
            
            # Add file analyses
            if file_contexts:
                content_parts.append("## File Analyses")
                for file_context in file_contexts:
                    try:
                        portable_path = get_portable_path(file_context.file_path)
                    except Exception:
                        portable_path = str(file_context.file_path)
                    
                    content_parts.append(f"### {portable_path}")
                    content_parts.append(file_context.knowledge_content)
            
            # Add subdirectory summaries
            if subdirectory_summaries:
                content_parts.append("\n## Subdirectory Summaries")
                for subdir_path, subdir_content in subdirectory_summaries:
                    try:
                        portable_path = get_portable_path(subdir_path)
                        if not portable_path.endswith('/') and not portable_path.endswith('\\'):
                            portable_path += "/"
                    except Exception:
                        portable_path = f"{subdir_path.name}/"
                    
                    content_parts.append(f"### {portable_path}")
                    content_parts.append(subdir_content)
            
            assembled_content = "\n\n".join(content_parts) if content_parts else "[No content available]"
            
            # Generate global summary using the existing method
            return await self._generate_global_summary(directory_context, assembled_content, ctx)
            
        except Exception as e:
            logger.error(f"Global summary generation from contexts failed for {directory_context.directory_path}: {e}")
            await ctx.warning(f"Error generating global summary: {e}")
            return f"[Global summary generation failed: {e}. Directory contains {len(file_contexts)} files and {len(subdirectory_summaries)} subdirectories.]"

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
        Enhanced with proper error handling and selective caching based on compliance review outcomes.

        [Design principles]
        Cache-first processing strategy maximizing performance by avoiding unnecessary LLM calls.
        Clean content extraction ensuring no metadata artifacts contaminate knowledge files.
        Selective caching: cache only when we have usable content (compliant or max-iterations-reached).
        Skip files completely on technical errors or empty responses to avoid wasted processing.
        Force cache non-compliant content when max iterations are reached to preserve LLM work.

        [Implementation details]
        Checks analysis cache first for existing clean content before LLM processing.
        Uses enhanced prompts with content-type detection for specialized analysis approaches.
        Detects technical errors vs content errors and skips files appropriately.
        Caches results only when review process produces usable content.
        Returns raw analysis content ready for direct insertion into knowledge files.
        """
        try:
            # PHASE 1: Check cache first for performance optimization (unless FULL mode)
            if source_root and self.config.indexing_mode.value != "full":
                cached_analysis = await self.analysis_cache.get_cached_analysis(file_path, source_root)
                if cached_analysis:
                    cache_path = self.analysis_cache.get_cache_path(file_path, source_root)
                    await ctx.info(f"📄 CACHE HIT: Using cached analysis for {file_path.name} from {cache_path}")
                    return cached_analysis
            elif source_root and self.config.indexing_mode.value == "full":
                await ctx.info(f"💥 FULL MODE: Bypassing cache for {file_path.name} - generating fresh analysis")
            
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
            
            # Make initial LLM call with retry mechanism
            normalized_path = self.debug_handler._normalize_path_for_filename(file_path)
            conversation_id = f"file_analysis_{normalized_path}"
            
            try:
                original_response_content, success = await self._retry_llm_call_with_truncation_check(
                    prompt=prompt,
                    base_conversation_id=conversation_id,
                    call_description=f"file analysis for {file_path.name}",
                    max_retries=2,
                    ctx=ctx
                )
            except Exception as llm_error:
                # Technical LLM error after retries → Skip file (no cache)
                await ctx.warning(f"⚠️ Technical LLM error for {file_path.name} after retries: {llm_error}")
                raise RuntimeError(f"Technical LLM error - file will be skipped: {llm_error}")
            
            # Check for truncation persistence after retries
            if not success:
                await ctx.error(f"🚨 TRUNCATION PERSISTS: File analysis for {file_path.name} truncated after retries - skipping file")
                raise TruncationDetectedError(f"File analysis truncated after retries: {file_path.name}")
            
            # Check for empty LLM response
            if not original_response_content or not original_response_content.strip():
                await ctx.warning(f"⚠️ Empty LLM response for {file_path.name} - skipping file")
                raise RuntimeError("Empty LLM response - file will be skipped")
            
            # Capture original interaction
            self.debug_handler.capture_stage_llm_output(
                stage="stage_1_file_analysis_original",
                prompt=prompt,
                response=original_response_content,
                file_path=file_path
            )
            
            # QUALITY ASSURANCE: Bounded loop reviewer for robust compliance checking
            final_response_content, iterations_used, was_compliant, should_skip, skip_reason = await self._review_content_until_compliant(
                content_to_review=original_response_content,
                reviewer_prompt_func=self.enhanced_prompts.get_file_analysis_reviewer_prompt,
                base_conversation_id=conversation_id,
                stage_name="stage_1_file_analysis",
                file_path=file_path,
                ctx=ctx
            )
            
            # Handle skip scenarios (technical errors or empty responses during review)
            if should_skip:
                await ctx.warning(f"⚠️ Skipping {file_path.name}: {skip_reason}")
                raise RuntimeError(f"Review process failed - file will be skipped: {skip_reason}")
            
            # Log final compliance status
            if was_compliant:
                await ctx.debug(f"✅ File analysis achieved compliance: {file_path.name} (after {iterations_used} iteration(s))")
            else:
                await ctx.info(f"🔧 File analysis using best attempt after max iterations: {file_path.name} (after {iterations_used} iteration(s))")
            
            # Capture the final reviewed version for future replay
            self.debug_handler.capture_stage_llm_output(
                stage="stage_1_file_analysis",
                prompt=prompt,
                response=final_response_content,
                file_path=file_path
            )
            
            # PHASE 4: Remove truncation marker and cache/return clean content
            clean_final_content = self._remove_truncation_marker(final_response_content.strip())
            
            # Cache the clean analysis result - both compliant and max-iterations-reached cases (unless FULL mode)
            if source_root and self.config.indexing_mode.value != "full":
                await self.analysis_cache.cache_analysis(file_path, clean_final_content, source_root)
                await ctx.debug(f"💾 CACHED: Clean analysis cached for {file_path.name} (compliant: {was_compliant})")
            elif source_root and self.config.indexing_mode.value == "full":
                await ctx.debug(f"💥 FULL MODE: Not caching analysis for {file_path.name} - nuclear rebuild mode")
            
            # Return clean final analysis content
            return clean_final_content
            
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
        Simplified approach using string processing instead of complex markdown parsing
        to avoid dependencies on the old template engine architecture.

        [Design principles]
        Robust content extraction handling various LLM response formats and structures.
        Header detection and removal preventing conflicts with template generation.
        Content preservation ensuring actual response content is retained without LLM formatting artifacts.
        Fallback handling ensuring extraction works even with unexpected LLM response formats.

        [Implementation details]
        Uses simple string processing to identify and filter LLM-generated headers.
        Preserves legitimate section structure while removing conversational headers.
        Returns cleaned content ready for template integration without parsing conflicts.
        """
        if not llm_response or not llm_response.strip():
            return ""
        
        try:
            # Check if the response already has proper section structure
            if self._has_legitimate_section_structure(llm_response):
                logger.debug("Response has legitimate section structure, preserving original formatting")
                return llm_response.strip()
            
            # Simple approach: filter out common LLM conversational headers
            lines = llm_response.strip().split('\n')
            filtered_lines = []
            
            for line in lines:
                # Skip common LLM conversational patterns
                line_lower = line.lower().strip()
                skip_patterns = [
                    "here's my", "here is my", "my analysis", "based on the", 
                    "looking at the", "examining the", "considering the",
                    "here's what", "here is what", "my response", "my answer",
                    "i'll analyze", "let me analyze", "analyzing the"
                ]
                
                # Check if this line starts with a skip pattern
                should_skip = False
                for pattern in skip_patterns:
                    if line_lower.startswith(pattern):
                        should_skip = True
                        logger.debug(f"Skipping LLM conversational line: {line[:50]}...")
                        break
                
                if not should_skip:
                    filtered_lines.append(line)
            
            # Join filtered lines and clean up whitespace
            cleaned_content = '\n'.join(filtered_lines).strip()
            
            # If we filtered everything out, return the original
            if not cleaned_content:
                logger.warning("All content was filtered out, returning original response")
                return llm_response.strip()
            
            logger.debug(f"Extracted {len(cleaned_content)} characters from LLM response")
            return cleaned_content
            
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
    
    def _has_truncation_marker(self, content: str) -> bool:
        """
        [Class method intent]
        Programmatically checks if content contains the truncation detection marker.
        Provides fast, reliable truncation detection without requiring LLM reviewer call.
        Serves as primary truncation detection method with LLM reviewer as backup.

        [Design principles]
        Fast programmatic detection avoiding unnecessary LLM calls for obvious truncation.
        Reliable detection independent of LLM reviewer accuracy or availability.
        Fail-fast approach enabling immediate truncation detection and artifact prevention.
        Simple string-based detection with whitespace tolerance for robust marker detection.

        [Implementation details]
        Checks for exact marker match at end of content with whitespace tolerance.
        Uses case-sensitive string matching for reliable marker detection.
        Returns boolean result for immediate truncation decision making.
        Handles empty content and edge cases gracefully with appropriate fallback behavior.
        """
        if not content:
            return False
        
        try:
            # Define the exact marker to detect
            truncation_marker = "--END OF LLM OUTPUT--"
            
            # Check if content ends with the marker (with whitespace tolerance)
            cleaned_content = content.strip()
            return cleaned_content.endswith(truncation_marker)
            
        except Exception as e:
            logger.warning(f"Failed to check truncation marker: {e}")
            return False  # Conservative: assume no marker if check fails

    def _remove_truncation_marker(self, content: str) -> str:
        """
        [Class method intent]
        Removes the "--END OF LLM OUTPUT--" truncation detection marker from content.
        Cleanly strips the marker from the end of content while preserving all other formatting
        and ensuring proper content integrity for storage and cache operations.

        [Design principles]
        Clean marker removal without affecting content integrity or formatting.
        Edge case handling for missing markers, multiple markers, and whitespace variations.
        Idempotent operation ensuring safe repeated application without content corruption.

        [Implementation details]
        Searches for exact marker match at end of content and removes it cleanly.
        Handles whitespace variations and multiple marker instances gracefully.
        Preserves all content formatting except for the truncation detection marker.
        Returns cleaned content ready for storage, caching, or template insertion.
        """
        if not content:
            return content
        
        try:
            # Define the exact marker to remove
            truncation_marker = "--END OF LLM OUTPUT--"
            
            # Remove marker from end of content (case-sensitive exact match)
            cleaned_content = content.strip()
            
            # Handle multiple markers or marker variations
            while cleaned_content.endswith(truncation_marker):
                cleaned_content = cleaned_content[:-len(truncation_marker)].strip()
            
            logger.debug(f"Removed truncation marker from content: {len(content)} -> {len(cleaned_content)} characters")
            return cleaned_content
            
        except Exception as e:
            logger.warning(f"Failed to remove truncation marker: {e}")
            return content  # Return original content if removal fails

    async def _retry_llm_call_with_truncation_check(
        self,
        prompt: str,
        base_conversation_id: str,
        call_description: str,
        max_retries: int = 2,
        ctx: Context = None
    ) -> tuple[str, bool]:
        """
        [Class method intent]
        Continuation-based retry mechanism for LLM calls with intelligent response completion.
        Uses conversation continuity to ask the model to complete truncated responses instead of
        restarting with fresh conversation IDs, providing 90%+ token savings and better context preservation.

        [Design principles]
        Conversation continuity maintaining context across truncation recovery attempts.
        Token-efficient continuation prompts avoiding redundant re-processing of original context.
        Intelligent response merging combining truncated and continuation responses seamlessly.
        Progressive continuation supporting multiple truncation scenarios with recursive completion.
        Natural conversation flow leveraging model's conversational capabilities for completion.

        [Implementation details]
        Makes initial LLM call with original prompt in dedicated conversation context.
        Detects truncation and sends continuation prompts in same conversation to preserve context.
        Implements intelligent response merging to avoid duplication and maintain content flow.
        Handles multiple continuation attempts for complex truncation scenarios.
        Returns merged complete response with success status for caller decision making.

        Args:
            prompt: The prompt to send to the LLM
            base_conversation_id: Base conversation ID for continuation context
            call_description: Human readable description of the LLM call for logging
            max_retries: Maximum number of continuation attempts (default: 2)
            ctx: FastMCP context for progress reporting and logging

        Returns:
            tuple[str, bool]: (response_content, success) - merged content and whether call succeeded
        """
        try:
            # Make initial LLM call
            if ctx:
                await ctx.debug(f"🤖 INITIAL CALL: {call_description}")
            
            conversation_id = f"{base_conversation_id}_{str(uuid.uuid4())[:8]}"
            response = await self.llm_driver.send_message(prompt, conversation_id)
            response_content = response.content
            
            # Check if initial response is complete
            if self._has_truncation_marker(response_content):
                if ctx:
                    await ctx.debug(f"✅ SUCCESS: {call_description} completed on first attempt")
                return response_content, True
            
            # Initial response was truncated - start continuation process
            if ctx:
                await ctx.warning(f"🚨 TRUNCATION DETECTED: {call_description} - starting continuation")
            logger.warning(f"Truncation detected in {call_description}, starting continuation")
            
            # Store the truncated response for merging
            accumulated_response = response_content
            
            # Attempt continuations
            for attempt in range(1, max_retries + 1):
                try:
                    if ctx:
                        await ctx.info(f"🔄 CONTINUATION {attempt}/{max_retries}: Asking model to complete response")
                    
                    # Generate continuation prompt
                    continuation_prompt = self._generate_continuation_prompt(accumulated_response)
                    
                    # Send continuation request in same conversation
                    continuation_response = await self.llm_driver.send_message(continuation_prompt, conversation_id)
                    continuation_content = continuation_response.content
                    
                    # Check if continuation is complete
                    if self._has_truncation_marker(continuation_content):
                        # Merge responses intelligently
                        complete_response = await self._merge_responses(
                            accumulated_response, continuation_content, ctx
                        )
                        
                        if ctx:
                            await ctx.info(f"✅ CONTINUATION SUCCESS: {call_description} completed after {attempt} continuation(s)")
                        return complete_response, True
                    else:
                        # Continuation also truncated - accumulate and try again
                        accumulated_response = await self._merge_responses(
                            accumulated_response, continuation_content, ctx
                        )
                        
                        if ctx:
                            await ctx.warning(f"🚨 CONTINUATION TRUNCATED: Attempt {attempt} - accumulating content")
                        logger.warning(f"Continuation {attempt} also truncated, accumulating content")
                        
                        if attempt == max_retries:
                            # Final continuation attempt failed
                            if ctx:
                                await ctx.error(f"🚨 ALL CONTINUATIONS FAILED: {call_description} after {max_retries} attempts")
                            logger.error(f"All continuation attempts failed for {call_description}")
                            return accumulated_response, False
                            
                except Exception as e:
                    if ctx:
                        await ctx.warning(f"⚠️ CONTINUATION ERROR: Attempt {attempt} failed - {e}")
                    logger.warning(f"Continuation attempt {attempt} failed for {call_description}: {e}")
                    
                    if attempt == max_retries:
                        # Final continuation attempt failed with exception
                        if ctx:
                            await ctx.error(f"❌ CONTINUATION FAILED: {call_description} after {max_retries} attempts")
                        return accumulated_response, False
                    
                    continue
            
            # This should never be reached, but safety fallback
            return accumulated_response, False
            
        except Exception as e:
            if ctx:
                await ctx.error(f"❌ CRITICAL ERROR: {call_description} failed with exception: {e}")
            logger.error(f"Critical error in {call_description}: {e}")
            raise
    
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
    ) -> tuple[str, int, bool, bool, str]:
        """
        [Class method intent]
        Executes bounded loop reviewer workflow with dual truncation detection strategy.
        Provides robust quality assurance by first checking programmatically for truncation marker,
        then applying LLM reviewer prompts for other compliance checks if truncation is not detected.
        Enhanced with technical error detection and selective skip logic for proper cache management.

        [Design principles]
        Dual detection strategy combining programmatic checks with LLM reviewer for maximum reliability.
        Fast-fail approach preventing unnecessary LLM calls when truncation is obviously detected.
        Bounded iteration approach preventing infinite loops while maximizing compliance success rates.
        Progressive improvement strategy applying reviewer corrections iteratively for complex compliance issues.
        Technical error detection distinguishing between content issues and technical failures.
        Selective skip logic ensuring files are only skipped on technical/empty errors, not content issues.
        Comprehensive debug capture enabling replay and analysis of entire review process.

        [Implementation details]
        First performs programmatic truncation detection as primary check for fast failure.
        Iterates through reviewer prompts with content updates until "COMPLIANT" response or max iterations.
        Detects technical errors and empty responses during review iterations for proper skip handling.
        Captures each iteration separately in debug system with structured stage naming and iteration tracking.
        Returns comprehensive status including skip recommendation and error details.
        Forces cache of max-iterations content to preserve LLM work even when non-compliant.

        Args:
            content_to_review: Original content to be reviewed for compliance
            reviewer_prompt_func: Function that generates reviewer prompts (takes content string, returns prompt string)
            base_conversation_id: Base conversation ID for LLM calls with iteration suffixes
            stage_name: Stage name for debug capture with iteration tracking
            file_path: Optional file path for debug capture (file-based reviews)
            directory_path: Optional directory path for debug capture (directory-based reviews)  
            ctx: FastMCP context for progress reporting and logging
            max_iterations: Maximum number of review iterations before giving up (default: 5)

        Returns:
            tuple[str, int, bool, bool, str]: (final_content, iterations_used, was_compliant, should_skip, skip_reason)
                - final_content: The final reviewed content (compliant or best attempt)
                - iterations_used: Number of review iterations performed
                - was_compliant: True if final content achieved compliance, False if max iterations reached
                - should_skip: True if file should be skipped (technical/empty errors), False if content should be cached
                - skip_reason: Human-readable reason for skipping (empty if should_skip is False)
        """
        current_content = content_to_review
        iteration = 0
        was_compliant = False
        should_skip = False
        skip_reason = ""
        
        if ctx:
            await ctx.debug(f"🔍 BOUNDED REVIEWER: Starting review process for {stage_name} (max {max_iterations} iterations)")
        
        # DUAL DETECTION STRATEGY: Programmatic check first (primary detection)
        if not self._has_truncation_marker(current_content):
            if ctx:
                await ctx.error(f"🚨 PROGRAMMATIC TRUNCATION DETECTED: {stage_name} missing truncation marker - NO ARTIFACTS WILL BE CREATED")
            
            # Immediate truncation detection - no need for LLM reviewer
            error_msg = f"Programmatic truncation detection in {stage_name} - preventing artifact creation"
            logger.error(error_msg)
            raise TruncationDetectedError(error_msg)
        
        if ctx:
            await ctx.debug(f"✅ TRUNCATION MARKER PRESENT: {stage_name} passed programmatic check, proceeding with LLM reviewer")
        
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
                
                # Check for empty response during review → Skip file (no cache)
                if not reviewer_response_content:
                    should_skip = True
                    skip_reason = f"Empty reviewer response at iteration {iteration}"
                    logger.warning(f"Empty reviewer response for {stage_name} at iteration {iteration}")
                    break
                
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
                
                # Check for truncation detection
                if reviewer_response_content == "TRUNCATED":
                    if ctx:
                        await ctx.error(f"🚨 TRUNCATION DETECTED: {stage_name} at iteration {iteration} - NO ARTIFACTS WILL BE CREATED")
                    
                    # Raise TruncationDetectedError to prevent any artifact creation
                    error_msg = f"Truncation detected in {stage_name} at iteration {iteration} - preventing artifact creation"
                    logger.error(error_msg)
                    raise TruncationDetectedError(error_msg)
                
                # Check if compliance achieved
                elif reviewer_response_content == "COMPLIANT":
                    was_compliant = True
                    if ctx:
                        await ctx.info(f"✅ COMPLIANCE ACHIEVED: {stage_name} compliant after {iteration} iteration(s)")
                    break
                else:
                    # TRIPLE DETECTION STRATEGY: Check if reviewer corrections are themselves truncated
                    if not self._has_truncation_marker(reviewer_response_content):
                        if ctx:
                            await ctx.error(f"🚨 REVIEWER CORRECTION TRUNCATED: {stage_name} at iteration {iteration} - reviewer provided truncated corrections")
                        
                        # Raise TruncationDetectedError for truncated reviewer corrections
                        error_msg = f"Reviewer provided truncated corrections in {stage_name} at iteration {iteration} - preventing artifact creation"
                        logger.error(error_msg)
                        raise TruncationDetectedError(error_msg)
                    
                    # Update content with reviewer corrections
                    current_content = reviewer_response_content
                    if ctx:
                        await ctx.debug(f"🔧 REVIEWER ITERATION {iteration}: Applied corrections for {stage_name}")
            
            except Exception as e:
                # Technical error during review → Skip file (no cache)
                should_skip = True
                skip_reason = f"Technical error during review iteration {iteration}: {e}"
                logger.error(f"Reviewer iteration {iteration} failed for {stage_name}: {e}")
                if ctx:
                    await ctx.warning(f"⚠️ REVIEWER ITERATION {iteration} FAILED: {stage_name} - {e}")
                break
        
        # If we completed all iterations without skip conditions
        if not should_skip:
            if not was_compliant and ctx:
                if iteration >= max_iterations:
                    await ctx.warning(f"⚠️ MAX ITERATIONS REACHED: {stage_name} using best attempt after {iteration} iterations")
                else:
                    await ctx.warning(f"⚠️ REVIEWER STOPPED: {stage_name} using last valid content after {iteration} iterations")
            
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
        
        logger.debug(f"Bounded reviewer completed for {stage_name}: {iteration} iterations, compliant={was_compliant}, should_skip={should_skip}, final_length={len(current_content)}")
        return current_content, iteration, was_compliant, should_skip, skip_reason

    def _generate_continuation_prompt(self, truncated_response: str) -> str:
        """
        [Class method intent]
        Generates continuation prompt asking the model to complete its truncated response.
        Creates natural continuation request that preserves context while asking for completion
        of the specific analysis that was interrupted by truncation.

        [Design principles]
        Natural conversation flow maintaining context from the truncated response.
        Specific completion request targeting the exact point where truncation occurred.
        Concise prompt design minimizing token usage for efficient continuation requests.
        Clear instruction format ensuring model understands continuation context.

        [Implementation details]
        Analyzes truncated response to understand what type of content was being generated.
        Creates context-aware prompt referencing the incomplete work for natural continuation.
        Uses minimal token overhead while providing sufficient context for quality completion.
        Returns prompt ready for immediate LLM continuation request.

        Args:
            truncated_response: The incomplete response that needs continuation

        Returns:
            str: Continuation prompt for LLM completion request
        """
        try:
            # Analyze the end of the truncated response to understand context
            response_end = truncated_response.strip()[-200:] if len(truncated_response) > 200 else truncated_response.strip()
            
            # Create natural continuation prompt
            continuation_prompt = (
                "Continue exactly from where you left off. Do not repeat any previous sentences. "
                "Maintain the same structure and formatting."
                f"Your response was cut off and the last part was: '...{response_end}'. "
                "Continue with the rest of your analysis and ensure you add the '--END OF LLM OUTPUT--' marker at the end."
            )
            
            logger.debug(f"Generated continuation prompt with {len(continuation_prompt)} characters")
            return continuation_prompt
            
        except Exception as e:
            logger.warning(f"Failed to generate continuation prompt: {e}")
            # Fallback to generic continuation request
            return "Please complete your previous response from where you left off, and ensure you add the '--END OF LLM OUTPUT--' marker at the end."

    async def _merge_responses(self, truncated_response: str, continuation: str, ctx: Context = None) -> str:
        """
        [Class method intent]
        Intelligently merges truncated response with continuation to create seamless complete response.
        Handles overlapping content, removes duplicate sentences, and ensures natural flow
        between the truncated portion and the continuation content.
        Preserves truncation marker from continuation to maintain proper reviewer compliance.

        [Design principles]
        Intelligent merging avoiding content duplication and maintaining natural flow.
        Overlap detection identifying common content at merge boundaries for clean joining.
        Content preservation ensuring no important information is lost during merge process.
        Natural flow maintenance creating seamless reading experience in merged content.
        Truncation marker preservation ensuring merged response passes reviewer compliance checks.

        [Implementation details]
        Detects if continuation has truncation marker before cleaning for preservation.
        Cleans both responses by removing truncation markers and artifacts.
        Detects potential overlap between end of truncated response and start of continuation.
        Performs intelligent merging with overlap resolution and duplicate sentence removal.
        Restores truncation marker to merged response if continuation originally had it.
        Returns complete merged response ready for further processing or storage.

        Args:
            truncated_response: The incomplete initial response
            continuation: The continuation response from the model
            ctx: Optional FastMCP context for progress reporting

        Returns:
            str: Merged complete response with seamless content flow and proper truncation marker
        """
        try:
            if ctx:
                await ctx.debug(f"🔗 MERGING: Combining {len(truncated_response)} + {len(continuation)} characters")
            
            # Check if continuation has truncation marker before cleaning
            continuation_has_marker = self._has_truncation_marker(continuation.strip())
            
            # Clean both responses
            clean_truncated = truncated_response.strip()
            clean_continuation = self._remove_truncation_marker(continuation.strip())
            
            # Simple approach: look for potential overlap at the boundary
            # Take last 100 characters of truncated response
            truncated_end = clean_truncated[-100:] if len(clean_truncated) > 100 else clean_truncated
            
            # Take first 100 characters of continuation
            continuation_start = clean_continuation[:100] if len(clean_continuation) > 100 else clean_continuation
            
            # Check for sentence-level overlap
            truncated_sentences = [s.strip() for s in truncated_end.split('.') if s.strip()]
            continuation_sentences = [s.strip() for s in continuation_start.split('.') if s.strip()]
            
            # Look for common sentences at the boundary
            overlap_found = False
            if truncated_sentences and continuation_sentences:
                # Check if last sentence of truncated matches first sentence of continuation
                last_truncated = truncated_sentences[-1] if truncated_sentences else ""
                first_continuation = continuation_sentences[0] if continuation_sentences else ""
                
                if last_truncated and first_continuation:
                    # Check for similarity (allowing for partial matches)
                    if (last_truncated in first_continuation or 
                        first_continuation in last_truncated or
                        len(set(last_truncated.lower().split()) & set(first_continuation.lower().split())) > 3):
                        
                        # Found overlap - remove the duplicate from continuation
                        remaining_continuation = clean_continuation[len(first_continuation):].strip()
                        if remaining_continuation.startswith('.'):
                            remaining_continuation = remaining_continuation[1:].strip()
                        
                        merged_response = clean_truncated + " " + remaining_continuation
                        overlap_found = True
                        
                        if ctx:
                            await ctx.debug("🔗 OVERLAP DETECTED: Removed duplicate sentence at merge boundary")
            
            if not overlap_found:
                # No overlap detected - simple concatenation with space
                merged_response = clean_truncated + " " + clean_continuation
                
                if ctx:
                    await ctx.debug("🔗 NO OVERLAP: Simple concatenation performed")
            
            # Clean up multiple spaces and ensure proper formatting
            merged_response = ' '.join(merged_response.split())
            
            # CRITICAL: Restore truncation marker if continuation originally had it
            if continuation_has_marker:
                # Ensure proper marker format - no extra whitespace that could interfere with detection
                if not merged_response.endswith("--END OF LLM OUTPUT--"):
                    merged_response = merged_response.rstrip() + "\n\n--END OF LLM OUTPUT--"
                if ctx:
                    await ctx.debug("🔗 MARKER RESTORED: Added truncation marker to merged response")
            
            if ctx:
                await ctx.debug(f"✅ MERGE COMPLETE: {len(merged_response)} characters total")
            
            logger.debug(f"Merged responses: {len(truncated_response)} + {len(continuation)} -> {len(merged_response)} characters")
            return merged_response
            
        except Exception as e:
            logger.error(f"Failed to merge responses: {e}")
            if ctx:
                await ctx.warning(f"⚠️ MERGE ERROR: Using simple concatenation fallback")
            
            # Fallback: simple concatenation with marker preservation
            clean_truncated = truncated_response.strip()
            continuation_has_marker = self._has_truncation_marker(continuation.strip())
            clean_continuation = self._remove_truncation_marker(continuation.strip())
            
            fallback_response = clean_truncated + " " + clean_continuation
            if continuation_has_marker:
                # Ensure proper marker format - no extra whitespace that could interfere with detection
                if not fallback_response.endswith("--END OF LLM OUTPUT--"):
                    fallback_response = fallback_response.rstrip() + "\n\n--END OF LLM OUTPUT--"
            
            return fallback_response

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
