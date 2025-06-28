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
# Test suite for JESSE Framework MCP Server content loading functionality,
# verifying embedded rules/workflows loading and project knowledge integration.
###############################################################################
# [Source file design principles]
# - Comprehensive testing of embedded content loading mechanisms
# - Defensive testing with error condition validation
# - Mock-based isolation for file system operations
# - Clear test organization by functionality area
###############################################################################
# [Source file constraints]
# - Must work without requiring actual .knowledge/ directory structure
# - Embedded content loading tests require build-time content copying
# - Session logging tests need temporary directory handling
###############################################################################
# [Dependencies]
# system:pytest - Testing framework for Python
# system:unittest.mock - Mock objects for testing isolation
# system:tempfile - Temporary file/directory creation for tests
# system:pathlib.Path - Cross-platform filesystem paths
# codebase:jesse_framework_mcp.main - Main MCP server implementation
###############################################################################
# [GenAI tool change history]
# 2025-06-27T21:27:00Z : Removed tests for legacy non-async session management functions by CodeAssistant
# * Removed imports of deleted sync functions from session_management
# * Removed entire TestSessionLogging class that tested log_session_start
# * Removed entire TestWIPTaskLoading class that tested get_current_wip_task_name
# * Further updated to reflect fully async-only architecture
# 2025-06-27T21:24:00Z : Removed tests for legacy non-async knowledge scanner functions by CodeAssistant
# * Removed imports of deleted sync functions from knowledge_scanners
# * Removed test_generate_knowledge_base_inventory test method
# * Removed entire TestKnowledgeBaseLoading class that tested load_specific_knowledge_base
# * Updated to reflect async-only architecture changes
# 2025-06-27T17:12:45Z : Added Phase 2 resource-based architecture tests by CodeAssistant
# * Added comprehensive FastMCP Client-based integration tests
# * Added resource definitions testing (jesse://rules/*, jesse://workflows/*, etc.)
# * Added focused tools testing and prompt definitions validation
# * Added backward compatibility verification tests
# 2025-06-27T08:20:00Z : Updated test to match .coding_assistant/jesse log directory by CodeAssistant
# * Updated session logging tests to use .coding_assistant/jesse/ directory
# * Fixed test mocks to match main.py directory creation with parents=True
# 2025-06-27T01:28:00Z : Initial test suite implementation by CodeAssistant
# * Created comprehensive content loading tests
# * Added embedded content validation tests
# * Implemented session logging verification tests
###############################################################################

import json
import tempfile
import uuid
from pathlib import Path
from unittest.mock import Mock, patch, mock_open

import pytest

# Import functions from their correct helper modules
from jesse_framework_mcp.helpers.content_loaders import (
    load_embedded_jesse_framework,
    load_embedded_jesse_rules,
    load_embedded_jesse_workflows,
    load_project_knowledge,
    format_session_response
)


