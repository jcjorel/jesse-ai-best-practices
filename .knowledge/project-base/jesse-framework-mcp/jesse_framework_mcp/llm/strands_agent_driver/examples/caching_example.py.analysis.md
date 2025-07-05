<!-- CACHE_METADATA_START -->
<!-- Source File: {PROJECT_ROOT}/jesse-framework-mcp/jesse_framework_mcp/llm/strands_agent_driver/examples/caching_example.py -->
<!-- Cached On: 2025-07-05T14:12:36.738270 -->
<!-- Source Modified: 2025-07-01T08:59:29.261995 -->
<!-- Cache Version: 1.0 -->
<!-- CACHE_METADATA_END -->

#### Functional Intent & Features

This file implements a comprehensive demonstration script for prompt caching capabilities in the Claude 4 Sonnet driver, showcasing performance optimization through cache hit analysis, response time comparisons, and cache management strategies for educational and testing purposes. The script enables developers to understand and validate the behavior of prompt caching configurations with live AWS Bedrock integration, demonstrating cost savings and performance improvements through repeated query optimization. Key semantic entities include `caching_demonstration()` function for primary cache testing, `cache_efficiency_test()` function for cache eviction and hit rate analysis, `StrandsClaude4Driver` class for AWS Bedrock integration, `Claude4SonnetConfig` configuration class with caching parameters, `enable_prompt_caching` configuration flag, `cache_ttl_seconds` TTL configuration with 300-second default, `max_cache_entries` size limit configuration, `from_cache` response attribute for cache hit detection, `send_message()` method for cached message processing, `get_conversation_stats()` method for cache statistics retrieval, `clear_conversation()` method for cache reset functionality, conversation identifiers `caching_example_conversation` and `cache_efficiency_test`, `BedrockConnectionError` and `StrandsDriverError` exception classes, and comprehensive performance metrics collection including response times, cache hit rates, and cost savings analysis. The system implements async-first architecture with detailed console output formatting and educational demonstration patterns.

##### Main Components

The file contains three primary async functions providing comprehensive prompt caching demonstration and analysis capabilities. The `caching_demonstration()` function performs the main caching test with identical question repetition, cache sensitivity analysis with question variations, and cache expiration demonstration through conversation clearing. The `cache_efficiency_test()` function implements cache eviction testing with a smaller cache size limit, multiple different questions to trigger cache replacement, and detailed hit rate analysis with statistical reporting. The `main()` function serves as the orchestration entry point with AWS credential validation, region detection, and sequential execution of both demonstration functions with comprehensive error handling and educational summary output. The script includes detailed performance timing using `time.time()` measurements, cache statistics retrieval and display, and structured console output with emoji-based visual indicators for different test phases.

###### Architecture & Design

The architecture implements a demonstration-focused design pattern with clear separation between basic caching validation and advanced cache efficiency testing, following educational progression from simple cache hits to complex eviction scenarios. The design emphasizes performance measurement and comparison through detailed timing analysis and statistical reporting. Key design patterns include the demonstration pattern with before-and-after performance comparisons, cache sensitivity testing pattern with question variations, cache eviction testing pattern with limited cache size, and educational pattern with detailed explanatory output and key takeaways. The system uses async context manager patterns for resource management, conversation isolation through unique identifiers, and comprehensive exception handling with specific error types and user-friendly messages for different failure scenarios.

####### Implementation Approach

The implementation uses async context managers for proper resource lifecycle management with `StrandsClaude4Driver` instances and explicit cache configuration through `Claude4SonnetConfig` parameters. Performance measurement employs `time.time()` before and after message sending with precise timing calculations and speedup ratio analysis. Cache testing uses identical question repetition to demonstrate cache hits, question variations to show cache sensitivity, and conversation clearing to reset cache state for controlled testing. The approach implements comprehensive error handling with specific exception types for AWS Bedrock connection issues and driver errors. Console output uses structured formatting with emoji indicators, performance metrics display, and detailed statistical analysis including cache hit rates, response time comparisons, and cost savings calculations.

######## External Dependencies & Integration Points

