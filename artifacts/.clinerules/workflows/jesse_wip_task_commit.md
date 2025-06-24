# WIP Task Commit Workflow

## Purpose
Create comprehensive, standards-compliant git commit messages that include multi-line details, leveraging git diff analysis and file history data to ensure accuracy and completeness.

## When to Use
- When committing any code changes to the repository
- After completing implementation of a WIP task or subtask
- When fixing bugs or making improvements
- For any repository changes that need version control

**Important Note**: When the `/jesse_wip_task_disable.md` workflow has been used to disable WIP task auto-loading, this commit workflow applies to the entire Git repository changes rather than being scoped to a specific WIP task context. In this case, commit messages should reflect the broader repository-wide changes being made.

## Workflow Steps

### 1. Analyze Changes with Git Diff
Run git diff commands to gather comprehensive information about changes:

```bash
# View unstaged changes
git -P diff

# View staged changes
git -P diff --staged

# Get file statistics
git -P diff --staged --stat

# Get list of modified files
git -P diff --staged --name-only
```

### 2. Extract Context from File History
For each modified file, examine:
- `[GenAI tool change history]` sections in file headers
- `[Function intent]` and `[Design principles]` in modified functions
- Recent changes to understand evolution patterns
- Dependencies and constraints documented in headers

### 3. Prepare Commit Message Structure
Create a commit message following this mandatory format:

```
<type>(<scope>): <subject line - max 72 chars>

[Commit intent]
<WHY this change was made>

[Implementation details]
<WHAT was changed and HOW>

[Impact analysis]
<Systems affected by this change>

[Testing performed]
<Validation and testing done>

[Related items]
- Issue: #<number>
- PR: #<number>
- Docs: <updates>
```

### 4. Fill Required Sections

#### 4.1 Subject Line
- Format: `<type>(<scope>): <subject>`
- Types: feat, fix, refactor, docs, test, perf, style, build, ci, chore
- Scope: Specific component/module name
- Subject: Imperative mood, max 72 chars total

#### 4.2 [Commit intent]
- Explain WHY the change was necessary
- Reference specific problems being solved
- Connect to project goals or user needs
- Use git diff data to ensure accuracy

#### 4.3 [Implementation details]
- **Maximum 4 lines (except when there are more than 4 major functional or technical changes)**
- List specific files modified (from git diff --name-only)
- Explain algorithms/approaches used
- Document architectural decisions
- Include line counts from git diff --stat
- Use bullet points for conciseness

#### 4.4 [Testing performed]
- **CRITICAL**: Only state tests were performed if you have concrete proof of test execution
- List specific tests run with evidence (test output, logs, screenshots)
- Include test results/metrics with actual numbers
- Document manual testing scenarios with verification details
- Mention edge cases verified with specific outcomes
- If no testing was performed, state "No testing performed" explicitly

#### 4.5 [Impact analysis]
- **Maximum 4 lines (except when there are more than 4 major functional or technical changes)**
- List affected components/systems
- Identify potential side effects
- Document breaking changes
- Note configuration impacts
- Use bullet points for conciseness

#### 4.6 [Related items]
- Link to issues/PRs
- Reference documentation updates
- Include WIP task references if applicable

### 5. Validate Commit Message
Before finalizing, verify:
- ✓ All 5 required sections present
- ✓ Subject line ≤ 72 characters
- ✓ Valid type and scope format
- ✓ Meaningful content (no placeholders)
- ✓ Accurate file references from git diff
- ✓ Alignment with file documentation

### 6. Present Commit Message for User Review
**MANDATORY USER CONFIRMATION STEP**:
1. Present the complete commit message to the user in a clear, formatted manner
2. Ask the user to review the commit message content for:
   - Accuracy of the technical details
   - Completeness of all required sections
   - Alignment with the actual changes made
   - Overall clarity and usefulness
3. **CRITICAL**: Ask explicitly: "Please review this commit message. Do you approve this commit message and confirm that the commit can proceed? (Yes/No)"
4. **Wait for explicit user confirmation** before proceeding to step 7
5. If user requests changes, return to step 3 to revise the commit message
6. Only proceed to commit creation after receiving explicit user approval

### 7. Create the Commit
```bash
# Option 1: Use git commit to open editor
git commit

# Option 2: Use git commit -m with proper formatting
git commit -m "type(scope): subject" -m "[Commit intent]..." -m "[Implementation details]..."
```

## Implementation Notes

### Definition of Major Functional or Technical Changes
The 4-line limit exception applies when a commit contains more than 4 of these major change types:

