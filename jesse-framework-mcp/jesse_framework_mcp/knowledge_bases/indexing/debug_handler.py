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
# Debug handler for LLM output persistence and replay in Knowledge Bases system.
# Implements comprehensive debug mode allowing capture and reuse of LLM interactions
# for debugging markdown formatting issues and template generation problems.
###############################################################################
# [Source file design principles]
# - Complete LLM interaction capture with structured file organization
# - Replay functionality enabling deterministic LLM output reuse
# - Clear debug artifact organization supporting easy debugging workflows
# - Metadata preservation ensuring full context reproduction capability
# - Error handling maintaining debug capability even with file system issues
###############################################################################
# [Source file constraints]
# - Debug files must be human-readable for manual inspection and modification
# - File naming must enable easy identification of specific LLM interactions
# - Replay functionality must maintain complete compatibility with original responses
# - Debug directory structure must support concurrent indexing operations
# - Performance impact must be minimal when debug mode is disabled
###############################################################################
# [Dependencies]
# <system>: json - Debug metadata serialization and structured data persistence
# <system>: pathlib - Debug file organization and cross-platform path handling
# <system>: datetime - Timestamp generation for debug artifact organization
# <system>: hashlib - Content hashing for duplicate detection and identification
# <system>: typing - Type annotations for debug data structures and parameters
###############################################################################
# [GenAI tool change history]
# 2025-07-01T21:59:00Z : Initial debug handler creation by CodeAssistant
# * Implemented LLM output persistence with structured file organization
# * Added replay functionality for deterministic LLM output reuse
# * Created metadata preservation for complete context reproduction
# * Established debug directory structure supporting concurrent operations
###############################################################################

"""
Debug Handler for Knowledge Bases LLM Interactions.

This module provides comprehensive debug mode functionality enabling capture,
persistence, and replay of all LLM interactions during knowledge base generation.
Supports debugging of markdown formatting and template generation issues.
"""

import json
import hashlib
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, NamedTuple
from dataclasses import dataclass, asdict

logger = logging.getLogger(__name__)


