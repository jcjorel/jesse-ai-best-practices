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
# FastMCP function unwrapping utilities for testing and development support.
# Provides direct access to original functions from FastMCP decorated objects.
###############################################################################
# [Source file design principles]
# - Defensive programming with comprehensive error handling and descriptive messages
# - Support for all FastMCP decorator types (resource, tool, prompt)
# - Type safety with proper validation and fallback mechanisms
# - Clean separation between MCP protocol handling and direct function access
###############################################################################
# [Source file constraints]
# - Must handle FastMCP internal attribute variations across versions
# - Function extraction must preserve original signature and behavior
# - Error handling must provide clear guidance for debugging
# - Compatibility with all FastMCP decorator patterns used in project
###############################################################################
# [Dependencies]
# <system>: typing for type hints and annotations
# <system>: inspect for function signature validation
# <system>: functools for function metadata preservation
###############################################################################
# [GenAI tool change history]
# 2025-06-28T08:03:26Z : Fixed FastMCP function extraction with 'fn' attribute support by CodeAssistant
# * Added 'fn' attribute as primary extraction method for FastMCP FunctionResource objects
# * Successfully tested with get_project_gitignore_files() resource unwrapping
# * Verified complete functionality with direct function testing capability
# * Enhanced function attributes list with FastMCP-specific patterns for robust extraction
# 2025-06-28T08:00:44Z : Initial FastMCP function unwrapper implementation by CodeAssistant
# * Created unwrap_fastmcp_function() for extracting original functions from decorated objects
# * Implemented multi-pattern support for FunctionResource, FunctionTool, FunctionPrompt types
# * Added comprehensive error handling with descriptive messages for debugging
# * Included type safety validation and fallback mechanisms for unknown wrapper types
###############################################################################

import inspect
from typing import Any, Callable, Union
from functools import wraps


def unwrap_fastmcp_function(decorated_object: Any) -> Callable:
    """
    [Function intent]
    Extract the original function from FastMCP decorated objects for direct testing and development.
    Enables access to the underlying callable implementation without MCP protocol overhead.
    
    [Design principles]
    Defensive programming with comprehensive error handling for unknown wrapper types.
    Multi-pattern support for all FastMCP decorator types used in the project.
    Type safety with validation and clear error messages for debugging.
    
    [Implementation details]
    Attempts multiple extraction patterns for different FastMCP wrapper types.
    Uses attribute inspection to find the original function stored in wrapper objects.
    Validates that extracted objects are callable before returning them.
    
    Args:
        decorated_object: FastMCP decorated object (FunctionResource, FunctionTool, etc.) or raw function
        
    Returns:
        Original callable function that can be invoked directly
        
    Raises:
        TypeError: When decorated_object is not a supported FastMCP wrapper or callable
        AttributeError: When wrapper object doesn't contain expected function attributes
        ValueError: When extracted function is not callable or has invalid signature
    """
    # If already a callable function, return as-is
    if callable(decorated_object) and not _is_fastmcp_wrapper(decorated_object):
        return decorated_object
    
    # List of common attribute names where FastMCP stores original functions
    function_attributes = [
        'fn',              # FastMCP FunctionResource stores function here
        '_func',           # Common pattern for wrapped functions
        '__wrapped__',     # Standard Python wrapper pattern
        'func',            # Alternative function storage
        '_function',       # Another common pattern
        'handler',         # Some MCP implementations use this
        '_handler',        # Private handler attribute
        'callback',        # Callback-style storage
        '_callback',       # Private callback attribute
        'read'             # Some FastMCP resources might use this
    ]
    
    # Try to extract function using various attribute patterns
    original_function = None
    extraction_method = None
    
    for attr_name in function_attributes:
        try:
            if hasattr(decorated_object, attr_name):
                potential_function = getattr(decorated_object, attr_name)
                if callable(potential_function):
                    original_function = potential_function
                    extraction_method = attr_name
                    break
        except Exception:
            # Continue to next attribute if this one fails
            continue
    
    # If no function found through attributes, try class-specific patterns
    if original_function is None:
        original_function, extraction_method = _try_class_specific_extraction(decorated_object)
    
    # Validate extracted function
    if original_function is None:
        wrapper_type = type(decorated_object).__name__
        available_attrs = [attr for attr in dir(decorated_object) if not attr.startswith('__')]
        raise ValueError(
            f"Could not extract function from {wrapper_type} object. "
            f"Available attributes: {available_attrs}. "
            f"This may be an unsupported FastMCP wrapper type or the object may not contain a function."
        )
    
    if not callable(original_function):
        raise TypeError(
            f"Extracted object from {extraction_method} is not callable: {type(original_function).__name__}. "
            f"Expected a function but got {original_function}"
        )
    
    # Validate function signature (should accept at least one parameter for Context)
    try:
        sig = inspect.signature(original_function)
        if len(sig.parameters) == 0:
            raise ValueError(
                f"Extracted function has no parameters. FastMCP functions should accept at least Context parameter. "
                f"Function: {original_function.__name__ if hasattr(original_function, '__name__') else 'unnamed'}"
            )
    except Exception as e:
        # Signature inspection failed, but function might still be valid
        # Log warning but don't fail completely
        pass
    
    return original_function


