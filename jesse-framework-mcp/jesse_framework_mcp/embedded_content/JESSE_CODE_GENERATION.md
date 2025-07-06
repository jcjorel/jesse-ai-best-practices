# JESSE_CODE_GENERATION.md - Consolidated Code Generation Standards

This file consolidates ALL code generation rules for the project, serving as the single source of truth for code creation, implementation approaches, and execution standards.

## 1. CRITICAL FOUNDATION RULES

### 1.1 Non-Negotiable Code Generation Standards
⚠️ **CRITICAL**: All code generation MUST follow these consolidated standards. **NO EXCEPTIONS PERMITTED**. This is a non-negotiable project standard that takes precedence over scattered individual rules.

### 1.2 Universal Application Policy
- These standards apply to ALL code generation activities without exception
- Task complexity, urgency, or scope are NOT valid exceptions
- Consistency across all code generation is mandatory

## 2. KISS (KEEP IT SIMPLE & STUPID) APPROACH

### 2.1 Core KISS Principles
When designing solutions and generating code, you MUST systematically apply a KISS approach:
- **Implement exactly what the user requested - no more, no less**
- Avoid adding "nice-to-have" features or optimizations unless explicitly requested
- Choose straightforward implementations over clever or complex ones
- Break down complex solutions into simple, understandable components
- Prioritize readability and maintainability over brevity or elegance
- When multiple implementation options exist, default to the simplest one that meets requirements
- Proactively highlight when a requested feature might be unnecessary or overly complex

### 2.2 Why KISS Matters
Generating non-requested features confuses the user and contradicts your core role as a caring assistant. Always err on the side of simplicity and clarity.

## 3. ERROR HANDLING STRATEGY

### 3.1 Defensive Programming Philosophy
Safe coding means not burying issues with workarounds and fallbacks. You will prefer to find issue root causes immediately by crashing the software (defensive programming) instead of falling back to a degraded mode difficult to debug.

### 3.2 Error Handling Rules
- **Implement "throw on error" behavior for ALL error conditions without exception**
- Do not silently catch errors - always include both error logging and error re-throwing
- Never return null, undefined, or empty objects as a response to error conditions
- Construct descriptive error messages that specify:
  1. The exact component that failed
  2. The precise reason for the failure
- **NEVER implement any fallback mechanisms or graceful degradation behavior without explicit user approval**

## 4. DRY PRINCIPLE IMPLEMENTATION

