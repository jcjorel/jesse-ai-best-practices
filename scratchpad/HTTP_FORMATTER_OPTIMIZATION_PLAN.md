# HTTP Formatter Optimization Implementation Plan
**Version**: v20250628 (HTTP/1.1-like Protocol Migration)
**Type**: Breaking Changes - Complete Migration
**Date**: 2025-06-29

## Executive Summary

Transform the JESSE Framework MCP HTTP formatter from custom boundary format to HTTP/1.1-like protocol structure with automatic error handling, complete override capabilities, and optimized header ordering.

## Current vs Target Format

### Current Format
```
--JESSE_FRAMEWORK_BOUNDARY_2025--
Content-Type: text/markdown
Content-Length: 18866
Content-Criticality: CRITICAL
Content-Description: Knowledge Management System Rules and Directives
Content-Section: framework-rule
Content-Location: file://{CLINE_RULES}/JESSE_KNOWLEDGE_MANAGEMENT.md
Content-Writable: false

<content>
```

### Target Format
```
--- ASYNC-HTTP-SECTION-START-v20250628
X-ASYNC-HTTP/1.1 200 OK
Content-Location: file://{PROJECT_ROOT}/.knowledge/git-clones/.gitignore
Content-Length: 1431
Content-Type: text/markdown
Content-Criticality: CRITICAL
Content-Description: Knowledge Management System Rules and Directives
Content-Section: framework-rule
Content-Writable: false
<other_headers>

<content_with_size_of_content_length>
```

## Implementation Phases

### Phase 1: Constants and Error Infrastructure
**Files**: `constants.py`, `http_formatter.py` (new classes only)
**Duration**: Foundation setup
**Risk**: Low - No breaking changes yet

#### 1.1 Update HTTP Constants
```python
# constants.py changes
HTTP_BOUNDARY = "ASYNC-HTTP-SECTION-START-v20250628"
HTTP_BOUNDARY_MARKER = f"--- {HTTP_BOUNDARY}"
```

#### 1.2 Add HTTP Error Infrastructure
```python
# http_formatter.py - New classes
class HttpStatus:
    """HTTP status code constants and utilities."""
    OK = 200
    NOT_FOUND = 404
    FORBIDDEN = 403
    INTERNAL_SERVER_ERROR = 500
    
    @classmethod
    def get_default_message(cls, code: int) -> str:
        """Get standard HTTP status message for code."""
        return {
            200: "OK",
            404: "Not Found", 
            403: "Forbidden",
            500: "Internal Server Error"
        }.get(code, "Unknown Status")

class HttpErrorHandler:
    """Generate standard error content and handle error scenarios."""
    
    ERROR_TEMPLATES = {
        404: "Resource not found: {location}",
        403: "Access denied: {location}",
        500: "Internal server error: {detail}"
    }
    
    @classmethod
    def generate_error_content(cls, status_code: int, location: str, detail: str = "") -> str:
        """Generate standard error content for HTTP status codes."""
        template = cls.ERROR_TEMPLATES.get(status_code, "Error {status_code}: {detail}")
        return template.format(status_code=status_code, location=location, detail=detail)
    
    @classmethod
    def detect_error_from_exception(cls, exc: Exception, location: str) -> tuple[int, str, str]:
        """Auto-detect HTTP status code from exception type."""
        if isinstance(exc, FileNotFoundError):
            return 404, HttpStatus.get_default_message(404), cls.generate_error_content(404, location)
        elif isinstance(exc, PermissionError):
            return 403, HttpStatus.get_default_message(403), cls.generate_error_content(403, location)
        else:
            return 500, HttpStatus.get_default_message(500), cls.generate_error_content(500, location, str(exc))
```

### Phase 2: Core Formatter Transformation
**Files**: `http_formatter.py` (format_http_section function)
**Duration**: Core implementation
**Risk**: High - Breaking changes begin

#### 2.1 Enhanced Function Signature
```python
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
```

