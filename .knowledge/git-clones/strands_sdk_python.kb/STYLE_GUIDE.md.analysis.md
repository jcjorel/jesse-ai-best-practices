<!-- CACHE_METADATA_START -->
<!-- Source File: {PROJECT_ROOT}/.knowledge/git-clones/strands_sdk_python/STYLE_GUIDE.md -->
<!-- Cached On: 2025-07-07T22:33:40.018923 -->
<!-- Source Modified: 2025-06-30T17:02:52.895757 -->
<!-- Cache Version: 1.0 -->
<!-- CACHE_METADATA_END -->

#### Functional Intent & Features

This style guide establishes standardized coding conventions and logging practices for the Strands Agents repository, providing consistent formatting rules, naming conventions, and structured logging patterns. The guide enables automated enforcement through linting rules and pre-commit hooks, reducing manual review overhead while ensuring code maintainability. Key semantic entities include `logger.debug()`, `logger.info()`, `logger.warning()` methods, `%s` string interpolation patterns, `<FIELD>=<VALUE>` structured logging format, `CloudWatch`, `Splunk` log service integrations, and pipe character (`|`) message separators. The documentation implements a field-value logging architecture that supports both human readability and machine parsing for monitoring systems.

##### Main Components

The guide contains two primary sections: an Overview section establishing general coding principles and automated enforcement strategies, and a Log Formatting section defining structured logging patterns. The logging component specifies field-value pair formatting, human-readable message construction, and string interpolation guidelines. Example sections demonstrate both correct and incorrect logging implementations, providing clear guidance for developers implementing logging throughout the codebase.

###### Architecture & Design

The style guide follows a structured logging design pattern that separates contextual data from human-readable messages using field-value pairs and pipe delimiters. The logging architecture prioritizes machine parseability for log aggregation services while maintaining human readability through consistent formatting rules. The design emphasizes automation through linting integration and pre-commit hooks, reducing the need for manual style enforcement during code reviews.

####### Implementation Approach

The logging implementation uses Python's built-in logging module with `%s` string interpolation for performance optimization, avoiding string formatting when log levels are disabled. Field-value pairs follow the `<FIELD>=<VALUE>` pattern with angle bracket enclosure for visual clarity, particularly for empty values. Message construction employs lowercase formatting without punctuation, using pipe characters for multi-statement separation. The approach integrates with automated tooling through linting rules and pre-commit hooks for consistent enforcement.

######## External Dependencies & Integration Points

**→ References:**
- `CloudWatch` - AWS log aggregation service for field extraction patterns
- `Splunk` - Enterprise log management platform for structured data parsing
- Python logging module - Built-in logging framework for message formatting
- Linting tools - Code quality enforcement for style compliance
- Pre-commit hooks - Automated style validation in development workflow

**← Referenced by:**
- Repository codebase - All Python modules implementing logging patterns
- Development workflow - Code review and quality assurance processes
- CI/CD pipeline - Automated style validation and enforcement

**⚡ Integration:**
The style guide serves as the central specification for code quality standards across the Strands Agents repository, enabling consistent logging practices that integrate seamlessly with enterprise log management systems while supporting automated enforcement through development tooling.

######### Edge Cases & Error Handling

The guide addresses empty value display through angle bracket enclosure (`field=<>` vs `field=`), ensuring visual clarity when debugging missing or null values. String interpolation performance considerations prevent unnecessary formatting operations when log levels are disabled through `%s` parameter passing. Multi-statement logging scenarios require pipe character separation to maintain readability while preserving structured format compliance.

########## Internal Implementation Details

The logging format specification requires comma separation between field-value pairs, angle bracket value enclosure for readability, and lowercase message formatting without terminal punctuation. String interpolation uses Python logging's recommended `%s` approach rather than f-strings or `.format()` methods for performance optimization. The structured format enables log parsing services to extract searchable fields while maintaining human-readable message content through pipe delimiter separation.

########### Code Usage Examples

These examples demonstrate proper structured logging implementation with field-value pairs and human-readable messages. The patterns show how to maintain consistency across different log levels while ensuring machine parseability.

```python
logger.debug("user_id=<%s>, action=<%s> | user performed action", user_id, action)
logger.info("request_id=<%s>, duration_ms=<%d> | request completed", request_id, duration)
logger.warning("attempt=<%d>, max_attempts=<%d> | retry limit approaching", attempt, max_attempts)
```

These examples illustrate common anti-patterns that violate the structured logging guidelines. The violations demonstrate formatting inconsistencies that reduce both human readability and machine parsing effectiveness.

```python
# Avoid: No structured fields, direct variable interpolation in message
logger.debug(f"User {user_id} performed action {action}")

# Avoid: Inconsistent formatting, punctuation
logger.info("Request completed in %d ms.", duration)

# Avoid: No separation between fields and message
logger.warning("Retry limit approaching! attempt=%d max_attempts=%d", attempt, max_attempts)
```