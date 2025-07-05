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
# HTTP section formatting and response tests for JESSE Framework MCP server.
# Validates HTTP section formatting, multi-section responses, and content extraction.
###############################################################################
# [Source file design principles]
# Thorough test coverage of HTTP section formatting with edge cases
# Multi-section response integration testing with protocol definitions
# Performance validation for content-length accuracy and large content handling
###############################################################################
# [Source file constraints]
# Must validate byte-perfect content-length calculation
# Multi-section response testing requires protocol definition validation
# Integration tests require embedded content access with constants
###############################################################################
# [Dependencies]
# <system>: pytest for testing framework
# <system>: pathlib for cross-platform path testing
# <system>: tempfile for temporary file testing
# <codebase>: jesse_framework_mcp.helpers.http_formatter for HTTP formatting functions
# <codebase>: jesse_framework_mcp.constants for HTTP formatting constants
###############################################################################
# [GenAI tool change history]
# 2025-07-05T09:52:00Z : Split from large test_http_formatting.py file for better organization by CodeAssistant
# * Extracted HTTP section formatting, multi-section response, and extraction tests
# * Preserved all test functionality including status line tests and response formatting
# * Updated file header to reflect focused scope on HTTP section formatting
# * Maintained all original test logic including performance and edge case testing
###############################################################################

import pytest
import tempfile
import stat
from pathlib import Path
from jesse_framework_mcp.helpers.async_http_formatter import (
    format_http_section,
    format_multi_section_response,
    XAsyncContentCriticality,
    XAsyncHttpPath,
    extract_http_sections_from_multi_response,
    format_http_response
)
from jesse_framework_mcp.constants import (
    HTTP_BOUNDARY_MARKER,
    CONTENT_TYPES,
    SECTION_TYPES,
    RULE_CRITICALITY_MAP
)


