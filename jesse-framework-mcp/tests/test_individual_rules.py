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
# Individual JESSE rule testing with FastMCP in-memory patterns.
# Comprehensive testing of each individual JESSE framework rule resource.
###############################################################################
# [Source file design principles]
# - Parametrized testing ensures consistent behavior across all rules
# - HTTP formatting verification maintained for all individual rules
# - Embedded content loading verification for each rule
# - Rule-specific content validation with consistent patterns
###############################################################################
# [Source file constraints]
# - Must use FastMCP InMemoryTransport for realistic testing
# - All JESSE framework rules must be tested individually
# - HTTP formatting consistency must be verified across all rules
# - Rule name conversion and description mapping must be validated
###############################################################################
# [Dependencies]
# system:pytest - Modern testing framework with parametrization support
# system:fastmcp.testing.InMemoryTransport - FastMCP in-memory testing transport
# codebase:jesse_framework_mcp.main.server - Main FastMCP server instance
# codebase:jesse_framework_mcp.resources.framework_rules - Rule helper functions
###############################################################################
# [GenAI tool change history]
# 2025-06-28T07:10:15Z : Initial individual rule testing implementation by CodeAssistant
# * Created parametrized testing for all JESSE framework rules
# * Implemented HTTP formatting verification for each rule individually
# * Added rule description mapping validation and name conversion testing
# * Established consistent rule content validation patterns
###############################################################################

import pytest
from fastmcp.testing import InMemoryTransport
from jesse_framework_mcp.main import server

