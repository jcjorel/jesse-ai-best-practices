<!-- CACHE_METADATA_START -->
<!-- Source File: {PROJECT_ROOT}/jesse-framework-mcp/utils.py -->
<!-- Cached On: 2025-07-05T14:49:46.905581 -->
<!-- Source Modified: 2025-06-28T10:03:54.492665 -->
<!-- Cache Version: 1.0 -->
<!-- CACHE_METADATA_END -->

#### Functional Intent & Features

This file implements FastMCP function unwrapping utilities for testing and development support, providing direct access to original functions from FastMCP decorated objects without MCP protocol overhead. The module enables developers to extract and validate underlying callable implementations from FastMCP wrapper objects for testing, debugging, and development workflows. Key semantic entities include primary function `unwrap_fastmcp_function()` for extracting original functions from decorated objects, helper functions `_is_fastmcp_wrapper()` and `_try_class_specific_extraction()` for wrapper detection and class-specific extraction patterns, metadata function `get_function_metadata()` for comprehensive function analysis, validation function `validate_fastmcp_function()` for FastMCP compatibility checking, imported modules `inspect` for function signature validation, `typing` for type hints and annotations, and `functools` for function metadata preservation, FastMCP wrapper types including `FunctionResource`, `FunctionTool`, and `FunctionPrompt`, function attribute patterns `fn`, `_func`, `__wrapped__`, `func`, `_function`, `handler`, `_handler`, `callback`, `_callback`, and `read` for extraction, exception types `TypeError`, `AttributeError`, and `ValueError` for comprehensive error handling, and validation parameters including `expected_context_param` for Context parameter checking. The system implements defensive programming with comprehensive error handling and descriptive messages while supporting all FastMCP decorator types with type safety and fallback mechanisms.

##### Main Components

The file contains four primary functions and two helper functions providing comprehensive FastMCP function unwrapping and validation capabilities. The `unwrap_fastmcp_function()` function serves as the main entry point for extracting original functions from FastMCP decorated objects with multi-pattern support. The `get_function_metadata()` function extracts comprehensive metadata from functions for debugging and validation including signature, docstring, and module information. The `validate_fastmcp_function()` function validates functions against FastMCP requirements checking async patterns, Context parameters, and documentation standards. Helper functions include `_is_fastmcp_wrapper()` for detecting FastMCP wrapper types based on class name patterns and attributes, and `_try_class_specific_extraction()` for attempting class-specific function extraction patterns for different FastMCP wrapper types. The module provides comprehensive support for `FunctionResource`, `FunctionTool`, and `FunctionPrompt` wrapper types with fallback mechanisms for unknown wrapper patterns.

###### Architecture & Design

The architecture implements a multi-pattern extraction system with defensive programming principles, following clean separation between MCP protocol handling and direct function access with comprehensive error handling and type safety validation. The design emphasizes support for all FastMCP decorator types through attribute inspection and class-specific extraction patterns, robust wrapper detection using multiple heuristics, and comprehensive validation with clear guidance for fixing issues. Key design patterns include the extraction pattern with multiple attribute attempts for different FastMCP wrapper storage mechanisms, validation pattern providing detailed compatibility checking with specific recommendations, helper pattern separating wrapper detection and class-specific extraction logic, metadata pattern extracting comprehensive function information for analysis, and fallback pattern providing graceful degradation for unknown wrapper types. The system uses composition over inheritance with specialized functions for different aspects, comprehensive error handling with descriptive messages, and type safety with proper validation throughout the extraction process.

####### Implementation Approach

The implementation uses attribute inspection algorithms with systematic attempts through predefined function attribute lists including `fn`, `_func`, `__wrapped__`, `func`, `_function`, `handler`, `_handler`, `callback`, `_callback`, and `read` for comprehensive extraction coverage. Wrapper detection employs class name pattern matching for FastMCP types and attribute presence checking for common wrapper characteristics. The approach implements class-specific extraction patterns for `Resource`, `Tool`, and `Prompt` wrapper types with dedicated attribute attempts for each category. Function validation uses `inspect.signature()` for parameter analysis and `inspect.iscoroutinefunction()` for async pattern verification. Error handling employs specific exception types with detailed error messages including available attributes and extraction methods for debugging support. Metadata extraction combines `inspect` module functions for signature, documentation, and source information with safe fallbacks for missing attributes. Type safety validation ensures extracted objects are callable with proper signature patterns before returning results.

######## External Dependencies & Integration Points