- **New API endpoints or significant API modifications**
- **Database schema changes (tables, columns, indexes)**
- **New architectural components or services**
- **Security-related modifications**
- **Performance optimizations affecting multiple systems**
- **Breaking changes to existing functionality**
- **Integration with new external services**
- **Bug fixes requiring changes across 3+ files/modules**
- **Configuration changes affecting system behavior**

### Git Diff Integration
Always use git diff data to populate:
- File names in [Implementation details]
- Change statistics (lines added/removed)
- Nature of modifications
- Affected functions/methods

### File History Leveraging
Cross-reference with file headers to ensure:
- Changes align with stated design principles
- Intent matches documented constraints
- History section gets updated post-commit

### Quality Standards
- Be specific, not vague ("fix bug" is forbidden)
- Include technical reasoning
- Document the "why" not just the "what"
- Make commit messages valuable for future developers

### Special Cases

#### Breaking Changes
Add a `[BREAKING CHANGE]` section:
```
[BREAKING CHANGE]
- API endpoint changed from /v1 to /v2
- Removed deprecated parameters
- Migration guide: docs/MIGRATION.md
```

#### Emergency Fixes
Even emergency fixes need full documentation:
```
fix(critical): Emergency patch for data loss

[Commit intent]
CRITICAL: Active data loss in production...
[Continue with all sections]
```

## Commit Message Standards Reference

## 2. COMMIT MESSAGE STRUCTURE

### 2.1 Mandatory Three-Part Structure
Every commit message MUST follow this exact structure:

```
<type>(<scope>): <subject line - max 72 chars>

[Commit intent]
<Comprehensive description of WHY this change was made>

[Implementation details]
<Technical details of WHAT was changed and HOW>

[Testing performed]
<Description of validation and testing done>

[Impact analysis]
<Systems, files, or features affected by this change>

[Related items]
- Issue: #<issue-number> (if applicable)
- PR: #<pr-number> (if applicable)
- Docs: <documentation-updates> (if applicable)
```

### 2.2 Type Definitions
Use these exact commit types:
- `feat`: New feature implementation
- `fix`: Bug fix or issue resolution
- `refactor`: Code restructuring without behavior change
- `docs`: Documentation-only changes
- `test`: Test additions or modifications
- `perf`: Performance improvements
- `style`: Code style/formatting changes
- `build`: Build system or dependency changes
- `ci`: CI/CD configuration changes
- `chore`: Maintenance tasks

### 2.3 Scope Requirements
- **Scope MUST be specific and meaningful**
- Use component, module, or feature names
- Examples: `(auth)`, `(api)`, `(nova-sonic)`, `(database)`
- Avoid generic scopes like `(misc)` or `(various)`

### 2.4 Subject Line Standards
- Maximum 72 characters including type and scope
- Use imperative mood ("Add feature" not "Added feature")
- No period at the end
- Capitalize first word after colon

## 3. REQUIRED SECTIONS

### 3.1 [Commit intent] Section
**Purpose**: Explain WHY this change was necessary
**Requirements**:
- Provide business or technical context
- Reference specific problems being solved
- Explain the motivation for the change
- Connect to project goals or user needs

**Example**:
```
[Commit intent]
Users reported intermittent WebSocket disconnections during Nova Sonic 
audio streaming sessions. This change implements automatic reconnection 
logic to maintain seamless audio processing even when network issues occur.
```

### 3.2 [Implementation details] Section
**Purpose**: Document WHAT was changed and HOW
**Requirements**:
- **Maximum 4 lines (except when there are more than 4 major functional or technical changes)**
- List specific files modified with brief descriptions
- Explain key algorithms or approaches used
- Document architectural decisions made
- Include technical reasoning for implementation choices
- Use concise bullet points to stay within limit

**Example**:
```
[Implementation details]
- Modified websocket_manager.py to add exponential backoff retry logic
- Implemented reconnection queue in nova_sonic_service.py
- Added connection state management with 3 retry attempts
- Used asyncio.wait_for() with 5-second timeout for reconnection
- Preserved audio buffer during reconnection attempts
```

### 3.3 [Testing performed] Section
**Purpose**: Document validation and quality assurance
**Requirements**:
- List specific tests run
- Include test results or performance metrics
- Document manual testing scenarios
- Mention edge cases verified

**Example**:
```
[Testing performed]
- Ran full test suite: 127 passed, 0 failed
- Manual testing with network throttling (3G, 4G, WiFi)
- Tested disconnection scenarios at various streaming points
- Verified audio buffer preservation during 5-second outages
- Performance: Reconnection completes in <500ms average
```

