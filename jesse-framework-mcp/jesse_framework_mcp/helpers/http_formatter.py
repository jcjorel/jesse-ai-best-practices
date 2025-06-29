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
# Universal HTTP-style formatting infrastructure for all JESSE Framework MCP resources.
# Provides standardized formatting with criticality awareness, portable path resolution,
# and consistent boundary markers for parseable multi-part content delivery.
###############################################################################
# [Source file design principles]
# Single responsibility for HTTP-style content formatting across all MCP resources
# Consistent structure with extensible headers and accurate content-length calculation
# Cross-platform portable path variable resolution for environment independence
# Defensive programming with comprehensive validation and descriptive error messages
###############################################################################
# [Source file constraints]
# Must maintain byte-perfect content-length calculation for semi-binary support
# Path resolution must work across Windows/Mac/Linux environments
# Error handling must follow throw-on-failure pattern without fallbacks
# All functions must be ready for async resource integration
###############################################################################
# [Dependencies]
# <system>: os, pathlib for cross-platform path operations
# <system>: typing for type hints and annotations
# <codebase>: jesse_framework_mcp.constants for HTTP format constants
###############################################################################
# [GenAI tool change history]
# 2025-06-29T17:26:26Z : Added HTTP 240 status code, preambule parameter, and protocol definition by CodeAssistant
# * Added HTTP 240 "Context Dependent Content" status code for task-specific content that must never be persisted in knowledge bases
# * Added optional preambule parameter to format_multi_section_response() with XML tag wrapping
# * Integrated comprehensive X-ASYNC-HTTP/1.1 protocol definition explaining format structure, headers, and status codes
# * Enhanced format_multi_section_response() to be self-documenting with protocol definition section
# * Zero breaking changes - all existing functionality preserved, new features are optional parameters
# 2025-06-28T14:22:52Z : Fixed HttpPath file:// URL filesystem operations support by CodeAssistant
# * Fixed HttpPath constructor to handle file:// URLs by extracting filesystem path while preserving original URL
# * Updated exists(), is_file(), read_text() and other filesystem methods to work with file:// URLs
# * Resolves critical bug where file://{PROJECT_ROOT}/.gitignore paths were treated as non-filesystem URLs
# * Session initialization now correctly detects existing .gitignore files instead of false negatives
# * Zero breaking changes - HTTP/HTTPS URLs still handled as before, only file:// URLs gained filesystem support
# 2025-06-28T11:41:05Z : Fixed Content-Location headers to preserve portable environment variables by CodeAssistant
# * Removed resolve_portable_path() call for string locations in format_http_section()
# * Content-Location headers now show portable paths like file://{PROJECT_ROOT}/... instead of resolved filesystem paths
# * Maintains cross-platform portability and environment independence for MCP resource headers
# * Zero breaking changes - all existing functionality preserved with improved portability
# 2025-06-28T06:47:00Z : Enhanced HttpPath with writable flag and replaced Path objects with HttpPath throughout by CodeAssistant
# * Added writable flag to HttpPath class constructor with default false (readonly)
# * Added is_writable() and get_last_modified_rfc7231() methods to HttpPath
# * Updated format_http_section() to use Union[str, HttpPath] instead of Union[str, Path]
# * Added Content-Writable header with true/false values based on writable flag
# * Replaced all Path object handling with HttpPath objects for consistency
# * Updated last_modified parameter to accept only HttpPath objects
# * Enhanced error handling and documentation for HttpPath integration
###############################################################################

import os
import datetime
from pathlib import Path
from typing import Dict, Optional, Union