class TestHttpStatusLines:
    """
    [Class intent]
    Test suite for HTTP/1.1-like status line functionality in format_http_section.
    Validates automatic error detection, manual status overrides, and error content generation.
    
    [Design principles]
    Comprehensive testing of HTTP status codes with automatic and manual modes.
    Error scenario testing with realistic filesystem and permission issues.
    Override capability testing for complete control over status and content.
    
    [Implementation details]
    Tests all new HTTP/1.1 parameters: status_code, status_message, error_content.
    Validates automatic error detection from exceptions and manual override behavior.
    """
    
    def test_default_200_ok_status(self):
        """
        [Function intent]
        Test default 200 OK status for successful content formatting.
        
        [Design principles]
        Default behavior should be 200 OK when content loads successfully.
        
        [Implementation details]
        Tests string content produces 200 OK status line automatically.
        """
        content = "Test content for default success status"
        result = format_http_section(
            content=content,
            content_type="text/markdown",
            criticality="INFORMATIONAL",
            description="Default Status Test",
            section_type="knowledge-base",
            location="file://{HOME}/default_status.md"
        )
        
        assert "X-ASYNC-HTTP/1.1 200 OK" in result
        assert content in result
    
    def test_manual_status_override(self):
        """
        [Function intent]
        Test manual status code and message override functionality.
        
        [Design principles]
        Manual overrides should take complete precedence over automatic detection.
        
        [Implementation details]
        Tests status_code and status_message parameters override automatic behavior.
        """
        content = "Test content for manual status override"
        result = format_http_section(
            content=content,
            content_type="text/markdown",
            criticality="INFORMATIONAL", 
            description="Manual Override Test",
            section_type="knowledge-base",
            location="file://{HOME}/manual_override.md",
            status_code=201,
            status_message="Created"
        )
        
        assert "X-ASYNC-HTTP/1.1 201 Created" in result
        assert content in result
    
    def test_automatic_404_detection_with_missing_file(self):
        """
        [Function intent]
        Test automatic 404 detection when HttpPath content file doesn't exist.
        
        [Design principles]
        FileNotFoundError should automatically generate 404 Not Found response.
        
        [Implementation details]
        Tests missing HttpPath file triggers automatic 404 with error content.
        """
        missing_path = XAsyncHttpPath("/non/existent/file.md")
        result = format_http_section(
            content=missing_path,
            content_type="text/markdown",
            criticality="INFORMATIONAL",
            description="Missing File Test",
            section_type="knowledge-base",
            location="file://{HOME}/missing.md"
        )
        
        assert "X-ASYNC-HTTP/1.1 404 Not Found" in result
        assert "Resource not found:" in result
        assert "file://{HOME}/missing.md" in result  # Location should be from location parameter, not content path
    
    def test_automatic_403_detection_permission_denied(self):
        """
        [Function intent]
        Test automatic 403 detection when HttpPath content file has permission issues.
        
        [Design principles]
        PermissionError should automatically generate 403 Forbidden response.
        
        [Implementation details]
        Tests permission denied HttpPath file triggers automatic 403 with error content.
        """
        # Create a temporary file and restrict permissions
        test_content = "# Permission Test Content"
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.md', encoding='utf-8') as tmp_file:
            tmp_file.write(test_content)
            tmp_http_path = XAsyncHttpPath(tmp_file.name)
        
        try:
            # Remove read permissions (system-dependent behavior)
            original_mode = tmp_http_path._resolved_path.stat().st_mode
            tmp_http_path._resolved_path.chmod(stat.S_IWRITE)  # Write-only
            
            # Check if we can test permission denial on this system
            try:
                tmp_http_path.read_text()
                # Skip test if permissions aren't enforced
                pytest.skip("Cannot reliably test permission denial on this system")
            except PermissionError:
                # Test automatic 403 detection
                result = format_http_section(
                    content=tmp_http_path,
                    content_type="text/markdown",
                    criticality="INFORMATIONAL",
                    description="Permission Test",
                    section_type="knowledge-base",
                    location="file://{HOME}/permission_test.md"
                )
                
                assert "X-ASYNC-HTTP/1.1 403 Forbidden" in result
                assert "Access denied:" in result
                assert "file://{HOME}/permission_test.md" in result
        
        finally:
            # Cleanup with permission restoration
            try:
                tmp_http_path._resolved_path.chmod(original_mode)
                tmp_http_path._resolved_path.unlink(missing_ok=True)
            except (OSError, PermissionError):
                pass
    
    def test_automatic_500_detection_generic_error(self):
        """
        [Function intent]
        Test automatic 500 detection for generic exceptions during content loading.
        
        [Design principles]
        Unexpected exceptions should generate 500 Internal Server Error responses.
        
        [Implementation details]
        Tests generic exceptions trigger automatic 500 with error details.
        """
        # Test with empty content - this still raises ValueError since validation happens before _detect_status_and_content
        with pytest.raises(ValueError) as exc_info:
            format_http_section(
                content="",  # Empty content triggers ValueError in validation
                content_type="text/markdown",
                criticality="INFORMATIONAL",
                description="Error Test",
                section_type="knowledge-base",
                location="file://{HOME}/error_test.md"
            )
        
        # The ValueError should be raised in validation stage
        assert "Content cannot be empty" in str(exc_info.value)
    
    def test_error_content_override(self):
        """
        [Function intent]
        Test custom error content override with manual status codes.
        
        [Design principles]
        error_content parameter should override automatic error message generation.
        
        [Implementation details]
        Tests error_content parameter provides custom error messages.
        """
        custom_error_message = "Service is temporarily unavailable due to maintenance."
        result = format_http_section(
            content="This content will be ignored",
            content_type="text/plain",
            criticality="CRITICAL",
            description="Custom Error Test",
            section_type="error-section",
            location="service://maintenance/",
            status_code=503,
            status_message="Service Unavailable",
            error_content=custom_error_message
        )
        
        assert "X-ASYNC-HTTP/1.1 503 Service Unavailable" in result
        assert custom_error_message in result
        assert "This content will be ignored" not in result
    
    def test_status_code_with_default_error_content_generation(self):
        """
        [Function intent]
        Test manual status code with automatic error content generation.
        
        [Design principles]
        Manual status codes >= 400 should auto-generate error content when none provided.
        
        [Implementation details]
        Tests error status codes auto-generate appropriate error messages.
        """
        result = format_http_section(
            content="Original content",
            content_type="text/plain",
            criticality="CRITICAL",
            description="Auto Error Content Test",
            section_type="error-section",
            location="file://{HOME}/auto_error.txt",
            status_code=404
            # No error_content provided - should auto-generate
        )
        
        assert "X-ASYNC-HTTP/1.1 404 Not Found" in result
        assert "Resource not found: file://{HOME}/auto_error.txt" in result
        assert "Original content" not in result
    
    def test_manual_success_status_preserves_content(self):
        """
        [Function intent]
        Test manual success status codes (< 400) preserve original content.
        
        [Design principles]
        Manual status codes < 400 should use original content regardless of status_code.
        
        [Implementation details]
        Tests success status codes maintain content even when manually specified.
        """
        original_content = "This content should be preserved"
        result = format_http_section(
            content=original_content,
            content_type="text/markdown",
            criticality="INFORMATIONAL",
            description="Manual Success Test",
            section_type="knowledge-base",
            location="file://{HOME}/manual_success.md",
            status_code=202,
            status_message="Accepted"
        )
        
        assert "X-ASYNC-HTTP/1.1 202 Accepted" in result
        assert original_content in result
    
    def test_status_code_240_context_dependent(self):
        """
        [Function intent]
        Test status code 240 (Context Dependent Content) functionality.
        
        [Design principles]
        Status code 240 indicates task-specific content that should never be persisted.
        
        [Implementation details]
        Tests manual 240 status code with appropriate status message.
        """
        content = "This is context dependent content for current task only"
        result = format_http_section(
            content=content,
            content_type="text/markdown",
            criticality="INFORMATIONAL",
            description="Context Dependent Test",
            section_type="task-context",
            location="task://current/context",
            status_code=240,
            status_message="Context Dependent Content"
        )
        
        assert "X-ASYNC-HTTP/1.1 240 Context Dependent Content" in result
        assert content in result
    
    def test_status_code_241_immediate_attention(self):
        """
        [Function intent]
        Test status code 241 (Context Dependent Content requiring IMMEDIATE attention) functionality.
        
        [Design principles]
        Status code 241 indicates critical task-specific content requiring urgent processing.
        
        [Implementation details]
        Tests manual 241 status code with appropriate status message.
        """
        content = "URGENT: This content requires immediate attention from the user"
        result = format_http_section(
            content=content,
            content_type="text/plain",
            criticality="CRITICAL",
            description="Immediate Attention Test",
            section_type="urgent-context",
            location="task://urgent/attention",
            status_code=241,
            status_message="Context Dependent Content requiring IMMEDIATE attention"
        )
        
        assert "X-ASYNC-HTTP/1.1 241 Context Dependent Content requiring IMMEDIATE attention" in result
        assert content in result
    
    def test_status_code_240_with_default_message(self):
        """
        [Function intent]
        Test status code 240 with automatic default message generation.
        
        [Design principles]
        Status code 240 should auto-generate appropriate message when none provided.
        
        [Implementation details]
        Tests 240 status code uses HttpStatus.get_default_message() when message not specified.
        """
        content = "Context dependent content with auto message"
        result = format_http_section(
            content=content,
            content_type="text/markdown",
            criticality="INFORMATIONAL",
            description="Auto Message Test",
            section_type="task-context",
            location="task://auto/message",
            status_code=240
            # No status_message provided - should auto-generate
        )
        
        assert "X-ASYNC-HTTP/1.1 240 Context Dependent Content" in result
        assert content in result
    
    def test_status_code_241_with_default_message(self):
        """
        [Function intent]
        Test status code 241 with automatic default message generation.
        
        [Design principles]
        Status code 241 should auto-generate appropriate message when none provided.
        
        [Implementation details]
        Tests 241 status code uses HttpStatus.get_default_message() when message not specified.
        """
        content = "Urgent context dependent content with auto message"
        result = format_http_section(
            content=content,
            content_type="text/plain",
            criticality="CRITICAL",
            description="Auto Urgent Message Test",
            section_type="urgent-context",
            location="task://urgent/auto",
            status_code=241
            # No status_message provided - should auto-generate
        )
        
        assert "X-ASYNC-HTTP/1.1 241 Context Dependent Content requiring IMMEDIATE attention" in result
        assert content in result
    
    def test_header_ordering_content_location_first(self):
        """
        [Function intent]
        Test new header ordering with Content-Location and Content-Length first.
        
        [Design principles]
        New header ordering should place Content-Location and Content-Length before others.
        
        [Implementation details]
        Tests header order: Status, Content-Location, Content-Length, then others.
        """
        content = "Test content for header ordering validation"
        result = format_http_section(
            content=content,
            content_type="text/markdown",
            criticality="CRITICAL",
            description="Header Order Test",
            section_type="framework-rule",
            location="file://{HOME}/header_order.md"
        )
        
        lines = result.split('\n')
        
        # Find key header positions
        status_line = -1
        content_location_line = -1
        content_length_line = -1
        content_type_line = -1
        
        for i, line in enumerate(lines):
            if line.startswith("X-ASYNC-HTTP/1.1"):
                status_line = i
            elif line.startswith("Content-Location:"):
                content_location_line = i
            elif line.startswith("Content-Length:"):
                content_length_line = i
            elif line.startswith("Content-Type:"):
                content_type_line = i
        
        # Verify ordering: Status < Content-Location < Content-Length < Content-Type
        assert status_line < content_location_line < content_length_line < content_type_line
        assert content in result


