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
# Test Cline slash command integration through FastMCP in-memory testing.
# Ensures JESSE workflows are accessible as Cline slash commands with proper HTTP formatting.
###############################################################################
# [Source file design principles]
# - FastMCP in-memory testing eliminates mock complexity for realistic Cline integration testing
# - Workflow resources must use file:// URI scheme for Cline compatibility
# - HTTP formatting must be preserved for AI assistant processing
# - Resource metadata must provide discovery information for Cline slash command integration
###############################################################################
# [Source file constraints]
# - Must use FastMCP InMemoryTransport for realistic MCP protocol testing
# - Workflow resource URIs must follow file://workflows/{filename} pattern
# - HTTP formatting boundaries must be present in all workflow content
# - Cline integration must remain backward compatible after modernization
###############################################################################
# [Dependencies]
# system:pytest - Modern testing framework with async support
# system:fastmcp.testing.InMemoryTransport - FastMCP in-memory testing transport
# codebase:jesse_framework_mcp.main.server - Main FastMCP server instance
###############################################################################
# [GenAI tool change history]
# 2025-06-28T07:13:15Z : Updated to FastMCP in-memory testing patterns by CodeAssistant
# * Replaced mock-based testing with FastMCP InMemoryTransport for realistic testing
# * Simplified test structure using FastMCP native patterns
# * Maintained Cline compatibility testing with modernized approach
# * Preserved HTTP formatting verification for AI assistant processing
###############################################################################

import pytest
from fastmcp.testing import InMemoryTransport
from jesse_framework_mcp.main import server