#### 2.2 Auto-Detection Logic
```python
def _detect_status_and_content(
    content: Union[str, 'HttpPath'],
    location: Union[str, 'HttpPath'],
    status_code: Optional[int],
    status_message: Optional[str], 
    error_content: Optional[str]
) -> tuple[int, str, str]:
    """
    Auto-detect HTTP status and content, with override support.
    Returns: (status_code, status_message, actual_content)
    """
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
    
    # Auto-detect from content loading
    try:
        if isinstance(content, str):
            actual_content = content
            if not actual_content:
                raise ValueError("Content cannot be empty")
        elif isinstance(content, HttpPath):
            actual_content = content.read_text(encoding='utf-8')
            if not actual_content:
                raise ValueError("Content cannot be empty")
        else:
            raise TypeError(f"content must be str or HttpPath, got {type(content).__name__}")
        
        # Success case
        final_status = status_code or 200
        final_message = status_message or HttpStatus.get_default_message(final_status)
        return final_status, final_message, actual_content
        
    except Exception as exc:
        # Auto-detect error status
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
```

#### 2.3 New Header Structure Implementation
```python
def format_http_section(...) -> str:
    """Enhanced format_http_section with HTTP/1.1-like protocol support."""
    
    # 1. Auto-detect or use provided status and content
    status_code, status_message, actual_content = _detect_status_and_content(
        content, location, status_code, status_message, error_content
    )
    
    # 2. Validate remaining parameters (same as before)
    if not content_type:
        raise ValueError("Content-Type must be specified")
    # ... other validations
    
    # 3. Validate and normalize criticality
    validated_criticality = ContentCriticality.validate(criticality)
    
    # 4. Handle location parameter for headers
    if isinstance(location, HttpPath):
        location_for_header = location.get_original_path()
    else:
        location_for_header = location
    
    # 5. Calculate precise content length
    content_bytes = actual_content.encode('utf-8')
    content_length = len(content_bytes)
    
    # 6. Build headers in NEW ORDER (Content-Location and Content-Length first)
    headers = [
        f"--- {HTTP_BOUNDARY}",
        f"X-ASYNC-HTTP/1.1 {status_code} {status_message}",
        f"Content-Location: {location_for_header}",
        f"Content-Length: {content_length}",
        f"Content-Type: {content_type}",
        f"Content-Criticality: {validated_criticality}",
        f"Content-Description: {description}",
        f"Content-Section: {section_type}",
        f"Content-Writable: {'true' if content_writable else 'false'}"
    ]
    
    # 7. Add Last-Modified (same logic as before)
    # ... existing Last-Modified logic
    
    # 8. Add additional headers (same as before)
    # ... existing additional headers logic 
    
    # 9. Combine headers and content
    headers.append("")  # Empty line separator
    formatted_section = "\n".join(headers) + actual_content
    
    return formatted_section
```

### Phase 3: Test Suite Complete Overhaul
**Files**: `tests/test_http_formatting.py`
**Duration**: Comprehensive test updates
**Risk**: Medium - Ensure no functionality regression

#### 3.1 Boundary Marker Updates
```python
# Update all test assertions from:
assert HTTP_BOUNDARY_MARKER in result
# To:
assert "--- ASYNC-HTTP-SECTION-START-v20250628" in result
```

#### 3.2 Status Line Test Coverage
```python
class TestHttpStatusLines:
    """Test HTTP/1.1-like status line functionality."""
    
    def test_default_200_ok_status(self):
        """Test default 200 OK status for successful content."""
        content = "Test content"
        result = format_http_section(...)
        assert "X-ASYNC-HTTP/1.1 200 OK" in result
    
    def test_manual_status_override(self):
        """Test manual status code override."""
        result = format_http_section(..., status_code=201, status_message="Created")
        assert "X-ASYNC-HTTP/1.1 201 Created" in result
    
    def test_automatic_404_detection(self):
        """Test automatic 404 for missing HttpPath files."""
        missing_path = HttpPath("/non/existent/file.md")
        result = format_http_section(content=missing_path, ...)
        assert "X-ASYNC-HTTP/1.1 404 Not Found" in result
        assert "Resource not found:" in result
    
    def test_automatic_403_detection(self):
        """Test automatic 403 for permission denied files."""
        # Implementation with permission testing
    
    def test_error_content_override(self):
        """Test custom error content override."""
        result = format_http_section(
            content=missing_path,
            ...,
            status_code=503,
            status_message="Service Unavailable",
            error_content="Custom maintenance message"
        )
        assert "X-ASYNC-HTTP/1.1 503 Service Unavailable" in result
        assert "Custom maintenance message" in result
```

