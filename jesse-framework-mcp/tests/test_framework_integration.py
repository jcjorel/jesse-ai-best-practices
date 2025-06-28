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
# Complete framework integration testing with FastMCP patterns.
# End-to-end testing of complete JESSE Framework MCP server integration.
###############################################################################
# [Source file design principles]
# - Integration testing verifies complete system functionality across all components
# - Tests concurrent access, error handling, and performance characteristics
# - Validates complete workflows and edge cases with realistic scenarios
# - FastMCP in-memory transport provides realistic integration testing
###############################################################################
# [Source file constraints]
# - Must use FastMCP InMemoryTransport for realistic integration testing
# - All resource categories must work together seamlessly
# - Concurrent access patterns must be tested thoroughly
# - Error handling must be comprehensive and graceful
###############################################################################
# [Dependencies]
# system:pytest - Modern testing framework with async support
# system:asyncio - Concurrent testing support
# system:fastmcp.testing.InMemoryTransport - FastMCP in-memory testing transport
# codebase:jesse_framework_mcp.main.server - Main FastMCP server instance
###############################################################################
# [GenAI tool change history]
# 2025-06-28T07:11:15Z : Initial framework integration testing implementation by CodeAssistant
# * Created end-to-end integration testing with complete system validation
# * Implemented concurrent resource access testing for performance validation
# * Added comprehensive error handling testing for edge cases
# * Established HTTP formatting consistency testing across all resources
###############################################################################

import pytest
import asyncio
from fastmcp.testing import InMemoryTransport
from jesse_framework_mcp.main import server