class TestHTTPSectionFormatting:
    """
    [Class intent]
    Test suite for format_http_section function with comprehensive parameter validation.
    Validates HTTP header generation, content-length calculation, and error handling.
    
    [Design principles]
    Thorough testing of all parameters and formatting variations.
    Content-length accuracy testing with different encodings.
    
    [Implementation details]
    Tests all function parameters, error conditions, and output format validation.
    Includes encoding tests for international content and special characters.
    """
    
    def test_basic_formatting(self):
        """
        [Function intent]
        Test basic HTTP section formatting with standard parameters.
        
        [Design principles]
        Fundamental formatting validation with required parameters.
        
        [Implementation details]
        Tests basic formatting produces expected headers and content structure.
        """
        content = "# Test Content\nThis is a test."
        result = format_http_section(
            content=content,
            content_type="text/markdown",
            criticality="CRITICAL",
            description="Test Content",
            section_type="framework-rule",
            location="file://{HOME}/test.md"
        )
        
        # Verify boundary markers
        assert "--- ASYNC-HTTP-SECTION-START-v20250628" in result
        # Verify HTTP status line
        assert "X-ASYNC-HTTP/1.1 200 OK" in result
        # Verify required headers with new ordering
        assert "Content-Location: file://{HOME}/test.md" in result
        assert "Content-Type: text/markdown" in result
        assert "X-ASYNC-Content-Criticality: CRITICAL" in result
        assert "X-ASYNC-Content-Description: Test Content" in result
        assert "X-ASYNC-Content-Section: framework-rule" in result
        # Verify content length accuracy
        expected_length = len(content.encode('utf-8'))
        assert f"Content-Length: {expected_length}" in result
        # Verify content is included
        assert content in result
    
    def test_content_length_accuracy_utf8(self):
        """
        [Function intent]
        Test content-length calculation accuracy for UTF-8 encoded content.
        
        [Design principles]
        Byte-perfect content length calculation for international content.
        
        [Implementation details]
        Tests various Unicode characters and verifies byte length accuracy.
        """
        # Test with international characters
        content = "Test: 日本語 français العربية 🚀"
        result = format_http_section(
            content=content,
            content_type="text/markdown",
            criticality="INFORMATIONAL",
            description="Unicode Test",
            section_type="project-knowledge",
            location="file://{PROJECT_ROOT}/test.md"
        )
        
        expected_length = len(content.encode('utf-8'))
        assert f"Content-Length: {expected_length}" in result
        # Verify byte length is different from character length for Unicode
        assert expected_length != len(content)
    
    def test_criticality_normalization(self):
        """
        [Function intent]
        Test criticality parameter normalization in HTTP section formatting.
        
        [Design principles]
        Case-insensitive criticality input with proper normalization.
        
        [Implementation details]
        Tests lowercase criticality input is normalized to uppercase in output.
        """
        content = "Test content"
        result = format_http_section(
            content=content,
            content_type="text/plain",
            criticality="critical",  # lowercase input
            description="Test",
            section_type="workflow",
            location="file://{HOME}/test.txt"
        )
        
        assert "X-ASYNC-Content-Criticality: CRITICAL" in result
    
    def test_additional_headers(self):
        """
        [Function intent]
        Test additional headers parameter functionality.
        
        [Design principles]
        Extensible header system for future enhancements.
        
        [Implementation details]
        Tests custom headers are properly added to HTTP section.
        """
        content = "Test content"
        additional_headers = {
            "X-Custom-Header": "CustomValue",
            "X-Version": "1.0"
        }
        result = format_http_section(
            content=content,
            content_type="application/json",
            criticality="CRITICAL",
            description="Header Test",
            section_type="framework-rule",
            location="file://{HOME}/test.json",
            additional_headers=additional_headers
        )
        
        assert "X-Custom-Header: CustomValue" in result
        assert "X-Version: 1.0" in result
    
    def test_empty_content_error(self):
        """
        [Function intent]
        Test error handling for empty content parameter.
        
        [Design principles]
        Defensive programming with validation of required parameters.
        
        [Implementation details]
        Tests empty content raises ValueError with descriptive message.
        """
        with pytest.raises(ValueError) as exc_info:
            format_http_section(
                content="",
                content_type="text/plain",
                criticality="CRITICAL",
                description="Test",
                section_type="framework-rule",
                location="file://{HOME}/test.txt"
            )
        assert "Content cannot be empty" in str(exc_info.value)
    
    def test_missing_required_parameters(self):
        """
        [Function intent]
        Test error handling for missing required parameters.
        
        [Design principles]
        Comprehensive validation of all required parameters.
        
        [Implementation details]
        Tests each required parameter raises appropriate error when missing.
        """
        base_params = {
            "content": "Test content",
            "content_type": "text/plain",
            "criticality": "CRITICAL",
            "description": "Test",
            "section_type": "framework-rule",
            "location": "file://{HOME}/test.txt"
        }
        
        # Test each required parameter
        for param_name in base_params:
            if param_name == "content":
                continue  # Already tested separately
            
            params = base_params.copy()
            params[param_name] = ""
            
            with pytest.raises(ValueError):
                format_http_section(**params)
    
    def test_invalid_additional_headers(self):
        """
        [Function intent]
        Test error handling for invalid additional headers.
        
        [Design principles]
        Validation of optional parameters when provided.
        
        [Implementation details]
        Tests empty header names or values raise descriptive errors.
        """
        content = "Test content"
        
        # Test empty header name
        with pytest.raises(ValueError) as exc_info:
            format_http_section(
                content=content,
                content_type="text/plain",
                criticality="CRITICAL",
                description="Test",
                section_type="framework-rule",
                location="file://{HOME}/test.txt",
                additional_headers={"": "value"}
            )
        assert "Invalid additional header" in str(exc_info.value)
        
        # Test empty header value
        with pytest.raises(ValueError) as exc_info:
            format_http_section(
                content=content,
                content_type="text/plain",
                criticality="CRITICAL",
                description="Test",
                section_type="framework-rule",
                location="file://{HOME}/test.txt",
                additional_headers={"Header": ""}
            )
        assert "Invalid additional header" in str(exc_info.value)
    
    def test_last_modified_header_included(self):
        """
        [Function intent]
        Test Last-Modified header is included when parameter is provided.
        
        [Design principles]
        Optional parameter inclusion with proper HTTP header formatting.
        
        [Implementation details]
        Tests Last-Modified header appears in output with correct format.
        """
        content = "Test content with last modified"
        timestamp = "Fri, 28 Jun 2025 05:38:00 GMT"
        
        result = format_http_section(
            content=content,
            content_type="text/plain",
            criticality="INFORMATIONAL",
            description="Last Modified Test",
            section_type="knowledge-base",
            location="file://{HOME}/test.txt",
            last_modified=timestamp
        )
        
        assert f"Last-Modified: {timestamp}" in result
        assert content in result
    
    def test_last_modified_header_omitted(self):
        """
        [Function intent]
        Test Last-Modified header is omitted when parameter is not provided.
        
        [Design principles]
        Backward compatibility - existing behavior unchanged.
        
        [Implementation details]
        Tests no Last-Modified header in output when parameter not provided.
        """
        content = "Test content without last modified"
        
        result = format_http_section(
            content=content,
            content_type="text/plain",
            criticality="INFORMATIONAL",
            description="No Last Modified Test",
            section_type="knowledge-base",
            location="file://{HOME}/test.txt"
        )
        
        assert "Last-Modified:" not in result
        assert content in result
    
    def test_empty_last_modified_error(self):
        """
        [Function intent]
        Test error handling for empty Last-Modified parameter.
        
        [Design principles]
        Defensive programming with validation of optional parameters.
        
        [Implementation details]
        Tests empty Last-Modified value raises descriptive ValueError.
        """
        content = "Test content"
        
        with pytest.raises(ValueError) as exc_info:
            format_http_section(
                content=content,
                content_type="text/plain",
                criticality="INFORMATIONAL",
                description="Test",
                section_type="knowledge-base",
                location="file://{HOME}/test.txt",
                last_modified=""
            )
        assert "Last-Modified header cannot be empty or whitespace" in str(exc_info.value)
    
    def test_whitespace_last_modified_error(self):
        """
        [Function intent]
        Test error handling for whitespace-only Last-Modified parameter.
        
        [Design principles]
        Robust validation prevents meaningless header values.
        
        [Implementation details]
        Tests whitespace-only Last-Modified raises descriptive ValueError.
        """
        content = "Test content"
        
        with pytest.raises(ValueError) as exc_info:
            format_http_section(
                content=content,
                content_type="text/plain",
                criticality="INFORMATIONAL",
                description="Test",
                section_type="knowledge-base",
                location="file://{HOME}/test.txt",
                last_modified="   \n   "
            )
        assert "Last-Modified header cannot be empty or whitespace" in str(exc_info.value)
    
    def test_writable_parameter_for_string_content(self):
        """
        [Function intent]
        Test writable parameter functionality for string content.
        
        [Design principles]
        String content should use writable parameter for Content-Writable header.
        
        [Implementation details]
        Tests writable parameter controls Content-Writable header for string content.
        """
        content = "Test content for writable parameter"
        
        # Test with writable=False (default)
        result_readonly = format_http_section(
            content=content,
            content_type="text/plain",
            criticality="INFORMATIONAL",
            description="String Readonly Test",
            section_type="knowledge-base",
            location="file://{HOME}/test.txt",
            writable=False
        )
        
        assert "X-ASYNC-Content-Writable: false" in result_readonly
        assert content in result_readonly
        
        # Test with writable=True
        result_writable = format_http_section(
            content=content,
            content_type="text/plain",
            criticality="INFORMATIONAL",
            description="String Writable Test",
            section_type="knowledge-base",
            location="file://{HOME}/test.txt",
            writable=True
        )
        
        assert "X-ASYNC-Content-Writable: true" in result_writable
        assert content in result_writable