class HttpStatus:
    """
    [Class intent]
    HTTP status code constants and utilities for standardized error handling.
    Provides common status codes and default messages for HTTP/1.1-like protocol.
    
    [Design principles]
    Standard HTTP status codes with consistent message mapping.
    Extensible design for additional status codes as needed.
    
    [Implementation details]
    Class constants for common HTTP status codes with utility method for default messages.
    """
    OK = 200
    CONTEXT_DEPENDENT = 240
    NOT_FOUND = 404
    FORBIDDEN = 403
    INTERNAL_SERVER_ERROR = 500
    
    @classmethod
    def get_default_message(cls, code: int) -> str:
        """
        [Class method intent]
        Get standard HTTP status message for given status code.
        
        [Design principles]
        Centralized mapping from status codes to standard HTTP messages.
        Unknown codes return generic message for graceful handling.
        
        [Implementation details]
        Dictionary lookup with fallback for unknown status codes.
        
        Args:
            code: HTTP status code integer
            
        Returns:
            Standard HTTP status message string
        """
        return {
            200: "OK",
            240: "Context Dependent Content",
            404: "Not Found", 
            403: "Forbidden",
            500: "Internal Server Error"
        }.get(code, "Unknown Status")


class HttpErrorHandler:
    """
    [Class intent]
    Generate standard error content and handle error scenarios for HTTP responses.
    Provides automatic error detection and standard error message templates.
    
    [Design principles]
    Consistent error content generation across all resource types.
    Automatic error detection from Python exception types.
    Template-based approach for maintainable error messages.
    
    [Implementation details]
    Error templates with format string substitution for dynamic content.
    Exception type mapping to appropriate HTTP status codes.
    """
    
    ERROR_TEMPLATES = {
        404: "Resource not found: {location}",
        403: "Access denied: {location}",
        500: "Internal server error: {detail}"
    }
    
    @classmethod
    def generate_error_content(cls, status_code: int, location: str, detail: str = "") -> str:
        """
        [Class method intent]
        Generate standard error content for HTTP status codes using templates.
        
        [Design principles]
        Template-based error content generation for consistency.
        Flexible parameter substitution for context-specific error messages.
        
        [Implementation details]
        Format string substitution with fallback template for unknown status codes.
        
        Args:
            status_code: HTTP status code for error type
            location: Resource location for error context
            detail: Additional error detail for context
            
        Returns:
            Formatted error content string
        """
        template = cls.ERROR_TEMPLATES.get(status_code, "Error {status_code}: {detail}")
        return template.format(status_code=status_code, location=location, detail=detail)
    
    @classmethod
    def detect_error_from_exception(cls, exc: Exception, location: str) -> tuple[int, str, str]:
        """
        [Class method intent]
        Auto-detect HTTP status code and generate error content from exception type.
        
        [Design principles]
        Automatic error classification based on Python exception types.
        Consistent mapping from filesystem errors to HTTP status codes.
        Complete error information tuple for easy consumption.
        
        [Implementation details]
        Exception type checking with fallback to 500 Internal Server Error.
        Uses generate_error_content for consistent error message formatting.
        
        Args:
            exc: Python exception to analyze
            location: Resource location for error context
            
        Returns:
            Tuple of (status_code, status_message, error_content)
        """
        if isinstance(exc, FileNotFoundError):
            return 404, HttpStatus.get_default_message(404), cls.generate_error_content(404, location)
        elif isinstance(exc, PermissionError):
            return 403, HttpStatus.get_default_message(403), cls.generate_error_content(403, location)
        else:
            return 500, HttpStatus.get_default_message(500), cls.generate_error_content(500, location, str(exc))


class ContentCriticality:
    """
    [Class intent]
    Content criticality levels for AI assistant processing priority and enforcement.
    Defines CRITICAL content that must be followed strictly vs INFORMATIONAL context.
    
    [Design principles]
    Simple enum-like class with validation for consistent criticality classification.
    Clear distinction between mandatory framework rules and helpful context information.
    
    [Implementation details]
    Two-level system: CRITICAL for framework rules/workflows, INFORMATIONAL for knowledge.
    Validation method ensures only valid criticality values are accepted.
    """
    CRITICAL = "CRITICAL"           # Must be followed strictly by AI assistants
    INFORMATIONAL = "INFORMATIONAL"  # Helpful context, not mandatory enforcement
    
    @classmethod
    def validate(cls, criticality: str) -> str:
        """
        [Class method intent]
        Validate and normalize criticality value to ensure only valid levels are used.
        
        [Design principles]
        Strict validation with immediate error on invalid input.
        Case-insensitive input with normalized uppercase output.
        
        [Implementation details]
        Checks criticality against valid class constants.
        Raises ValueError with descriptive message for invalid inputs.
        
        Args:
            criticality: Criticality level to validate
            
        Returns:
            Normalized uppercase criticality value
            
        Raises:
            ValueError: When criticality is not CRITICAL or INFORMATIONAL
        """
        if criticality.upper() not in [cls.CRITICAL, cls.INFORMATIONAL]:
            raise ValueError(
                f"Invalid criticality '{criticality}'. Must be '{cls.CRITICAL}' or '{cls.INFORMATIONAL}'"
            )
        return criticality.upper()


