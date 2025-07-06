# JESSE_CODE_COMMENTS.md - Consolidated Code Documentation Standards

This file consolidates ALL code documentation rules for the project, serving as the single source of truth for code comments, headers, and documentation standards.

## 1. CRITICAL FOUNDATION RULES

### 1.1 Non-Negotiable Three-Section Pattern
⚠️ **CRITICAL**: ALL functions, methods, and classes MUST include the three-section documentation pattern regardless of size or complexity. **NO EXCEPTIONS PERMITTED** (except for Markdown files). This is a non-negotiable project standard that takes precedence over all other considerations except correct code functionality.

**The Three Mandatory Sections (in exact order):**
```
[Function/Class method/Class intent] <!-- It is **critical** to fully capture and contextualize the intent -->
[Design principles]
[Implementation details]
```

### 1.2 Universal Application Policy
- This pattern applies to ALL code elements without exception:
  - Every function (including one-liners)
  - Every method (including getters/setters)
  - Every class (including simple data classes)
  - Every script entry point
- File size, complexity, or "obviousness" are NOT valid exceptions

### 1.3 Self-Correction Mechanism
If you notice you've implemented code without proper documentation:
1. **IMMEDIATELY** stop further implementation
2. Add the missing documentation sections in the correct order
3. Verify against the checklist
4. Resume implementation only after documentation is complete

## 2. FILE-LEVEL DOCUMENTATION STANDARDS

### 2.1 Mandatory File Header Template
All non-markdown files (including Dockerfile, Shell scripts...) MUST begin with this exact header structure:

```
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
# <Describe the detailed purpose of this file. Intent must be fully captured and contextualized.>
###############################################################################
# [Source file design principles]
# <List key design principles guiding this implementation>
###############################################################################
# [Source file constraints]
# <Document any limitations or requirements for this file>
###############################################################################
# [Dependencies] <!-- Never reference documents in <project_root>/scratchpad/ directory -->
# <File paths of others codebase and documentation files. List also language specific libraries if any>
# <List of markdown files in doc/ that provide broader context for this file>
# <Prefix the dependency with its kind like "<codebase|system|other>:<dependency>"
#    <"codebase" kind means a reference to any artifact in the current project codebase>
#    <"system" kind means a reference toward an external artifact provided by the environement (files, librairies, modules...)>
###############################################################################
# [GenAI tool change history] <!-- Change history sorted from the newest to the oldest -->
# YYYY-MM-DDThh:mm:ssZ : <summary of change> by CodeAssistant
# * <change detail>
###############################################################################
```

### 2.2 Header Application Rules
- Place header at the very top of each file before any other content
- Apply to ALL non-markdown files in the project
- Maintain header completeness - no sections may be omitted
- Update header content to reflect file evolution

### 2.3 Change History Management
- Document all changes using precise timestamp format: `YYYY-MM-DDThh:mm:ssZ`
- Keep only the 4 most recent records, sorted newest to oldest
- Include both summary and detailed change information
- Never delete the history section entirely

## 3. FUNCTION/METHOD/CLASS DOCUMENTATION STANDARDS

### 3.1 The Three-Section Documentation Pattern

#### Section 1: Intent
- **Label**: `[Function intent]`, `[Class method intent]`, or `[Class intent]`
- **Purpose**: Clear description of what the code element does and why it exists
- **Requirements**: Must fully capture and contextualize the purpose

#### Section 2: Design Principles
- **Label**: `[Design principles]`
- **Purpose**: Patterns, approaches, and architectural decisions
- **Requirements**: Must explain WHY the code is designed this way and how/when to use it

#### Section 3: Implementation Details
- **Label**: `[Implementation details]`
- **Purpose**: HOW the code works internally
- **Requirements**: Key algorithms, data structures, and technical notes with enough information to help code element maintenance

### 3.2 Documentation Quality Standards
- Write insightful comments that allow understanding without need for reading code
- When using adjectives (e.g., "efficient", "robust"), ALWAYS provide specific factual justifications in the same sentence
- Avoid vague wording - provide precise technical reasons
- Design principles should enable reuse elsewhere in the codebase
- Implementation details should aid maintenance and debugging

### 3.3 Standard Parameter/Return Documentation
Include language-appropriate parameter and return documentation:
- Parameter types and descriptions
- Return value types and meanings
- Exception/error conditions
- Side effects (if any)

## 4. LANGUAGE-SPECIFIC TEMPLATES

### 4.1 Python Documentation Template

#### Python Function Template
```python
def function_name(param1, param2, optional_param=None):
    """
    [Function intent]
    Clear description of the function's purpose and role in the system.
    
    [Design principles]
    Patterns and approaches used, along with rationale for design choices.
    
    [Implementation details]
    Key technical implementation notes like algorithms used, processing flow, etc.
    
    Args:
        param1 (type): Description of first parameter
        param2 (type): Description of second parameter
        optional_param (type, optional): Description of optional parameter. Defaults to None.
        
    Returns:
        type: Description of return value
        
    Raises:
        ExceptionType: When and why this exception is raised
    """
    # Implementation...
```