**→ Inbound:**
- `asyncio` (external library) - async event loop management for demonstration execution and timing measurements
- `sys` (external library) - Python path manipulation for module imports and exit handling with status codes
- `os` (external library) - environment variable access for AWS credentials and region configuration
- `time` (external library) - high-precision timing measurements for performance analysis and cache comparison
- `pathlib.Path` (external library) - cross-platform path operations for module import path construction
- `strands_agent_driver:StrandsClaude4Driver` - main driver class for AWS Bedrock Claude 4 integration with caching support
- `strands_agent_driver:Claude4SonnetConfig` - configuration class with prompt caching parameters and TTL settings
- `strands_agent_driver:StrandsDriverError` - driver-specific exception handling for operational errors
- `strands_agent_driver:BedrockConnectionError` - AWS Bedrock connection error handling for authentication issues

**← Outbound:**
- Developer education workflows - consuming caching demonstration output for understanding performance optimization strategies
- Performance testing and validation processes - using cache efficiency results to verify driver caching functionality
- Documentation and training materials - referencing cache performance metrics and optimization patterns for educational content
- AWS Bedrock service integration - generating actual API calls and cache operations for live demonstration when credentials are available

**⚡ System role and ecosystem integration:**
- **System Role**: Educational demonstration component for Strands Agent Driver prompt caching feature, providing hands-on performance analysis and cache optimization examples for developers learning efficient API usage patterns
- **Ecosystem Position**: Peripheral educational component supporting developer understanding of caching strategies and performance optimization, demonstrating core driver functionality without being part of production workflows
- **Integration Pattern**: Used by developers through direct script execution for learning cache optimization, consumed by performance testing processes for validation, and integrated with AWS Bedrock services for live cache demonstration when proper credentials are configured

######### Edge Cases & Error Handling

The system handles missing AWS credentials gracefully by detecting environment variables and providing informative warnings without failing the demonstration. AWS Bedrock connection errors are caught with specific `BedrockConnectionError` handling and user-friendly messages explaining authentication requirements. Driver operational errors are managed through `StrandsDriverError` exception handling with detailed error context. Keyboard interrupts are handled with clean exit messages and proper signal handling using `sys.exit(1)`. The script manages cache expiration scenarios through conversation clearing and fresh conversation initialization. Performance measurement edge cases include zero response times with infinity handling for speedup calculations. Cache statistics retrieval handles missing or unavailable cache data gracefully with conditional display logic.

########## Internal Implementation Details

The demonstration uses hardcoded test questions including "What are the main principles of object-oriented programming?" for consistent cache testing and multiple variations for sensitivity analysis. Cache configuration employs specific parameter values including 300-second TTL, 10-entry maximum for main demonstration, and 3-entry maximum for efficiency testing. Performance timing uses `time.time()` measurements with millisecond precision and speedup calculations using division with infinity handling. Conversation IDs are explicitly set to `caching_example_conversation` and `cache_efficiency_test` for clear session isolation. Console output uses structured formatting with specific emoji indicators, section dividers using `=` characters, and detailed statistical reporting including percentages and ratios. Cache statistics access uses `get_conversation_stats()` with conditional checking for cache availability and structured data display.

########### Code Usage Examples

Basic prompt caching configuration demonstrates the essential setup pattern for enabling cache optimization. This approach shows explicit parameter configuration for TTL, cache size limits, and caching enablement for performance-focused applications.

```python
# Configure Claude 4 Sonnet driver with prompt caching enabled for performance optimization
config = Claude4SonnetConfig(
    enable_prompt_caching=True,
    cache_ttl_seconds=300,  # 5 minutes
    max_cache_entries=10,
    temperature=0.7
)

async with StrandsClaude4Driver(config) as driver:
    conversation_id = "caching_example_conversation"
    await driver.start_conversation(conversation_id, {"example": "caching"})
```

Cache performance measurement showcases the timing analysis pattern for comparing cached versus non-cached responses. This pattern demonstrates how to measure and analyze the performance benefits of prompt caching with detailed metrics collection.

```python
# Measure cache performance with timing analysis and hit rate detection
test_question = "What are the main principles of object-oriented programming?"

# First call - should go to API
start_time = time.time()
response1 = await driver.send_message(test_question, conversation_id)
first_call_time = time.time() - start_time

# Second call - should come from cache
start_time = time.time()
response2 = await driver.send_message(test_question, conversation_id)
second_call_time = time.time() - start_time

# Calculate performance improvement
if response2.from_cache:
    speedup = first_call_time / second_call_time if second_call_time > 0 else float('inf')
    print(f"Speed increase: {speedup:.1f}x faster")
    print(f"Response identical: {response1.content == response2.content}")
```