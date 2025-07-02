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
# 2025-07-01T18:56:00Z : Aligned summarization with individual file analysis factual directives by CodeAssistant
# * Updated global summary prompt to use same factual directives as individual file analysis
# * Added "Present FACTUAL TECHNICAL INFORMATION only - no quality judgments" requirement
# * Enhanced prompt with same technical focus requirements for consistent analysis approach
# 2025-07-01T17:15:00Z : Implemented 3-phase generation workflow by CodeAssistant
# * Redesigned workflow: individual file analysis → programmatic insertion → global summary generation
# * Updated directory processing to use incremental markdown building with template engine
# * Implemented factual file analysis without judgmental language and token-efficient architecture
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
from .markdown_template_engine import MarkdownTemplateEngine, FileAnalysis, DirectorySummary
from .enhanced_prompts import EnhancedPrompts
from .debug_handler import DebugHandler

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
        self.template_engine = MarkdownTemplateEngine()
        
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
    
    async def build_file_knowledge(self, file_context: FileContext, ctx: Context) -> FileContext:
        """
        [Class method intent]
        Generates comprehensive file knowledge using Claude 4 Sonnet analysis.
        Processes file content through LLM to create fully integrated knowledge content
        following established format patterns and intemporal writing standards.

        [Design principles]
        Single file analysis through Claude 4 Sonnet with comprehensive content understanding.
        Content chunking for large files exceeding LLM context window constraints.
        Full knowledge content generation following established knowledge base format patterns.
        Error handling enabling graceful degradation when LLM processing fails.

        [Implementation details]
        Reads file content and determines if chunking is required based on size limits.
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
    
    async def build_directory_summary_3_phase(self, directory_context: DirectoryContext, ctx: Context, source_root: Optional[Path] = None) -> DirectoryContext:
        """
        [Class method intent]
        Implements 3-phase directory knowledge generation workflow for token efficiency and content quality.
        Phase 1: Individual file analysis insertion, Phase 2: Subdirectory assembly, Phase 3: Global summary generation.
        Uses incremental markdown building with programmatic content insertion and comprehensive LLM synthesis.

        [Design principles]
        3-phase generation workflow optimizing token usage through selective LLM usage and programmatic assembly.
        Individual file analysis uses factual LLM processing without judgmental language or quality assessments.
        Programmatic content insertion for file analyses and subdirectory summaries maintaining structural consistency.
        Global summary generation leverages complete assembled content for comprehensive synthesis and architectural insights.

        [Implementation details]
        Phase 1: Initialize base markdown structure and insert individual file analyses programmatically.
        Phase 2: Insert subdirectory global summaries programmatically for hierarchical knowledge integration.
        Phase 3: Generate global summary using LLM analysis of complete assembled content for comprehensive synthesis.
        Uses template engine 3-phase methods for incremental building and standard markdown compatibility.
        """
        if not self.llm_driver:
            await self.initialize()
        
        processing_start = datetime.now()
        
        try:
            await ctx.info(f"Building 3-phase directory knowledge for: {directory_context.directory_path}")
            
            # Phase 1: Initialize base markdown structure
            await ctx.debug("Phase 1: Initializing base directory knowledge structure")
            markdown_content = self.template_engine.initialize_directory_knowledge_base(directory_context.directory_path)
            
            # Phase 1: Insert individual file contexts programmatically
            file_contexts = self._collect_file_contexts(directory_context)
            if file_contexts:
                await ctx.debug(f"Phase 1: Inserting {len(file_contexts)} file contexts")
                markdown_content = self.template_engine.insert_file_contexts(markdown_content, file_contexts)
            
            # Phase 2: Insert subdirectory summaries programmatically
            subdirectory_summaries = self._collect_subdirectory_summaries(directory_context)
            if subdirectory_summaries:
                await ctx.debug(f"Phase 2: Inserting {len(subdirectory_summaries)} subdirectory summaries")
                markdown_content = self.template_engine.insert_subdirectory_summaries(markdown_content, subdirectory_summaries)
            
            # Phase 3: Generate global summary using assembled content
            await ctx.debug("Phase 3: Generating global summary from assembled content")
            assembled_content = self.template_engine.extract_assembled_content(markdown_content)
            
            # Generate global summary prompt with same factual directives as individual file analysis
            global_summary_prompt = f"""