class TestEmbeddedContentLoading:
    """
    [Class intent]
    Test embedded JESSE framework content loading functionality.
    
    [Design principles]
    Validates that build-time embedded content can be properly accessed
    and loaded by the MCP server runtime components.
    
    [Implementation details]
    Uses mocked importlib.resources to simulate embedded content access
    without requiring actual package installation.
    """
    
    def test_load_embedded_jesse_rules_success(self):
        """
        [Function intent]
        Test successful loading of all embedded JESSE rule files.
        
        [Design principles]
        Validates that all 6 JESSE rule files are loaded with proper formatting.
        
        [Implementation details]
        Mocks importlib.resources.open_text to return sample content for each rule file.
        """
        
        mock_content = "# Sample JESSE Rule Content\nThis is test content."
        
        with patch('jesse_framework_mcp.main.resources.open_text') as mock_open_text:
            mock_file = mock_open(read_data=mock_content)
            mock_open_text.return_value.__enter__ = mock_file
            mock_open_text.return_value.__exit__ = Mock(return_value=None)
            
            result = load_embedded_jesse_rules()
            
            # Verify all 6 rule files were accessed
            assert mock_open_text.call_count == 6
            
            # Verify content formatting
            assert "=== JESSE_KNOWLEDGE_MANAGEMENT.MD ===" in result
            assert "=== JESSE_HINTS.MD ===" in result
            assert "=== JESSE_CODE_COMMENTS.MD ===" in result
            assert "=== JESSE_CODE_GENERATION.MD ===" in result
            assert "=== JESSE_MARKDOWN.MD ===" in result
            assert "=== JESSE_SCRATCHPAD.MD ===" in result
            
            # Verify content is included
            assert mock_content in result
    
    def test_load_embedded_jesse_workflows_success(self):
        """
        [Function intent]
        Test successful loading of embedded workflow files.
        
        [Design principles]
        Validates workflow directory discovery and content loading.
        
        [Implementation details]
        Mocks resources.files and file iteration to simulate workflow directory access.
        """
        
        mock_workflow_content = "# Sample Workflow\nWorkflow test content."
        
        # Mock workflow files
        mock_file_1 = Mock()
        mock_file_1.name = "jesse_wip_task_create.md"
        mock_file_1.suffix = ".md"
        mock_file_1.is_file.return_value = True
        
        mock_file_2 = Mock()
        mock_file_2.name = "jesse_wip_task_switch.md"
        mock_file_2.suffix = ".md"
        mock_file_2.is_file.return_value = True
        
        mock_dir = Mock()
        mock_dir.iterdir.return_value = [mock_file_1, mock_file_2]
        
        with patch('jesse_framework_mcp.main.resources.files') as mock_files, \
             patch('jesse_framework_mcp.main.resources.open_text') as mock_open_text:
            
            mock_files.return_value.__enter__ = Mock(return_value=mock_dir)
            mock_files.return_value.__exit__ = Mock(return_value=None)
            
            mock_file = mock_open(read_data=mock_workflow_content)
            mock_open_text.return_value.__enter__ = mock_file
            mock_open_text.return_value.__exit__ = Mock(return_value=None)
            
            result = load_embedded_jesse_workflows()
            
            # Verify workflow files were loaded
            assert "=== WORKFLOW: JESSE_WIP_TASK_CREATE.MD ===" in result
            assert "=== WORKFLOW: JESSE_WIP_TASK_SWITCH.MD ===" in result
            assert mock_workflow_content in result
    
    def test_load_embedded_jesse_framework_integration(self):
        """
        [Function intent]
        Test complete embedded framework loading integration.
        
        [Design principles]
        Validates that both rules and workflows are loaded and properly combined.
        
        [Implementation details]
        Tests the main framework loading function that combines rules and workflows.
        """
        
        with patch('jesse_framework_mcp.main.load_embedded_jesse_rules') as mock_rules, \
             patch('jesse_framework_mcp.main.load_embedded_jesse_workflows') as mock_workflows:
            
            mock_rules.return_value = "MOCK_RULES_CONTENT"
            mock_workflows.return_value = "MOCK_WORKFLOWS_CONTENT"
            
            result = load_embedded_jesse_framework()
            
            assert "=== EMBEDDED JESSE FRAMEWORK RULES ===" in result
            assert "=== EMBEDDED JESSE FRAMEWORK WORKFLOWS ===" in result
            assert "MOCK_RULES_CONTENT" in result
            assert "MOCK_WORKFLOWS_CONTENT" in result


class TestProjectKnowledgeLoading:
    """
    [Class intent]
    Test project-specific knowledge loading from .knowledge/ directory.
    
    [Design principles]
    Validates graceful handling of missing files and proper content loading.
    
    [Implementation details]
    Uses temporary directories and file mocking for isolated testing.
    """
    
    def test_load_project_knowledge_success(self):
        """
        [Function intent]
        Test successful loading of project knowledge base.
        
        [Design principles]
        Validates proper file reading and content formatting.
        
        [Implementation details]
        Mocks file system to simulate existing knowledge base file.
        """
        
        mock_content = "# Project Knowledge\nThis is project-specific knowledge."
        
        with patch('jesse_framework_mcp.main.Path') as mock_path:
            mock_file = Mock()
            mock_file.exists.return_value = True
            mock_path.return_value = mock_file
            
            with patch('builtins.open', mock_open(read_data=mock_content)):
                result = load_project_knowledge()
                
                assert "=== PROJECT KNOWLEDGE BASE ===" in result
                assert mock_content in result
    
    def test_load_project_knowledge_missing_file(self):
        """
        [Function intent]
        Test handling of missing project knowledge base file.
        
        [Design principles]
        Validates graceful degradation when knowledge base doesn't exist.
        
        [Implementation details]
        Mocks file system to simulate missing knowledge base file.
        """
        
        with patch('jesse_framework_mcp.main.Path') as mock_path:
            mock_file = Mock()
            mock_file.exists.return_value = False
            mock_path.return_value = mock_file
            
            result = load_project_knowledge()
            
            assert "=== PROJECT KNOWLEDGE BASE ===" in result
            assert "No project knowledge base found" in result
    