def resolve_portable_path(location: str) -> str:
    """
    [Function intent]
    Resolve portable path variables to actual filesystem paths for cross-platform compatibility.
    Transforms JESSE path variables into absolute paths for current environment.
    
    [Design principles]
    Cross-platform path resolution supporting all standard JESSE path variables.
    Immediate resolution without caching for current working directory accuracy.
    
    [Implementation details]
    Replaces {PROJECT_ROOT}, {HOME}, {CLINE_RULES}, {CLINE_WORKFLOWS} variables
    with actual resolved paths using pathlib for cross-platform compatibility.
    
    Args:
        location: Path string with variable placeholders
        
    Returns:
        Resolved absolute path with all variables substituted
        
    Raises:
        OSError: When path resolution fails due to filesystem issues
    """
    try:
        # Define path variable mappings
        variables = {
            '{PROJECT_ROOT}': str(Path.cwd()),
            '{HOME}': str(Path.home()),
            '{CLINE_RULES}': str(Path.home() / 'Cline' / 'Rules'),
            '{CLINE_WORKFLOWS}': str(Path.home() / 'Cline' / 'Workflows')
        }
        
        # Resolve all variables in the location
        resolved = location
        for variable, value in variables.items():
            resolved = resolved.replace(variable, value)
        
        return resolved
        
    except Exception as e:
        raise OSError(f"Failed to resolve portable path '{location}': {str(e)}")