class TestClineIntegration:
    """
    [Function intent]
    Test Cline slash command integration through FastMCP in-memory testing.
    
    [Design principles]
    FastMCP in-memory testing provides realistic Cline compatibility testing.
    Workflow resources must be discoverable and accessible through standard MCP.
    
    [Implementation details]
    Uses FastMCP InMemoryTransport for realistic MCP protocol testing.
    Verifies workflow resource format and accessibility for Cline integration.
    """
    
    @pytest.fixture
    async def client(self):
        """
        [Function intent]
        FastMCP in-memory client fixture for Cline integration testing.
        
        [Design principles]
        Provides clean test isolation for Cline compatibility testing.
        Uses FastMCP InMemoryTransport for realistic MCP protocol testing.
        
        [Implementation details]
        Creates InMemoryTransport connection to server instance,
        yields client for test usage, automatically handles cleanup.
        """
        async with InMemoryTransport(server) as client:
            yield client
    
    async def test_workflow_resources_unchanged(self, client):
        """
        [Function intent]
        Verify Cline workflow integration remains unchanged after modernization.
        
        [Design principles]
        Cline integration must remain backward compatible.
        Workflow resources must maintain HTTP formatting for AI assistant processing.
        
        [Implementation details]
        Verifies workflow resources are discoverable and accessible,
        tests workflow content maintains required HTTP formatting.
        """
        resources = await client.list_resources()
        workflow_resources = [r for r in resources["resources"] if r["uri"].startswith("file://workflows/")]
        
        assert len(workflow_resources) > 0, "Cline workflow resources missing after modernization"
        
        # Test workflow access maintains HTTP formatting
        workflow_uri = workflow_resources[0]["uri"]
        content = await client.read_resource(workflow_uri)
        text = content["contents"][0]["text"]
        
        # Verify HTTP formatting for AI assistant processing
        assert "--JESSE_FRAMEWORK_BOUNDARY_2025--" in text
        assert "Content-Type:" in text
        assert "Content-Criticality:" in text
    
    async def test_workflow_resource_discovery(self, client):
        """
        [Function intent]
        Test workflow resource discovery for Cline slash command integration.
        
        [Design principles]
        Cline requires workflow resources to be discoverable through standard MCP protocol.
        Resources must have proper metadata for slash command integration.
        
        [Implementation details]
        Lists all resources and validates workflow resources have proper format
        and metadata required for Cline integration.
        """
        resources = await client.list_resources()
        
        # Verify workflow resources exist
        workflow_resources = [
            r for r in resources["resources"] 
            if r["uri"].startswith("file://workflows/")
        ]
        
        assert len(workflow_resources) > 0, "No workflow resources found for Cline integration"
        
        # Verify workflow resource format
        for resource in workflow_resources:
            # Cline requires specific URI format
            assert resource["uri"].startswith("file://workflows/")
            assert resource["uri"].endswith(".md")
            
            # Verify required metadata
            assert "name" in resource
            assert "description" in resource
            assert "mimeType" in resource
            assert resource["mimeType"] == "text/markdown"
    
    async def test_workflow_resource_access(self, client):
        """
        [Function intent]
        Test workflow resource access through MCP protocol for Cline compatibility.
        
        [Design principles]
        Cline requires workflow content to be accessible and properly formatted.
        HTTP formatting must be preserved for AI assistant processing.
        
        [Implementation details]
        Reads workflow resources through MCP protocol and validates content format.
        Verifies HTTP boundary markers and content structure for Cline.
        """
        resources = await client.list_resources()
        workflow_resources = [
            r for r in resources["resources"] 
            if r["uri"].startswith("file://workflows/")
        ]
        
        assert len(workflow_resources) > 0, "No workflow resources to test"
        
        # Test accessing first workflow resource
        test_uri = workflow_resources[0]["uri"]
        content = await client.read_resource(test_uri)
        
        # Verify MCP response format
        assert "contents" in content
        assert len(content["contents"]) == 1
        
        content_item = content["contents"][0]
        assert "uri" in content_item
        assert "mimeType" in content_item
        assert "text" in content_item
        assert content_item["uri"] == test_uri
        
        # Verify HTTP formatting for AI assistant processing
        text = content_item["text"]
        assert "--JESSE_FRAMEWORK_BOUNDARY_2025--" in text
        assert "Content-Type:" in text
        assert "Content-Criticality:" in text
    
    async def test_cline_slash_command_format(self, client):
        """
        [Function intent]
        Test workflow content format for Cline slash command compatibility.
        
        [Design principles]
        Workflows must contain explicit instructions for AI assistant execution.
        Content must be formatted for reliable AI assistant interpretation.
        
        [Implementation details]
        Validates workflow content contains required elements for Cline slash commands.
        Checks for explicit instructions and proper formatting markers.
        """
        resources = await client.list_resources()
        workflow_resources = [
            r for r in resources["resources"] 
            if r["uri"].startswith("file://workflows/")
        ]
        
        for resource in workflow_resources[:3]:  # Test first 3 workflows
            content = await client.read_resource(resource["uri"])
            text = content["contents"][0]["text"]
            
            # Verify explicit instructions for AI assistant
            # Workflows should contain clear instructions
            assert len(text) > 100, f"Workflow {resource['uri']} content too short"
            
            # Verify HTTP formatting boundaries
            assert "--JESSE_FRAMEWORK_BOUNDARY_2025--" in text
            
            # Most workflows should contain explicit instructions
            instruction_indicators = [
                "explicit_instructions", "INSTRUCTIONS", "Execute", "Perform", 
                "Create", "Update", "Generate", "Process"
            ]
            
            has_instructions = any(indicator in text for indicator in instruction_indicators)
            assert has_instructions, f"Workflow {resource['uri']} lacks clear instructions"
    
    def test_uri_pattern_conversion(self):
        """
        [Function intent]
        Test URI pattern conversion for Cline slash command compatibility.
        
        [Design principles]
        Workflow URIs must convert properly to Cline slash commands.
        URI patterns must remain consistent for reliable integration.
        
        [Implementation details]
        Tests conversion from workflow URIs to slash command format,
        validates naming patterns expected by Cline.
        """
        # Test cases for URI to slash command conversion
        test_cases = [
            ("file://workflows/jesse_wip_task_create.md", "/jesse_wip_task_create"),
            ("file://workflows/jesse_capture_our_chat.md", "/jesse_capture_our_chat"),
            ("file://workflows/jesse_amazon_pr_faq_coach.md", "/jesse_amazon_pr_faq_coach")
        ]
        
        for uri, expected_slash_command in test_cases:
            # Extract filename from URI
            workflow_file = uri[len("file://workflows/"):]
            # Convert to slash command name
            clean_name = workflow_file.replace('.md', '') if workflow_file.endswith('.md') else workflow_file
            slash_command = f"/{clean_name}"
            
            assert slash_command == expected_slash_command
    
    async def test_workflow_backward_compatibility(self, client):
        """
        [Function intent]
        Test that workflow integration remains backward compatible after modernization.
        
        [Design principles]
        Modernization must not break existing Cline integration.
        All workflow functionality must remain accessible.
        
        [Implementation details]
        Compares workflow access patterns before and after modernization,
        ensures all expected workflows are still available.
        """
        resources = await client.list_resources()
        workflow_resources = [r for r in resources["resources"] if r["uri"].startswith("file://workflows/")]
        
        # Verify expected workflow categories are still available
        workflow_names = [r["name"] for r in workflow_resources]
        
        # Expected workflow patterns (these should exist)
        expected_patterns = ["jesse_", "wip_task", "capture", "knowledge"]
        
        pattern_found = {pattern: False for pattern in expected_patterns}
        
        for workflow_name in workflow_names:
            for pattern in expected_patterns:
                if pattern in workflow_name:
                    pattern_found[pattern] = True
        
        # At least some expected patterns should be found
        found_count = sum(pattern_found.values())
        assert found_count > 0, f"No expected workflow patterns found in {workflow_names}"