#### 3.3 Header Order Test Updates
```python
def test_header_ordering_content_location_first(self):
    """Test new header ordering with Content-Location and Content-Length first."""
    result = format_http_section(...)
    
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
    
    # Verify ordering
    assert status_line < content_location_line < content_length_line < content_type_line
```

### Phase 4: Resource File Updates
**Files**: All files using http_formatter (6+ files)
**Duration**: Integration updates
**Risk**: Low - Mostly signature compatible

#### 4.1 Files Requiring Updates
- `resources/knowledge.py`
- `resources/project_resources.py` 
- `resources/framework_rules.py`
- `resources/session_init.py`
- `resources/workflows.py`
- `resources/wip_tasks.py`
- `helpers/project_root.py`
- `main.py`

#### 4.2 Update Strategy
Most files will work unchanged due to backwards-compatible function signature. Only constants import needs update:

```python
# Update imports from:
from ..constants import HTTP_BOUNDARY_MARKER
# To:
from ..constants import HTTP_BOUNDARY_MARKER  # Same import, new value
```

Special cases requiring manual updates:
- Any hardcoded boundary references
- Any parsing logic expecting old format
- Any tests within resource files

### Phase 5: Integration Testing and Validation
**Files**: All project files
**Duration**: Comprehensive validation
**Risk**: Low - Verification phase

#### 5.1 Test Execution Strategy
```bash
# Phase 5.1: Run existing test suite
cd jesse-framework-mcp
uv run python -m pytest tests/test_http_formatting.py -v

# Phase 5.2: Run integration tests
uv run python test_project_root.py --dump

# Phase 5.3: Test individual resources
uv run python test_session_init_resource.py
uv run python test_gitignore_resource.py
uv run python test_new_resources.py

# Phase 5.4: Full system test
uv run python -m pytest tests/ -v
```

#### 5.2 Validation Checklist
- [ ] All 58 HTTP formatting tests pass
- [ ] Session initialization works with new format
- [ ] Error scenarios generate proper HTTP status codes
- [ ] Content-Length remains byte-accurate
- [ ] Multi-section responses maintain coherence
- [ ] HttpPath integration works unchanged
- [ ] All resource endpoints return new format
- [ ] No performance regression in large content

## Risk Mitigation

### High-Risk Items
1. **Test Suite Updates**: 58 tests need boundary marker updates
   - **Mitigation**: Systematic find/replace with verification
   
2. **Content-Length Accuracy**: Must remain byte-perfect
   - **Mitigation**: Preserve existing calculation logic exactly

3. **HttpPath Integration**: Complex dual-path functionality  
   - **Mitigation**: No changes to HttpPath class, only formatter output

### Medium-Risk Items
1. **Resource File Integration**: 6+ files use the formatter
   - **Mitigation**: Backwards-compatible function signature

2. **Error Handling Changes**: New auto-detection logic
   - **Mitigation**: Comprehensive test coverage for all error scenarios

### Low-Risk Items
1. **Constants Updates**: Simple value changes
2. **Header Reordering**: Structural change only
3. **Status Line Addition**: Pure addition, no replacement

## Success Criteria

### Functional Requirements
- ✅ New HTTP/1.1-like format with status lines
- ✅ Automatic error detection (404, 403, 500)
- ✅ Complete override capability for all aspects
- ✅ Header ordering: Content-Location and Content-Length first
- ✅ Byte-perfect Content-Length calculation preserved
- ✅ All existing functionality maintained

### Technical Requirements  
- ✅ All 58 existing tests updated and passing
- ✅ New test coverage for HTTP status functionality
- ✅ No performance regression
- ✅ No breaking changes to HttpPath class
- ✅ Session initialization works with new format
- ✅ All resource endpoints return new format

### Quality Requirements
- ✅ Comprehensive error handling with standard HTTP codes
- ✅ Clear documentation and examples
- ✅ Maintainable code structure
- ✅ Consistent behavior across all resources

## Implementation Timeline

### Phase 1 (Foundation): 30 minutes
- Update constants.py
- Add HttpStatus and HttpErrorHandler classes
- No breaking changes yet

### Phase 2 (Core Changes): 60 minutes  
- Transform format_http_section function
- Implement auto-detection logic
- Add new header structure
- **Breaking changes begin**