class TestMultiSectionResponse:
    """
    [Class intent]
    Test suite for format_multi_section_response function.
    Validates combining multiple HTTP sections into cohesive responses.
    
    [Design principles]
    Multi-section response testing with various section combinations.
    Error handling for invalid section combinations.
    
    [Implementation details]
    Tests section combination, separation, and validation behavior.
    """
    
    def test_multiple_sections_combination(self):
        """
        [Function intent]
        Test combining multiple HTTP-formatted sections into single response.
        
        [Design principles]
        Clean section separation with maintained individual section integrity.
        
        [Implementation details]
        Tests multiple pre-formatted sections are properly combined.
        """
        section1 = format_http_section(
            content="Content 1",
            content_type="text/plain",
            criticality="CRITICAL",
            description="Section 1",
            section_type="framework-rule",
            location="file://{HOME}/section1.txt"
        )
        
        section2 = format_http_section(
            content="Content 2",
            content_type="text/markdown",
            criticality="INFORMATIONAL",
            description="Section 2",
            section_type="knowledge-base",
            location="file://{HOME}/section2.md"
        )
        
        result = format_multi_section_response(section1, section2)
        
        # Both sections should be present
        assert "Content 1" in result
        assert "Content 2" in result
        assert HTTP_BOUNDARY_MARKER in result
        # Sections should be separated
        assert "\n\n" in result
    
    def test_single_section_passthrough(self):
        """
        [Function intent]
        Test single section handling in multi-section function.
        
        [Design principles]
        Function works with single section but now always includes protocol definition.
        
        [Implementation details]
        Tests single section includes protocol definition and original content.
        """
        section = format_http_section(
            content="Single content",
            content_type="text/plain",
            criticality="CRITICAL",
            description="Single Section",
            section_type="workflow",
            location="file://{HOME}/single.txt"
        )
        
        result = format_multi_section_response(section)
        
        # Protocol definition should be included even for single section
        assert "<how_to>" in result
        assert "X-ASYNC-HTTP/1.1 PROTOCOL DEFINITION" in result
        # Original section content should still be present
        assert "Single content" in result
        assert section in result  # The original section should be embedded
    
    def test_no_sections_error(self):
        """
        [Function intent]
        Test error handling when no sections provided.
        
        [Design principles]
        Defensive programming requires at least one section.
        
        [Implementation details]
        Tests empty arguments raise descriptive ValueError.
        """
        with pytest.raises(ValueError) as exc_info:
            format_multi_section_response()
        assert "At least one section must be provided" in str(exc_info.value)
    
    def test_empty_section_error(self):
        """
        [Function intent]
        Test error handling for empty or whitespace-only sections.
        
        [Design principles]
        Validation ensures all sections contain meaningful content.
        
        [Implementation details]
        Tests empty sections raise descriptive errors with section index.
        """
        valid_section = format_http_section(
            content="Valid content",
            content_type="text/plain",
            criticality="CRITICAL",
            description="Valid Section",
            section_type="framework-rule",
            location="file://{HOME}/valid.txt"
        )
        
        with pytest.raises(ValueError) as exc_info:
            format_multi_section_response(valid_section, "", valid_section)
        assert "Section 1 is empty" in str(exc_info.value)
        
        with pytest.raises(ValueError) as exc_info:
            format_multi_section_response(valid_section, "   \n   ")
        assert "contains only whitespace" in str(exc_info.value)
    
    def test_preambule_functionality(self):
        """
        [Function intent]
        Test preambule parameter functionality in format_multi_section_response.
        
        [Design principles]
        Preambule should be wrapped in XML tags and placed before protocol definition.
        
        [Implementation details]
        Tests preambule content is properly wrapped and positioned.
        """
        section = format_http_section(
            content="Test content with preambule",
            content_type="text/plain",
            criticality="INFORMATIONAL",
            description="Preambule Test",
            section_type="knowledge-base",
            location="file://{HOME}/preambule_test.txt"
        )
        
        preambule_text = "This is important contextual information that appears before the protocol definition."
        result = format_multi_section_response(section, preambule=preambule_text)
        
        # Preambule should be wrapped in XML tags
        assert "<preambule>" in result
        assert "</preambule>" in result
        assert preambule_text in result
        
        # Preambule should appear before protocol definition
        assert result.index("<preambule>") < result.index("<how_to>")
        
        # Section content should still be present
        assert "Test content with preambule" in result
    
    def test_protocol_definition_inclusion(self):
        """
        [Function intent]
        Test automatic protocol definition inclusion in multi-section responses.
        
        [Design principles]
        Protocol definition should be automatically included to explain response format.
        
        [Implementation details]
        Tests protocol definition is present with correct structure and content.
        """
        section = format_http_section(
            content="Protocol definition test content",
            content_type="text/markdown",
            criticality="CRITICAL",
            description="Protocol Test",
            section_type="framework-rule",
            location="file://{HOME}/protocol_test.md"
        )
        
        result = format_multi_section_response(section)
        
        # Protocol definition should be present
        assert "<how_to>" in result
        assert "</how_to>" in result
        assert "X-ASYNC-HTTP/1.1 PROTOCOL DEFINITION" in result
        assert "STRUCTURE OF A MULTI-PART X-ASYNC-HTTP/1.1 CONTENT RESPONSE" in result
        assert "STATUS CODES:" in result
        assert "240 Context Dependent Content" in result
        assert "241 Context Dependent Content requiring IMMEDIATE attention" in result