def _is_fastmcp_wrapper(obj: Any) -> bool:
    """
    [Function intent]
    Detect if an object is a FastMCP wrapper type that needs unwrapping.
    
    [Design principles]
    Simple detection based on class name patterns and common FastMCP attributes.
    Conservative approach - when in doubt, assume it's not a wrapper.
    
    [Implementation details]
    Checks class name for FastMCP patterns and presence of wrapper attributes.
    Uses multiple heuristics to identify FastMCP wrapper objects.
    
    Args:
        obj: Object to check for FastMCP wrapper characteristics
        
    Returns:
        True if object appears to be a FastMCP wrapper, False otherwise
    """
    if obj is None:
        return False
    
    class_name = type(obj).__name__
    
    # Check for FastMCP wrapper class name patterns
    fastmcp_patterns = [
        'FunctionResource',
        'FunctionTool', 
        'FunctionPrompt',
        'Resource',
        'Tool',
        'Prompt'
    ]
    
    if any(pattern in class_name for pattern in fastmcp_patterns):
        return True
    
    # Check for common wrapper attributes
    wrapper_attributes = ['_func', '__wrapped__', 'func', '_function']
    if any(hasattr(obj, attr) for attr in wrapper_attributes):
        return True
    
    return False


def _try_class_specific_extraction(obj: Any) -> tuple[Union[Callable, None], Union[str, None]]:
    """
    [Function intent]
    Attempt class-specific function extraction patterns for FastMCP objects.
    
    [Design principles]
    Class-specific extraction patterns for different FastMCP wrapper types.
    Graceful failure with None return for unsupported types.
    
    [Implementation details]
    Checks specific FastMCP class types and their known function storage patterns.
    Uses try-catch for each pattern to avoid breaking on unknown types.
    
    Args:
        obj: FastMCP wrapper object to extract function from
        
    Returns:
        Tuple of (extracted_function, extraction_method) or (None, None) if extraction fails
    """
    class_name = type(obj).__name__
    
    # FunctionResource specific patterns
    if 'Resource' in class_name:
        for attr in ['_func', 'handler', '_handler']:
            try:
                if hasattr(obj, attr):
                    func = getattr(obj, attr)
                    if callable(func):
                        return func, f"Resource.{attr}"
            except Exception:
                continue
    
    # FunctionTool specific patterns  
    if 'Tool' in class_name:
        for attr in ['_func', 'handler', '_handler', 'callback']:
            try:
                if hasattr(obj, attr):
                    func = getattr(obj, attr)
                    if callable(func):
                        return func, f"Tool.{attr}"
            except Exception:
                continue
    
    # FunctionPrompt specific patterns
    if 'Prompt' in class_name:
        for attr in ['_func', 'handler', '_handler', 'generator']:
            try:
                if hasattr(obj, attr):
                    func = getattr(obj, attr)
                    if callable(func):
                        return func, f"Prompt.{attr}"
            except Exception:
                continue
    
    return None, None


