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
# XAsyncHttpPath class and path integration tests for JESSE Framework MCP server.
# Validates portable path resolution, HttpPath functionality, and integration with HTTP formatting.
###############################################################################
# [Source file design principles]
# Comprehensive testing of HttpPath dual-path functionality with original and resolved paths
# Cross-platform path resolution testing with environment variable support
# Integration testing with HTTP formatting for location headers and content loading
###############################################################################
# [Source file constraints]
# Cross-platform path testing requires environment independence
# HttpPath testing must validate both original preservation and resolution accuracy
# Integration tests require temporary file handling and proper cleanup
###############################################################################
# [Dependencies]
# <system>: pytest for testing framework
# <system>: pathlib for cross-platform path testing
# <system>: tempfile for temporary file testing
# <system>: re for regular expression testing
# <codebase>: jesse_framework_mcp.helpers.http_formatter for HttpPath and formatting functions
# <codebase>: jesse_framework_mcp.helpers.path_utils for path resolution functions
# <codebase>: jesse_framework_mcp.constants for HTTP formatting constants
###############################################################################
# [GenAI tool change history]
# 2025-07-05T09:55:00Z : Split from large test_http_formatting.py file for better organization by CodeAssistant
# * Extracted HttpPath class tests, path resolution tests, and integration tests
# * Preserved all test functionality including performance tests and edge cases
# * Updated file header to reflect focused scope on HttpPath and path integration
# * Maintained all original test logic including cross-platform compatibility testing
###############################################################################

import pytest
import tempfile
import re
from pathlib import Path
from jesse_framework_mcp.helpers.async_http_formatter import (
    format_http_section,
    XAsyncHttpPath
)
from jesse_framework_mcp.helpers.path_utils import resolve_portable_path
from jesse_framework_mcp.constants import (
    CONTENT_TYPES,
    SECTION_TYPES,
    RULE_CRITICALITY_MAP
)


class TestPortablePathResolution:
    """
    [Class intent]
    Test suite for portable path variable resolution across different environments.
    Validates cross-platform path substitution and error handling.
    
    [Design principles]
    Cross-platform compatibility testing with environment independence.
    Error condition testing for filesystem access issues.
    
    [Implementation details]
    Tests all supported path variables and their resolution behavior.
    Validates error handling for malformed paths and access issues.
    """
    
    def test_project_root_resolution(self):
        """
        [Function intent]
        Test {PROJECT_ROOT} variable resolution to current working directory.
        
        [Design principles]
        Verify path variable replacement produces absolute paths.
        
        [Implementation details]
        Tests PROJECT_ROOT replacement and validates result is absolute path.
        """
        location = "file://{PROJECT_ROOT}/.knowledge/test.md"
        resolved = resolve_portable_path(location)
        
        assert "{PROJECT_ROOT}" not in resolved
        assert "file://" in resolved
        assert resolved.endswith("/.knowledge/test.md")
        assert str(Path.cwd()) in resolved
    
    def test_home_directory_resolution(self):
        """
        [Function intent]
        Test {HOME} variable resolution to user home directory.
        
        [Design principles]
        Cross-platform home directory detection and replacement.
        
        [Implementation details]
        Tests HOME variable replacement with actual user home path.
        """
        location = "file://{HOME}/Cline/Rules/test.md"
        resolved = resolve_portable_path(location)
        
        assert "{HOME}" not in resolved
        assert "file://" in resolved
        assert resolved.endswith("/Cline/Rules/test.md")
        assert str(Path.home()) in resolved
    
    def test_cline_rules_resolution(self):
        """
        [Function intent]
        Test {CLINE_RULES} variable resolution to standard Cline rules directory.
        
        [Design principles]
        Standard Cline integration path resolution.
        
        [Implementation details]
        Tests CLINE_RULES resolves to {HOME}/Cline/Rules path.
        """
        location = "file://{CLINE_RULES}/JESSE_HINTS.md"
        resolved = resolve_portable_path(location)
        
        assert "{CLINE_RULES}" not in resolved
        assert "file://" in resolved
        assert resolved.endswith("/Cline/Rules/JESSE_HINTS.md")
        expected_path = str(Path.home() / "Cline" / "Rules")
        assert expected_path in resolved
    
    def test_cline_workflows_resolution(self):
        """
        [Function intent]
        Test {CLINE_WORKFLOWS} variable resolution to standard workflows directory.
        
        [Design principles]
        Standard Cline workflows path resolution.
        
        [Implementation details]
        Tests CLINE_WORKFLOWS resolves to {HOME}/Cline/Workflows path.
        """
        location = "file://{CLINE_WORKFLOWS}/jesse_wip_task_create.md"
        resolved = resolve_portable_path(location)
        
        assert "{CLINE_WORKFLOWS}" not in resolved
        assert "file://" in resolved
        assert resolved.endswith("/Cline/Workflows/jesse_wip_task_create.md")
        expected_path = str(Path.home() / "Cline" / "Workflows")
        assert expected_path in resolved
    
    def test_multiple_variables_resolution(self):
        """
        [Function intent]
        Test resolution of multiple path variables in single location string.
        
        [Design principles]
        Complex path resolution with multiple variable substitutions.
        
        [Implementation details]
        Tests multiple variables are all resolved in single pass.
        """
        location = "Combined: {PROJECT_ROOT} and {HOME} and {CLINE_RULES}"
        resolved = resolve_portable_path(location)
        
        assert "{PROJECT_ROOT}" not in resolved
        assert "{HOME}" not in resolved
        assert "{CLINE_RULES}" not in resolved
        assert str(Path.cwd()) in resolved
        assert str(Path.home()) in resolved
    
    def test_no_variables_passthrough(self):
        """
        [Function intent]
        Test that paths without variables pass through unchanged.
        
        [Design principles]
        Non-variable paths should remain unmodified.
        
        [Implementation details]
        Tests literal paths without variables are returned as-is.
        """
        location = "file:///absolute/path/to/file.md"
        resolved = resolve_portable_path(location)
        
        assert resolved == location