class HttpPath:
    """
    [Class intent]
    Path-like object that maintains both original portable path string and resolved filesystem path.
    Enables Location headers to show portable paths while filesystem operations use resolved paths.
    Supports writable flag for Cline integration to indicate if content should be writable.
    
    [Design principles]
    Dual-path storage: original portable string for headers, resolved path for filesystem operations.
    Composition over inheritance for reliable Path functionality delegation.
    Writable flag is functional (not filesystem-based) for AI assistant content editing control.
    
    [Implementation details]
    Stores original_path (with variables) and contains Path object (resolved filesystem path).
    Uses existing resolve_portable_path() infrastructure for consistency and reliability.
    Writable flag defaults to false (readonly) for security and stability.
    """
    
    def __init__(self, path_with_variables: str, writable: bool = False):
        """
        [Class method intent]
        Create new HttpPath instance with resolved filesystem path and writable flag.
        
        [Design principles]
        Use composition to contain Path object with resolved path.
        Store original path separately for header generation needs.
        Writable flag is purely functional for AI assistant guidance, not filesystem permissions.
        Handle file:// URLs by extracting filesystem path while preserving original URL.
        
        [Implementation details]
        Resolves variables using existing resolve_portable_path() function.
        Creates internal Path object with resolved path, stores original for access.
        Stores writable flag with default false (readonly) for conservative content handling.
        Special handling for file:// URLs - extract filesystem path for operations.
        
        Args:
            path_with_variables: Path string containing JESSE framework variables
            writable: Whether content should be writable for Cline (default: False - readonly)
            
        Raises:
            OSError: When path resolution fails due to filesystem issues
        """
        # Store original path with variables
        self._original_path = path_with_variables
        
        # Store writable flag for Cline integration
        self._writable = writable
        
        # Resolve variables to get filesystem path
        resolved_path = resolve_portable_path(path_with_variables)
        
        # Handle different URL types
        if resolved_path.startswith('file://'):
            # For file:// URLs, extract filesystem path but keep original URL
            filesystem_path = resolved_path[7:]  # Remove 'file://' prefix
            self._resolved_path = Path(filesystem_path)
            self._resolved_path_str = resolved_path  # Keep full URL for debugging
        elif resolved_path.startswith(('http://', 'https://')):
            # For HTTP/HTTPS URLs, store as string (no filesystem operations)
            self._resolved_path_str = resolved_path
            self._resolved_path = None
        else:
            # For filesystem paths, use Path object
            self._resolved_path = Path(resolved_path)
            self._resolved_path_str = None
    
    def get_original_path(self) -> str:
        """
        [Function intent]
        Return the original path string with variables for Location headers.
        
        [Design principles]
        Provides access to unresolved portable path for header generation.
        Maintains separation between display path and filesystem path.
        
        [Implementation details]
        Returns stored original path string without variable resolution.
        
        Returns:
            Original path string containing JESSE framework variables
        """
        return self._original_path
    
    def get_resolved_path(self) -> str:
        """
        [Function intent]
        Return the resolved path string, consistent with str() representation.
        
        [Design principles]
        Consistent with __str__() method for predictable behavior.
        Complements get_original_path() for full path transparency.
        
        [Implementation details]
        Returns same result as str() conversion for consistency.
        
        Returns:
            Resolved path string, preserving URL format when applicable
        """
        return str(self)
    
    def is_writable(self) -> bool:
        """
        [Function intent]
        Return the functional writable flag for Cline integration.
        
        [Design principles]
        Functional flag independent of filesystem permissions for AI assistant guidance.
        Defaults to false (readonly) for conservative content handling and security.
        
        [Implementation details]
        Returns stored writable flag set during construction.
        
        Returns:
            True if content should be writable for Cline, False if readonly
        """
        return self._writable
    
    def get_last_modified_rfc7231(self) -> str:
        """
        [Function intent]
        Get RFC 7231 formatted timestamp from file modification time.
        
        [Design principles]
        Convenient method to get HTTP-compatible timestamp for Last-Modified headers.
        Uses file system modification time for accurate timestamps.
        
        [Implementation details]
        Reads file mtime using stat() method and converts to RFC 7231 format.
        Uses UTC timezone for consistent HTTP header formatting.
        
        Returns:
            RFC 7231 formatted timestamp string (e.g., "Fri, 28 Jun 2025 06:47:00 GMT")
            
        Raises:
            FileNotFoundError: When file does not exist
            PermissionError: When file cannot be accessed due to permissions
            OSError: When file access fails or path is URL (not supported)
        """
        if self._resolved_path is None:
            raise OSError(f"Cannot get modification time from URL: {self._resolved_path_str}")
        
        try:
            mod_time = self._resolved_path.stat().st_mtime
            # Convert Unix timestamp to RFC 7231 format
            dt = datetime.datetime.fromtimestamp(mod_time, tz=datetime.timezone.utc)
            return dt.strftime("%a, %d %b %Y %H:%M:%S GMT")
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found for Last-Modified: {self._resolved_path}")
        except PermissionError:
            raise PermissionError(f"Permission denied accessing file for Last-Modified: {self._resolved_path}")
        except OSError as e:
            raise OSError(f"Error accessing file for Last-Modified '{self._resolved_path}': {str(e)}")
    
    def __str__(self) -> str:
        """
        [Function intent]
        Return string representation of resolved path, preserving URL format when applicable.
        
        [Design principles]
        Default string conversion preserves URL format for file:// URLs.
        
        [Implementation details]
        Returns full URL for file:// paths, filesystem path for regular paths, URL string for HTTP/HTTPS.
        
        Returns:
            Resolved path as string, preserving URL format when applicable
        """
        if self._resolved_path is not None:
            # For file:// URLs, return the full URL, not just the filesystem path
            if self._resolved_path_str is not None:
                return self._resolved_path_str
            else:
                return str(self._resolved_path)
        else:
            return self._resolved_path_str
    
    def __truediv__(self, other):
        """
        [Function intent]
        Support path joining with / operator, returning new HttpPath.
        
        [Design principles]
        Path-like behavior for building new paths from existing HttpPath.
        
        [Implementation details]
        Creates new HttpPath with original path joined and resolved path joined.
        
        Args:
            other: Path component to join
            
        Returns:
            New HttpPath with joined paths
        """
        # Join original path for header display
        joined_original = f"{self._original_path}/{other}"
        return HttpPath(joined_original)
    
    # Delegate common Path methods to internal resolved path (filesystem paths and file:// URLs)
    def exists(self) -> bool:
        """Return True if path exists (filesystem paths and file:// URLs supported)."""
        if self._resolved_path is not None:
            return self._resolved_path.exists()
        else:
            # Non-file URLs (http://, https://) don't support filesystem existence checks
            return False
    
    def is_file(self) -> bool:
        """Return True if path is a file (only for filesystem paths, not URLs)."""
        if self._resolved_path is not None:
            return self._resolved_path.is_file()
        else:
            # URLs are not considered files in filesystem terms
            return False
    
    def is_dir(self) -> bool:
        """Return True if path is a directory (only for filesystem paths, not URLs)."""
        if self._resolved_path is not None:
            return self._resolved_path.is_dir()
        else:
            # URLs are not directories in filesystem terms
            return False
    
    def read_text(self, encoding='utf-8'):
        """Read and return file contents as text (only for filesystem paths, not URLs)."""
        if self._resolved_path is not None:
            return self._resolved_path.read_text(encoding=encoding)
        else:
            raise OSError(f"Cannot read text from URL: {self._resolved_path_str}")
    
    def stat(self):
        """Return stat result for the path (only for filesystem paths, not URLs)."""
        if self._resolved_path is not None:
            return self._resolved_path.stat()
        else:
            raise OSError(f"Cannot stat URL: {self._resolved_path_str}")
    
    @property
    def parent(self):
        """Return parent path as regular Path object (only for filesystem paths)."""
        if self._resolved_path is not None:
            return self._resolved_path.parent
        else:
            # For URLs, we could return a simplified parent, but it's better to be explicit
            raise OSError(f"Parent not supported for URL: {self._resolved_path_str}")
    
    @property
    def name(self):
        """Return final component of the path."""
        if self._resolved_path is not None:
            return self._resolved_path.name
        else:
            # For URLs, extract the last path component
            if '/' in self._resolved_path_str:
                return self._resolved_path_str.split('/')[-1]
            else:
                return self._resolved_path_str
    
    @property
    def suffix(self):
        """Return file suffix."""
        if self._resolved_path is not None:
            return self._resolved_path.suffix
        else:
            # For URLs, extract suffix from the last path component
            name = self.name
            if '.' in name:
                return '.' + name.split('.')[-1]
            else:
                return ''
    
    def __repr__(self) -> str:
        """Return repr showing both original and resolved paths."""
        resolved = self.get_resolved_path()
        return f"HttpPath(original='{self._original_path}', resolved='{resolved}')"