**→ Inbound:**
- `inspect` (external library) - function signature validation, metadata extraction, and source code analysis for comprehensive function introspection
- `typing` (external library) - type hints and annotations including Any, Callable, Union for comprehensive type safety
- `functools` (external library) - function metadata preservation and wrapper utilities for maintaining function characteristics

**← Outbound:**
- FastMCP resource handlers - consuming `unwrap_fastmcp_function()` for direct function access during testing and development workflows
- Testing frameworks - using extracted functions for unit testing without MCP protocol overhead
- Development tools - accessing function metadata and validation results for debugging and analysis
- Session initialization systems - using function unwrapping for direct function invocation and compatibility checking
- Resource validation systems - consuming validation functions for FastMCP compliance verification

**⚡ System role and ecosystem integration:**
- **System Role**: Development and testing utility for Jesse Framework MCP Server ecosystem, providing direct access to underlying function implementations from FastMCP decorated objects for testing, debugging, and development workflows
- **Ecosystem Position**: Support utility serving development and testing needs, enabling direct function access without MCP protocol complexity while maintaining compatibility with all FastMCP decorator patterns
- **Integration Pattern**: Used by developers for testing FastMCP resources directly, consumed by testing frameworks for unit test execution, integrated with development workflows for function analysis and validation, and coordinated with FastMCP decorators for seamless function extraction across different wrapper types

######### Edge Cases & Error Handling

The system handles unknown FastMCP wrapper types through comprehensive attribute inspection with fallback to class-specific extraction patterns when standard attributes unavailable. Missing function attributes are managed through systematic attempts across multiple attribute names with descriptive error messages listing available attributes for debugging. Non-callable extracted objects trigger `TypeError` exceptions with specific object type information and extraction method context. Invalid function signatures are handled through `inspect.signature()` validation with warnings for functions lacking Context parameters. Wrapper detection edge cases include objects with partial FastMCP characteristics handled through conservative detection heuristics. Function metadata extraction manages missing attributes through safe fallbacks preventing extraction failures. Signature inspection failures are handled gracefully with continued execution and warning messages rather than complete failure. Class-specific extraction handles unknown class types through pattern matching with graceful None returns for unsupported wrapper types.

########## Internal Implementation Details

The module uses systematic attribute inspection with predefined lists including primary `fn` attribute for FastMCP FunctionResource objects and fallback attributes for various wrapper patterns. Wrapper detection implements class name pattern matching for `FunctionResource`, `FunctionTool`, `FunctionPrompt`, `Resource`, `Tool`, and `Prompt` patterns with attribute presence checking for `_func`, `__wrapped__`, `func`, and `_function`. Class-specific extraction employs dedicated patterns for Resource, Tool, and Prompt wrapper types with specific attribute attempts including `_func`, `handler`, `_handler`, and `callback` for each category. Function validation uses `inspect.iscoroutinefunction()` for async requirement checking and parameter analysis for Context parameter validation. Metadata extraction combines `inspect.signature()`, `inspect.getdoc()`, `inspect.getfile()`, and `inspect.getsourcelines()` with exception handling for unavailable information. Error messages include specific wrapper types, available attributes, and extraction methods for comprehensive debugging support. Type safety validation ensures callable objects with proper signatures before function return.

########### Code Usage Examples

FastMCP function unwrapping demonstrates the primary usage pattern for extracting original functions from decorated objects for direct testing. This approach enables developers to test FastMCP resources without MCP protocol overhead while maintaining full function access.

```python
# Extract original function from FastMCP decorated resource for direct testing
# Enables testing without MCP protocol complexity while preserving function behavior
from utils import unwrap_fastmcp_function

# Unwrap FastMCP resource to access underlying function
original_function = unwrap_fastmcp_function(decorated_resource)
# Direct function invocation for testing with Context parameter
result = await original_function(context, *args, **kwargs)
```

Function validation showcases the FastMCP compatibility checking pattern for ensuring proper function structure. This pattern provides comprehensive validation with specific recommendations for fixing compatibility issues.

```python
# Validate function compatibility with FastMCP requirements and get detailed feedback
# Provides comprehensive validation results with specific recommendations for fixes
from utils import validate_fastmcp_function, get_function_metadata

# Validate FastMCP function requirements
validation_result = validate_fastmcp_function(function, expected_context_param="ctx")
if not validation_result['is_valid']:
    print("Validation issues:", validation_result['issues'])
    print("Recommendations:", validation_result['recommendations'])

# Extract comprehensive function metadata for analysis
metadata = get_function_metadata(function)
print(f"Function: {metadata['name']}, Parameters: {metadata['parameters']}")
```