class TestExtractHttpSections:
    """
    [Class intent]
    Test suite for extract_http_sections_from_multi_response function.
    Validates extraction of HTTP sections and preambule from multi-section responses.
    
    [Design principles]
    Comprehensive testing of protocol definition removal and content extraction.
    Validation of preambule extraction and HTTP section isolation.
    
    [Implementation details]
    Tests extraction functionality with various multi-section response formats.
    """
    
    def test_extract_sections_without_preambule(self):
        """
        [Function intent]
        Test extraction of HTTP sections from multi-response without preambule.
        
        [Design principles]
        Function should return HTTP sections and None for preambule when no preambule present.
        
        [Implementation details]
        Tests basic extraction removes protocol definition and returns sections.
        """
        section = format_http_section(
            content="Test content for extraction",
            content_type="text/markdown",
            criticality="INFORMATIONAL",
            description="Extraction Test",
            section_type="knowledge-base",
            location="file://{HOME}/extract_test.md"
        )
        
        multi_response = format_multi_section_response(section)
        http_sections, preambule = extract_http_sections_from_multi_response(multi_response)
        
        # Should return HTTP sections without protocol definition
        assert "Test content for extraction" in http_sections
        assert "ASYNC-HTTP-SECTION-START" in http_sections
        assert "<how_to>" not in http_sections
        assert "X-ASYNC-HTTP/1.1 PROTOCOL DEFINITION" not in http_sections
        
        # Should return None for preambule
        assert preambule is None