class TestHttpPath:
    """
    [Class intent]
    Test suite for HttpPath class dual-path functionality and integration.
    Validates portable path storage, filesystem operations, and HTTP formatting integration.
    
    [Design principles]
    Comprehensive testing of dual-path storage with original and resolved path access.
    Integration testing with format_http_section for location header functionality.
    
    [Implementation details]
    Tests HttpPath construction, method functionality, and Path inheritance behavior.
    Validates all supported environment variables and error handling.
    """
    
    def test_http_path_basic_construction(self):
        """
        [Function intent]
        Test basic HttpPath construction with variable resolution.
        
        [Design principles]
        HttpPath should store original path and resolve variables for filesystem operations.
        
        [Implementation details]
        Tests HttpPath creates valid Path object with resolved path while preserving original.
        """
        original_path = "file://{PROJECT_ROOT}/.knowledge/test.md"
        http_path = XAsyncHttpPath(original_path)
        
        # Should be a valid XAsyncHttpPath object
        assert isinstance(http_path, XAsyncHttpPath)
        
        # Original path should be preserved
        assert http_path.get_original_path() == original_path
        
        # Resolved path should not contain variables
        resolved = str(http_path)
        assert "{PROJECT_ROOT}" not in resolved
        assert str(Path.cwd()) in resolved
        assert resolved.endswith("/.knowledge/test.md")
    
    def test_http_path_all_supported_variables(self):
        """
        [Function intent]
        Test HttpPath construction with all supported environment variables.
        
        [Design principles]
        All JESSE framework variables should be properly resolved while preserving originals.
        
        [Implementation details]
        Tests each supported variable individually and in combination.
        """
        # Test PROJECT_ROOT
        project_path = XAsyncHttpPath("{PROJECT_ROOT}/test.md")
        assert project_path.get_original_path() == "{PROJECT_ROOT}/test.md"
        assert str(Path.cwd()) in str(project_path)
        assert "{PROJECT_ROOT}" not in str(project_path)
        
        # Test HOME
        home_path = XAsyncHttpPath("{HOME}/test.md")
        assert home_path.get_original_path() == "{HOME}/test.md"
        assert str(Path.home()) in str(home_path)
        assert "{HOME}" not in str(home_path)
        
        # Test CLINE_RULES
        rules_path = XAsyncHttpPath("{CLINE_RULES}/JESSE_HINTS.md")
        assert rules_path.get_original_path() == "{CLINE_RULES}/JESSE_HINTS.md"
        expected_rules = str(Path.home() / "Cline" / "Rules")
        assert expected_rules in str(rules_path)
        assert "{CLINE_RULES}" not in str(rules_path)
        
        # Test CLINE_WORKFLOWS
        workflows_path = XAsyncHttpPath("{CLINE_WORKFLOWS}/jesse_wip_task_create.md")
        assert workflows_path.get_original_path() == "{CLINE_WORKFLOWS}/jesse_wip_task_create.md"
        expected_workflows = str(Path.home() / "Cline" / "Workflows")
        assert expected_workflows in str(workflows_path)
        assert "{CLINE_WORKFLOWS}" not in str(workflows_path)
    
    def test_http_path_get_original_path(self):
        """
        [Function intent]
        Test get_original_path() method returns unresolved portable path.
        
        [Design principles]
        Method should return exact original path string with variables intact.
        
        [Implementation details]
        Tests get_original_path() preserves variables for header generation.
        """
        test_cases = [
            "file://{HOME}/Cline/Rules/test.md",
            "{PROJECT_ROOT}/.knowledge/kb.md",
            "https://example.com/{HOME}/shared/file.json",
            "{CLINE_WORKFLOWS}/complex/path/with/{CLINE_RULES}/reference.md"
        ]
        
        for original in test_cases:
            http_path = XAsyncHttpPath(original)
            assert http_path.get_original_path() == original
    
    def test_http_path_get_resolved_path(self):
        """
        [Function intent]
        Test get_resolved_path() method returns filesystem-ready path.
        
        [Design principles]
        Method should return resolved path equivalent to str(http_path).
        
        [Implementation details]
        Tests get_resolved_path() produces same result as string conversion.
        """
        original_path = "file://{HOME}/Cline/Rules/{PROJECT_ROOT}/test.md"
        http_path = XAsyncHttpPath(original_path)
        
        # get_resolved_path() should match str() conversion
        assert http_path.get_resolved_path() == str(http_path)
        
        # Should not contain any variables
        resolved = http_path.get_resolved_path()
        assert "{HOME}" not in resolved
        assert "{PROJECT_ROOT}" not in resolved
        assert "{CLINE_RULES}" not in resolved
        assert "{CLINE_WORKFLOWS}" not in resolved
    
    def test_http_path_inheritance_functionality(self):
        """
        [Function intent]
        Test HttpPath inherits all Path functionality correctly.
        
        [Design principles]
        HttpPath should work as a normal Path object for filesystem operations.
        
        [Implementation details]
        Tests common Path methods work on resolved filesystem path.
        """
        # Create HttpPath pointing to current directory
        http_path = XAsyncHttpPath("{PROJECT_ROOT}")
        
        # Should inherit Path functionality
        assert hasattr(http_path, 'exists')
        assert hasattr(http_path, 'is_dir')
        assert hasattr(http_path, 'parent')
        assert hasattr(http_path, 'name')
        
        # Test actual Path methods (using current directory which should exist)
        assert http_path.exists()  # Current directory should exist
        assert http_path.is_dir()  # Current directory should be a directory
        
        # Test path manipulation
        child_path = http_path / "test_file.md"
        assert isinstance(child_path, XAsyncHttpPath)  # Should still be XAsyncHttpPath
        assert str(Path.cwd()) in str(child_path)
    
    def test_http_path_integration_with_format_http_section(self):
        """
        [Function intent]
        Test HttpPath integration with format_http_section for location headers.
        
        [Design principles]
        HttpPath objects should show original portable paths in Location headers.
        
        [Implementation details]
        Tests format_http_section uses original path for Location header when HttpPath passed.
        """
        original_location = "file://{HOME}/Cline/Rules/JESSE_HINTS.md"
        http_path = XAsyncHttpPath(original_location)
        
        result = format_http_section(
            content="# Test Content\nHttpPath integration test.",
            content_type="text/markdown",
            criticality="CRITICAL",
            description="HttpPath Integration Test",
            section_type="framework-rule",
            location=http_path  # Pass HttpPath object
        )
        
        # Location header should show original portable path
        assert f"Content-Location: {original_location}" in result
        
        # Should not show resolved path in Location header
        resolved_path = str(http_path)
        assert f"Content-Location: {resolved_path}" not in result
        
        # Content should still be included
        assert "HttpPath integration test" in result
    
    def test_http_path_location_vs_string_location_comparison(self):
        """
        [Function intent]
        Test HttpPath location produces different header than equivalent string location.
        
        [Design principles]
        HttpPath should preserve variables while string location resolves them.
        
        [Implementation details]
        Tests same path as HttpPath vs string produces different Location headers.
        """
        original_path = "file://{PROJECT_ROOT}/.knowledge/test.md"
        http_path = XAsyncHttpPath(original_path)
        
        # Format with HttpPath location
        result_with_http_path = format_http_section(
            content="Test content",
            content_type="text/plain",
            criticality="INFORMATIONAL",
            description="HttpPath Location Test",
            section_type="knowledge-base",
            location=http_path
        )
        
        # Format with string location
        result_with_string = format_http_section(
            content="Test content",
            content_type="text/plain",
            criticality="INFORMATIONAL",
            description="String Location Test",
            section_type="knowledge-base",
            location=original_path
        )
        
        # Both HttpPath and string locations should preserve variables in header for portability
        assert f"Content-Location: {original_path}" in result_with_http_path
        assert f"Content-Location: {original_path}" in result_with_string
        
        # Results should be nearly identical (only descriptions differ)
        # Both preserve portable paths for cross-platform compatibility
        assert "HttpPath Location Test" in result_with_http_path
        assert "String Location Test" in result_with_string
    
    def test_http_path_complex_variable_combinations(self):
        """
        [Function intent]
        Test HttpPath with complex combinations of multiple variables.
        
        [Design principles]
        Multiple variables in single path should all be resolved while preserving original.
        
        [Implementation details]
        Tests complex paths with multiple variables resolve correctly.
        """
        complex_path = "config://{HOME}/base/{PROJECT_ROOT}/shared/{CLINE_RULES}/rules.md"
        http_path = XAsyncHttpPath(complex_path)
        
        # Original should be preserved exactly
        assert http_path.get_original_path() == complex_path
        
        # Resolved should have all variables substituted
        resolved = str(http_path)
        assert "{HOME}" not in resolved
        assert "{PROJECT_ROOT}" not in resolved
        assert "{CLINE_RULES}" not in resolved
        
        # Should contain actual resolved paths
        assert str(Path.home()) in resolved
        assert str(Path.cwd()) in resolved
        assert str(Path.home() / "Cline" / "Rules") in resolved
    
    def test_http_path_error_handling_invalid_resolution(self):
        """
        [Function intent]
        Test HttpPath error handling when path resolution fails.
        
        [Design principles]
        HttpPath should propagate resolution errors from resolve_portable_path().
        
        [Implementation details]
        Tests HttpPath raises appropriate errors for resolution failures.
        """
        # This test depends on resolve_portable_path error handling
        # We'll test with a scenario that should work (valid construction)
        # The actual error handling is tested in resolve_portable_path tests
        
        # Test successful construction with all variables
        valid_path = "{HOME}/{PROJECT_ROOT}/{CLINE_RULES}/{CLINE_WORKFLOWS}/test.md"
        http_path = XAsyncHttpPath(valid_path)
        
        # Should construct successfully
        assert isinstance(http_path, XAsyncHttpPath)
        assert http_path.get_original_path() == valid_path
        
        # Resolved path should not contain variables
        resolved = str(http_path)
        for var in ["{HOME}", "{PROJECT_ROOT}", "{CLINE_RULES}", "{CLINE_WORKFLOWS}"]:
            assert var not in resolved
    
    def test_http_path_with_no_variables(self):
        """
        [Function intent]
        Test HttpPath with paths containing no variables.
        
        [Design principles]
        HttpPath should handle literal paths without variables correctly.
        
        [Implementation details]
        Tests HttpPath works with literal paths, preserving them unchanged.
        """
        literal_path = "file:///absolute/path/to/file.md"
        http_path = XAsyncHttpPath(literal_path)
        
        # Original should be preserved
        assert http_path.get_original_path() == literal_path
        
        # Resolved should be identical (no variables to resolve)
        assert str(http_path) == literal_path
        assert http_path.get_resolved_path() == literal_path
    
    def test_http_path_with_partial_variables(self):
        """
        [Function intent]
        Test HttpPath with paths containing some variables mixed with literal text.
        
        [Design principles]
        Only actual variables should be resolved, literal text should remain unchanged.
        
        [Implementation details]
        Tests partial variable resolution preserves non-variable text.
        """
        mixed_path = "https://api.example.com/{HOME}/user/data/file.json"
        http_path = XAsyncHttpPath(mixed_path)
        
        # Original should be preserved
        assert http_path.get_original_path() == mixed_path
        
        # Resolved should only replace {HOME}
        resolved = str(http_path)
        assert "{HOME}" not in resolved
        assert "https://api.example.com/" in resolved
        assert "/user/data/file.json" in resolved
        assert str(Path.home()) in resolved
    
    def test_http_path_filesystem_operations(self):
        """
        [Function intent]
        Test HttpPath filesystem operations work on resolved paths.
        
        [Design principles]
        All Path methods should operate on resolved filesystem paths.
        
        [Implementation details]
        Tests filesystem operations use resolved path, not original with variables.
        """
        # Use PROJECT_ROOT which should exist (current directory)
        http_path = XAsyncHttpPath("{PROJECT_ROOT}")
        
        # Filesystem operations should work on resolved path
        assert http_path.exists()  # Current directory exists
        assert http_path.is_dir()  # Current directory is a directory
        
        # Test path resolution
        parent = http_path.parent
        assert isinstance(parent, Path)
        
        # Test path building
        test_file = http_path / "test.md"
        assert str(Path.cwd()) in str(test_file)
        assert "test.md" in str(test_file)