def _detect_status_and_content(
    content: Union[str, 'HttpPath'],
    location: Union[str, 'HttpPath'],
    status_code: Optional[int],
    status_message: Optional[str], 
    error_content: Optional[str]
) -> tuple[int, str, str]:
    """
    [Function intent]
    Auto-detect HTTP status and content, with override support.
    Returns tuple of (status_code, status_message, actual_content).
    
    [Design principles]
    Automatic error detection with complete override capability.
    Consistent error handling across all resource types.
    Priority: manual overrides > auto-detection > default success.
    
    [Implementation details]
    Handles manual status/content overrides first, then attempts content loading.
    Auto-detects errors from exceptions during content loading.
    Preserves existing content loading logic with enhanced error handling.
    
    Args:
        content: The content to process (string or HttpPath)
        location: Resource location for error context
        status_code: Optional manual status code override
        status_message: Optional manual status message override
        error_content: Optional manual error content override
        
    Returns:
        Tuple of (final_status_code, final_status_message, final_content)
        
    Raises:
        TypeError: When content parameter type is invalid (always raised)
        ValueError: When content is empty string (only raised if no status override)
    """
    # Validate content type first - this always raises exception for invalid types
    if not isinstance(content, (str, HttpPath)):
        raise TypeError(f"content must be str or HttpPath, got {type(content).__name__}")
    
    # Handle manual overrides first
    if status_code is not None:
        final_status = status_code
        final_message = status_message or HttpStatus.get_default_message(status_code)
        
        if error_content is not None:
            return final_status, final_message, error_content
        elif status_code >= 400:
            # Generate default error content for error codes
            location_str = location.get_original_path() if isinstance(location, HttpPath) else location
            final_content = HttpErrorHandler.generate_error_content(status_code, location_str)
            return final_status, final_message, final_content
    
    # Handle empty string content - always raise ValueError unless status override
    if isinstance(content, str) and not content and status_code is None:
        raise ValueError("Content cannot be empty")
    
    # Auto-detect from content loading
    try:
        if isinstance(content, str):
            actual_content = content
        elif isinstance(content, HttpPath):
            actual_content = content.read_text(encoding='utf-8')
            if not actual_content and status_code is None:
                raise ValueError("Content cannot be empty")
        
        # Success case
        final_status = status_code or 200
        final_message = status_message or HttpStatus.get_default_message(final_status)
        return final_status, final_message, actual_content
        
    except ValueError as validation_exc:
        # ValueError should be raised for validation issues when no status override
        if status_code is None:
            raise validation_exc
        # With status override, treat as any other exception
        final_status = status_code
        final_message = status_message or HttpStatus.get_default_message(status_code)
        if error_content is not None:
            final_content = error_content
        else:
            location_str = location.get_original_path() if isinstance(location, HttpPath) else location
            final_content = HttpErrorHandler.generate_error_content(final_status, location_str, str(validation_exc))
        return final_status, final_message, final_content
        
    except Exception as exc:
        # Auto-detect error status (only for non-validation errors when no status override)
        if status_code is None:
            location_str = location.get_original_path() if isinstance(location, HttpPath) else location
            auto_status, auto_message, auto_content = HttpErrorHandler.detect_error_from_exception(exc, location_str)
            final_status = auto_status
            final_message = status_message or auto_message
            final_content = error_content or auto_content
        else:
            # Manual status with auto error content
            final_status = status_code
            final_message = status_message or HttpStatus.get_default_message(status_code)
            if error_content is not None:
                final_content = error_content
            else:
                location_str = location.get_original_path() if isinstance(location, HttpPath) else location
                final_content = HttpErrorHandler.generate_error_content(final_status, location_str, str(exc))
        
        return final_status, final_message, final_content