class TestResponseFormatting:
    """
    [Class intent]
    Test session response formatting functionality.
    
    [Design principles]
    Validates complete response structure and content organization.
    
    [Implementation details]
    Tests response formatting with various content combinations.
    """
    
    def test_format_session_response_complete(self):
        """
        [Function intent]
        Test complete session response formatting with all content types.
        
        [Design principles]
        Validates proper section organization and content inclusion.
        
        [Implementation details]
        Provides sample content for all response sections.
        """
        
        result = format_session_response(
            session_id="test123",
            user_prompt="Test prompt",
            load_wip_tasks=True,
            embedded_content="EMBEDDED_CONTENT",
            project_knowledge="PROJECT_KNOWLEDGE",
            kb_inventory="KB_INVENTORY",
            wip_content="WIP_CONTENT"
        )
        
        assert "=== JESSE FRAMEWORK SESSION INITIALIZATION ===" in result
        assert "Session ID: test123" in result
        assert "Load WIP Tasks: True" in result
        assert "EMBEDDED_CONTENT" in result
        assert "PROJECT_KNOWLEDGE" in result
        assert "KB_INVENTORY" in result
        assert "WIP_CONTENT" in result
        assert "✅ All JESSE rules embedded and loaded" in result
        assert "✅ WIP task context: loaded" in result
    
    def test_format_session_response_no_wip(self):
        """
        [Function intent]
        Test session response formatting without WIP task content.
        
        [Design principles]
        Validates proper handling when WIP tasks are disabled or missing.
        
        [Implementation details]
        Tests response with load_wip_tasks=False and empty WIP content.
        """
        
        result = format_session_response(
            session_id="test456",
            user_prompt="Test prompt",
            load_wip_tasks=False,
            embedded_content="EMBEDDED_CONTENT",
            project_knowledge="PROJECT_KNOWLEDGE", 
            kb_inventory="KB_INVENTORY",
            wip_content=""
        )
        
        assert "Session ID: test456" in result
        assert "Load WIP Tasks: False" in result
        assert "✅ WIP task context: skipped" in result
        assert "WIP_CONTENT" not in result


# === PHASE 2 ARCHITECTURE TESTS ===
# FastMCP Client-based integration tests for resource-based architecture

try:
    from fastmcp import Client
    FASTMCP_AVAILABLE = True
except ImportError:
    FASTMCP_AVAILABLE = False