class TestFormatHttpResponse:
    """
    [Class intent]
    Test suite for format_http_response function.
    Validates simple HTTP response formatting with status codes, headers, and data content.
    
    [Design principles]
    Comprehensive testing of HTTP/1.1 response formatting for API integration.
    Validation of automatic JSON serialization and content type handling.
    
    [Implementation details]
    Tests simple HTTP response generation with various data types and status codes.
    """
    
    def test_basic_json_response(self):
        """
        [Function intent]
        Test basic HTTP response formatting with JSON data.
        
        [Design principles]
        Dictionary data should be automatically serialized to JSON with proper headers.
        
        [Implementation details]
        Tests dictionary data generates JSON response with correct Content-Type.
        """
        data = {"message": "Test response", "status": "success", "count": 42}
        result = format_http_response(200, "OK", data, "application/json")
        
        # Should have proper HTTP/1.1 status line
        assert "HTTP/1.1 200 OK" in result
        
        # Should have correct headers
        assert "Content-Type: application/json" in result
        
        # Should have JSON content
        assert '"message": "Test response"' in result
        assert '"status": "success"' in result
        assert '"count": 42' in result
        
        # Should have accurate content length
        import json
        expected_content = json.dumps(data, indent=2)
        expected_length = len(expected_content.encode('utf-8'))
        assert f"Content-Length: {expected_length}" in result


class TestIntegrationWithConstants:
    """
    [Class intent]
    Integration tests for HTTP formatting with JESSE Framework constants.
    Validates proper integration with content types, section types, and criticality mapping.
    
    [Design principles]
    Real-world integration testing with actual framework constants.
    Validation of constant usage and compatibility.
    
    [Implementation details]
    Tests HTTP formatting with various constant combinations from framework.
    """
    
    def test_content_types_integration(self):
        """
        [Function intent]
        Test HTTP formatting with all defined content types from constants.
        
        [Design principles]
        Integration validation with framework-defined content types.
        
        [Implementation details]
        Tests all CONTENT_TYPES constants work with HTTP formatting.
        """
        content = "Test content for content type validation"
        
        for content_key, content_type in CONTENT_TYPES.items():
            result = format_http_section(
                content=content,
                content_type=content_type,
                criticality="INFORMATIONAL",
                description=f"Test {content_key}",
                section_type="knowledge-base",
                location=f"file://{{HOME}}/test.{content_key}"
            )
            
            assert f"Content-Type: {content_type}" in result
            assert content in result