Analyze this complete directory content and generate a comprehensive global summary:

**DIRECTORY**: {directory_context.directory_path}/

**ASSEMBLED CONTENT**:
{assembled_content}

**CRITICAL REQUIREMENTS:**
- Present FACTUAL TECHNICAL INFORMATION only - no quality judgments, no enhancement proposal
- Identify specific design patterns, implementation strategies, and technical components
- Document integration points, dependencies, and system relationships
- Provide technical facts needed for code maintenance and understanding
- Write in present tense only
- Be concise and developer-focused
- **DIRECTORY FORMATTING**: When mentioning directory names, ALWAYS add a trailing slash (e.g., "src/" not "src", "tests/" not "tests")
- **DO NOT generate any headers or markdown formatting** - provide only the content text

**ANALYSIS REQUIREMENTS**:
- Provide comprehensive overview of the directory's role and purpose
- Identify key architectural patterns and design decisions
- Highlight important integration points and relationships
- Focus on technical insights that enable system understanding
- Be concise but comprehensive

Generate a global summary that synthesizes all the individual file analyses and subdirectory content into a cohesive understanding of this directory's purpose and implementation.

**IMPORTANT:** 
- Provide factual technical information without subjective quality assessments
- Focus on what the code does and how it works, not how well it works
- Return ONLY the summary content without any headers, markdown formatting, or section titles
- The content will be inserted programmatically into the correct section
"""
            
            # Check for replay response for global summary
            global_summary_replay = self.debug_handler.get_stage_replay_response(
                stage="stage_5_global_summary",
                directory_path=directory_context.directory_path
            )
            
            if global_summary_replay:
                await ctx.info(f"🔄 REPLAY MODE: Reusing cached global summary for {directory_context.directory_path.name}/ (no LLM call made)")
                global_summary = self._extract_content_from_llm_response(global_summary_replay.strip())
            else:
                # Generate global summary through Claude 4 Sonnet
                conversation_id = f"global_summary_{directory_context.directory_path.name}_{datetime.now().isoformat()}"
                await ctx.info(f"🤖 LLM CALL: Generating global directory summary for {directory_context.directory_path.name}/ using Claude 4 Sonnet")
                response = await self.llm_driver.send_message(global_summary_prompt, conversation_id)
                
                # Capture using predictable stage-based debug
                self.debug_handler.capture_stage_llm_output(
                    stage="stage_5_global_summary",
                    prompt=global_summary_prompt,
                    response=response.content,
                    directory_path=directory_context.directory_path
                )
                
                # Parse the LLM response to extract only content, not headers
                global_summary = self._extract_content_from_llm_response(response.content.strip())
            
            # Generate directory analysis for remaining sections
            await ctx.debug("Phase 3: Generating directory architectural analysis")
            child_content_summary = self._prepare_child_content_summary(directory_context)
            directory_prompt = self.enhanced_prompts.get_directory_analysis_prompt(
                directory_path=directory_context.directory_path,
                file_count=len(directory_context.file_contexts),
                subdirectory_count=len(directory_context.subdirectory_contexts),
                child_content_summary=child_content_summary
            )
            
            # Check for replay response for directory analysis
            directory_analysis_replay = self.debug_handler.get_stage_replay_response(
                stage="stage_4_directory_analysis",
                directory_path=directory_context.directory_path
            )
            
            if directory_analysis_replay:
                await ctx.info(f"🔄 REPLAY MODE: Reusing cached architectural analysis for {directory_context.directory_path.name}/ (no LLM call made)")
                directory_response_content = directory_analysis_replay
            else:
                await ctx.info(f"🤖 LLM CALL: Generating architectural analysis for {directory_context.directory_path.name}/ using Claude 4 Sonnet")
                conversation_id = f"global_summary_{directory_context.directory_path.name}_{datetime.now().isoformat()}"
                directory_response = await self.llm_driver.send_message(directory_prompt, conversation_id + "_architecture")
                directory_response_content = directory_response.content
                
                # Capture using predictable stage-based debug
                self.debug_handler.capture_stage_llm_output(
                    stage="stage_4_directory_analysis",
                    prompt=directory_prompt,
                    response=directory_response_content,
                    directory_path=directory_context.directory_path
                )
            parsed_sections = self.enhanced_prompts.parse_structured_response(directory_response_content)
            
            # Create DirectorySummary dataclass
            directory_summary = DirectorySummary(
                directory_path=directory_context.directory_path,
                what_this_directory_contains=parsed_sections.get("what_this_directory_contains", "Analysis not available"),
                how_its_organized=parsed_sections.get("how_its_organized", "Analysis not available"),
                common_patterns=parsed_sections.get("common_patterns", "Analysis not available"),
                how_it_connects=parsed_sections.get("how_it_connects", "Analysis not available")
            )
            
            # Phase 3: Finalize with global summary and directory insights
            await ctx.debug("Phase 3: Finalizing knowledge file with global summary")
            markdown_content = self.template_engine.finalize_with_global_summary(
                markdown_content=markdown_content,
                global_summary=global_summary,
                directory_summary=directory_summary,
                file_count=len(file_contexts),
                subdirectory_count=len(subdirectory_summaries)
            )
            
            # Validate final markdown structure
            if not self.template_engine.validate_markdown_structure(markdown_content):
                logger.warning(f"Final markdown structure validation failed for: {directory_context.directory_path}")
            
            # Determine knowledge file path and write
            knowledge_file_path = self._get_knowledge_file_path(directory_context.directory_path, source_root)
            await self._write_knowledge_file(knowledge_file_path, markdown_content)
            
            await ctx.info(f"3-phase knowledge generation completed: {knowledge_file_path}")
            
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
            logger.error(f"3-phase directory knowledge generation failed for {directory_context.directory_path}: {e}", exc_info=True)
            
            return DirectoryContext(
                directory_path=directory_context.directory_path,
                file_contexts=directory_context.file_contexts,
                subdirectory_contexts=directory_context.subdirectory_contexts,
                processing_status=ProcessingStatus.FAILED,
                error_message=str(e),
                processing_start_time=processing_start,
                processing_end_time=datetime.now()
            )

    async def build_directory_summary(self, directory_context: DirectoryContext, ctx: Context, source_root: Optional[Path] = None) -> DirectoryContext:
        """
        [Class method intent]
        Legacy directory summary generation method maintained for compatibility.
        For new implementations, use build_directory_summary_3_phase for optimal token efficiency
        and content quality through the 3-phase generation workflow.

        [Design principles]
        Maintains backward compatibility with existing hierarchical indexer implementations.
        Provides fallback functionality when 3-phase generation is not required or available.
        Delegates to 3-phase implementation for improved performance and quality.

        [Implementation details]
        Calls build_directory_summary_3_phase to leverage improved token efficiency and content quality.
        Maintains same interface and return type for seamless integration with existing code.
        """
        # Delegate to 3-phase implementation for optimal results
        return await self.build_directory_summary_3_phase(directory_context, ctx, source_root)
    
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
        Processes single file content through simplified LLM analysis generating raw markdown output.
        Uses enhanced prompts for architectural focus with natural markdown response
        stored directly without parsing or transformation.

        [Design principles]
        Simplified LLM processing eliminating complex parsing and structured response handling.
        Raw content storage enabling direct insertion into directory knowledge files.
        Natural markdown generation leveraging LLM's native markdown capabilities.
        Token efficiency through direct content usage without additional processing overhead.

        [Implementation details]
        Uses enhanced prompts with content-type detection for specialized analysis approaches.
        Processes LLM response as raw markdown content without parsing or transformation.
        Returns raw LLM response ready for direct insertion into knowledge files.
        """
        try:
            # Detect content type for specialized analysis
            content_type = self.enhanced_prompts.detect_content_type(file_path, content)
            
            # Generate simplified analysis prompt
            prompt = self.enhanced_prompts.get_file_analysis_prompt(
                file_path=file_path,
                file_content=content,
                file_size=len(content),
                content_type=content_type
            )
            
            # Process through Claude 4 Sonnet with debug support
            normalized_path = self.debug_handler._normalize_path_for_filename(file_path)
            conversation_id = f"file_analysis_{normalized_path}"
            
            # Check for replay response using predictable stage-based debug
            replay_response = self.debug_handler.get_stage_replay_response(
                stage="stage_1_file_analysis",
                file_path=file_path
            )
            
            if replay_response:
                await ctx.info(f"🔄 REPLAY MODE: Reusing cached LLM response for {file_path.name} (no LLM call made)")
                await ctx.debug(f"Using replay response for file analysis: {file_path}")
                response_content = replay_response
            else:
                await ctx.info(f"🤖 LLM CALL: Generating new analysis for {file_path.name} using Claude 4 Sonnet")
                await ctx.debug(f"Making fresh LLM call for file analysis: {file_path}")
                response = await self.llm_driver.send_message(prompt, conversation_id)
                response_content = response.content
                
                # Capture interaction using predictable stage-based debug
                self.debug_handler.capture_stage_llm_output(
                    stage="stage_1_file_analysis",
                    prompt=prompt,
                    response=response_content,
                    file_path=file_path
                )
            
            # Return raw LLM response without parsing or transformation
            return response_content.strip()
            
        except Exception as e:
            logger.error(f"Simplified file processing failed for {file_path}: {e}")
            raise
    
    async def _process_large_file(self, file_path: Path, content: str, ctx: Context) -> str:
        """
        [Class method intent]
        Processes large files through content chunking and multi-pass Claude 4 Sonnet analysis.
        Splits content into manageable chunks and aggregates analysis results
        into comprehensive file summary with raw markdown output.

        [Design principles]
        Content chunking enabling processing of files exceeding LLM context constraints.
        Multi-pass analysis with aggregation for comprehensive large file understanding.
        Chunk overlap preservation maintaining context continuity across boundaries.
        Summary aggregation combining chunk analyses into unified file understanding.

        [Implementation details]
        Splits content into chunks based on configuration size limits with overlap.
        Processes each chunk through Claude 4 Sonnet with chunk-specific prompts.
        Aggregates chunk analyses into final comprehensive file summary.
        Returns raw LLM response ready for direct insertion into knowledge files.
        """
        await ctx.info(f"Processing large file with chunking: {file_path}")
        
        # Split content into chunks
        chunks = self._split_content_into_chunks(content)
        chunk_summaries = []
        
        # Process each chunk
        for i, chunk in enumerate(chunks):
            try:
                # Use enhanced prompts for chunk analysis
                content_type = self.enhanced_prompts.detect_content_type(file_path, chunk)
                prompt = self.enhanced_prompts.get_file_analysis_prompt(
                    file_path=file_path,
                    file_content=chunk,
                    file_size=len(chunk),
                    content_type=content_type
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
- Respond in clear, well-formatted markdown
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
            if file_context.is_completed and file_context.knowledge_content:
                summaries.append(f"## {file_context.file_path.name}\n{file_context.knowledge_content}")
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
                    # Include a condensed version of directory summary
                    if hasattr(subdir_context.directory_summary, 'directory_overview'):
                        # DirectorySummary object - extract overview
                        content_parts.append(f"**Summary**: {subdir_context.directory_summary.directory_overview[:300]}...")
                    else:
                        # String summary - use directly
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
    
    def _collect_subdirectory_summaries(self, directory_context: DirectoryContext) -> List[DirectorySummary]:
        """
        [Class method intent]
        Collects DirectorySummary objects from completed subdirectory contexts for template engine integration.
        Extracts structured directory summary data from completed contexts for programmatic
        template assembly and hierarchical markdown generation.

        [Design principles]
        Structured data extraction enabling clean template engine integration.
        DirectorySummary dataclass compatibility supporting consistent template parameter passing.
        Error handling ensuring graceful degradation when directory summary extraction fails.

        [Implementation details]
        Iterates through completed subdirectory contexts extracting summary data.
        Creates DirectorySummary objects from processed directory contexts for template engine.
        Handles missing or failed directory summaries gracefully with fallback objects.
        """
        subdirectory_summaries = []
        
        for subdir_context in directory_context.subdirectory_contexts:
            if subdir_context.processing_status == ProcessingStatus.COMPLETED and subdir_context.directory_summary:
                try:
                    # Use the actual DirectorySummary object if it exists
                    if isinstance(subdir_context.directory_summary, DirectorySummary):
                        subdirectory_summaries.append(subdir_context.directory_summary)
                    else:
                        # Create DirectorySummary from string summary (fallback for legacy)
                        directory_summary = DirectorySummary(
                            directory_path=subdir_context.directory_path,
                            what_this_directory_contains=str(subdir_context.directory_summary)[:500] + "..." if len(str(subdir_context.directory_summary)) > 500 else str(subdir_context.directory_summary),
                            how_its_organized="See overview section",
                            common_patterns="See overview section", 
                            how_it_connects="See overview section"
                        )
                        subdirectory_summaries.append(directory_summary)
                except Exception as e:
                    logger.warning(f"Failed to extract DirectorySummary for {subdir_context.directory_path}: {e}")
                    raise
                        
        return subdirectory_summaries
    
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
        Writes generated knowledge file content using intelligent strategy detection.
        Uses header-based editing for existing files and template generation for new files.
        Provides safe content writing with proper formatting and error handling.

        [Design principles]
        Intelligent writing strategy based on file existence and content structure.
        Header-based editing for existing files preserving document structure and preventing corruption.
        Template generation for new files ensuring consistent knowledge file format.
        Robust error handling with fallback strategies for reliable knowledge file persistence.

        [Implementation details]
        Detects existing files and uses mistletoe-based header editing when possible.
        Falls back to complete file replacement for new files or when header editing fails.
        Creates complete parent directory structure and handles filesystem errors gracefully.
        Validates file structure before and after operations ensuring content integrity.
        """
        try:
            # Ensure complete parent directory structure exists
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Check if file exists and can be safely edited
            if file_path.exists() and await self._should_use_header_based_editing(file_path):
                logger.debug(f"Using header-based editing for existing file: {file_path}")
                success = await self._update_existing_knowledge_file(file_path, content)
                if success:
                    logger.debug(f"Knowledge file updated using header-based editing: {file_path}")
                    return
                else:
                    logger.warning(f"Header-based editing failed, falling back to complete replacement: {file_path}")
            
            # Default: write new file or complete replacement
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
                
            logger.debug(f"Knowledge file written: {file_path}")
            
        except Exception as e:
            logger.error(f"Failed to write knowledge file {file_path}: {e}")
            raise
    
    async def _should_use_header_based_editing(self, file_path: Path) -> bool:
        """
        [Class method intent]
        Determines whether existing knowledge file should use header-based editing.
        Validates file structure and content compatibility with mistletoe-based editing operations.

        [Design principles]
        Safe editing detection preventing corruption of incompatible or malformed files.
        Structure validation ensuring header-based editing operations will succeed.
        Conservative approach favoring complete replacement over risky editing operations.

        [Implementation details]
        Validates existing file structure using template engine validation methods.
        Checks for required headers and markdown structure compatibility.
        Returns boolean indicating safe header-based editing capability.
        """
        try:
            # Validate that the existing file has proper structure for header-based editing  
            if not self.template_engine.validate_existing_file_structure(file_path):
                logger.debug(f"File structure validation failed for header-based editing: {file_path}")
                return False
            
            # Check if file has recognizable headers that we can work with
            headers = self.template_engine.find_available_headers(file_path)
            if not headers:
                logger.debug(f"No headers found for header-based editing: {file_path}")
                return False
            
            # Look for standard knowledge file headers that indicate compatibility
            standard_headers = {"Global Summary", "Architecture and Design", "Key Patterns", 
                             "Integration Points", "File Knowledge Integration", "Subdirectory Knowledge Integration"}
            
            existing_headers = {header['text'] for header in headers}
            has_standard_structure = bool(standard_headers.intersection(existing_headers))
            
            if not has_standard_structure:
                logger.debug(f"File lacks standard knowledge base headers for editing: {file_path}")
                return False
            
            logger.debug(f"File suitable for header-based editing with {len(headers)} headers: {file_path}")
            return True
            
        except Exception as e:
            logger.warning(f"Failed to determine header-based editing compatibility for {file_path}: {e}")
            return False
    
    async def _update_existing_knowledge_file(self, file_path: Path, new_content: str) -> bool:
        """
        [Class method intent]
        Updates existing knowledge file using header-based editing to preserve structure.
        Selectively updates sections while maintaining document integrity and existing formatting.

        [Design principles]
        Selective content updates preserving document structure and existing formatting.
        Header-based section identification enabling precise content replacement without corruption.
        Error handling with graceful fallback ensuring reliable knowledge file updates.

        [Implementation details]
        Parses new content to extract section updates for header-based editing.
        Uses mistletoe-based editing to selectively update specific sections.
        Validates results and provides success feedback for calling methods.
        Handles editing failures gracefully returning false for fallback processing.
        """
        try:
            # Parse the new content to identify sections to update
            new_doc = self.template_engine.markdown_parser.parse_content(new_content)
            if not new_doc:
                logger.error(f"Failed to parse new content for header-based editing: {file_path}")
                return False
            
            # Extract sections from new content
            new_headers = self.template_engine.markdown_parser.find_available_headers(new_doc)
            
            # Update each section that exists in the new content
            updated_sections = 0
            for header_info in new_headers:
                header_text = header_info['text']
                
                # Skip metadata sections that shouldn't be updated
                if header_text.startswith('End of ') or 'Generated:' in header_text:
                    continue
                
                # Get section content from new document
                header_token = header_info['token']
                section_content = self.template_engine.markdown_parser.get_section_content(new_doc, header_token)
                
                if section_content:
                    # Render section content to markdown
                    section_markdown = ""
                    for token in section_content:
                        # Create temporary document for rendering individual tokens
                        temp_doc = type(new_doc)([])
                        temp_doc.children = [token]
                        token_markdown = self.template_engine.markdown_parser.render_to_markdown(temp_doc)
                        if token_markdown:
                            section_markdown += token_markdown + "\n"
                    
                    # Update the section in the existing file
                    if section_markdown.strip():
                        success = self.template_engine.update_section_by_header(
                            file_path, header_text, section_markdown.strip()
                        )
                        if success:
                            updated_sections += 1
                            logger.debug(f"Updated section '{header_text}' in {file_path}")
                        else:
                            logger.warning(f"Failed to update section '{header_text}' in {file_path}")
            
            # Update metadata timestamp
            timestamp_content = f"*Generated: {datetime.now().isoformat()}*"
            self.template_engine.update_section_by_header(file_path, "Generated:", timestamp_content)
            
            logger.debug(f"Successfully updated {updated_sections} sections using header-based editing: {file_path}")
            return updated_sections > 0
            
        except Exception as e:
            logger.error(f"Header-based editing failed for {file_path}: {e}")
            return False
    
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