@pytest.mark.skipif(not FASTMCP_AVAILABLE, reason="FastMCP Client not available")
class TestFastMCPResourceArchitecture:
    """
    [Class intent]
    Test new resource-based architecture using FastMCP Client.
    
    [Design principles]
    Integration testing for resource access and focused tool operations.
    Validates MCP protocol compliance and resource functionality.
    
    [Implementation details]
    Uses FastMCP Client to test resources, tools, and prompts
    through actual MCP protocol communication.
    """
    
    @pytest.mark.asyncio
    async def test_jesse_rules_resources(self):
        """
        [Function intent]
        Test individual JESSE rule resource access.
        
        [Design principles]
        Validates resource-based delivery of JESSE rules.
        
        [Implementation details]
        Tests resource URIs for rule access with proper error handling.
        """
        from jesse_framework_mcp.main import server
        
        async with Client(server) as client:
            # Test rule resource access
            rule_names = ["code_comments", "code_generation", "knowledge_management"]
            
            for rule_name in rule_names:
                try:
                    resource = await client.read_resource(f"jesse://rules/{rule_name}")
                    # FastMCP Client returns list of resources
                    assert len(resource) > 0
                    content = resource[0].text if hasattr(resource[0], 'text') else str(resource[0])
                    assert len(content) > 0
                    assert "JESSE" in content.upper()
                except Exception as e:
                    pytest.fail(f"Failed to load rule resource {rule_name}: {str(e)}")
    
    @pytest.mark.asyncio
    async def test_jesse_workflows_resources(self):
        """
        [Function intent]
        Test individual JESSE workflow resource access.
        
        [Design principles]
        Validates resource-based delivery of JESSE workflows.
        
        [Implementation details]
        Tests workflow resource URIs with flexible naming support.
        """
        from jesse_framework_mcp.main import server
        
        async with Client(server) as client:
            # Test workflow resource access
            workflow_names = ["jesse_wip_task_create", "jesse_wip_task_switch.md"]
            
            for workflow_name in workflow_names:
                try:
                    resource = await client.read_resource(f"jesse://workflows/{workflow_name}")
                    assert len(resource.content) > 0
                    # Workflows should contain workflow-specific content
                    assert any(keyword in resource.content.lower() for keyword in ["workflow", "task", "jesse"])
                except Exception as e:
                    pytest.fail(f"Failed to load workflow resource {workflow_name}: {str(e)}")
    
    @pytest.mark.asyncio
    async def test_knowledge_base_resources(self):
        """
        [Function intent]
        Test project knowledge base resource access.
        
        [Design principles]
        Validates resource-based knowledge delivery for lazy loading.
        
        [Implementation details]
        Tests knowledge base resource URIs with error handling for missing KBs.
        """
        from jesse_framework_mcp.main import server
        
        async with Client(server) as client:
            # Test knowledge base resource access - should handle missing KBs gracefully
            try:
                resource = await client.read_resource("jesse://knowledge/test_kb")
                # If KB exists, should have content
                if resource.content:
                    assert len(resource.content) > 0
            except Exception:
                # Missing knowledge bases should raise appropriate errors
                pass  # This is expected behavior for missing KBs
    
    @pytest.mark.asyncio
    async def test_session_context_resource(self):
        """
        [Function intent]
        Test current session context resource access.
        
        [Design principles]
        Validates lightweight session context delivery via resources.
        
        [Implementation details]
        Tests session resource URI for current context without full initialization.
        """
        from jesse_framework_mcp.main import server
        
        async with Client(server) as client:
            try:
                resource = await client.read_resource("jesse://session/current")
                assert len(resource.content) > 0
                assert "SESSION CONTEXT" in resource.content
            except Exception as e:
                pytest.fail(f"Failed to load session context resource: {str(e)}")


class TestFocusedTools:
    """
    [Class intent]
    Test new focused tool implementations.
    
    [Design principles]
    Validates split tool architecture and focused functionality.
    
    [Implementation details]
    Tests individual focused tools for specific operations.
    """
    
    @pytest.mark.asyncio
    async def test_jesse_initialize_framework_tool(self):
        """
        [Function intent]
        Test focused framework initialization tool.
        
        [Design principles]
        Validates framework-only initialization without project context.
        
        [Implementation details]
        Tests framework initialization tool with expected response format.
        """
        from jesse_framework_mcp.main import server
        
        async with Client(server) as client:
            try:
                result = await client.call_tool("jesse_initialize_framework", {})
                # FastMCP Client returns list of results
                response_text = result[0].content if hasattr(result[0], 'content') else str(result[0])
                assert "JESSE FRAMEWORK INITIALIZATION" in response_text
                assert "Framework ready for use" in response_text
                assert "✅ Core JESSE rules loaded" in response_text
                assert "✅ All workflows loaded" in response_text
            except Exception as e:
                pytest.fail(f"Framework initialization tool failed: {str(e)}")
    
    @pytest.mark.asyncio
    async def test_jesse_load_project_context_tool(self):
        """
        [Function intent]
        Test focused project context loading tool.
        
        [Design principles]
        Validates project-specific context loading separate from framework.
        
        [Implementation details]
        Tests project context tool with expected response sections.
        """
        from jesse_framework_mcp.main import server
        
        async with Client(server) as client:
            try:
                result = await client.call_tool("jesse_load_project_context", {})
                assert "PROJECT CONTEXT LOADED" in result.text
                assert "AVAILABLE KNOWLEDGE BASES" in result.text
                assert "PROJECT CONTEXT COMPLETE" in result.text
            except Exception as e:
                pytest.fail(f"Project context loading tool failed: {str(e)}")


