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
# Tests for standardized handler interface and registry architecture.
# Validates IndexingHandler interface implementation, HandlerRegistry functionality,
# and warn-and-skip behavior for unsupported content types.
###############################################################################
# [Source file design principles]
# - Comprehensive interface compliance testing ensuring all handlers implement complete contracts
# - Handler registry functionality validation covering registration, routing, and extensibility
# - Warn-and-skip behavior verification preventing incorrect processing of unsupported content
# - Handler-specific path calculation testing ensuring proper file placement and organization
# - Integration testing validating seamless operation with existing indexing architecture
###############################################################################
# [Source file constraints]
# - Test isolation ensuring no cross-test contamination or dependency
# - Mock usage preventing filesystem dependencies and external service calls
# - Comprehensive coverage ensuring all interface methods and registry functionality tested
# - Error scenario testing validating robust handling of edge cases and failures
# - Performance considerations ensuring tests execute efficiently without blocking CI/CD
###############################################################################
# [Dependencies]
# <codebase>: ../jesse_framework_mcp/knowledge_bases/indexing/handler_interface - Handler interface and registry
# <codebase>: ../jesse_framework_mcp/knowledge_bases/indexing/special_handlers - Concrete handler implementations
# <codebase>: ../jesse_framework_mcp/knowledge_bases/models/indexing_config - Configuration structures
# <system>: pytest - Testing framework for unit and integration tests
# <system>: pathlib - Cross-platform path operations for test scenarios
# <system>: unittest.mock - Mocking framework for isolated testing
###############################################################################
# [GenAI tool change history]
# 2025-07-07T20:37:00Z : INITIAL IMPLEMENTATION - Created comprehensive handler interface and registry tests by CodeAssistant
# * Created test coverage for HandlerRegistry registration, routing, and warn-and-skip behavior
# * Added test coverage for IndexingHandler interface compliance in GitCloneHandler and ProjectBaseHandler
# * Implemented path calculation tests ensuring proper knowledge and cache file placement
# * Added integration tests validating seamless operation with existing indexing architecture
# * VALIDATES: Handler interface architecture fixes git-clone hierarchy placement issues
###############################################################################

"""
Tests for Standardized Handler Interface and Registry Architecture.

This module provides comprehensive test coverage for the IndexingHandler interface
and HandlerRegistry, ensuring proper handler registration, routing, and path delegation.
"""

import pytest
from pathlib import Path
from unittest.mock import Mock, AsyncMock, patch

from jesse_framework_mcp.knowledge_bases.indexing.handler_interface import (
    IndexingHandler, 
    HandlerRegistry,
    DecisionReason
)
from jesse_framework_mcp.knowledge_bases.indexing.special_handlers import (
    GitCloneHandler,
    ProjectBaseHandler
)
from jesse_framework_mcp.knowledge_bases.models.indexing_config import IndexingConfig


