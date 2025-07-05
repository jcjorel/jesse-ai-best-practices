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
# Core HTTP functionality tests for JESSE Framework MCP server HTTP formatting infrastructure.
# Validates HTTP status codes, error handling, and content criticality classification.
###############################################################################
# [Source file design principles]
# Thorough test coverage for HTTP status constants and error handling
# Comprehensive validation of content criticality levels and normalization
# Integration testing with actual error scenarios and exception mapping
###############################################################################
# [Source file constraints]
# Must validate proper HTTP status code constants and message mapping
# Error testing must verify exception-to-status mapping behavior
# Criticality validation must handle case-insensitive input normalization
###############################################################################
# [Dependencies]
# <system>: pytest for testing framework
# <codebase>: jesse_framework_mcp.helpers.http_formatter for HTTP status and error classes
###############################################################################
# [GenAI tool change history]
# 2025-07-05T09:51:00Z : Split from large test_http_formatting.py file for better organization by CodeAssistant
# * Extracted core HTTP functionality tests including HttpStatus, HttpErrorHandler, and ContentCriticality
# * Preserved all test functionality and comprehensive coverage from original file
# * Updated file header to reflect focused scope on core HTTP functionality
# * Maintained all original test logic and validation patterns
###############################################################################

import pytest
from jesse_framework_mcp.helpers.async_http_formatter import (
    XAsyncContentCriticality,
    XAsyncHttpStatus,
    XAsyncHttpErrorHandler
)


class TestHttpStatus:
    """
    [Class intent]
    Test suite for HttpStatus class status code constants and utilities.
    Validates status code constants and default message mapping functionality.
    
    [Design principles]
    Comprehensive testing of all supported status codes with message mapping.
    Validation of extensible design for future status code additions.
    
    [Implementation details]
    Tests all class constants and get_default_message() method behavior.
    Validates handling of known and unknown status codes.
    """
    
    def test_status_code_constants(self):
        """
        [Function intent]
        Test all HttpStatus class constants have correct values.
        
        [Design principles]
        Validate all status code constants match expected HTTP standards.
        
        [Implementation details]
        Tests each constant has the expected integer value.
        """
        assert XAsyncHttpStatus.OK == 200
        assert XAsyncHttpStatus.CONTEXT_DEPENDENT == 240
        assert XAsyncHttpStatus.CONTEXT_DEPENDENT_IMMEDIATE == 241
        assert XAsyncHttpStatus.NOT_FOUND == 404
        assert XAsyncHttpStatus.FORBIDDEN == 403
        assert XAsyncHttpStatus.INTERNAL_SERVER_ERROR == 500
    
    def test_get_default_message_known_codes(self):
        """
        [Function intent]
        Test get_default_message() returns correct messages for known status codes.
        
        [Design principles]
        Standard HTTP status messages should be properly mapped.
        
        [Implementation details]
        Tests all supported status codes return expected messages.
        """
        assert XAsyncHttpStatus.get_default_message(200) == "OK"
        assert XAsyncHttpStatus.get_default_message(240) == "Context Dependent Content"
        assert XAsyncHttpStatus.get_default_message(241) == "Context Dependent Content requiring IMMEDIATE attention"
        assert XAsyncHttpStatus.get_default_message(404) == "Not Found"
        assert XAsyncHttpStatus.get_default_message(403) == "Forbidden"
        assert XAsyncHttpStatus.get_default_message(500) == "Internal Server Error"
    
    def test_get_default_message_unknown_code(self):
        """
        [Function intent]
        Test get_default_message() handles unknown status codes gracefully.
        
        [Design principles]
        Unknown codes should return generic message for graceful handling.
        
        [Implementation details]
        Tests unknown status codes return "Unknown Status" message.
        """
        assert XAsyncHttpStatus.get_default_message(999) == "Unknown Status"
        assert XAsyncHttpStatus.get_default_message(123) == "Unknown Status"
        assert XAsyncHttpStatus.get_default_message(0) == "Unknown Status"