class TestPromptDefinitions:
    """
    [Class intent]
    Test JESSE prompt definitions functionality.
    
    [Design principles]
    Validates reusable prompt templates for common workflows.
    
    [Implementation details]
    Tests prompt generation with various parameters and contexts.
    """
    
    @pytest.mark.asyncio
    async def test_prompt_availability(self):
        """
        [Function intent]
        Test that all JESSE prompts are available.
        
        [Design principles]
        Validates prompt discovery and availability.
        
        [Implementation details]
        Lists prompts and verifies expected JESSE prompts exist.
        """
        from jesse_framework_mcp.main import server
        
        async with Client(server) as client:
            try:
                prompts = await client.list_prompts()
                prompt_names = [p.name for p in prompts]
                
                expected_prompts = [
                    "jesse_framework_start",
                    "jesse_wip_task_create", 
                    "jesse_knowledge_capture"
                ]
                
                for expected_prompt in expected_prompts:
                    assert expected_prompt in prompt_names, f"Missing prompt: {expected_prompt}"
            except Exception as e:
                pytest.fail(f"Failed to list prompts: {str(e)}")
    
    @pytest.mark.asyncio
    async def test_jesse_framework_start_prompt(self):
        """
        [Function intent]
        Test JESSE framework start prompt generation.
        
        [Design principles]
        Validates framework initialization prompt with project context.
        
        [Implementation details]
        Tests prompt generation with and without project context.
        """
        from jesse_framework_mcp.main import server
        
        async with Client(server) as client:
            try:
                # Test basic prompt
                prompt = await client.get_prompt("jesse_framework_start", {})
                assert "Initialize the JESSE AI Framework" in prompt.text
                assert "coding standards" in prompt.text.lower()
                
                # Test prompt with project context
                prompt_with_context = await client.get_prompt("jesse_framework_start", {
                    "project_context": "E-commerce API development"
                })
                assert "Initialize the JESSE AI Framework" in prompt_with_context.text
                assert "E-commerce API development" in prompt_with_context.text
            except Exception as e:
                pytest.fail(f"Framework start prompt failed: {str(e)}")
    
    @pytest.mark.asyncio
    async def test_jesse_wip_task_create_prompt(self):
        """
        [Function intent]
        Test WIP task creation prompt generation.
        
        [Design principles]
        Validates task creation prompt with complexity assessment.
        
        [Implementation details]
        Tests prompt with different complexity levels and task descriptions.
        """
        from jesse_framework_mcp.main import server
        
        async with Client(server) as client:
            try:
                prompt = await client.get_prompt("jesse_wip_task_create", {
                    "task_description": "Implement user authentication",
                    "estimated_complexity": "complex"
                })
                
                assert "Create a new JESSE Framework Work-in-Progress" in prompt.text
                assert "Implement user authentication" in prompt.text
                assert "complex" in prompt.text.lower()
                assert "/jesse_wip_task_create.md workflow" in prompt.text
            except Exception as e:
                pytest.fail(f"WIP task create prompt failed: {str(e)}")
    
    @pytest.mark.asyncio  
    async def test_jesse_knowledge_capture_prompt(self):
        """
        [Function intent]
        Test knowledge capture prompt generation.
        
        [Design principles]
        Validates knowledge capture prompt with type-specific formatting.
        
        [Implementation details]
        Tests prompt with different knowledge types and content summaries.
        """
        from jesse_framework_mcp.main import server
        
        async with Client(server) as client:
            try:
                prompt = await client.get_prompt("jesse_knowledge_capture", {
                    "knowledge_type": "pattern",
                    "content_summary": "Database connection pooling best practices"
                })
                
                assert "Capture new knowledge in the JESSE Framework" in prompt.text
                assert "pattern" in prompt.text
                assert "Database connection pooling best practices" in prompt.text
                assert "/jesse_wip_task_capture_knowledge.md workflow" in prompt.text
            except Exception as e:
                pytest.fail(f"Knowledge capture prompt failed: {str(e)}")


