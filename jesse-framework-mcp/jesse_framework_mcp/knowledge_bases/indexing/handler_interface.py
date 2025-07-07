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
# Standardized handler interface and registry for Knowledge Bases Hierarchical Indexing System.
# Defines abstract base class for all indexing handlers enabling extensible processing of different
# content types (project-base, git-clone, PDF, etc.) with consistent path calculation and cleanup logic.
###############################################################################
# [Source file design principles]
# - Abstract interface ensuring consistent handler behavior across all content types
# - Handler registry providing automatic discovery, routing, and extensibility
# - Warn-and-skip approach for unsupported content types preventing incorrect processing
# - Delegated path calculations eliminating hardcoded assumptions in decision engine
# - Clear separation of concerns between handler-specific logic and core indexing engine
###############################################################################
# [Source file constraints]
# - All handlers must implement complete IndexingHandler interface contract
# - Handler registry must support dynamic registration for extensibility
# - Path calculations must be handler-specific without cross-handler dependencies
# - Error handling must provide clear feedback about unsupported content types
# - Interface must support future extension without breaking existing handlers
###############################################################################
# [Dependencies]
# <codebase>: ..models.indexing_config - Configuration and filtering logic
# <codebase>: ..models.knowledge_context - Context structures for processing
# <system>: pathlib - Cross-platform path operations and calculations
# <system>: abc - Abstract base class definition and enforcement
# <system>: typing - Type hints and interface definitions
# <system>: logging - Structured logging for handler operations
# <system>: fastmcp - Context and progress reporting interface
###############################################################################
# [GenAI tool change history]
# 2025-07-07T20:31:00Z : INITIAL IMPLEMENTATION - Created standardized handler interface and registry architecture by CodeAssistant
# * Created IndexingHandler abstract base class defining complete interface contract
# * Implemented HandlerRegistry with automatic discovery, routing, and warn-and-skip logic
# * Added DecisionReason.NO_HANDLER_AVAILABLE for unsupported content types
# * Designed extensible architecture supporting future handler types without core changes
# * RESOLVES: Git-clone hierarchies incorrectly placed in project-base directory due to hardcoded paths in RebuildDecisionEngine
###############################################################################

"""
Standardized Handler Interface and Registry for Hierarchical Indexing System.

This module defines the abstract interface that all indexing handlers must implement,
along with a registry system for automatic handler discovery and routing. Eliminates
hardcoded path assumptions and enables clean extensibility for new content types.
"""

import logging
from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from pathlib import Path
from enum import Enum

from fastmcp import Context

# Import models (will be imported in actual implementation)
# from ..models import IndexingConfig, DirectoryContext

logger = logging.getLogger(__name__)


class DecisionReason(Enum):
    """Extended decision reasons including handler-related decisions"""
    # Existing reasons (imported from models.rebuild_decisions)
    CACHE_STALE = "cache_stale"
    CACHE_FRESH = "cache_fresh"
    COMPREHENSIVE_STALENESS = "comprehensive_staleness"
    UP_TO_DATE = "up_to_date"
    EMPTY_DIRECTORY = "empty_directory"
    ORPHANED_KNOWLEDGE_FILE = "orphaned_knowledge_file"
    ORPHANED_ANALYSIS_CACHE = "orphaned_analysis_cache"
    CHILD_DIRECTORY_REBUILT = "child_directory_rebuilt"
    DECISION_ERROR = "decision_error"
    
    # NEW: Handler-related decision reasons
    NO_HANDLER_AVAILABLE = "no_handler_available"