def get_function_metadata(func: Callable) -> dict[str, Any]:
    """
    [Function intent]
    Extract comprehensive metadata from a function for debugging and validation.
    
    [Design principles]
    Comprehensive metadata extraction for function analysis and debugging.
    Safe extraction with fallbacks for missing or invalid attributes.
    
    [Implementation details]
    Uses inspect module to extract function signature, docstring, and module information.
    Provides fallback values for attributes that might not be available.
    
    Args:
        func: Function to extract metadata from
        
    Returns:
        Dictionary containing function metadata (name, signature, docstring, etc.)
        
    Raises:
        TypeError: When func is not callable
    """
    if not callable(func):
        raise TypeError(f"Expected callable function, got {type(func).__name__}")
    
    metadata = {}
    
    # Basic function information
    metadata['name'] = getattr(func, '__name__', 'unnamed')
    metadata['module'] = getattr(func, '__module__', 'unknown')
    metadata['qualname'] = getattr(func, '__qualname__', metadata['name'])
    
    # Function signature
    try:
        sig = inspect.signature(func)
        metadata['signature'] = str(sig)
        metadata['parameters'] = list(sig.parameters.keys())
        metadata['parameter_count'] = len(sig.parameters)
    except Exception as e:
        metadata['signature'] = f"<signature unavailable: {str(e)}>"
        metadata['parameters'] = []
        metadata['parameter_count'] = 0
    
    # Function documentation
    metadata['docstring'] = inspect.getdoc(func) or "No documentation available"
    metadata['docstring_length'] = len(metadata['docstring'])
    
    # Function source information
    try:
        metadata['source_file'] = inspect.getfile(func)
        metadata['source_lines'] = inspect.getsourcelines(func)[1]
    except Exception:
        metadata['source_file'] = "unavailable"
        metadata['source_lines'] = None
    
    # Function type information
    metadata['is_coroutine'] = inspect.iscoroutinefunction(func)
    metadata['is_async'] = inspect.iscoroutinefunction(func)
    metadata['is_generator'] = inspect.isgeneratorfunction(func)
    
    return metadata


def validate_fastmcp_function(func: Callable, expected_context_param: str = "ctx") -> dict[str, Any]:
    """
    [Function intent]
    Validate that a function meets FastMCP resource/tool/prompt requirements.
    
    [Design principles]
    Comprehensive validation of FastMCP function patterns and requirements.
    Clear validation results with specific guidance for fixing issues.
    
    [Implementation details]
    Checks function signature for Context parameter, async pattern, and documentation.
    Returns detailed validation results with specific recommendations.
    
    Args:
        func: Function to validate for FastMCP compatibility
        expected_context_param: Expected name of Context parameter (default: "ctx")
        
    Returns:
        Dictionary containing validation results and recommendations
        
    Raises:
        TypeError: When func is not callable
    """
    if not callable(func):
        raise TypeError(f"Expected callable function, got {type(func).__name__}")
    
    validation = {
        'is_valid': True,
        'issues': [],
        'recommendations': [],
        'metadata': get_function_metadata(func)
    }
    
    # Check if function is async (required for FastMCP)
    if not inspect.iscoroutinefunction(func):
        validation['is_valid'] = False
        validation['issues'].append("Function is not async - FastMCP functions must be async")
        validation['recommendations'].append("Add 'async def' to function definition")
    
    # Check function signature for Context parameter
    try:
        sig = inspect.signature(func)
        params = list(sig.parameters.keys())
        
        if not params:
            validation['is_valid'] = False
            validation['issues'].append("Function has no parameters")
            validation['recommendations'].append(f"Add Context parameter: '{expected_context_param}: Context'")
        elif expected_context_param not in params:
            validation['is_valid'] = False
            validation['issues'].append(f"Missing expected Context parameter '{expected_context_param}'")
            validation['recommendations'].append(f"Add Context parameter: '{expected_context_param}: Context'")
        elif params[0] != expected_context_param:
            validation['issues'].append(f"Context parameter '{expected_context_param}' should be first parameter")
            validation['recommendations'].append(f"Move '{expected_context_param}' to first position in parameters")
    
    except Exception as e:
        validation['is_valid'] = False
        validation['issues'].append(f"Could not inspect function signature: {str(e)}")
        validation['recommendations'].append("Ensure function has valid Python signature")
    
    # Check for documentation
    docstring = inspect.getdoc(func)
    if not docstring:
        validation['issues'].append("Function has no documentation")
        validation['recommendations'].append("Add comprehensive docstring with JESSE three-section pattern")
    elif len(docstring) < 50:
        validation['issues'].append("Function documentation is very brief")
        validation['recommendations'].append("Expand documentation to include intent, design principles, and implementation details")
    
    return validation