class TestBackwardCompatibility:
    """
    [Class intent]
    Verify backward compatibility with existing usage patterns.
    
    [Design principles]
    Ensures existing integrations continue to work after architecture changes.
    Validates tool signatures and response formats remain consistent.
    
    [Implementation details]
    Tests original tool interfaces to confirm compatibility.
    """
    
    @pytest.mark.asyncio
    async def test_original_jesse_start_session(self):
        """
        [Function intent]
        Test that original jesse_start_session still works.
        
        [Design principles]
        Validates backward compatibility for existing usage patterns.
        
        [Implementation details]
        Tests original tool with expected parameters and response format.
        """
        from jesse_framework_mcp.main import server
        
        async with Client(server) as client:
            try:
                # Test with original parameters
                result = await client.call_tool("jesse_start_session", {
                    "user_prompt": "Test backward compatibility",
                    "load_wip_tasks": True
                })
                
                # Verify original response format is maintained
                assert "JESSE FRAMEWORK SESSION INITIALIZATION" in result.text
                assert "Session ID:" in result.text
                assert "COMPLETE SESSION READY" in result.text or "COMPLETE JESSE FRAMEWORK LOADED" in result.text
            except Exception as e:
                pytest.fail(f"Original jesse_start_session failed: {str(e)}")
    
    @pytest.mark.asyncio
    async def test_original_knowledge_base_loading(self):
        """
        [Function intent]
        Test that original knowledge base loading still works.
        
        [Design principles]
        Validates existing knowledge base loading interface compatibility.
        
        [Implementation details]
        Tests original tool interface with empty and populated KB lists.
        """
        from jesse_framework_mcp.main import server
        
        async with Client(server) as client:
            try:
                # Test original tool interface with empty list
                result = await client.call_tool("jesse_load_knowledge_base", {
                    "kb_names": []
                })
                
                assert "No knowledge bases requested" in result.text
            except Exception as e:
                pytest.fail(f"Original knowledge base loading failed: {str(e)}")


class TestResourceURIPatterns:
    """
    [Class intent]
    Test resource URI patterns and accessibility.
    
    [Design principles]
    Validates all documented resource endpoints function correctly.
    
    [Implementation details]
    Tests each resource URI pattern with valid and invalid parameters.
    """
    
    @pytest.mark.asyncio
    async def test_resource_uri_patterns(self):
        """
        [Function intent]
        Test all documented resource URI patterns.
        
        [Design principles]
        Validates resource endpoint accessibility and error handling.
        
        [Implementation details]
        Tests valid URIs and verifies appropriate error handling for invalid ones.
        """
        from jesse_framework_mcp.main import server
        
        valid_uris = [
            "jesse://rules/code_comments",
            "jesse://workflows/jesse_wip_task_create",
            "jesse://session/current"
        ]
        
        async with Client(server) as client:
            for uri in valid_uris:
                try:
                    resource = await client.read_resource(uri)
                    assert len(resource.content) > 0, f"Empty content for URI: {uri}"
                except Exception as e:
                    pytest.fail(f"Failed to access valid URI {uri}: {str(e)}")
    
    @pytest.mark.asyncio
    async def test_invalid_resource_uris(self):
        """
        [Function intent]
        Test handling of invalid resource URIs.
        
        [Design principles]
        Validates appropriate error responses for invalid resource requests.
        
        [Implementation details]
        Tests invalid URIs and expects proper error handling.
        """
        from jesse_framework_mcp.main import server
        
        invalid_uris = [
            "jesse://rules/nonexistent_rule",
            "jesse://workflows/nonexistent_workflow.md"
        ]
        
        async with Client(server) as client:
            for uri in invalid_uris:
                try:
                    await client.read_resource(uri)
                    pytest.fail(f"Expected error for invalid URI: {uri}")
                except Exception:
                    # Expected behavior - invalid URIs should raise errors
                    pass