### 3.4 [Impact analysis] Section
**Purpose**: Document the scope and effects of changes
**Requirements**:
- **Maximum 4 lines (except when there are more than 4 major functional or technical changes)**
- List all affected components or systems
- Identify potential side effects
- Document breaking changes (if any)
- Note configuration or deployment impacts
- Use concise bullet points to stay within limit

**Example**:
```
[Impact analysis]
- WebSocket connections now auto-recover from network issues
- No API changes - backward compatible
- May increase server connection count during recovery
- Requires NOVA_SONIC_RECONNECT_ENABLED=true in production
```

### 3.5 [Related items] Section
**Purpose**: Link to related issues, PRs, and documentation
**Format**:
```
[Related items]
- Issue: #234 (WebSocket disconnection reports)
- PR: #567 (if applicable)
- Docs: Updated NOVA_SONIC_API.md with reconnection behavior
```

## 4. COMMIT MESSAGE EXAMPLES

### 4.1 Feature Implementation Example
```
feat(nova-sonic): Add automatic WebSocket reconnection with buffering

[Commit intent]
Users experienced disrupted audio transcription when network connectivity
briefly dropped during streaming sessions. This feature ensures continuous
service by automatically reconnecting and preserving audio data.

[Implementation details]
- Created ReconnectionManager class in websocket_manager.py
- Implemented circular buffer for audio data (5-second capacity)
- Added exponential backoff: 100ms, 200ms, 400ms, 800ms, 1600ms
- Integrated with existing WebSocketManager lifecycle
- Used asyncio.Queue for thread-safe audio buffering

[Testing performed]
- Unit tests: 15 new tests for ReconnectionManager
- Integration tests: Simulated 50 disconnection scenarios
- Load testing: 100 concurrent connections with random disconnects
- Manual testing on unstable mobile networks
- All existing tests pass without modification

[Impact analysis]
- Improves reliability for mobile and unstable network users
- Adds ~50KB memory overhead per active connection
- No changes to client API or existing behavior
- Graceful degradation if reconnection fails after 5 attempts

[Related items]
- Issue: #1234 (User reports of streaming interruptions)
- Docs: Added reconnection section to NOVA_SONIC_API.md
```

### 4.2 Bug Fix Example (4-Line Limit Compliant)
```
fix(auth): Resolve token expiration race condition in parallel requests

[Commit intent]
Multiple parallel API requests near token expiration time caused 
authentication failures. The first request would refresh the token,
but subsequent requests used the old token before the refresh completed.

[Implementation details]
- Added token refresh mutex in aws_credentials_manager.py
- Implemented request queuing during token refresh
- Cache refreshed tokens with 5-minute early expiration
- Modified _ensure_valid_token() to be thread-safe

[Testing performed]
- Reproduced original issue with 10 parallel requests
- Verified fix with 100 parallel requests near expiration
- Token refresh called exactly once per expiration
- No performance degradation in normal operation
- Added test_parallel_token_refresh() test case

[Impact analysis]
- Fixes intermittent 401 errors in high-concurrency scenarios
- Slight latency increase (~10ms) for requests during refresh
- No API changes required
- Improved reliability for batch processing operations

[Related items]
- Issue: #789 (Intermittent auth failures)
- Issue: #790 (Duplicate token refresh calls)
```

### 4.3 Refactoring Example
```
refactor(database): Extract repository pattern from service layer

[Commit intent]
Service classes contained mixed business logic and database queries,
making testing difficult and violating single responsibility principle.
This refactor separates data access into dedicated repository classes.

[Implementation details]
- Created repository/ directory with base Repository class
- Extracted UserRepository from UserService (12 methods)
- Extracted TranscriptionRepository from TranscriptionService (8 methods)
- Services now dependency-inject repositories
- Implemented repository interfaces for testing
- Moved SQL queries to repository constants

[Testing performed]
- All existing service tests pass unchanged
- Added 25 repository-specific unit tests
- Integration tests verify same database behavior
- Performance benchmarks show no regression
- Mock repositories simplify service testing

[Impact analysis]
- Improves testability and separation of concerns
- No external API changes
- Database queries now centralized for optimization
- Foundation for future caching layer
- Requires repository registration in dependency injection

[Related items]
- Docs: Updated ARCHITECTURE.md with repository pattern
- Docs: Added section to DEVELOPMENT.md on testing repositories
```