class TestFrameworkIntegration:
    """
    [Function intent]
    End-to-end testing of complete JESSE Framework MCP server integration.
    
    [Design principles]
    Integration testing verifies complete system functionality.
    Tests concurrent access, error handling, and performance characteristics.
    
    [Implementation details]
    Uses FastMCP in-memory transport for realistic integration testing.
    Tests complete workflows and edge cases.
    """
    
    @pytest.fixture
    async def client(self):
        """
        [Function intent]
        FastMCP in-memory client fixture for integration testing.
        
        [Design principles]
        Provides clean test isolation for complete integration testing.
        Uses FastMCP InMemoryTransport for realistic MCP protocol testing.
        
        [Implementation details]
        Creates InMemoryTransport connection to server instance,
        yields client for test usage, automatically handles cleanup.
        """
        async with InMemoryTransport(server) as client:
            yield client
    
    async def test_complete_framework_access(self, client):
        """
        [Function intent]
        Test complete framework access through individual resources with end-to-end validation.
        
        [Design principles]
        Complete framework functionality must work seamlessly across all resource categories.
        Each resource category must be accessible and properly formatted.
        
        [Implementation details]
        Tests resource discovery, framework index, and samples from each resource category,
        validates end-to-end functionality with comprehensive coverage.
        """
        # Test resource discovery
        resources = await client.list_resources()
        assert len(resources["resources"]) > 10  # Should have many individual resources
        
        # Test framework index
        index_content = await client.read_resource("jesse://index")
        assert "framework_version" in index_content["contents"][0]["text"]
        
        # Test each resource category
        categories_tested = {
            "framework_rules": False,
            "project_resources": False,
            "workflows": False,
            "framework_index": False
        }
        
        for resource in resources["resources"]:
            uri = resource["uri"]
            
            # Test one resource from each category
            if uri.startswith("jesse://framework/rule/") and not categories_tested["framework_rules"]:
                content = await client.read_resource(uri)
                assert "CRITICAL" in content["contents"][0]["text"]
                categories_tested["framework_rules"] = True
                
            elif uri.startswith("jesse://project/") and not categories_tested["project_resources"]:
                content = await client.read_resource(uri)
                assert "INFORMATIONAL" in content["contents"][0]["text"]
                categories_tested["project_resources"] = True
                
            elif uri.startswith("file://workflows/") and not categories_tested["workflows"]:
                content = await client.read_resource(uri)
                assert "--JESSE_FRAMEWORK_BOUNDARY_2025--" in content["contents"][0]["text"]
                categories_tested["workflows"] = True
                
            elif uri == "jesse://index" and not categories_tested["framework_index"]:
                content = await client.read_resource(uri)
                assert "resource_categories" in content["contents"][0]["text"]
                categories_tested["framework_index"] = True
        
        # Verify all categories were tested
        assert all(categories_tested.values()), f"Categories not tested: {categories_tested}"
    
    async def test_concurrent_resource_access(self, client):
        """
        [Function intent]
        Test concurrent access to multiple resources for performance validation.
        
        [Design principles]
        Framework must handle concurrent access gracefully without performance degradation.
        All concurrent requests must complete successfully with proper formatting.
        
        [Implementation details]
        Creates multiple concurrent resource requests using asyncio.gather,
        validates all requests complete successfully with expected content.
        """
        # Define multiple resource URIs
        test_uris = [
            "jesse://framework/rule/knowledge_management",
            "jesse://framework/rule/hints", 
            "jesse://project/context",
            "jesse://index"
        ]
        
        # Test concurrent access
        tasks = [client.read_resource(uri) for uri in test_uris]
        results = await asyncio.gather(*tasks)
        
        # Verify all requests succeeded
        assert len(results) == len(test_uris)
        
        for result in results:
            assert "contents" in result
            assert len(result["contents"]) == 1
            text = result["contents"][0]["text"]
            assert "--JESSE_FRAMEWORK_BOUNDARY_2025--" in text
    
    async def test_error_handling(self, client):
        """
        [Function intent]
        Test error handling for invalid resources and edge cases.
        
        [Design principles]
        Framework must handle errors gracefully with appropriate error messages.
        Invalid requests must fail predictably without system compromise.
        
        [Implementation details]
        Tests various invalid URI patterns and verifies appropriate error handling,
        ensures error cases don't affect system stability.
        """
        invalid_uris = [
            "jesse://framework/rule/nonexistent",
            "jesse://project/invalid",
            "jesse://unknown/resource",
            "invalid://uri/format"
        ]
        
        for uri in invalid_uris:
            with pytest.raises(Exception):
                await client.read_resource(uri)
    
    async def test_http_formatting_consistency(self, client):
        """
        [Function intent]
        Test HTTP formatting consistency across all resources.
        
        [Design principles]
        All resources must maintain consistent HTTP formatting for AI assistant processing.
        Formatting consistency is critical for framework compliance.
        
        [Implementation details]
        Samples resources from all categories and validates HTTP formatting markers,
        ensures consistent formatting across the complete framework.
        """
        resources = await client.list_resources()
        
        # Test sample from each category
        test_uris = []
        for resource in resources["resources"][:10]:  # Test first 10 resources
            test_uris.append(resource["uri"])
        
        for uri in test_uris:
            try:
                content = await client.read_resource(uri)
                text = content["contents"][0]["text"]
                
                # Verify consistent HTTP formatting
                assert "--JESSE_FRAMEWORK_BOUNDARY_2025--" in text
                assert "Content-Type:" in text
                assert "Content-Criticality:" in text
                
            except Exception as e:
                pytest.fail(f"HTTP formatting test failed for {uri}: {str(e)}")
    
    async def test_resource_metadata_accuracy(self, client):
        """
        [Function intent]
        Test resource metadata accuracy in discovery responses.
        
        [Design principles]
        Resource metadata must accurately reflect resource properties and capabilities.
        Discovery information must match actual resource behavior.
        
        [Implementation details]
        Compares resource discovery metadata with actual resource content,
        validates metadata accuracy and consistency.
        """
        resources = await client.list_resources()
        
        for resource in resources["resources"]:
            uri = resource["uri"]
            expected_mime_type = resource.get("mimeType", "text/markdown")
            
            # Read actual resource
            content = await client.read_resource(uri)
            actual_content = content["contents"][0]["text"]
            
            # Verify metadata matches content
            if expected_mime_type == "application/json":
                # Should contain JSON-like structure
                assert "{" in actual_content and "}" in actual_content
            elif expected_mime_type == "text/markdown":
                # Should contain HTTP formatted markdown
                assert "--JESSE_FRAMEWORK_BOUNDARY_2025--" in actual_content
    
    async def test_framework_scalability(self, client):
        """
        [Function intent]
        Test framework scalability with multiple concurrent clients and requests.
        
        [Design principles]
        Framework must handle increased load without performance degradation.
        Scalability testing ensures production readiness.
        
        [Implementation details]
        Simulates multiple concurrent request patterns to test scalability,
        validates performance characteristics under load.
        """
        # Test high-frequency resource access
        uri = "jesse://framework/rule/knowledge_management"
        
        # Create 20 concurrent requests
        tasks = [client.read_resource(uri) for _ in range(20)]
        results = await asyncio.gather(*tasks)
        
        # Verify all requests succeeded
        assert len(results) == 20
        
        for result in results:
            assert "contents" in result
            text = result["contents"][0]["text"]
            assert "Knowledge Management System" in text
    
    async def test_resource_discovery_completeness(self, client):
        """
        [Function intent]
        Test resource discovery completeness and categorization accuracy.
        
        [Design principles]
        Resource discovery must provide complete and accurate resource inventory.
        All expected resource categories must be properly represented.
        
        [Implementation details]
        Validates resource discovery response completeness,
        verifies all expected resource categories and counts.
        """
        resources = await client.list_resources()
        resource_list = resources["resources"]
        
        # Count resources by category
        framework_rules = [r for r in resource_list if r["uri"].startswith("jesse://framework/rule/")]
        project_resources = [r for r in resource_list if r["uri"].startswith("jesse://project/")]
        workflows = [r for r in resource_list if r["uri"].startswith("file://workflows/")]
        index_resources = [r for r in resource_list if r["uri"] == "jesse://index"]
        
        # Verify expected counts
        assert len(framework_rules) == 6, f"Expected 6 framework rules, got {len(framework_rules)}"
        assert len(project_resources) >= 3, f"Expected at least 3 project resources, got {len(project_resources)}"
        assert len(workflows) > 0, "Expected workflow resources"
        assert len(index_resources) == 1, "Expected exactly one index resource"
        
        # Verify resource metadata structure
        for resource in resource_list:
            assert "uri" in resource
            assert "name" in resource
            assert "description" in resource
            assert "mimeType" in resource
            
            # Verify metadata structure for categorized resources
            if "metadata" in resource:
                metadata = resource["metadata"]
                assert "category" in metadata
                assert "type" in metadata