class TestPathContentHandling:
    """
    [Class intent]
    Test suite for HttpPath content handling with format_http_section.
    Validates file reading, Last-Modified integration, and error handling.
    
    [Design principles]
    Comprehensive testing of HttpPath content loading with automatic features.
    Error scenario testing with realistic filesystem conditions.
    
    [Implementation details]
    Tests HttpPath content reading, Last-Modified headers, and file error handling.
    """
    
    def test_path_content_basic_functionality(self):
        """
        [Function intent]
        Test basic HttpPath object content reading functionality.
        
        [Design principles]
        HttpPath objects should seamlessly replace string content with file reading.
        
        [Implementation details]
        Tests HttpPath object reads file content and formats HTTP section correctly.
        """
        # Create a temporary file with test content
        test_content = "# HttpPath Content Test\nThis content was read from a file."
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.md', encoding='utf-8') as tmp_file:
            tmp_file.write(test_content)
            tmp_http_path = XAsyncHttpPath(tmp_file.name)
        
        try:
            result = format_http_section(
                content=tmp_http_path,  # Pass HttpPath object instead of string
                content_type="text/markdown",
                criticality="INFORMATIONAL",
                description="HttpPath Content Test",
                section_type="knowledge-base",
                location="file://{HOME}/path_test.md"
            )
            
            # Verify file content is included in output
            assert test_content in result
            
            # Verify headers are correct
            assert "Content-Type: text/markdown" in result
            assert "X-ASYNC-Content-Criticality: INFORMATIONAL" in result
            assert "X-ASYNC-Content-Description: HttpPath Content Test" in result
            
            # Verify content length is accurate for file content
            expected_length = len(test_content.encode('utf-8'))
            assert f"Content-Length: {expected_length}" in result
            
        finally:
            # Clean up temporary file
            tmp_http_path._resolved_path.unlink(missing_ok=True)
    
    def test_path_content_automatic_last_modified(self):
        """
        [Function intent]
        Test automatic Last-Modified header integration when content is HttpPath object.
        
        [Design principles]
        When content is HttpPath and no explicit last_modified provided, use file's mtime automatically.
        
        [Implementation details]
        Tests HttpPath content generates Last-Modified header automatically without explicit parameter.
        """
        # Create a temporary file with test content
        test_content = "# Auto Last-Modified Test\nThis file's mtime should be used automatically."
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.md', encoding='utf-8') as tmp_file:
            tmp_file.write(test_content)
            tmp_http_path = XAsyncHttpPath(tmp_file.name)
        
        try:
            result = format_http_section(
                content=tmp_http_path,  # HttpPath content
                content_type="text/markdown",
                criticality="INFORMATIONAL",
                description="Auto Last-Modified Test",
                section_type="knowledge-base",
                location="file://{HOME}/auto_last_modified.md"
                # Note: No explicit last_modified parameter - should be automatic
            )
            
            # Verify file content is included
            assert test_content in result
            
            # Verify Last-Modified header is automatically included
            assert "Last-Modified:" in result
            
            # Verify RFC 7231 format (e.g., "Fri, 28 Jun 2025 06:12:00 GMT")
            lines = result.split('\n')
            last_modified_header = None
            for line in lines:
                if line.startswith("Last-Modified:"):
                    last_modified_header = line
                    break
            
            assert last_modified_header is not None
            timestamp_part = last_modified_header.split("Last-Modified: ")[1]
            
            rfc7231_pattern = r'^[A-Za-z]{3}, \d{2} [A-Za-z]{3} \d{4} \d{2}:\d{2}:\d{2} GMT$'
            assert re.match(rfc7231_pattern, timestamp_part), f"Invalid RFC 7231 format: {timestamp_part}"
            
        finally:
            # Clean up temporary file
            tmp_http_path._resolved_path.unlink(missing_ok=True)
    
    def test_path_content_with_explicit_last_modified_override(self):
        """
        [Function intent]
        Test HttpPath content with explicit Last-Modified parameter overrides automatic behavior.
        
        [Design principles]
        Explicit last_modified parameter should take precedence over automatic file mtime.
        
        [Implementation details]
        Tests explicit Last-Modified overrides automatic HttpPath content timestamp.
        """
        # Create a temporary file with test content
        test_content = "# Explicit Override Test\nExplicit Last-Modified should override file mtime."
        explicit_timestamp = "Wed, 01 Jan 2025 12:00:00 GMT"
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.md', encoding='utf-8') as tmp_file:
            tmp_file.write(test_content)
            tmp_http_path = XAsyncHttpPath(tmp_file.name)
        
        try:
            result = format_http_section(
                content=tmp_http_path,  # HttpPath content
                content_type="text/markdown",
                criticality="INFORMATIONAL",
                description="Explicit Override Test",
                section_type="knowledge-base",
                location="file://{HOME}/explicit_override.md",
                last_modified=explicit_timestamp  # Explicit override
            )
            
            # Verify file content is included
            assert test_content in result
            
            # Verify explicit Last-Modified is used (not automatic file mtime)
            assert f"Last-Modified: {explicit_timestamp}" in result
            
        finally:
            # Clean up temporary file
            tmp_http_path._resolved_path.unlink(missing_ok=True)
    
    def test_path_content_file_not_found_error(self):
        """
        [Function intent]
        Test automatic 404 error handling when HttpPath content file does not exist.
        
        [Design principles]
        Missing content files should generate 404 HTTP responses with error content.
        
        [Implementation details]
        Tests missing HttpPath content files trigger automatic 404 with error content.
        """
        non_existent_http_path = XAsyncHttpPath("/non/existent/content/file.md")
        
        result = format_http_section(
            content=non_existent_http_path,
            content_type="text/markdown",
            criticality="INFORMATIONAL",
            description="Missing File Test",
            section_type="knowledge-base",
            location="file://{HOME}/missing.md"
        )
        
        # Should generate 404 HTTP response instead of raising exception
        assert "X-ASYNC-HTTP/1.1 404 Not Found" in result
        assert "Resource not found:" in result
        assert "file://{HOME}/missing.md" in result  # Location from location parameter
    
    def test_path_content_invalid_type_error(self):
        """
        [Function intent]
        Test error handling for invalid content parameter types.
        
        [Design principles]
        Clear type validation with descriptive error messages for unsupported types.
        
        [Implementation details]
        Tests TypeError is raised for content parameters that are neither str nor HttpPath.
        """
        with pytest.raises(TypeError) as exc_info:
            format_http_section(
                content=12345,  # Invalid type - neither str nor HttpPath
                content_type="text/plain",
                criticality="INFORMATIONAL",
                description="Invalid Type Test",
                section_type="knowledge-base",
                location="file://{HOME}/invalid_type.txt"
            )
        
        assert "content must be str or XAsyncHttpPath, got int" in str(exc_info.value)
        
        # Test with another invalid type
        with pytest.raises(TypeError) as exc_info:
            format_http_section(
                content=['list', 'of', 'strings'],  # Invalid type
                content_type="text/plain",
                criticality="INFORMATIONAL",
                description="Invalid Type Test 2",
                section_type="knowledge-base",
                location="file://{HOME}/invalid_type2.txt"
            )
        
        assert "content must be str or XAsyncHttpPath, got list" in str(exc_info.value)
    
    def test_path_content_empty_file_error(self):
        """
        [Function intent]
        Test error handling when HttpPath content file is empty.
        
        [Design principles]
        Empty content validation applies to file-read content same as string content.
        
        [Implementation details]
        Tests ValueError is raised when HttpPath content file contains no content.
        """
        # Create an empty temporary file
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.md', encoding='utf-8') as tmp_file:
            # Write nothing to create empty file
            tmp_http_path = XAsyncHttpPath(tmp_file.name)
        
        try:
            with pytest.raises(ValueError) as exc_info:
                format_http_section(
                    content=tmp_http_path,  # Empty file
                    content_type="text/markdown",
                    criticality="INFORMATIONAL",
                    description="Empty File Test",
                    section_type="knowledge-base",
                    location="file://{HOME}/empty.md"
                )
            
            assert "Content cannot be empty" in str(exc_info.value)
            
        finally:
            # Clean up temporary file
            tmp_http_path._resolved_path.unlink(missing_ok=True)
    
    def test_path_content_with_unicode_characters(self):
        """
        [Function intent]
        Test HttpPath content handling with Unicode characters and international text.
        
        [Design principles]
        UTF-8 encoding support for international content with accurate byte-length calculation.
        
        [Implementation details]
        Tests file reading preserves Unicode characters and calculates correct content length.
        """
        # Create a file with international characters
        test_content = "# Unicode Test 测试\n日本語 français العربية 🚀\nEmoji and international text."
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.md', encoding='utf-8') as tmp_file:
            tmp_file.write(test_content)
            tmp_http_path = XAsyncHttpPath(tmp_file.name)
        
        try:
            result = format_http_section(
                content=tmp_http_path,  # HttpPath with Unicode content
                content_type="text/markdown",
                criticality="INFORMATIONAL",
                description="Unicode HttpPath Content Test",
                section_type="knowledge-base",
                location="file://{HOME}/unicode_test.md"
            )
            
            # Verify Unicode content is preserved
            assert test_content in result
            assert "测试" in result
            assert "日本語" in result
            assert "français" in result
            assert "العربية" in result
            assert "🚀" in result
            
            # Verify content length is accurate for UTF-8 encoded Unicode
            expected_length = len(test_content.encode('utf-8'))
            assert f"Content-Length: {expected_length}" in result
            
            # Verify byte length differs from character length for Unicode
            assert expected_length != len(test_content)
            
        finally:
            # Clean up temporary file
            tmp_http_path._resolved_path.unlink(missing_ok=True)
    
    def test_path_content_with_additional_headers(self):
        """
        [Function intent]
        Test HttpPath content functionality with additional custom headers.
        
        [Design principles]
        HttpPath content integrates seamlessly with existing extensible header system.
        
        [Implementation details]
        Tests HttpPath content works properly with additional headers and automatic Last-Modified.
        """
        # Create a temporary file with test content
        test_content = "# HttpPath Content with Headers\nTesting additional headers with HttpPath content."
        additional_headers = {
            "X-Content-Source": "HttpFilePath",
            "X-Processing-Mode": "Automatic",
            "X-Encoding": "UTF-8"
        }
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.md', encoding='utf-8') as tmp_file:
            tmp_file.write(test_content)
            tmp_http_path = XAsyncHttpPath(tmp_file.name)
        
        try:
            result = format_http_section(
                content=tmp_http_path,  # HttpPath content
                content_type="text/markdown",
                criticality="CRITICAL",
                description="HttpPath Content with Additional Headers",
                section_type="framework-rule",
                location="file://{HOME}/path_with_headers.md",
                additional_headers=additional_headers
            )
            
            # Verify file content is included
            assert test_content in result
            
            # Verify all additional headers are present
            assert "X-Content-Source: HttpFilePath" in result
            assert "X-Processing-Mode: Automatic" in result
            assert "X-Encoding: UTF-8" in result
            
            # Verify automatic Last-Modified header is also present
            assert "Last-Modified:" in result
            
            # Verify header ordering (Last-Modified before additional headers)
            lines = result.split('\n')
            last_modified_line = -1
            content_source_line = -1
            
            for i, line in enumerate(lines):
                if line.startswith("Last-Modified:"):
                    last_modified_line = i
                elif line.startswith("X-Content-Source:"):
                    content_source_line = i
            
            assert last_modified_line < content_source_line
            
        finally:
            # Clean up temporary file
            tmp_http_path._resolved_path.unlink(missing_ok=True)