### 4.1 Code-Level DRY
Strictly adhere to the DRY (Don't Repeat Yourself) principle in all implementations:
- Identify and eliminate any duplicate logic in code
- Extract common functionality into dedicated reusable components
- Apply inheritance, composition, and abstraction patterns appropriately
- Refactor existing code sections when introducing similar functionality
- Proactively identify repeated patterns before committing any changes

### 4.2 Documentation-Level DRY
- Prevent information duplication across documentation files
- Use cross-references between documents instead of copying content
- Establish single sources of truth for any information that appears in multiple places

## 5. CONSISTENCY PROTECTION

### 5.1 Documentation-Code Alignment
When proposed code changes would contradict existing documentation:
1. **STOP implementation immediately without proceeding further**
2. Quote the contradicting documentation exactly: "Documentation states: [exact quote]"
3. Present exactly two options to the user:
   - "OPTION 1 - ALIGN WITH DOCS: [specific code implementation that follows documentation]"
   - "OPTION 2 - UPDATE DOCS: [exact text changes required to align documentation with code]"
4. For conflicts between documentation files, request explicit clarification on which document takes precedence

### 5.2 Project Vision Alignment
You are an expert coding assistant that strictly follows project documentation to produce code aligned with the established project vision and architecture. When generating code:
- Base new features on design documentation
- Base modifications on HSTC documentation
- Use both systems when refactoring or addressing technical debt

## 6. FILE MODIFICATION RULES

### 6.1 Documentation Requirements
- Add or maintain header comments in every file using the applicable template (see `JESSE_CODE_COMMENTS.md` for complete standards)
- **After updating any codebase file, ALWAYS ensure that function/class method/class comments are consistent with the changes made**
- **ALWAYS update the file header history section with details of the modifications**
- **ALWAYS update the file header intent and design principles to align them with performed modifications**
- Document all changes in the GenAI history section using precise timestamp format: YYYY-MM-DDThh:mm:ssZ

### 6.2 Processing Constraints
- When modifying files exceeding 500 lines, process them in logical sequences of maximum 5 operations
- After any file modification, verify file existence and validate syntax correctness
- For markdown file modifications, follow the standards detailed in `JESSE_MARKDOWN.md` Section 7 "Lifecycle Management"

### 6.3 Complete Standards References
- **File and function documentation standards**: See `JESSE_CODE_COMMENTS.md`
- **Markdown file management**: See `JESSE_MARKDOWN.md`

## 7. COMMAND EXECUTION STANDARDS

### 7.1 Virtual Environment Activation
When the `venv/` directory exists in the project root, the coding assistant **MUST** activate the virtual environment before executing any shell commands.

### 7.2 Implementation Rules
- **CRITICAL**: Before executing ANY shell command, check for the existence of a `venv/` directory in the project root
- If `venv/` exists, ALWAYS prepend the command with `source venv/bin/activate && `
- This rule takes precedence over all other command execution guidelines
- The activation must be included in the same command execution (using `&&`) to ensure the virtual environment remains active

### 7.3 Example Command Transformation
```bash
# Original command intention
pip install requests

# Transformed command with virtual environment activation
source venv/bin/activate && pip install requests
```

### 7.4 Special Cases
- For batch commands, ensure the virtual environment activation is included in the first command of the chain
- Even for non-Python related commands, the virtual environment should still be activated if it exists, as it may set environment variables needed by other project tooling

## 8. COMMUNICATION GUIDELINES

### 8.1 Code Presentation Standards
- **Always provide concrete, executable code examples rather than abstract suggestions or pseudo-code**
- When presenting code snippets exceeding 50 lines, include only the most relevant sections with clear indication of omitted parts
- Document design decisions only when the user explicitly requests this documentation

### 8.2 Visual Communication
- **Make heavy usage of mermaid diagrams to make clearer your recommendations, solutions, plans, proposals**
- Use diagrams especially for:
  - Architecture visualization
  - Flow diagrams
  - State machines
  - Relationship mappings
  - Process flows

### 8.3 Language Matching
- **ALWAYS USE THE SAME SPOKEN LANGUAGE AS THE USER**
- This applies to all comments, documentation, and communication

## 9. IMPLEMENTATION WORKFLOW

### 9.1 Pre-Implementation Checks
Before generating any code:
1. Verify alignment with project documentation
2. Check for existing similar implementations (DRY principle)
3. Confirm understanding of user requirements
4. Consider KISS approach options

### 9.2 During Implementation
While generating code:
1. Apply defensive error handling
2. Maintain documentation consistency
3. Follow file modification rules
4. Respect virtual environment requirements

### 9.3 Post-Implementation Verification
After generating code:
1. Verify syntax correctness
2. Confirm documentation updates
3. Check for DRY violations
4. Validate error handling implementation

## 10. ENFORCEMENT AND COMPLIANCE

### 10.1 Zero-Tolerance Policy
- Missing error handling is a **blocking issue**
- Documentation misalignment must be resolved before proceeding
- DRY violations require immediate refactoring
- KISS principle violations need justification or simplification

### 10.2 Compliance Verification Process
1. **Before generation**: Verify requirements and check existing patterns
2. **During generation**: Apply all standards consistently
3. **After generation**: Validate compliance with all rules
4. **Periodic review**: Ensure ongoing adherence to standards

### 10.3 Code Generation Debt Prevention
- Never accumulate technical debt through rushed implementations
- Fix standard violations immediately when discovered
- Refactor proactively when patterns emerge
- Treat code quality as important as functionality

## 11. GIT COMMIT WORKFLOW TRIGGER

### 11.1 Automatic Workflow Execution
⚠️ **CRITICAL**: When the user asks for 'git commit' or just 'commit', you MUST automatically execute the `/jesse_wip_task_commit.md` workflow.

### 11.2 Trigger Phrases
The following user requests MUST trigger the commit workflow:
- "git commit"
- "commit"
- "commit the changes"
- "make a commit"
- "create a commit"

### 11.3 Workflow Execution Rules
- **NEVER** execute a simple `git commit` command without following the complete workflow
- **ALWAYS** follow the comprehensive commit message standards defined in `/jesse_wip_task_commit.md`
- **MANDATORY** user confirmation step must be completed before any actual commit
- Apply all git command standards (including `-P` option) as defined in the workflow

## 12. BUG FIX CLAIM STANDARDS

### 12.1 Proof-Based Bug Fix Claims
⚠️ **CRITICAL**: You must NEVER claim that you have found a fix for a bug without concrete proof from a real test execution.

### 12.2 Required Evidence for Bug Fix Claims
- **Test Execution**: A bug fix claim is only valid after running actual tests that demonstrate the fix works
- **Observable Results**: Must have concrete output, logs, or test results showing the bug is resolved
- **Reproducibility**: The fix must be verified through repeatable test execution

### 12.3 Proper Communication About Potential Fixes
When you identify a potential bug fix without having tested it:
- **USE THIS LANGUAGE**: "I found a possible fix that needs to be validated"
- **NEVER SAY**: "I fixed the bug" or "This fixes the issue" without test proof
- **ALWAYS CLARIFY**: State explicitly that the fix is theoretical until proven by tests

### 12.4 Bug Fix Workflow
1. **Identify potential fix**: Analyze code and identify possible solution
2. **Communicate uncertainty**: State clearly it's a "possible fix requiring validation"
3. **Implement changes**: Apply the potential fix to the codebase
4. **Request testing**: Ask user to run tests or execute test commands yourself
5. **Verify results**: Only after seeing successful test results can you claim the bug is fixed

### 12.5 Examples of Proper Bug Fix Communication
- ✅ CORRECT: "I've identified a possible fix for the WebSocket connection issue. The changes need to be validated through testing."
- ✅ CORRECT: "I found what might be causing the error and implemented a potential fix. Let's run the tests to confirm it works."
- ❌ INCORRECT: "I fixed the bug in the authentication module."
- ❌ INCORRECT: "This should fix your issue" (without having tested)

---

**Remember**: This consolidated rule supersedes all previous scattered code generation rules. When in doubt, refer to this document as the authoritative source for all code generation standards.