class TestIndividualRules:
    """
    [Function intent]
    Comprehensive testing of each individual JESSE framework rule resource.
    
    [Design principles]
    Parametrized testing ensures consistent behavior across all rules.
    Verify HTTP formatting, content criticality, and rule-specific content.
    
    [Implementation details]
    Tests each JESSE rule individually with consistent validation patterns.
    Verifies embedded content loading and HTTP formatting preservation.
    """
    
    @pytest.fixture
    async def client(self):
        """
        [Function intent]
        FastMCP in-memory client fixture for individual rule testing.
        
        [Design principles]
        Provides clean test isolation for rule-specific testing.
        Uses FastMCP InMemoryTransport for realistic MCP protocol testing.
        
        [Implementation details]
        Creates InMemoryTransport connection to server instance,
        yields client for test usage, automatically handles cleanup.
        """
        async with InMemoryTransport(server) as client:
            yield client
    
    @pytest.mark.parametrize("rule_name,expected_content", [
        ("knowledge_management", "Knowledge Management System"),
        ("hints", "AI Assistant Enforcement"),
        ("code_comments", "Code Documentation Standards"),
        ("code_generation", "Code Generation Standards"),
        ("markdown", "Markdown File Management"),
        ("scratchpad", "Scratchpad Directory Management")
    ])
    async def test_individual_rule_resource(self, client, rule_name, expected_content):
        """
        [Function intent]
        Test each JESSE rule resource individually with parametrized validation.
        
        [Design principles]
        Parametrized testing ensures all rules follow consistent patterns.
        Each rule must have CRITICAL criticality and proper HTTP formatting.
        
        [Implementation details]
        Tests individual rule URI access, verifies HTTP formatting,
        validates rule-specific content and portable path resolution.
        
        Args:
            client: FastMCP in-memory client fixture
            rule_name: Rule name for URI construction
            expected_content: Expected content snippet for validation
        """
        uri = f"jesse://framework/rule/{rule_name}"
        content = await client.read_resource(uri)
        text = content["contents"][0]["text"]
        
        # Verify HTTP formatting preserved
        assert "--JESSE_FRAMEWORK_BOUNDARY_2025--" in text
        assert "Content-Criticality: CRITICAL" in text
        assert "Content-Type: text/markdown" in text
        
        # Verify rule-specific content
        assert expected_content in text
        
        # Verify portable path resolution
        assert "{CLINE_RULES}" in text
    
    async def test_rule_descriptions(self, client):
        """
        [Function intent]
        Test rule description mapping for all JESSE framework rules.
        
        [Design principles]
        Rule descriptions must be accurate and human-readable.
        Consistent description format across all rules.
        
        [Implementation details]
        Validates description mapping function against expected descriptions,
        ensures all rule names have appropriate descriptions.
        """
        from jesse_framework_mcp.resources.framework_rules import get_rule_description
        
        expected_descriptions = {
            'knowledge_management': 'Knowledge Management System Rules and Directives',
            'hints': 'AI Assistant Enforcement Rules and Directives',
            'code_comments': 'Code Documentation Standards and Requirements',
            'code_generation': 'Code Generation Standards and Best Practices',
            'markdown': 'Markdown File Management Standards',
            'scratchpad': 'Scratchpad Directory Management Standards'
        }
        
        for rule_name, expected_desc in expected_descriptions.items():
            actual_desc = get_rule_description(rule_name)
            assert actual_desc == expected_desc, f"Description mismatch for {rule_name}"
    
    async def test_rule_name_conversion(self, client):
        """
        [Function intent]
        Test rule name conversion from JESSE file names to resource names.
        
        [Design principles]
        Rule name conversion must be consistent and predictable.
        All expected rules must be available through name conversion.
        
        [Implementation details]
        Validates get_available_rule_names function returns all expected rules,
        ensures file name to resource name conversion works correctly.
        """
        from jesse_framework_mcp.resources.framework_rules import get_available_rule_names
        
        rule_names = await get_available_rule_names()
        expected_rules = [
            "knowledge_management", "hints", "code_comments",
            "code_generation", "markdown", "scratchpad"
        ]
        
        for expected_rule in expected_rules:
            assert expected_rule in rule_names, f"Expected rule {expected_rule} not found in {rule_names}"
        
        # Verify rule count matches expectation
        assert len(rule_names) == len(expected_rules), f"Rule count mismatch: expected {len(expected_rules)}, got {len(rule_names)}"
    
    async def test_rule_routing_function(self, client):
        """
        [Function intent]
        Test rule routing function for individual rule access.
        
        [Design principles]
        Rule routing must correctly map rule names to handler functions.
        Error handling for unknown rules must be appropriate.
        
        [Implementation details]
        Tests get_rule_by_name function with valid and invalid rule names,
        verifies proper routing and error handling behavior.
        """
        from jesse_framework_mcp.resources.framework_rules import get_rule_by_name
        from fastmcp.testing import MockContext
        
        # Test valid rule routing
        valid_rules = ["knowledge_management", "hints", "code_comments"]
        
        for rule_name in valid_rules:
            ctx = MockContext()
            content = await get_rule_by_name(rule_name, ctx)
            
            # Verify content returned
            assert isinstance(content, str)
            assert len(content) > 0
            assert "--JESSE_FRAMEWORK_BOUNDARY_2025--" in content
        
        # Test invalid rule handling
        ctx = MockContext()
        with pytest.raises(ValueError, match="Unknown JESSE rule"):
            await get_rule_by_name("nonexistent_rule", ctx)
    
    @pytest.mark.parametrize("rule_name", [
        "knowledge_management", "hints", "code_comments",
        "code_generation", "markdown", "scratchpad"
    ])
    async def test_individual_rule_content_completeness(self, client, rule_name):
        """
        [Function intent]
        Test content completeness for each individual JESSE rule.
        
        [Design principles]
        Each rule must contain sufficient content for framework compliance.
        Content structure must follow JESSE documentation standards.
        
        [Implementation details]
        Validates each rule has minimum content requirements,
        verifies structural elements and framework-specific markers.
        
        Args:
            client: FastMCP in-memory client fixture
            rule_name: Rule name for individual testing
        """
        uri = f"jesse://framework/rule/{rule_name}"
        content = await client.read_resource(uri)
        text = content["contents"][0]["text"]
        
        # Verify minimum content length (rules should be comprehensive)
        assert len(text) > 1000, f"Rule {rule_name} content too short: {len(text)} characters"
        
        # Verify essential JESSE framework markers
        assert "JESSE" in text.upper()
        assert "CRITICAL" in text  # All framework rules are critical
        
        # Verify content structure markers
        expected_markers = [
            "Content-Type:",
            "Content-Criticality:",
            "Content-Description:",
            "Content-Location:"
        ]
        
        for marker in expected_markers:
            assert marker in text, f"Missing marker '{marker}' in rule {rule_name}"