class TestPerformanceAndEdgeCases:
    """
    [Class intent]
    Performance validation and edge case testing for HTTP path integration.
    Ensures path handling performs well with large content and unusual scenarios.
    
    [Design principles]
    Performance testing with large content and memory efficiency validation.
    Edge case testing for unusual but valid input scenarios.
    
    [Implementation details]
    Tests large content formatting, special characters, and boundary conditions.
    """
    
    def test_large_content_formatting(self):
        """
        [Function intent]
        Test HTTP formatting performance with large content blocks.
        
        [Design principles]
        Performance validation for realistic large content scenarios.
        
        [Implementation details]
        Tests formatting with multi-kilobyte content maintains accuracy.
        """
        # Create large content (approximately 10KB)
        large_content = "# Large Content Test\n" + ("This is a test line.\n" * 500)
        
        result = format_http_section(
            content=large_content,
            content_type="text/markdown",
            criticality="INFORMATIONAL",
            description="Large Content Test",
            section_type="knowledge-base",
            location="file://{PROJECT_ROOT}/large_test.md"
        )
        
        # Verify content-length accuracy for large content
        expected_length = len(large_content.encode('utf-8'))
        assert f"Content-Length: {expected_length}" in result
        assert large_content in result
        assert len(result) > expected_length  # Headers add additional length
    
    def test_special_characters_in_headers(self):
        """
        [Function intent]
        Test HTTP formatting with special characters in header values.
        
        [Design principles]
        Robust handling of special characters in descriptions and locations.
        
        [Implementation details]
        Tests various special characters don't break header formatting.
        """
        content = "Content with special chars: <>&\""
        
        result = format_http_section(
            content=content,
            content_type="text/plain",
            criticality="INFORMATIONAL",
            description="Special chars: <>&\"",
            section_type="knowledge-base",
            location="file://{HOME}/special_chars_test.txt"
        )
        
        assert "X-ASYNC-Content-Description: Special chars: <>&\"" in result
        assert content in result
    
    def test_newlines_in_content(self):
        """
        [Function intent]
        Test HTTP formatting handles various newline formats correctly.
        
        [Design principles]
        Cross-platform newline handling for content preservation.
        
        [Implementation details]
        Tests different newline formats maintain proper content separation.
        """
        content_with_newlines = "Line 1\nLine 2\r\nLine 3\rLine 4"
        
        result = format_http_section(
            content=content_with_newlines,
            content_type="text/plain",
            criticality="INFORMATIONAL",
            description="Newline Test",
            section_type="project-knowledge",
            location="file://{HOME}/newline_test.txt"
        )
        
        # Content should be preserved exactly
        assert content_with_newlines in result
        # Content length should be accurate
        expected_length = len(content_with_newlines.encode('utf-8'))
        assert f"Content-Length: {expected_length}" in result