class TestHandlerInterface:
    """
    [Class intent]
    Tests for IndexingHandler abstract interface ensuring complete contract implementation.
    Validates that all concrete handlers implement required interface methods correctly.

    [Design principles]
    Comprehensive interface compliance testing ensuring consistent handler behavior.
    Abstract interface validation preventing incomplete handler implementations.
    Contract enforcement testing ensuring all handlers provide expected functionality.

    [Implementation details]
    Tests all abstract methods are implemented in concrete handler classes.
    Validates handler type identification and capability declaration functionality.
    Verifies path calculation methods produce correct knowledge and cache file locations.
    """

    def test_git_clone_handler_implements_interface(self):
        """
        [Function intent]
        Validates GitCloneHandler implements complete IndexingHandler interface.
        Ensures all abstract methods are properly implemented with expected behavior.

        [Design principles]
        Interface compliance verification ensuring complete contract implementation.
        Git-clone handler validation ensuring specialized functionality is properly exposed.

        [Implementation details]
        Creates GitCloneHandler instance and verifies all interface methods are callable.
        Tests handler type identification and capability declaration for git-clone paths.
        """
        config = Mock(spec=IndexingConfig)
        handler = GitCloneHandler(config)
        
        # Verify handler implements interface
        assert isinstance(handler, IndexingHandler)
        assert handler.get_handler_type() == "git-clone"
        
        # Test path capability detection
        git_clone_path = Path("/project/.knowledge/git-clones/repo1")
        regular_path = Path("/project/src/main.py")
        
        assert handler.can_handle(git_clone_path) == True
        assert handler.can_handle(regular_path) == False

    def test_project_base_handler_implements_interface(self):
        """
        [Function intent]
        Validates ProjectBaseHandler implements complete IndexingHandler interface.
        Ensures all abstract methods are properly implemented with expected behavior.

        [Design principles]
        Interface compliance verification ensuring complete contract implementation.
        Project-base handler validation ensuring fallback functionality is properly exposed.

        [Implementation details]
        Creates ProjectBaseHandler instance and verifies all interface methods are callable.
        Tests handler type identification and capability declaration for project paths.
        """
        config = Mock(spec=IndexingConfig)
        handler = ProjectBaseHandler(config)
        
        # Verify handler implements interface
        assert isinstance(handler, IndexingHandler)
        assert handler.get_handler_type() == "project-base"
        
        # Test path capability detection (project-base accepts non-specialized paths)
        regular_path = Path("/project/src/main.py")
        assert handler.can_handle(regular_path) == True

    def test_handler_path_calculations(self):
        """
        [Function intent]
        Tests handler-specific path calculation methods for knowledge and cache files.
        Validates that different handlers produce different file organization strategies.

        [Design principles]
        Path calculation validation ensuring handlers control their file organization.
        Handler-specific behavior verification preventing hardcoded path assumptions.

        [Implementation details]
        Tests GitCloneHandler and ProjectBaseHandler path calculation methods.
        Verifies git-clone files go to git-clone directories and project-base files go to project-base directories.
        """
        config = Mock(spec=IndexingConfig)
        
        # Test GitCloneHandler path calculations
        git_handler = GitCloneHandler(config)
        git_clone_root = Path("/project/.knowledge/git-clones/repo1")
        git_knowledge_path = git_handler.get_knowledge_path(git_clone_root, git_clone_root)
        
        assert str(git_knowledge_path).endswith("root_kb.md")
        assert "git-clones" in str(git_knowledge_path) or git_knowledge_path == git_clone_root / "root_kb.md"
        
        # Test ProjectBaseHandler path calculations
        project_handler = ProjectBaseHandler(config)
        project_root = Path("/project")
        project_knowledge_path = project_handler.get_knowledge_path(project_root, project_root)
        
        assert str(project_knowledge_path).endswith("root_kb.md")
        assert "project-base" in str(project_knowledge_path)