def format_http_section(
    content: Union[str, 'HttpPath'],
    content_type: str,
    criticality: str,
    description: str,
    section_type: str,
    location: Union[str, 'HttpPath'],
    additional_headers: Optional[Dict[str, str]] = None,
    last_modified: Optional[Union[str, 'HttpPath']] = None,
    writable: bool = False,
    # NEW HTTP/1.1 Parameters
    status_code: Optional[int] = None,        # Auto-detect or override
    status_message: Optional[str] = None,     # Auto-generate or override  
    error_content: Optional[str] = None       # Custom error messages
) -> str:
    """
    [Function intent]
    Format any content with standardized HTTP/1.1-like headers and boundary markers.
    Creates consistent, parseable multi-part content sections for MCP resource delivery.
    Supports HTTP status codes, automatic error detection, and complete override capabilities.
    
    [Design principles]
    Universal formatter supporting all MCP resource content types with HTTP/1.1-like protocol structure.
    Automatic error detection with complete override capability for all aspects.
    Header ordering: Content-Location and Content-Length first for improved parsing.
    Writable flag provides functional control over content editability independent of filesystem permissions.
    
    [Implementation details]
    Uses _detect_status_and_content for automatic error detection and override handling.
    Calculates precise UTF-8 byte length for Content-Length header accuracy.
    Uses new HTTP boundary markers with X-ASYNC-HTTP/1.1 status line.
    Validates criticality level and resolves portable paths before formatting.
    
    Args:
        content: The actual content to format (string) or HttpPath object to read content from
        content_type: MIME type (text/markdown, application/json, etc.)
        criticality: CRITICAL or INFORMATIONAL classification
        description: Human-readable content description
        section_type: Type classification (workflow, knowledge-base, etc.)
        location: Portable file path with variables (string) or HttpPath object
        additional_headers: Optional extra headers for extensibility
        last_modified: Optional HttpPath object for Last-Modified header
        writable: Whether content should be writable for Cline (default: False - readonly)
        status_code: Optional HTTP status code override (auto-detect if None)
        status_message: Optional HTTP status message override (auto-generate if None)
        error_content: Optional custom error content override
        
    Returns:
        Complete HTTP/1.1-like formatted section with headers and content
        
    Raises:
        ValueError: When required parameters are invalid or empty
        TypeError: When content parameter type is invalid
        FileNotFoundError: When HttpPath content file does not exist (if no overrides)
        PermissionError: When HttpPath content file cannot be read due to permissions (if no overrides)
        OSError: When path resolution fails or file access errors occur (if no overrides)
    """
    # 1. Auto-detect or use provided status and content
    final_status, final_status_message, actual_content = _detect_status_and_content(
        content, location, status_code, status_message, error_content
    )
    
    # 2. Input validation for remaining parameters
    if not content_type:
        raise ValueError("Content-Type must be specified")
    if not description:
        raise ValueError("Content-Description must be specified")
    if not section_type:
        raise ValueError("Content-Section must be specified")
    if not location:
        raise ValueError("Content-Location must be specified")
    
    # 3. Validate and normalize criticality
    validated_criticality = ContentCriticality.validate(criticality)
    
    # 4. Handle location parameter for headers
    if isinstance(location, HttpPath):
        # HttpPath objects preserve variables for cross-platform portability
        location_for_header = location.get_original_path()
    else:
        # String locations also preserve variables for cross-platform portability
        location_for_header = location
    
    # 5. Calculate precise content length
    content_bytes = actual_content.encode('utf-8')
    content_length = len(content_bytes)
    
    # 6. Determine writable flag (prioritize HttpPath if content was HttpPath)
    if isinstance(content, HttpPath):
        content_writable = content.is_writable()
    else:
        content_writable = writable
    
    # 7. Build headers in NEW ORDER (Content-Location and Content-Length first)
    from ..constants import HTTP_BOUNDARY_MARKER
    headers = [
        HTTP_BOUNDARY_MARKER,
        f"X-ASYNC-HTTP/1.1 {final_status} {final_status_message}",
        f"Content-Location: {location_for_header}",
        f"Content-Length: {content_length}",
        f"Content-Type: {content_type}",
        f"Content-Criticality: {validated_criticality}",
        f"Content-Description: {description}",
        f"Content-Section: {section_type}",
        f"Content-Writable: {'true' if content_writable else 'false'}"
    ]
    
    # 8. Add Last-Modified header (preserve existing logic, but skip for error responses)
    effective_last_modified = last_modified
    if isinstance(content, HttpPath) and last_modified is None and final_status < 400:
        # Only auto-add Last-Modified from content HttpPath if this is a success response
        effective_last_modified = content
    
    if effective_last_modified is not None:
        if isinstance(effective_last_modified, str):
            if not effective_last_modified or not effective_last_modified.strip():
                raise ValueError("Last-Modified header cannot be empty or whitespace")
            timestamp_str = effective_last_modified
        elif isinstance(effective_last_modified, HttpPath):
            try:
                timestamp_str = effective_last_modified.get_last_modified_rfc7231()
            except FileNotFoundError:
                raise FileNotFoundError(f"File not found for Last-Modified header: {effective_last_modified}")
            except PermissionError:
                raise PermissionError(f"Permission denied accessing file for Last-Modified header: {effective_last_modified}")
            except OSError as e:
                raise OSError(f"Error accessing file for Last-Modified header '{effective_last_modified}': {str(e)}")
        else:
            raise TypeError(f"last_modified must be str or HttpPath, got {type(effective_last_modified).__name__}")
        
        headers.append(f"Last-Modified: {timestamp_str}")
    
    # 9. Add additional headers (preserve existing logic)
    if additional_headers:
        for header_name, header_value in additional_headers.items():
            if not header_name or not header_value:
                raise ValueError(f"Invalid additional header: '{header_name}': '{header_value}'")
            headers.append(f"{header_name}: {header_value}")
    
    # 10. Combine headers and content
    headers.append("")  # Empty line separator
    formatted_section = "\n".join(headers) + actual_content
    
    return formatted_section