class TestHttpErrorHandler:
    """
    [Class intent]
    Test suite for HttpErrorHandler class functionality.
    Validates error content generation and exception-to-status mapping.
    
    [Design principles]
    Comprehensive testing of error handling and template-based content generation.
    Validation of automatic error detection from Python exceptions.
    
    [Implementation details]
    Tests error template formatting, exception mapping, and error content generation.
    """
    
    def test_generate_error_content_known_codes(self):
        """
        [Function intent]
        Test error content generation for known status codes.
        
        [Design principles]
        Template-based error content should use proper format substitution.
        
        [Implementation details]
        Tests error templates generate expected content with parameter substitution.
        """
        result_404 = XAsyncHttpErrorHandler.generate_error_content(404, "file://test.md")
        assert "Resource not found: file://test.md" == result_404
        
        result_403 = XAsyncHttpErrorHandler.generate_error_content(403, "file://protected.md")
        assert "Access denied: file://protected.md" == result_403
        
        result_500 = XAsyncHttpErrorHandler.generate_error_content(500, "file://error.md", "Test detail")
        assert "Internal server error: Test detail" == result_500
    
    def test_generate_error_content_unknown_code(self):
        """
        [Function intent]
        Test error content generation for unknown status codes.
        
        [Design principles]
        Unknown codes should use fallback template with status code included.
        
        [Implementation details]
        Tests unknown status codes generate generic error content.
        """
        result = XAsyncHttpErrorHandler.generate_error_content(999, "file://test.md", "Custom detail")
        assert "Error 999: Custom detail" == result
    
    def test_detect_error_from_exception_file_not_found(self):
        """
        [Function intent]
        Test automatic error detection for FileNotFoundError exceptions.
        
        [Design principles]
        FileNotFoundError should map to 404 status with appropriate content.
        
        [Implementation details]
        Tests FileNotFoundError generates 404 status and error content.
        """
        exc = FileNotFoundError("File not found")
        status_code, status_message, error_content = XAsyncHttpErrorHandler.detect_error_from_exception(
            exc, "file://missing.md"
        )
        
        assert status_code == 404
        assert status_message == "Not Found"
        assert "Resource not found: file://missing.md" == error_content
    
    def test_detect_error_from_exception_permission_error(self):
        """
        [Function intent]
        Test automatic error detection for PermissionError exceptions.
        
        [Design principles]
        PermissionError should map to 403 status with appropriate content.
        
        [Implementation details]
        Tests PermissionError generates 403 status and error content.
        """
        exc = PermissionError("Permission denied")
        status_code, status_message, error_content = XAsyncHttpErrorHandler.detect_error_from_exception(
            exc, "file://protected.md"
        )
        
        assert status_code == 403
        assert status_message == "Forbidden"
        assert "Access denied: file://protected.md" == error_content
    
    def test_detect_error_from_exception_generic_error(self):
        """
        [Function intent]
        Test automatic error detection for generic exceptions.
        
        [Design principles]
        Generic exceptions should map to 500 status with exception details.
        
        [Implementation details]
        Tests generic exceptions generate 500 status and detailed error content.
        """
        exc = ValueError("Invalid input value")
        status_code, status_message, error_content = XAsyncHttpErrorHandler.detect_error_from_exception(
            exc, "file://invalid.md"
        )
        
        assert status_code == 500
        assert status_message == "Internal Server Error"
        assert "Internal server error: Invalid input value" == error_content


class TestContentCriticality:
    """
    [Class intent]
    Test suite for ContentCriticality enum validation and normalization.
    Verifies correct handling of valid and invalid criticality levels.
    
    [Design principles]
    Comprehensive validation testing with case sensitivity and error handling.
    Tests for both valid inputs and expected error conditions.
    
    [Implementation details]
    Tests validate() method with various input formats and invalid values.
    Verifies proper error messages and case normalization behavior.
    """
    
    def test_valid_criticality_uppercase(self):
        """
        [Function intent]
        Test validation of valid criticality levels in uppercase format.
        
        [Design principles]
        Direct validation of expected uppercase input values.
        
        [Implementation details]
        Tests CRITICAL and INFORMATIONAL uppercase inputs return unchanged.
        """
        assert XAsyncContentCriticality.validate("CRITICAL") == "CRITICAL"
        assert XAsyncContentCriticality.validate("INFORMATIONAL") == "INFORMATIONAL"
    
    def test_valid_criticality_lowercase(self):
        """
        [Function intent]
        Test validation and normalization of lowercase criticality inputs.
        
        [Design principles]
        Case-insensitive input handling with uppercase normalization.
        
        [Implementation details]
        Tests lowercase inputs are properly converted to uppercase.
        """
        assert XAsyncContentCriticality.validate("critical") == "CRITICAL"
        assert XAsyncContentCriticality.validate("informational") == "INFORMATIONAL"
    
    def test_valid_criticality_mixed_case(self):
        """
        [Function intent]
        Test validation of mixed case criticality inputs.
        
        [Design principles]
        Robust case handling for various input formats.
        
        [Implementation details]
        Tests various mixed case combinations normalize to uppercase.
        """
        assert XAsyncContentCriticality.validate("Critical") == "CRITICAL"
        assert XAsyncContentCriticality.validate("InFormAtional") == "INFORMATIONAL"
    
    def test_invalid_criticality_raises_error(self):
        """
        [Function intent]
        Test that invalid criticality values raise descriptive ValueError.
        
        [Design principles]
        Defensive programming with clear error messages for invalid input.
        
        [Implementation details]
        Tests various invalid inputs and verifies error message content.
        """
        with pytest.raises(ValueError) as exc_info:
            XAsyncContentCriticality.validate("invalid")
        assert "Invalid criticality 'invalid'" in str(exc_info.value)
        
        with pytest.raises(ValueError) as exc_info:
            XAsyncContentCriticality.validate("HIGH")
        assert "Must be 'CRITICAL' or 'INFORMATIONAL'" in str(exc_info.value)
        
        with pytest.raises(ValueError) as exc_info:
            XAsyncContentCriticality.validate("")
        assert "Invalid criticality ''" in str(exc_info.value)