class IndexingHandler(ABC):
    """
    [Class intent]
    Abstract base class defining the contract for all indexing handlers.
    Enables extensible processing of different content types (project-base, git-clone, PDF, etc.)
    with consistent path calculation, cleanup logic, and processing behavior.

    [Design principles]
    Abstract interface ensuring all handlers implement identical contracts for consistent behavior.
    Handler-specific path calculations eliminating hardcoded assumptions in core components.
    Comprehensive content processing covering discovery, analysis, and cleanup operations.
    Clear responsibility separation between handler logic and core indexing engine.
    Extensible design supporting future content types without modifying existing components.

    [Implementation details]
    All methods are abstract requiring concrete implementation in derived classes.
    Path calculation methods provide handler-specific knowledge and cache file locations.
    Processing methods handle content discovery and DirectoryContext generation.
    Cleanup methods identify orphaned files in handler-managed directories.
    Mapping methods provide reverse path calculations for validation and cleanup operations.
    """
    
    def __init__(self, config):  # IndexingConfig type will be imported
        """
        [Class method intent]
        Initializes handler with configuration for content-specific processing.
        Stores configuration reference for filtering rules and processing parameters.

        [Design principles]
        Configuration-driven behavior enabling flexible handler customization.
        Common initialization pattern shared across all handler implementations.

        [Implementation details]
        Stores config reference for use in filtering and processing methods.
        Base implementation provides common configuration access patterns.
        """
        self.config = config
    
    @abstractmethod
    def get_handler_type(self) -> str:
        """
        [Class method intent]
        Returns unique handler type identifier for registry and logging purposes.
        Enables handler identification and routing in registry system.

        [Design principles]
        Unique identifier ensuring unambiguous handler identification in registry.
        Clear naming convention supporting debugging and monitoring operations.

        [Implementation details]
        Returns string identifier like 'git-clone', 'project-base', 'pdf', etc.
        Used by registry for handler lookup and routing decisions.
        """
        pass
    
    @abstractmethod
    def can_handle(self, source_path: Path) -> bool:
        """
        [Class method intent]
        Determines if this handler can process the given source path.
        Enables automatic handler selection based on path characteristics.

        [Design principles]
        Clear capability declaration preventing incorrect handler selection.
        Path-based routing enabling automatic content type detection.
        Boolean decision supporting registry's handler selection logic.

        [Implementation details]
        Analyzes path characteristics to determine handler compatibility.
        Returns True only for paths this handler is designed to process.
        Used by registry to select appropriate handler for content processing.
        """
        pass
    
    @abstractmethod
    def get_knowledge_path(self, target_path: Path, source_root: Path) -> Path:
        """
        [Class method intent]
        Calculates knowledge file path for target using handler-specific logic.
        Eliminates hardcoded path assumptions enabling handler-controlled file placement.

        [Design principles]
        Handler-specific path calculation ensuring knowledge files are properly located.
        Consistent path generation supporting predictable file organization.
        Flexibility enabling different organizational strategies per content type.

        [Implementation details]
        Calculates knowledge file location based on handler's organizational strategy.
        May use different naming conventions (root_kb.md vs directory_kb.md).
        Returns absolute path for knowledge file creation and management.
        """
        pass
    
    @abstractmethod
    def get_cache_path(self, file_path: Path, source_root: Path) -> Path:
        """
        [Class method intent]
        Calculates analysis cache path for file using handler-specific logic.
        Enables handler-controlled cache organization aligned with content structure.

        [Design principles]
        Handler-specific cache organization supporting efficient cache management.
        Consistent cache location calculation enabling reliable cache operations.
        Organizational alignment between content structure and cache structure.

        [Implementation details]
        Calculates cache file location using handler's organizational strategy.
        Maintains relationship between source files and corresponding cache files.
        Returns absolute path for cache file creation and management.
        """
        pass
    
    @abstractmethod
    async def process_structure(self, source_path: Path, ctx: Context) -> 'DirectoryContext':
        """
        [Class method intent]
        Processes source structure returning DirectoryContext for indexing.
        Implements handler-specific discovery and context generation logic.

        [Design principles]
        Handler-specific processing logic accommodating different content organizations.
        Comprehensive structure analysis covering files and subdirectories.
        Context generation supporting downstream indexing operations.

        [Implementation details]
        Discovers files and subdirectories using handler-specific filtering rules.
        Creates FileContext and DirectoryContext objects with appropriate metadata.
        Returns structured context ready for indexing engine processing.
        """
        pass
    
    @abstractmethod
    def should_process_item(self, item_path: Path, source_root: Path) -> bool:
        """
        [Class method intent]
        Determines if item should be processed based on handler-specific rules.
        Provides content-specific filtering for files and directories.

        [Design principles]
        Handler-specific filtering enabling appropriate content selection.
        Consistent filtering logic supporting predictable processing behavior.
        Integration with configuration rules for flexible exclusion management.

        [Implementation details]
        Applies handler-specific exclusion rules for content filtering.
        Considers configuration exclusions and content-specific requirements.
        Returns boolean decision for item inclusion in processing.
        """
        pass
    
    @abstractmethod
    async def find_orphaned_files(self, source_root: Path, ctx: Context) -> List[Path]:
        """
        [Class method intent]
        Finds orphaned files in handler-managed areas for cleanup operations.
        Implements handler-specific orphaned file detection and cleanup logic.

        [Design principles]
        Handler-specific cleanup ensuring only appropriate files are identified for removal.
        Comprehensive orphaned file detection covering all handler-managed locations.
        Safe cleanup operations preventing accidental deletion of valid files.

        [Implementation details]
        Scans handler-managed directories identifying files without corresponding sources.
        Validates orphaned status using handler-specific validation logic.
        Returns list of confirmed orphaned files ready for safe deletion.
        """
        pass
    
    @abstractmethod
    def map_knowledge_to_source(self, knowledge_path: Path, source_root: Path) -> Optional[Path]:
        """
        [Class method intent]
        Maps knowledge file back to corresponding source path for validation.
        Enables reverse path calculation for cleanup and validation operations.

        [Design principles]
        Reverse path mapping supporting validation and cleanup operations.
        Handler-specific mapping logic accommodating different organizational strategies.
        Robust error handling returning None for invalid or unresolvable paths.

        [Implementation details]
        Calculates corresponding source path from knowledge file location.
        Uses handler-specific path organization knowledge for accurate mapping.
        Returns None for paths that cannot be resolved to valid sources.
        """
        pass
    
    @abstractmethod
    def map_cache_to_source(self, cache_path: Path, source_root: Path) -> Optional[Path]:
        """
        [Class method intent]
        Maps cache file back to corresponding source path for validation.
        Enables reverse path calculation for cache cleanup and validation operations.

        [Design principles]
        Reverse path mapping supporting cache validation and cleanup operations.
        Handler-specific mapping logic accommodating different cache organizations.
        Robust error handling returning None for invalid or unresolvable paths.

        [Implementation details]
        Calculates corresponding source path from cache file location.
        Uses handler-specific cache organization knowledge for accurate mapping.
        Returns None for paths that cannot be resolved to valid sources.
        """
        pass