def format_multi_section_response(*sections: str, preambule: Optional[str] = None) -> str:
    """
    [Function intent]
    Combine multiple HTTP-formatted sections into a single multi-part response with optional preambule.
    Creates complete MCP resource responses with protocol definition and multiple content sections.
    
    [Design principles]
    Optional preambule wrapped in XML tags for contextual information outside HTTP protocol.
    Self-documenting protocol definition explains X-ASYNC-HTTP/1.1 format to readers.
    Simple concatenation of pre-formatted sections with section separators.
    Maintains individual section integrity while creating cohesive responses.
    
    [Implementation details]
    Places preambule first (if provided) wrapped in <preambule></preambule> XML tags.
    Includes X-ASYNC-HTTP/1.1 protocol definition after preambule and before first section.
    Joins sections with double newlines for clear visual separation.
    Assumes all sections are already properly HTTP-formatted.
    
    Args:
        *sections: Variable number of HTTP-formatted section strings
        preambule: Optional contextual text placed before protocol definition
        
    Returns:
        Combined multi-part response string with optional preambule and protocol definition
        
    Raises:
        ValueError: When no sections provided or sections are empty
    """
    if not sections:
        raise ValueError("At least one section must be provided")
    
    # Validate all sections are non-empty
    for i, section in enumerate(sections):
        if not section or not section.strip():
            raise ValueError(f"Section {i} is empty or contains only whitespace")
    
    # Build response components
    response_parts = []
    
    # 1. Add preambule if provided
    if preambule is not None and preambule.strip():
        response_parts.append(f"<preambule>\n{preambule.strip()}\n</preambule>")
    
    # 2. Add X-ASYNC-HTTP/1.1 protocol definition
    protocol_definition = """=== X-ASYNC-HTTP/1.1 PROTOCOL DEFINITION ===

This response uses a pseudo-HTTP/1.1 protocol for structured multi-part content delivery:

STRUCTURE:
- Each section begins with boundary marker: --- ASYNC-HTTP-SECTION-START-v20250628
- Status line format: X-ASYNC-HTTP/1.1 {code} {message}
- Headers follow HTTP/1.1 conventions with JESSE-specific extensions
- Empty line separates headers from content body
- Content is UTF-8 encoded with byte-accurate Content-Length

KEY HEADERS:
- Content-Location: Portable path with {PROJECT_ROOT}, {HOME} variables
- Content-Length: Exact UTF-8 byte count for precise parsing
- Content-Type: MIME type (text/markdown, application/json, etc.)
- Content-Criticality: CRITICAL (must follow) vs INFORMATIONAL (context only)
- Content-Description: Human-readable content summary
- Content-Section: Type classification (workflow, knowledge-base, etc.)
- Content-Writable: true/false indicating if content should be editable
- Last-Modified: RFC 7231 timestamp when available

STATUS CODES:
- 200 OK: Content successfully loaded and available
- 240 Context Dependent Content: Task-specific content, never persist in knowledge bases
- 403 Forbidden: Access denied to resource
- 404 Not Found: Resource does not exist
- 500 Internal Server Error: Processing failure

CRITICALITY LEVELS:
- CRITICAL: Framework rules and workflows that must be strictly followed
- INFORMATIONAL: Knowledge base content and contextual information

PATH VARIABLES:
- {PROJECT_ROOT}: Current working directory
- {HOME}: User home directory  
- {CLINE_RULES}: Global Cline rules directory
- {CLINE_WORKFLOWS}: Global Cline workflows directory

PARSING NOTES:
- Sections are independent - process each separately
- Content-Length enables binary-safe content handling
- Boundary markers allow reliable section separation
- Status codes indicate processing requirements and content persistence rules"""
    
    response_parts.append(protocol_definition)
    
    # 3. Add all HTTP sections
    response_parts.extend(sections)
    
    # 4. Join all parts with double newlines for clear separation
    return "\n\n".join(response_parts)