#### Python Class Template
```python
class ClassName:
    """
    [Class intent]
    Clear description of the class's purpose and role in the system.
    
    [Design principles]
    Patterns and approaches used, along with rationale for design choices.
    
    [Implementation details]
    Key technical implementation notes, inheritance details, etc.
    """
    
    def __init__(self, param1, param2=None):
        """
        [Class method intent]
        Initialize a new instance of the class.
        
        [Design principles]
        Design decisions related to initialization.
        
        [Implementation details]
        How parameters are stored and initial state is set up.
        
        Args:
            param1 (type): Description of first parameter
            param2 (type, optional): Description of second parameter. Defaults to None.
        """
        # Implementation...
```

### 4.2 JavaScript Documentation Template

```javascript
/**
 * [Class intent]
 * Manages user authentication state and processes throughout the application.
 *
 * [Design principles]
 * Single responsibility for auth state management.
 * Clear separation between auth logic and UI components.
 *
 * [Implementation details]
 * Implements the Observer pattern to notify components of auth state changes.
 * Uses localStorage for persistent login state with encryption.
 *
 * @class AuthManager
 */
class AuthManager {
  /**
   * [Class method intent]
   * Creates a new AuthManager instance with initial configuration.
   *
   * [Design principles]
   * Fail-secure initialization with validation of stored credentials.
   *
   * [Implementation details]
   * Sets up listeners and initializes from encrypted localStorage if available.
   *
   * @param {Object} config - Configuration options
   * @param {boolean} config.autoRefresh - Whether to auto-refresh tokens
   */
  constructor(config) {
    // Implementation...
  }
}
```

### 4.3 Bash Documentation Template

```bash
#!/usr/bin/env bash

# [Script intent]
# Clear description of the script's purpose and role in the system.
#
# [Design principles]
# Patterns and approaches used, along with rationale for design choices.
#
# [Implementation details]
# Key technical implementation notes like algorithms used, processing flow, etc.
#
# Usage: script_name.sh [OPTIONS]
# Options:
#   -h, --help     Show usage information
#   -v, --verbose  Enable verbose output
#
# Exit Codes:
#   0 - Success
#   1 - General error

# [Function intent]
# Clear description of the function's purpose.
#
# [Design principles]
# Why the function is designed this way.
#
# [Implementation details]
# How the function works internally.
#
# Arguments:
#   $1 - Description of first argument
#   $2 - Description of second argument
#
# Returns:
#   0 on success, non-zero on error
function function_name() {
  # Implementation...
  return 0
}
```

## 5. DOCUMENTATION QUALITY & VERIFICATION

### 5.1 Quality Criteria
- **Completeness**: All three sections present and meaningful
- **Clarity**: Understandable without reading the implementation
- **Specificity**: Concrete details, not generic statements
- **Justification**: All quality claims backed by technical reasons
- **Consistency**: Aligned with file header and project documentation

### 5.2 Verification Checklist
After implementing ANY function, method, or class, ALWAYS verify:
1. ✓ Documentation includes ALL THREE required sections in exact order
2. ✓ Section labels match the template exactly
3. ✓ Intent section fully captures the purpose
4. ✓ Design principles explain the "why"
5. ✓ Implementation details explain the "how"
6. ✓ Parameter/return documentation matches actual signature
7. ✓ Exception documentation covers all error cases
8. ✓ No outdated or contradictory information

### 5.3 Consistency Requirements
- Function/method documentation must align with file header intent
- Design principles must be consistent across related functions
- Implementation details must match actual code behavior
- All documentation must use present tense (no "was implemented" or "will be")
- All texts generated within function/class comments, file headers, or documentation MUST NEVER refer to past implementations

## 6. DOCUMENTATION LIFECYCLE MANAGEMENT

### 6.1 File Modification Protocol
When modifying any file:
1. **ALWAYS** update the file header history section
2. **ALWAYS** update file intent/design if modifications change them
3. **ALWAYS** ensure function/method/class comments remain accurate
4. **ALWAYS** verify consistency between header and function documentation

### 6.2 Change History Requirements
- Use precise timestamp format: `YYYY-MM-DDThh:mm:ssZ`
- Include meaningful summary and specific details
- Maintain 4-entry limit (remove oldest when adding new)
- Sort entries from newest to oldest

### 6.3 Markdown Changelog Integration
For markdown file modifications, follow the standards detailed in `JESSE_MARKDOWN.md` Section 7 "Lifecycle Management".

### 6.4 Post-Modification Verification
After any file modification:
1. Verify file existence and syntax correctness
2. Confirm all documentation sections remain valid
3. Check for consistency across all documentation levels
4. Ensure no documentation refers to past implementations

## 7. ENFORCEMENT AND COMPLIANCE

### 7.1 Zero-Tolerance Policy
- Missing documentation is a **blocking issue**
- Incomplete documentation must be fixed before proceeding
- "TODO: Add documentation" is NOT acceptable
- Documentation quality is as important as code quality

### 7.2 Compliance Verification Process
1. **Before commit**: Verify all new/modified code has complete documentation
2. **During review**: Check documentation quality and completeness
3. **After merge**: Monitor for documentation degradation
4. **Periodic audit**: Ensure ongoing compliance

### 7.3 Documentation Debt Prevention
- Never accumulate documentation debt
- Fix documentation issues immediately when discovered
- Update documentation BEFORE modifying code
- Treat documentation as part of the implementation

---

**Remember**: This consolidated rule supersedes all previous scattered documentation rules. When in doubt, refer to this document as the authoritative source for all code documentation standards.