class HandlerRegistry:
    """
    [Class intent]
    Registry and factory for indexing handlers providing automatic discovery, routing,
    and extensibility. Implements warn-and-skip approach for unsupported content types
    ensuring safe processing and clear feedback about content coverage.

    [Design principles]
    Automatic handler registration and discovery eliminating manual routing logic.
    Warn-and-skip approach for unsupported content preventing incorrect processing.
    Extensible architecture supporting dynamic handler addition without core changes.
    Clear feedback about handler availability and content processing coverage.
    Safety-first approach skipping unknown content rather than processing incorrectly.

    [Implementation details]
    Maintains list of registered handlers with automatic default handler registration.
    Provides handler lookup based on path characteristics and capability declarations.
    Implements warning system for unsupported content with clear user feedback.
    Supports handler registration for extensibility and customization.
    Tracks handler availability and provides debugging information for troubleshooting.
    """
    
    def __init__(self, config):  # IndexingConfig type will be imported
        """
        [Class method intent]
        Initializes handler registry with configuration and registers default handlers.
        Sets up core handler ecosystem with built-in content type support.

        [Design principles]
        Automatic default handler registration eliminating manual setup requirements.
        Configuration-driven handler initialization supporting customizable behavior.
        Extensible foundation supporting additional handler registration.

        [Implementation details]
        Stores configuration reference for handler initialization.
        Registers built-in handlers for project-base and git-clone content types.
        Maintains handler list for lookup and routing operations.
        """
        self.config = config
        self._handlers: List[IndexingHandler] = []
        self._register_default_handlers()
    
    def _register_default_handlers(self):
        """
        [Class method intent]
        Registers built-in handlers for core content types.
        Provides essential handler coverage for standard content processing.

        [Design principles]
        Core content type coverage ensuring system functionality out of the box.
        Extensible foundation supporting additional handler types through registration.

        [Implementation details]
        Imports and registers GitCloneHandler and ProjectBaseHandler.
        Handler registration order matters - specialized handlers first, then fallback.
        """
        try:
            from .special_handlers import GitCloneHandler, ProjectBaseHandler
            
            # Register specialized handlers first (they have specific capability checks)
            self.register_handler(GitCloneHandler(self.config))
            
            # Register fallback handler last (it accepts non-specialized paths)
            self.register_handler(ProjectBaseHandler(self.config))
            
            logger.info(f"Registered {len(self._handlers)} default handlers")
            
        except ImportError as e:
            logger.error(f"Failed to import handlers: {e}")
            raise
        except Exception as e:
            logger.error(f"Failed to register default handlers: {e}")
            raise
    
    def register_handler(self, handler: IndexingHandler):
        """
        [Class method intent]
        Registers a new handler in the registry for content processing.
        Enables extensibility through dynamic handler addition.

        [Design principles]
        Dynamic handler registration supporting extensibility and customization.
        Type checking ensuring only compatible handlers are registered.
        Registry maintenance supporting handler lookup and routing operations.

        [Implementation details]
        Adds handler to internal list for lookup operations.
        Validates handler implements IndexingHandler interface.
        Maintains registration order for handler priority management.
        """
        if not isinstance(handler, IndexingHandler):
            raise TypeError(f"Handler must implement IndexingHandler interface: {type(handler)}")
        
        self._handlers.append(handler)
        logger.info(f"Registered handler: {handler.get_handler_type()}")
    
    def get_handler_for_path(self, source_path: Path) -> Optional[IndexingHandler]:
        """
        [Class method intent]
        Gets appropriate handler for source path using capability-based selection.
        Returns None if no handler can process the path, supporting warn-and-skip approach.

        [Design principles]
        Capability-based handler selection ensuring appropriate processing.
        Warn-and-skip approach preventing incorrect processing of unsupported content.
        Clear None return indicating no suitable handler available.

        [Implementation details]
        Iterates through registered handlers checking capability with can_handle().
        Returns first handler claiming capability for path processing.
        Returns None if no handler can process path, enabling warn-and-skip behavior.
        """
        for handler in self._handlers:
            try:
                if handler.can_handle(source_path):
                    return handler
            except Exception as e:
                logger.warning(f"Handler capability check failed for {handler.get_handler_type()}: {e}")
                continue
        
        # No handler available - warn and skip approach
        logger.warning(f"No indexing handler available for path: {source_path}")
        return None
    
    async def get_handler_for_path_with_context(self, source_path: Path, ctx: Context) -> Optional[IndexingHandler]:
        """
        [Class method intent]
        Gets handler with user-visible warning for unsupported content types.
        Provides clear feedback about content processing coverage and limitations.

        [Design principles]
        User-visible feedback about unsupported content enabling informed decisions.
        Consistent warning messages supporting troubleshooting and extensibility planning.
        Context-aware logging supporting monitoring and debugging operations.

        [Implementation details]
        Uses get_handler_for_path() for handler selection logic.
        Provides context-based warning when no handler is available.
        Returns None to signal warn-and-skip behavior to calling code.
        """
        handler = self.get_handler_for_path(source_path)
        
        if handler is None:
            await ctx.warning(f"⚠️ SKIP: No handler available for {source_path.name} - content will not be indexed")
            logger.info(f"Available handlers: {[h.get_handler_type() for h in self._handlers]}")
        
        return handler
    
    def get_handler_by_type(self, handler_type: str) -> Optional[IndexingHandler]:
        """
        [Class method intent]
        Gets handler by type identifier for specific handler access.
        Enables direct handler lookup for testing and specialized operations.

        [Design principles]
        Direct handler access supporting testing and specialized use cases.
        Type-based lookup enabling handler-specific operations when needed.
        Optional return supporting graceful handling of missing handler types.

        [Implementation details]
        Searches registered handlers for matching type identifier.
        Returns None if handler type not found rather than raising exception.
        Supports debugging and testing scenarios requiring specific handler access.
        """
        for handler in self._handlers:
            if handler.get_handler_type() == handler_type:
                return handler
        return None
    
    def get_all_handlers(self) -> List[IndexingHandler]:
        """
        [Class method intent]
        Returns copy of all registered handlers for inspection and iteration.
        Supports registry introspection and bulk operations on handlers.

        [Design principles]
        Registry introspection supporting debugging and monitoring operations.
        Defensive copying preventing external modification of registry state.
        Comprehensive handler access for bulk operations and analysis.

        [Implementation details]
        Returns shallow copy of handler list preserving registry isolation.
        Enables iteration over all handlers for cleanup and analysis operations.
        Supports debugging and monitoring use cases requiring handler enumeration.
        """
        return self._handlers.copy()
    
    def get_registry_info(self) -> Dict[str, Any]:
        """
        [Class method intent]
        Returns registry information for debugging and monitoring purposes.
        Provides comprehensive overview of registered handlers and their capabilities.

        [Design principles]
        Comprehensive registry introspection supporting debugging and monitoring.
        Structured information format enabling programmatic analysis and reporting.
        Handler capability summary supporting troubleshooting and extensibility planning.

        [Implementation details]
        Collects handler type information and capability summaries.
        Returns structured dictionary with registry statistics and handler details.
        Supports monitoring dashboards and debugging tools requiring registry visibility.
        """
        return {
            "handler_count": len(self._handlers),
            "handler_types": [h.get_handler_type() for h in self._handlers],
            "registry_initialized": len(self._handlers) > 0
        }
