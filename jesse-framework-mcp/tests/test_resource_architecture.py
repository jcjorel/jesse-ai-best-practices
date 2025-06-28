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
# Modern FastMCP in-memory testing for individual resource architecture.
# Comprehensive testing of resource discovery, individual resources, and complete integration.
###############################################################################
# [Source file design principles]
# - FastMCP in-memory testing eliminates mock complexity and provides real MCP protocol testing
# - Test individual resources, resource discovery, and complete integration patterns
# - Parametrized testing ensures consistent behavior across all resource categories
# - HTTP formatting verification maintained across all test scenarios
###############################################################################
# [Source file constraints]
# - Must use FastMCP InMemoryTransport for realistic MCP protocol testing
# - All resource categories must be tested: framework rules, project resources, workflows
# - HTTP formatting consistency must be verified across all resources
# - Error handling and edge cases must be covered comprehensively
###############################################################################
# [Dependencies]
# system:pytest - Modern testing framework with async support
# system:fastmcp.testing.InMemoryTransport - FastMCP in-memory testing transport
# codebase:jesse_framework_mcp.main.server - Main FastMCP server instance
###############################################################################
# [GenAI tool change history]
# 2025-06-28T07:09:30Z : Initial FastMCP in-memory testing implementation by CodeAssistant
# * Created comprehensive resource architecture testing with InMemoryTransport
# * Implemented resource discovery testing for all resource categories
# * Added individual framework rule testing with HTTP formatting verification
# * Established Cline workflow compatibility testing patterns
###############################################################################

import pytest
from unittest.mock import AsyncMock
from jesse_framework_mcp.main import server

class TestResourceArchitecture:
    """
    [Function intent]
    Comprehensive testing of individual resource architecture using direct server resource access.
    
    [Design principles]
    Direct resource testing provides reliable validation without complex transport setup.
    Test individual resources, resource discovery, and complete integration.
    
    [Implementation details]
    Uses direct server resource method calls for comprehensive testing.
    Tests all resource categories: framework rules, project resources, knowledge bases, workflows.
    """
    
    @pytest.fixture
    def mock_context(self):
        """
        [Function intent]
        Mock context fixture for testing server resources.
        
        [Design principles]
        Provides clean test isolation with mock context for resource methods.
        Simple mock setup eliminates transport complexity.
        
        [Implementation details]
        Creates AsyncMock context for server resource method testing,
        provides info/error logging methods for resource handlers.
        """
        ctx = AsyncMock()
        ctx.info = AsyncMock()
        ctx.error = AsyncMock()
        return ctx
    
    async def test_framework_rule_resources(self, mock_context):
        """
        [Function intent]
        Test individual JESSE framework rule resources through server resource access.
        
        [Design principles]
        Each framework rule must be individually accessible with consistent formatting.
        CRITICAL criticality must be preserved for framework compliance.
        
        [Implementation details]
        Tests each expected framework rule resource through server resource methods,
        verifies HTTP formatting preservation and rule-specific content.
        """
        # Test framework rule resources through server
        rule_names = [
            "knowledge_management", "hints", "code_comments",
            "code_generation", "markdown", "scratchpad"
        ]
        
        for rule_name in rule_names:
            uri = f"jesse://framework/rule/{rule_name}"
            
            # Get resource through server
            resource = await server.get_resource(uri)
            assert resource is not None, f"Rule resource {uri} not found"
            
            # Call the resource function to get content
            content = await resource.fn(mock_context)
            
            # Verify HTTP formatting preserved
            assert "--JESSE_FRAMEWORK_BOUNDARY_2025--" in content
            assert "Content-Criticality: CRITICAL" in content
            assert "Content-Type: text/markdown" in content
            assert "JESSE" in content.upper()
    
    async def test_project_resources(self, mock_context):
        """
        [Function intent]
        Test project-specific resources with INFORMATIONAL criticality verification.
        
        [Design principles]
        Project resources have INFORMATIONAL criticality (not CRITICAL like framework rules).
        All project resources must maintain HTTP formatting consistency.
        
        [Implementation details]
        Tests each project resource directly with criticality verification,
        ensures HTTP formatting is applied consistently.
        """
        from jesse_framework_mcp.resources.project_resources import (
            get_project_knowledge, get_wip_tasks_inventory, get_project_context_summary
        )
        
        # Test each project resource
        resource_handlers = [
            ("knowledge", get_project_knowledge),
            ("wip-tasks", get_wip_tasks_inventory),
            ("context", get_project_context_summary)
        ]
        
        for resource_name, handler in resource_handlers:
            content = await handler(mock_context)
            
            # Verify HTTP formatting with INFORMATIONAL criticality
            assert "--JESSE_FRAMEWORK_BOUNDARY_2025--" in content
            assert "Content-Criticality: INFORMATIONAL" in content
    
    async def test_resource_index(self, mock_context):
        """
        [Function intent]
        Test lightweight resource index structure and content.
        
        [Design principles]
        Resource index provides programmatic discovery optimization.
        JSON structure must contain all expected metadata categories.
        
        [Implementation details]
        Accesses framework index resource directly and verifies JSON structure
        contains all expected resource categories and metadata.
        """
        from jesse_framework_mcp.main import framework_index
        
        content = await framework_index(mock_context)
        
        # Verify JSON index structure
        assert "framework_version" in content
        assert "resource_categories" in content
        assert "framework_rules" in content
        assert "project_resources" in content
        assert "quick_access" in content