### Phase 3 (Test Updates): 90 minutes
- Update all 58 test assertions
- Add new HTTP status test coverage
- Update boundary marker expectations
- Verify all tests pass

### Phase 4 (Integration): 30 minutes
- Update resource file imports
- Verify session initialization
- Test all endpoints

### Phase 5 (Validation): 45 minutes
- Run comprehensive test suite
- Performance validation
- Error scenario verification
- Documentation updates

**Total Estimated Duration**: 4.5 hours

## Error Scenario Examples

### Example 1: Auto-404 Detection
```python
# Code
missing_file = HttpPath("/non/existent/file.md")
result = format_http_section(
    content=missing_file,
    content_type="text/markdown",
    criticality="INFORMATIONAL",
    description="Missing Resource",
    section_type="error-section",
    location="file://{PROJECT_ROOT}/missing.md"
)

# Output
--- ASYNC-HTTP-SECTION-START-v20250628
X-ASYNC-HTTP/1.1 404 Not Found
Content-Location: file://{PROJECT_ROOT}/missing.md
Content-Length: 43
Content-Type: text/plain
Content-Criticality: INFORMATIONAL
Content-Description: Error Loading Resource
Content-Section: error-section
Content-Writable: false

Resource not found: file://{PROJECT_ROOT}/missing.md
```

### Example 2: Manual Override
```python
# Code
result = format_http_section(
    content="Service temporarily unavailable",
    content_type="text/plain",
    criticality="CRITICAL",
    description="Service Status",
    section_type="error-section",
    location="service://maintenance/",
    status_code=503,
    status_message="Service Unavailable",
    error_content="System maintenance in progress. Please try again later."
)

# Output
--- ASYNC-HTTP-SECTION-START-v20250628
X-ASYNC-HTTP/1.1 503 Service Unavailable
Content-Location: service://maintenance/
Content-Length: 67
Content-Type: text/plain
Content-Criticality: CRITICAL
Content-Description: Service Status
Content-Section: error-section
Content-Writable: false

System maintenance in progress. Please try again later.
```

### Example 3: Success Case
```bash
# Code
result = format_http_section(
    content="# JESSE Framework\nThis is working content.",
    content_type="text/markdown",
    criticality="CRITICAL",
    description="Framework Documentation",  
    section_type="framework-rule",
    location="file://{CLINE_RULES}/JESSE_FRAMEWORK.md"
)

# Output
--- ASYNC-HTTP-SECTION-START-v20250628
X-ASYNC-HTTP/1.1 200 OK
Content-Location: file://{CLINE_RULES}/JESSE_FRAMEWORK.md
Content-Length: 48
Content-Type: text/markdown
Content-Criticality: CRITICAL
Content-Description: Framework Documentation
Content-Section: framework-rule
Content-Writable: false

# JESSE Framework
This is working content.
```

## Files to Modify Summary

### Core Changes (Breaking)
1. `jesse_framework_mcp/constants.py` - Update HTTP_BOUNDARY
2. `jesse_framework_mcp/helpers/http_formatter.py` - Complete function rewrite
3. `tests/test_http_formatting.py` - Update all 58 tests

### Integration Updates (Compatible)
4. `jesse_framework_mcp/resources/knowledge.py` - Verify imports
5. `jesse_framework_mcp/resources/project_resources.py` - Verify imports
6. `jesse_framework_mcp/resources/framework_rules.py` - Verify imports
7. `jesse_framework_mcp/resources/session_init.py` - Verify imports
8. `jesse_framework_mcp/resources/workflows.py` - Verify imports
9. `jesse_framework_mcp/resources/wip_tasks.py` - Verify imports and boundary usage
10. `jesse_framework_mcp/helpers/project_root.py` - Verify imports
11. `jesse_framework_mcp/main.py` - Verify imports

### Test Integration
12. All demo files (`demo_*.py`) - Update for new format
13. All test files (`test_*.py`) - Verify integration

## Next Steps

This plan provides the complete roadmap for implementing HTTP/1.1-like protocol support in the JESSE Framework MCP HTTP formatter. The implementation maintains all existing functionality while adding comprehensive error handling and override capabilities.

**Ready for implementation approval and execution.**
