# Jesse Do Your Magic Workflow

## Purpose
Perform a deep-dive compliance analysis on code files to verify adherence to project standards, documentation requirements, and best practices. This workflow helps identify areas where code quality, documentation, or architectural principles may need improvement.

## Trigger
When user types "Do your magic" in their request.

## Scope Determination
- **Default scope**: Currently displayed file in editor (VSCode visible files)
- **Custom scope**: Files/directories listed after command (e.g., "Do your magic src/components/auth")

## Workflow Steps

### 1. Initiate Magic Mode
Respond with exactly:
```
ENTERING MAGIC MODE 😉! Performing deep-dive analysis on system prompt...
```

### 2. Perform Compliance Analysis
Analyze the specified scope against all project standards:

```
[COMPLIANCE ANALYSIS: {scope}]
- Checking strict respect to documentation standards...
- Checking that source file intent reflects functions/class/methods intents
- Analyzing code structure against design principles...
- Checking code cyclomatic complexity...
- Assessing code maintainability... 
- Verifying documentation references relevance...
{detailed findings with specific line references}
{recommendations for improving compliance}
```

### 3. Analysis Components

#### Documentation Standards Check
- Verify file header completeness (see `JESSE_CODE_COMMENTS.md`)
- Check three-section pattern compliance for all functions/methods/classes
- Validate change history format and recency
- Ensure dependency documentation accuracy

#### Code Quality Analysis
- **Intent Alignment**: Verify source file intent matches actual implementation
- **Function/Method Intents**: Check if documented intents reflect actual behavior
- **Design Principles**: Validate adherence to documented design patterns
- **Cyclomatic Complexity**: Identify overly complex code sections
- **Maintainability**: Assess code readability and structure

#### Reference Validation
- Check if documented dependencies exist and are current
- Verify markdown file references are valid
- Ensure no references to scratchpad files
- Validate cross-references between related files

### 4. Present Findings
Structure findings in priority order:
1. **Critical Issues**: Missing documentation, violated standards
2. **High Priority**: Misaligned intents, complex code sections
3. **Medium Priority**: Outdated references, minor inconsistencies
4. **Low Priority**: Style improvements, optional enhancements

### 5. Propose Remediation Plan
After completing the analysis:
- Present a prioritized list of remediation actions
- Group related fixes together
- Estimate complexity for each remediation
- **CRITICAL**: Explicitly ask for user confirmation before implementing any recommendations

## Implementation Guidelines

### Analysis Depth
- Read all relevant files completely before analysis
- Use line-specific references for all findings
- Provide concrete examples of issues found
- Suggest specific fixes, not generic improvements

### Communication Style
- Use technical but clear language
- Include code snippets to illustrate issues
- Provide rationale for each recommendation
- Maintain encouraging tone while being thorough

### Integration with Modes
- This workflow can trigger PLAN mode if remediation is complex
- Works within current operational mode constraints
- Respects DESIGN mode restrictions if active

## Example Usage

### Simple File Analysis
```
User: "Do your magic"
Assistant: [Analyzes currently visible file in VSCode]
```

### Directory Analysis
```
User: "Do your magic src/components/"
Assistant: [Analyzes all files in src/components/ directory]
```

### Multiple Files
```
User: "Do your magic backend/main.py backend/services/nova_sonic_service.py"
Assistant: [Analyzes specified files]
```

## Related Standards
- Code documentation standards: `JESSE_CODE_COMMENTS.md`
- Code generation standards: `JESSE_CODE_GENERATION.md`
- Markdown standards: `JESSE_MARKDOWN.md`
- Scratchpad standards: `JESSE_SCRATCHPAD.md`

## Post-Analysis Actions
1. Wait for user confirmation before implementing fixes
2. If approved, implement changes following all project standards
3. Update file headers with change history
4. Verify fixes resolve identified issues
5. Re-run analysis if requested to confirm improvements