@dataclass
class LLMInteraction:
    """
    [Class intent]
    Structured container for complete LLM interaction data including prompt, response,
    metadata, and processing context for comprehensive debug capture and replay.

    [Design principles]
    Complete interaction capture enabling full reproduction of LLM processing context.
    Structured data organization supporting easy debugging and manual inspection.
    Metadata preservation ensuring context understanding during debugging sessions.

    [Implementation details]
    Includes prompt text, response content, timestamp, and processing parameters.
    Supports serialization for persistence and replay functionality.
    Contains enough context for understanding interaction purpose and results.
    """
    interaction_id: str
    conversation_id: str
    prompt: str
    response: str
    timestamp: str
    processing_type: str  # 'file_analysis', 'global_summary', 'directory_analysis', etc.
    file_path: Optional[str] = None
    directory_path: Optional[str] = None
    chunk_info: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class DebugHandler:
    """
    [Class intent]
    Enhanced debug handler for LLM interaction persistence and replay with pipeline stage organization.
    Manages capture of all LLM interactions with predictable filenames and clear stage separation
    enabling deterministic debugging workflows with easy manual inspection.

    [Design principles]
    Stage-based organization with clear pipeline phase separation for debugging clarity.
    Predictable filename generation enabling deterministic replay and easy file location.
    Memory-only operation in non-debug mode for optimal performance.
    Automatic replay detection preventing redundant LLM calls when debug files exist.
    Human-readable debug artifacts with clear stage organization for workflow understanding.

    [Implementation details]
    Uses normalized file paths for predictable filename generation.
    Organizes debug files by pipeline stage rather than generic processing type.
    Supports both capture mode (saving LLM outputs) and replay mode (loading saved outputs).
    Maintains stage-specific directory structure for clear debugging workflows.
    """
    
    # Pipeline stage definitions for clear debug organization
    PIPELINE_STAGES = {
        'stage_1_file_analysis': 'Individual file content analysis',
        'stage_2_chunk_analysis': 'Large file chunking analysis', 
        'stage_3_chunk_aggregation': 'Combining chunk analyses into file summary',
        'stage_4_directory_analysis': 'Architectural directory analysis',
        'stage_5_global_summary': 'Final directory-level synthesis'
    }
    
    def __init__(self, debug_enabled: bool = False, debug_output_directory: Optional[Path] = None, enable_replay: bool = False):
        """
        [Class method intent]
        Initializes enhanced debug handler with pipeline stage organization and predictable filename support.
        Sets up stage-based debug directory structure and configures operation mode based on parameters.

        [Design principles]
        Lazy initialization minimizing overhead when debug mode is disabled.
        Pipeline stage-based directory structure supporting clear debugging workflows.
        Predictable filename strategy enabling deterministic replay functionality.

        [Implementation details]
        Creates pipeline stage directories on first use for optimal performance.
        Configures capture and replay modes with stage-aware file organization.
        Sets up predictable filename generation for easy replay detection.
        """
        self.debug_enabled = debug_enabled
        self.enable_replay = enable_replay
        self.debug_directory: Optional[Path] = None
        self.memory_cache: Dict[str, str] = {}  # In-memory cache for non-debug mode
        self.interactions_cache: Dict[str, LLMInteraction] = {}  # Cache for loaded interactions
        
        if self.debug_enabled or self.enable_replay:
            if debug_output_directory:
                self.debug_directory = debug_output_directory / "llm_debug"
            else:
                import tempfile
                self.debug_directory = Path(tempfile.gettempdir()) / "jesse_llm_debug"
            
            # Create stage-based debug directory structure
            self._ensure_debug_directory()
            logger.info(f"Enhanced debug handler initialized: enabled={debug_enabled}, replay={enable_replay}, directory={self.debug_directory}")
        else:
            logger.info("Debug handler initialized in memory-only mode")
    
    def _ensure_debug_directory(self) -> None:
        """
        [Class method intent]
        Creates stage-based debug directory structure with pipeline stage organization.
        Ensures directory exists and is writable for debug artifact persistence with predictable structure.

        [Design principles]
        Lazy directory creation minimizing file system operations when debug is disabled.
        Pipeline stage-based subdirectory structure supporting clear debugging workflows.
        Error handling ensuring graceful degradation when directory creation fails.

        [Implementation details]
        Creates main debug directory and pipeline stage subdirectories.
        Uses PIPELINE_STAGES definitions for consistent stage organization.
        Creates README file documenting stage purposes for user understanding.
        Handles permission errors and provides clear error messages for troubleshooting.
        """
        if not self.debug_directory:
            return
        
        try:
            # Create main debug directory
            self.debug_directory.mkdir(parents=True, exist_ok=True)
            
            # Create pipeline stage subdirectories
            for stage_name, stage_description in self.PIPELINE_STAGES.items():
                stage_dir = self.debug_directory / stage_name
                stage_dir.mkdir(exist_ok=True)
                logger.debug(f"Created debug stage directory: {stage_name}")
            
            # Create stage documentation
            self._create_stage_documentation()
            
            logger.debug(f"Pipeline stage debug directory structure created: {self.debug_directory}")
            
        except Exception as e:
            logger.warning(f"Failed to create debug directory structure: {e}")
            self.debug_enabled = False
            self.enable_replay = False
    
    def _create_stage_documentation(self) -> None:
        """
        [Class method intent]
        Creates human-readable documentation for pipeline stages and debug workflow.
        Provides clear understanding of debug directory organization and stage purposes.

        [Design principles]
        Human-readable documentation supporting easy debugging workflow understanding.
        Clear stage purpose explanation enabling effective debug artifact navigation.
        Comprehensive workflow documentation for manual debugging processes.

        [Implementation details]
        Creates README.md in debug directory with stage descriptions and usage examples.
        Documents predictable filename patterns for easy replay debugging.
        Provides clear workflow instructions for manual debug artifact inspection.
        """
        if not self.debug_directory:
            return
        
        try:
            readme_path = self.debug_directory / "PIPELINE_STAGES.md"
            with open(readme_path, 'w', encoding='utf-8') as f:
                f.write("# Knowledge Bases Debug Pipeline Stages\n\n")
                f.write("This directory contains LLM debug artifacts organized by pipeline stage for easy debugging.\n\n")
                
                f.write("## Pipeline Stage Organization\n\n")
                for stage_name, stage_description in self.PIPELINE_STAGES.items():
                    f.write(f"### {stage_name}\n")
                    f.write(f"**Purpose**: {stage_description}\n\n")
                    f.write(f"**Files**: Located in `{stage_name}/` subdirectory\n")
                    f.write(f"**Naming Pattern**: `{{normalized_path}}_{{prompt|response}}.txt`\n\n")
                
                f.write("## Predictable Filename Examples\n\n")
                f.write("```\n")
                f.write("stage_1_file_analysis/\n")
                f.write("├── src_main_py_prompt.txt\n")
                f.write("├── src_main_py_response.txt\n")
                f.write("├── utils_helper_py_prompt.txt\n")
                f.write("└── utils_helper_py_response.txt\n\n")
                f.write("stage_5_global_summary/\n")
                f.write("├── project_root_prompt.txt\n")
                f.write("└── project_root_response.txt\n")
                f.write("```\n\n")
                
                f.write("## Debug Workflow\n\n")
                f.write("1. **Capture Mode**: LLM outputs are saved to predictable file locations\n")
                f.write("2. **Replay Mode**: Existing files are used instead of calling LLM\n")
                f.write("3. **Manual Inspection**: Edit response files to test different outputs\n")
                f.write("4. **Deterministic Debugging**: Same inputs always produce same file locations\n\n")
                
                f.write("## Memory-Only Mode\n\n")
                f.write("When debug mode is disabled, LLM outputs are kept in memory only for optimal performance.\n")
                f.write("No files are created and no disk I/O occurs during normal operation.\n")
            
            logger.debug(f"Created pipeline stage documentation: {readme_path}")
            
        except Exception as e:
            logger.warning(f"Failed to create stage documentation: {e}")
    
    def _normalize_path_for_filename(self, path: Path) -> str:
        """
        [Class method intent]
        Normalizes file or directory path into predictable filename component.
        Converts path separators and special characters into underscore-based naming
        enabling deterministic debug file location and replay functionality.

        [Design principles]
        Deterministic filename generation enabling predictable debug file locations.
        Cross-platform compatibility handling different path separator conventions.
        Human-readable filenames supporting easy manual debugging workflows.

        [Implementation details]
        Replaces path separators with underscores for flat filename structure.
        Handles special characters and spaces to create filesystem-safe filenames.
        Preserves path hierarchy information through underscore-separated components.
        Returns normalized string suitable for use in debug filename generation.
        """
        try:
            # Convert path to string and normalize separators
            path_str = str(path).replace('\\', '/').replace('/', '_')
            
            # Handle special characters and clean up
            path_str = path_str.replace(' ', '_').replace('-', '_').replace('.', '_')
            
            # Remove leading/trailing underscores and collapse multiple underscores
            path_str = path_str.strip('_')
            while '__' in path_str:
                path_str = path_str.replace('__', '_')
            
            return path_str.lower()
            
        except Exception as e:
            logger.warning(f"Failed to normalize path {path}: {e}")
            return "unknown_path"
    
    def capture_stage_llm_output(
        self,
        stage: str,
        prompt: str,
        response: str,
        file_path: Optional[Path] = None,
        directory_path: Optional[Path] = None,
        chunk_info: Optional[str] = None
    ) -> None:
        """
        [Class method intent]
        Captures LLM output with stage-specific organization and predictable filename generation.
        Uses pipeline stage and normalized path components to create deterministic file locations
        enabling easy replay debugging and manual inspection workflows.

        [Design principles]
        Stage-based organization with predictable filename patterns for easy debugging.
        Automatic replay detection preventing redundant LLM calls when debug files exist.
        Memory-only operation in non-debug mode for optimal performance.
        Deterministic file locations enabling reliable debugging workflows.

        [Implementation details]
        Generates predictable filenames based on stage and normalized path components.
        Creates separate prompt and response files for easy manual inspection and editing.
        Stores outputs in memory cache for non-debug mode operation.
        Organizes files by pipeline stage for clear debugging workflow understanding.
        """
        # Store in memory cache regardless of debug mode
        cache_key = f"{stage}_{self._normalize_path_for_filename(file_path or directory_path or Path('unknown'))}"
        self.memory_cache[f"{cache_key}_prompt"] = prompt
        self.memory_cache[f"{cache_key}_response"] = response
        
        # Only persist to disk if debug mode is enabled
        if not self.debug_enabled or not self.debug_directory:
            return
        
        try:
            # Ensure stage directory exists
            stage_dir = self.debug_directory / stage
            stage_dir.mkdir(exist_ok=True)
            
            # Generate predictable filename
            if file_path:
                normalized_name = self._normalize_path_for_filename(file_path)
            elif directory_path:
                normalized_name = self._normalize_path_for_filename(directory_path)
            else:
                normalized_name = "unknown_target"
            
            # Add chunk info if present
            if chunk_info:
                normalized_name += f"_chunk_{chunk_info.replace(' ', '_').replace('/', '_')}"
            
            # Save prompt and response with predictable names
            prompt_file = stage_dir / f"{normalized_name}_prompt.txt"
            response_file = stage_dir / f"{normalized_name}_response.txt"
            
            with open(prompt_file, 'w', encoding='utf-8') as f:
                f.write(prompt)
            
            with open(response_file, 'w', encoding='utf-8') as f:
                f.write(response)
            
            logger.debug(f"Captured stage {stage} LLM output: {normalized_name}")
            
        except Exception as e:
            logger.warning(f"Failed to capture stage LLM output for {stage}: {e}")
    
    def get_stage_replay_response(
        self,
        stage: str,
        file_path: Optional[Path] = None,
        directory_path: Optional[Path] = None,
        chunk_info: Optional[str] = None
    ) -> Optional[str]:
        """
        [Class method intent]
        Retrieves saved LLM response using predictable filename generation for replay functionality.
        Checks for existing debug files based on stage and normalized path components
        enabling deterministic replay debugging without redundant LLM calls.

        [Design principles]
        Predictable filename-based lookup enabling deterministic replay functionality.
        Memory cache fallback for non-debug mode operation.
        Graceful fallback when no saved response exists for given parameters.
        Performance optimization through memory cache and predictable file locations.

        [Implementation details]
        Generates same predictable filename as capture method for consistent lookup.
        Checks memory cache first for non-debug mode or recent captures.
        Falls back to file system lookup for debug mode with persistent storage.
        Returns None when no matching response exists, allowing fallback to live LLM calls.
        """
        # Generate same filename as capture method
        if file_path:
            normalized_name = self._normalize_path_for_filename(file_path)
        elif directory_path:
            normalized_name = self._normalize_path_for_filename(directory_path)
        else:
            normalized_name = "unknown_target"
        
        # Add chunk info if present
        if chunk_info:
            normalized_name += f"_chunk_{chunk_info.replace(' ', '_').replace('/', '_')}"
        
        cache_key = f"{stage}_{normalized_name}_response"
        
        # Check memory cache first
        if cache_key in self.memory_cache:
            logger.debug(f"Replay response found in memory cache: {stage}/{normalized_name}")
            return self.memory_cache[cache_key]
        
        # Check file system if debug mode and replay enabled
        if self.enable_replay and self.debug_directory:
            try:
                response_file = self.debug_directory / stage / f"{normalized_name}_response.txt"
                if response_file.exists():
                    with open(response_file, 'r', encoding='utf-8') as f:
                        response = f.read()
                    
                    # Cache for future use
                    self.memory_cache[cache_key] = response
                    
                    logger.debug(f"Replay response loaded from file: {stage}/{normalized_name}")
                    return response
                    
            except Exception as e:
                logger.warning(f"Failed to load replay response from {stage}/{normalized_name}: {e}")
        
        logger.debug(f"No replay response found for {stage}/{normalized_name}")
        return None
    
    def capture_llm_interaction(
        self,
        conversation_id: str,
        prompt: str,
        response: str,
        processing_type: str,
        file_path: Optional[Path] = None,
        directory_path: Optional[Path] = None,
        chunk_info: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        [Class method intent]
        Captures complete LLM interaction data and persists to debug files for later analysis.
        Creates structured debug artifacts with human-readable organization and metadata.

        [Design principles]
        Complete interaction capture with minimal performance impact on main processing.
        Human-readable file organization supporting easy debugging workflows.
        Comprehensive metadata preservation enabling full context reproduction.
        Error handling ensuring debug failures don't impact main indexing operations.

        [Implementation details]
        Generates unique interaction ID based on prompt hash and timestamp.
        Creates separate files for prompt, response, and metadata for easy inspection.
        Organizes files by processing type and includes timestamp for chronological sorting.
        Updates debug index for replay functionality and interaction discovery.
        """
        if not self.debug_enabled or not self.debug_directory:
            return ""
        
        try:
            # Generate unique interaction ID
            timestamp = datetime.now().isoformat()
            prompt_hash = hashlib.md5(prompt.encode()).hexdigest()[:8]
            interaction_id = f"{processing_type}_{prompt_hash}_{timestamp.replace(':', '-').replace('.', '_')}"
            
            # Create LLM interaction object
            interaction = LLMInteraction(
                interaction_id=interaction_id,
                conversation_id=conversation_id,
                prompt=prompt,
                response=response,
                timestamp=timestamp,
                processing_type=processing_type,
                file_path=str(file_path) if file_path else None,
                directory_path=str(directory_path) if directory_path else None,
                chunk_info=chunk_info,
                metadata=metadata
            )
            
            # Save to debug files
            debug_subdir = self.debug_directory / processing_type
            debug_subdir.mkdir(exist_ok=True)
            
            # Save prompt
            prompt_file = debug_subdir / f"{interaction_id}_prompt.txt"
            with open(prompt_file, 'w', encoding='utf-8') as f:
                f.write(prompt)
            
            # Save response
            response_file = debug_subdir / f"{interaction_id}_response.txt"
            with open(response_file, 'w', encoding='utf-8') as f:
                f.write(response)
            
            # Save metadata
            metadata_file = debug_subdir / f"{interaction_id}_metadata.json"
            with open(metadata_file, 'w', encoding='utf-8') as f:
                json.dump(asdict(interaction), f, indent=2, ensure_ascii=False)
            
            # Cache interaction for replay
            self.interactions_cache[interaction_id] = interaction
            
            # Update debug index
            self._update_debug_index()
            
            logger.debug(f"Captured LLM interaction: {interaction_id}")
            return interaction_id
            
        except Exception as e:
            logger.warning(f"Failed to capture LLM interaction: {e}")
            return ""
    
    def get_replay_response(
        self,
        conversation_id: str,
        prompt: str,
        processing_type: str,
        file_path: Optional[Path] = None,
        directory_path: Optional[Path] = None
    ) -> Optional[str]:
        """
        [Class method intent]
        Retrieves saved LLM response for replay functionality based on prompt matching.
        Enables deterministic debugging by reusing previously captured LLM outputs.

        [Design principles]
        Exact prompt matching ensuring replay responses correspond to identical inputs.
        Graceful fallback when no matching interaction is found for given prompt.
        Performance optimization through interaction caching and hash-based lookup.
        Context awareness considering file and directory paths for accurate matching.

        [Implementation details]
        Searches cached interactions for matching prompts and processing context.
        Uses prompt hash and processing type for efficient interaction lookup.
        Falls back to file system search if interaction not found in cache.
        Returns None when no matching interaction exists, allowing fallback to live LLM calls.
        """
        if not self.enable_replay or not self.debug_directory:
            return None
        
        try:
            # Generate prompt hash for lookup
            prompt_hash = hashlib.md5(prompt.encode()).hexdigest()[:8]
            
            # Search cached interactions first
            for interaction in self.interactions_cache.values():
                if (interaction.processing_type == processing_type and 
                    prompt_hash in interaction.interaction_id and
                    interaction.prompt == prompt):
                    
                    # Additional context matching for precision
                    context_match = True
                    if file_path and interaction.file_path:
                        context_match = str(file_path) == interaction.file_path
                    if directory_path and interaction.directory_path:
                        context_match = context_match and str(directory_path) == interaction.directory_path
                    
                    if context_match:
                        logger.debug(f"Replay response found: {interaction.interaction_id}")
                        return interaction.response
            
            # Search file system if not cached
            debug_subdir = self.debug_directory / processing_type
            if debug_subdir.exists():
                for metadata_file in debug_subdir.glob("*_metadata.json"):
                    try:
                        with open(metadata_file, 'r', encoding='utf-8') as f:
                            interaction_data = json.load(f)
                        
                        if interaction_data.get('prompt') == prompt:
                            # Load response from corresponding file
                            response_file = metadata_file.parent / f"{metadata_file.stem.replace('_metadata', '_response')}.txt"
                            if response_file.exists():
                                with open(response_file, 'r', encoding='utf-8') as f:
                                    response = f.read()
                                
                                # Cache for future use
                                interaction = LLMInteraction(**interaction_data)
                                self.interactions_cache[interaction.interaction_id] = interaction
                                
                                logger.debug(f"Replay response loaded from file: {interaction.interaction_id}")
                                return response
                    except Exception as e:
                        logger.warning(f"Failed to load interaction from {metadata_file}: {e}")
            
            logger.debug(f"No replay response found for {processing_type} with prompt hash {prompt_hash}")
            return None
            
        except Exception as e:
            logger.warning(f"Failed to get replay response: {e}")
            return None
    
    def _update_debug_index(self) -> None:
        """
        [Class method intent]
        Updates debug index file with current interaction inventory for debugging navigation.
        Creates human-readable index supporting easy discovery of captured interactions.

        [Design principles]
        Human-readable index format supporting manual debugging workflows.
        Comprehensive interaction listing with context and processing information.
        Performance optimization through incremental index updates rather than full rebuilds.

        [Implementation details]
        Generates index with interaction summaries organized by processing type.
        Includes timestamps, file paths, and interaction IDs for easy navigation.
        Creates both detailed JSON index and human-readable text summary.
        Handles index update errors gracefully without impacting main operations.
        """
        if not self.debug_directory:
            return
        
        try:
            index_data = {
                'generated_at': datetime.now().isoformat(),
                'debug_directory': str(self.debug_directory),
                'interactions_by_type': {},
                'total_interactions': len(self.interactions_cache)
            }
            
            # Organize interactions by processing type
            for interaction in self.interactions_cache.values():
                proc_type = interaction.processing_type
                if proc_type not in index_data['interactions_by_type']:
                    index_data['interactions_by_type'][proc_type] = []
                
                index_data['interactions_by_type'][proc_type].append({
                    'interaction_id': interaction.interaction_id,
                    'timestamp': interaction.timestamp,
                    'conversation_id': interaction.conversation_id,
                    'file_path': interaction.file_path,
                    'directory_path': interaction.directory_path,
                    'chunk_info': interaction.chunk_info
                })
            
            # Save JSON index
            index_file = self.debug_directory / "debug_index.json"
            with open(index_file, 'w', encoding='utf-8') as f:
                json.dump(index_data, f, indent=2, ensure_ascii=False)
            
            # Create human-readable summary
            summary_file = self.debug_directory / "README.md"
            with open(summary_file, 'w', encoding='utf-8') as f:
                f.write(f"# LLM Debug Artifacts\n\n")
                f.write(f"Generated: {index_data['generated_at']}\n")
                f.write(f"Total Interactions: {index_data['total_interactions']}\n\n")
                
                for proc_type, interactions in index_data['interactions_by_type'].items():
                    f.write(f"## {proc_type.replace('_', ' ').title()} ({len(interactions)} interactions)\n\n")
                    for interaction in interactions:
                        f.write(f"- **{interaction['interaction_id']}**\n")
                        f.write(f"  - Timestamp: {interaction['timestamp']}\n")
                        if interaction['file_path']:
                            f.write(f"  - File: {interaction['file_path']}\n")
                        if interaction['directory_path']:
                            f.write(f"  - Directory: {interaction['directory_path']}\n")
                        if interaction['chunk_info']:
                            f.write(f"  - Chunk: {interaction['chunk_info']}\n")
                        f.write("\n")
            
            logger.debug(f"Debug index updated with {len(self.interactions_cache)} interactions")
            
        except Exception as e:
            logger.warning(f"Failed to update debug index: {e}")
    
    def get_debug_summary(self) -> Dict[str, Any]:
        """
        [Class method intent]
        Provides comprehensive debug session summary with interaction statistics and file locations.
        Supports debugging workflow by providing overview of captured interactions and their organization.

        [Design principles]
        Comprehensive debugging information supporting effective debugging workflows.
        Statistical summary enabling understanding of LLM interaction patterns.
        File location information supporting direct access to debug artifacts.

        [Implementation details]
        Aggregates interaction counts by processing type for statistical analysis.
        Provides file system locations for direct debug artifact access.
        Includes timing information and interaction distribution statistics.
        Returns structured data suitable for debugging reports and analysis.
        """
        summary = {
            'debug_enabled': self.debug_enabled,
            'replay_enabled': self.enable_replay,
            'debug_directory': str(self.debug_directory) if self.debug_directory else None,
            'total_interactions': len(self.interactions_cache),
            'interactions_by_type': {},
            'latest_interactions': []
        }
        
        if not self.interactions_cache:
            return summary
        
        # Count interactions by type
        for interaction in self.interactions_cache.values():
            proc_type = interaction.processing_type
            if proc_type not in summary['interactions_by_type']:
                summary['interactions_by_type'][proc_type] = 0
            summary['interactions_by_type'][proc_type] += 1
        
        # Get latest interactions (last 5)
        sorted_interactions = sorted(
            self.interactions_cache.values(),
            key=lambda x: x.timestamp,
            reverse=True
        )
        
        for interaction in sorted_interactions[:5]:
            summary['latest_interactions'].append({
                'interaction_id': interaction.interaction_id,
                'processing_type': interaction.processing_type,
                'timestamp': interaction.timestamp,
                'file_path': interaction.file_path,
                'directory_path': interaction.directory_path
            })
        
        return summary
    
    def load_existing_interactions(self) -> None:
        """
        [Class method intent]
        Loads existing debug interactions from file system for replay functionality.
        Enables continuation of debugging sessions across multiple indexing runs.

        [Design principles]
        Comprehensive interaction loading supporting replay functionality across sessions.
        Error handling ensuring partial loading success even with corrupted debug files.
        Performance optimization through selective loading based on replay requirements.

        [Implementation details]
        Scans debug directory structure for existing interaction metadata files.
        Loads interaction data into cache for efficient replay lookup.
        Handles corrupted or incomplete debug files gracefully with error logging.
        Updates debug index after loading for consistent debugging state.
        """
        if not self.debug_directory or not self.debug_directory.exists():
            return
        
        try:
            loaded_count = 0
            
            # Scan all processing type subdirectories
            for subdir in self.debug_directory.iterdir():
                if subdir.is_dir() and subdir.name != "metadata":
                    for metadata_file in subdir.glob("*_metadata.json"):
                        try:
                            with open(metadata_file, 'r', encoding='utf-8') as f:
                                interaction_data = json.load(f)
                            
                            interaction = LLMInteraction(**interaction_data)
                            self.interactions_cache[interaction.interaction_id] = interaction
                            loaded_count += 1
                            
                        except Exception as e:
                            logger.warning(f"Failed to load interaction from {metadata_file}: {e}")
            
            logger.info(f"Loaded {loaded_count} existing debug interactions for replay")
            
            # Update index with loaded interactions
            if loaded_count > 0:
                self._update_debug_index()
                
        except Exception as e:
            logger.warning(f"Failed to load existing debug interactions: {e}")
    
    def cleanup(self) -> None:
        """
        [Class method intent]
        Performs cleanup operations for debug handler including final index updates and cache clearing.
        Ensures debug artifacts are properly finalized and resources are released.

        [Design principles]
        Proper resource cleanup ensuring debug artifacts are properly persisted.
        Final index updates providing complete debugging session summary.
        Graceful error handling preventing cleanup failures from impacting main operations.

        [Implementation details]
        Performs final debug index update with complete interaction inventory.
        Clears interaction cache to release memory resources.
        Handles cleanup errors gracefully with appropriate logging.
        """
        try:
            if self.debug_enabled and self.interactions_cache:
                self._update_debug_index()
                logger.info(f"Debug handler cleanup completed: {len(self.interactions_cache)} interactions captured")
            
            # Clear cache
            self.interactions_cache.clear()
            
        except Exception as e:
            logger.warning(f"Debug handler cleanup error: {e}")