## 5. VALIDATION AND ENFORCEMENT

### 5.1 Pre-Commit Validation
Every commit message MUST pass these checks:
1. ✓ Contains all 5 required sections
2. ✓ Subject line ≤ 72 characters
3. ✓ Valid type and scope format
4. ✓ Each section has meaningful content (not placeholder text)
5. ✓ No single-line commits
6. ✓ Proper section headers with square brackets
7. ✓ [Implementation details] and [Impact analysis] ≤ 4 lines (unless >4 major changes)

### 5.2 Content Quality Standards
- **Specificity**: Avoid vague descriptions like "fix bug" or "update code"
- **Completeness**: Each section must fully address its purpose
- **Accuracy**: Technical details must match actual implementation
- **Clarity**: Use clear, technical language without ambiguity
- **Relevance**: Include only information relevant to the commit

### 5.3 Automated Enforcement
```bash
# Git hook example for .git/hooks/commit-msg
#!/bin/bash
# Validates commit message format

required_sections=(
    "[Commit intent]"
    "[Implementation details]"
    "[Testing performed]"
    "[Impact analysis]"
    "[Related items]"
)

commit_msg=$(cat "$1")

# Check for required sections
for section in "${required_sections[@]}"; do
    if ! grep -q "^$section" "$1"; then
        echo "ERROR: Missing required section: $section"
        exit 1
    fi
done

# Validate subject line length
first_line=$(head -n 1 "$1")
if [ ${#first_line} -gt 72 ]; then
    echo "ERROR: Subject line exceeds 72 characters"
    exit 1
fi
```

## 6. SPECIAL COMMIT TYPES

### 6.1 Breaking Changes
For commits with breaking changes, add a breaking change section:
```
[BREAKING CHANGE]
- Changed API endpoint from /api/v1/transcribe to /api/v2/transcribe
- Removed deprecated 'format' parameter
- Response structure now includes 'metadata' wrapper
- Migration guide: docs/MIGRATION_V2.md
```

### 6.2 Emergency Fixes
Even emergency fixes require full documentation:
```
fix(critical): Emergency patch for data loss in streaming buffer

[Commit intent]
CRITICAL: Active data loss occurring in production when buffer 
overflows. This emergency fix prevents data corruption while 
proper solution is developed.

[Implementation details]
- Added overflow check in streaming_audio_processor.py
- Temporary: Drop oldest frames when buffer full
- Added error logging for overflow events
- Set buffer limit to 10MB (was unlimited)

[Testing performed]
- Verified data loss prevention in overflow scenario
- Confirmed no data loss under normal load
- Emergency production test on staging environment
- Performance impact negligible (<1% CPU increase)

[Impact analysis]
- Prevents data corruption immediately
- May drop audio frames under extreme load
- Temporary solution - proper fix tracked in #999
- No API changes

[Related items]
- Issue: #998 (CRITICAL: Data corruption in streaming)
- Follow-up: #999 (Implement proper buffer management)
```

### 6.3 Documentation-Only Changes
Even documentation changes need context:
```
docs(api): Clarify WebSocket connection lifecycle and error handling

[Commit intent]
Developers were confused about WebSocket state transitions and error
recovery procedures. This update provides clear examples and state
diagrams for all connection scenarios.

[Implementation details]
- Added state diagram to NOVA_SONIC_API.md
- Documented all error codes with examples
- Added troubleshooting section with common issues
- Included code snippets for each connection phase
- Created error handling best practices guide

[Testing performed]
- Validated all code examples execute correctly
- Checked links and references
- Reviewed with 3 team members for clarity
- Tested mermaid diagrams render properly

[Impact analysis]
- Improves developer experience
- Reduces support questions about WebSocket errors
- No code changes
- May require translation updates

[Related items]
- Issue: #456 (WebSocket documentation unclear)
- Feedback: Developer survey Q3 2024
```

## 7. COMMIT MESSAGE ANTI-PATTERNS

### 7.1 Forbidden Practices
- ❌ Single-line commits: "Fix bug"
- ❌ Vague descriptions: "Update files"
- ❌ Missing sections: Partial commit messages
- ❌ Placeholder text: "TODO: Add details"
- ❌ Multiple unrelated changes in one commit
- ❌ Personal notes: "Finally got this working!"
- ❌ Temporal references: "Fix yesterday's bug"

### 7.2 Common Mistakes to Avoid
- Using past tense instead of imperative mood
- Forgetting to update issue references
- Copy-pasting sections from previous commits
- Including commented code in commit messages
- Making sections too brief or too verbose
- Focusing on what without explaining why