class TestHandlerRegistry:
    """
    [Class intent]
    Tests for HandlerRegistry functionality including registration, routing, and extensibility.
    Validates warn-and-skip behavior and proper handler selection based on path characteristics.

    [Design principles]
    Registry functionality validation ensuring proper handler management and routing.
    Warn-and-skip behavior testing preventing incorrect processing of unsupported content.
    Extensibility testing ensuring new handlers can be added without breaking existing functionality.

    [Implementation details]
    Tests handler registration, lookup, and routing functionality.
    Validates warn-and-skip behavior when no suitable handler is available.
    Tests registry introspection and debugging functionality.
    """

    def test_registry_initialization(self):
        """
        [Function intent]
        Tests HandlerRegistry initialization and default handler registration.
        Validates that built-in handlers are properly registered during initialization.

        [Design principles]
        Registry initialization validation ensuring out-of-the-box functionality.
        Default handler registration testing ensuring core content types are supported.

        [Implementation details]
        Creates HandlerRegistry instance and verifies default handlers are registered.
        Tests handler count and type identification functionality.
        """
        config = Mock(spec=IndexingConfig)
        registry = HandlerRegistry(config)
        
        # Verify default handlers are registered
        assert len(registry.get_all_handlers()) >= 2  # GitClone + ProjectBase
        
        handler_types = [h.get_handler_type() for h in registry.get_all_handlers()]
        assert "git-clone" in handler_types
        assert "project-base" in handler_types

    def test_handler_routing(self):
        """
        [Function intent]
        Tests handler routing based on path characteristics and capability declarations.
        Validates that appropriate handlers are selected for different content types.

        [Design principles]
        Handler routing validation ensuring appropriate handler selection.
        Path-based routing testing enabling automatic content type detection.

        [Implementation details]
        Tests git-clone and project-base path routing to appropriate handlers.
        Verifies specialized handlers are selected before fallback handlers.
        """
        config = Mock(spec=IndexingConfig)
        registry = HandlerRegistry(config)
        
        # Test git-clone path routing
        git_clone_path = Path("/project/.knowledge/git-clones/repo1")
        git_handler = registry.get_handler_for_path(git_clone_path)
        
        assert git_handler is not None
        assert git_handler.get_handler_type() == "git-clone"
        
        # Test regular project path routing
        regular_path = Path("/project/src/main.py")
        project_handler = registry.get_handler_for_path(regular_path)
        
        assert project_handler is not None
        assert project_handler.get_handler_type() == "project-base"

    @pytest.mark.asyncio
    async def test_warn_and_skip_behavior(self):
        """
        [Function intent]
        Tests warn-and-skip behavior when no handler can process a given path.
        Validates that unsupported content generates warnings and returns None.

        [Design principles]
        Warn-and-skip behavior validation preventing incorrect processing of unsupported content.
        Clear feedback testing ensuring users understand content processing limitations.

        [Implementation details]
        Creates mock path that no handler can process.
        Verifies warning is generated and None is returned.
        Tests context-aware warning functionality.
        """
        config = Mock(spec=IndexingConfig)
        registry = HandlerRegistry(config)
        
        # Mock all handlers to reject the path
        for handler in registry.get_all_handlers():
            handler.can_handle = Mock(return_value=False)
        
        unsupported_path = Path("/some/unknown/content.xyz")
        ctx = AsyncMock()
        
        # Test warn-and-skip behavior
        result = await registry.get_handler_for_path_with_context(unsupported_path, ctx)
        
        assert result is None
        ctx.warning.assert_called_once()
        assert "SKIP" in str(ctx.warning.call_args)

    def test_handler_registry_extensibility(self):
        """
        [Function intent]
        Tests HandlerRegistry extensibility through dynamic handler registration.
        Validates that new handlers can be added without breaking existing functionality.

        [Design principles]
        Registry extensibility validation ensuring new content types can be supported.
        Dynamic registration testing enabling customization and extension.

        [Implementation details]
        Creates custom handler implementing IndexingHandler interface.
        Registers custom handler and verifies it's available for routing.
        Tests that existing handlers continue to work after new registration.
        """
        config = Mock(spec=IndexingConfig)
        registry = HandlerRegistry(config)
        
        # Create mock custom handler
        custom_handler = Mock(spec=IndexingHandler)
        custom_handler.get_handler_type.return_value = "custom"
        custom_handler.can_handle.return_value = False  # Won't interfere with other tests
        
        # Register custom handler
        initial_count = len(registry.get_all_handlers())
        registry.register_handler(custom_handler)
        
        # Verify registration
        assert len(registry.get_all_handlers()) == initial_count + 1
        
        custom_retrieved = registry.get_handler_by_type("custom")
        assert custom_retrieved is custom_handler

    def test_registry_info_and_debugging(self):
        """
        [Function intent]
        Tests HandlerRegistry introspection and debugging functionality.
        Validates registry information retrieval for monitoring and troubleshooting.

        [Design principles]
        Registry introspection validation supporting debugging and monitoring operations.
        Debugging functionality testing enabling troubleshooting and analysis.

        [Implementation details]
        Tests get_registry_info() method for comprehensive registry status.
        Verifies handler enumeration and statistics functionality.
        """
        config = Mock(spec=IndexingConfig)
        registry = HandlerRegistry(config)
        
        # Test registry information
        info = registry.get_registry_info()
        
        assert "handler_count" in info
        assert "handler_types" in info
        assert "registry_initialized" in info
        
        assert info["handler_count"] >= 2
        assert info["registry_initialized"] == True
        assert isinstance(info["handler_types"], list)


class TestDecisionReasonExtension:
    """
    [Class intent]
    Tests for DecisionReason enum extension with handler-related reasons.
    Validates that new decision reasons are properly defined and accessible.

    [Design principles]
    Decision reason extension validation ensuring proper integration with existing decision logic.
    Enum consistency testing preventing conflicts with existing decision reasons.

    [Implementation details]
    Tests that NO_HANDLER_AVAILABLE reason is properly defined.
    Verifies enum consistency and accessibility.
    """

    def test_no_handler_available_reason_exists(self):
        """
        [Function intent]
        Tests that NO_HANDLER_AVAILABLE decision reason is properly defined.
        Validates enum extension for handler-related decision scenarios.

        [Design principles]
        Decision reason availability validation ensuring proper integration.
        Enum extension testing preventing missing decision reason scenarios.

        [Implementation details]
        Verifies NO_HANDLER_AVAILABLE enum value exists and is accessible.
        Tests enum value consistency and string representation.
        """
        # Test that new decision reason exists
        assert hasattr(DecisionReason, 'NO_HANDLER_AVAILABLE')
        assert DecisionReason.NO_HANDLER_AVAILABLE.value == "no_handler_available"
        
        # Test that it's accessible alongside existing reasons
        all_reasons = list(DecisionReason)
        assert DecisionReason.NO_HANDLER_AVAILABLE in all_reasons
        assert DecisionReason.CACHE_STALE in all_reasons  # Verify existing reasons still work