## 8. INTEGRATION WITH PROJECT WORKFLOW

### 8.1 Commit Message and Code Review
- Reviewers MUST verify commit message completeness
- Commit messages are part of code review criteria
- Incomplete messages block PR approval
- Reviewers should suggest improvements

### 8.2 Commit Message and Documentation
- Significant commits should trigger documentation updates
- Commit messages serve as changelog sources
- [Related items] section must list documentation changes
- Feature commits should reference updated user guides

### 8.3 Commit Message and Issue Tracking
- Always link to related issues when applicable
- Close issues with proper commit references
- Use issue numbers for traceability
- Update issue status based on commit type

## 9. COMMIT MESSAGE PREPARATION WORKFLOW

### 9.1 Using Git Diff for Commit Preparation
**CRITICAL**: Before writing any commit message, you MUST use `git diff` to analyze changes and gather comprehensive information:

```bash
# View unstaged changes
git -P diff

# View staged changes
git -P diff --staged

# View changes with context
git -P diff -U10  # Shows 10 lines of context

# View changes for specific files
git -P diff path/to/file.py
```

### 9.2 Leveraging File History Data
When preparing commit messages, extract valuable context from:

1. **File Header History**:
   - Check the `[GenAI tool change history]` section in modified files
   - Reference recent changes to understand evolution
   - Identify patterns or related modifications

2. **Function/Method Documentation**:
   - Review `[Function intent]` sections for context
   - Check `[Design principles]` to ensure alignment
   - Verify `[Implementation details]` match your changes

3. **Data Sources for Implementation Details**:
   ```bash
   # Get list of modified files
   git -P diff --name-only
   
   # Get statistics about changes
   git -P diff --stat
   
   # Get word-level diff for better granularity
   git -P diff --word-diff
   ```

### 9.3 Commit Message Creation Process
1. **Run git diff to analyze changes**:
   ```bash
   git -P diff --staged
   ```

2. **Extract key information**:
   - File names and paths modified
   - Nature of changes (additions, deletions, modifications)
   - Specific functions or methods affected
   - Line counts and change statistics

3. **Cross-reference with file documentation**:
   - Read file headers for design context
   - Check function documentation for intent
   - Verify alignment with stated principles

4. **Construct comprehensive commit message**:
   - Use diff data for `[Implementation details]`
   - Reference file history for continuity
   - Include specific line numbers when relevant

### 9.4 Example Workflow
```bash
# 1. Stage your changes
git add -p  # Interactive staging for precision

# 2. Analyze staged changes
git -P diff --staged --stat
git -P diff --staged

# 3. Review file headers and documentation
# (Check modified files for context)

# 4. Create commit with comprehensive message
git commit  # Opens editor with template
```

## 10. TOOLING AND AUTOMATION

### 10.1 Commit Message Templates
Configure git to use a template:
```bash
# .gitmessage template
<type>(<scope>): <subject>

[Commit intent]


[Implementation details]


[Testing performed]


[Impact analysis]


[Related items]
- Issue: #
- PR: #
- Docs: 
```

### 10.2 IDE Integration
- Configure IDE commit dialog with template
- Use snippets for common sections
- Enable commit message linting
- Set up pre-commit validation

### 10.3 Helpful Commands
```bash
# Set up commit template
git config --local commit.template .gitmessage

# Amend commit message
git commit --amend

# View commit with full message
git -P show --format=fuller

# Search commits by message content
git -P log --grep="[Commit intent]"

# Pre-commit diff analysis
git -P diff --staged --name-status
git -P diff --staged --stat
```

## 10. ENFORCEMENT AND COMPLIANCE

### 10.1 Zero-Tolerance Policy
- Missing required sections is a **blocking issue**
- Single-line commits must be amended immediately
- Vague descriptions require revision
- Quality is as important as code changes

### 10.2 Compliance Verification Process
1. **Before commit**: Use template and fill all sections
2. **During commit**: Validate against standards
3. **Code review**: Verify message quality
4. **Post-merge**: Monitor for compliance trends

### 10.3 Continuous Improvement
- Regular team reviews of commit message quality
- Update templates based on project evolution
- Share exemplary commit messages as references
- Refine sections based on team feedback

---

**Remember**: This consolidated rule supersedes all previous scattered commit message rules. When in doubt, refer to this document as the authoritative source for all git commit message standards. Every commit tells a story - make it complete, clear, and valuable for future developers.
