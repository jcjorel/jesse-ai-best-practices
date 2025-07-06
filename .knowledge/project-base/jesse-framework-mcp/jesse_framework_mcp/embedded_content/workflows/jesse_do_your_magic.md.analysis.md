<!-- CACHE_METADATA_START -->
<!-- Source File: {PROJECT_ROOT}/jesse-framework-mcp/jesse_framework_mcp/embedded_content/workflows/jesse_do_your_magic.md -->
<!-- Cached On: 2025-07-06T11:39:47.549697 -->
<!-- Source Modified: 2025-06-24T19:31:39.891821 -->
<!-- Cache Version: 1.0 -->
<!-- CACHE_METADATA_END -->

#### Functional Intent & Features

This file defines the comprehensive `Jesse Do Your Magic` workflow for performing deep-dive compliance analysis on code files within the Jesse Framework ecosystem, providing automated verification of adherence to project standards, documentation requirements, and architectural principles. The workflow delivers systematic code quality assessment through structured analysis phases including documentation standards verification, code quality evaluation, and reference validation. Key semantic entities include the `Do your magic` trigger phrase, `MAGIC MODE` activation response, `COMPLIANCE ANALYSIS` structured output format, `VSCode` editor integration for scope determination, documentation standards references to `JESSE_CODE_COMMENTS.md`, `JESSE_CODE_GENERATION.md`, `JESSE_MARKDOWN.md`, and `JESSE_SCRATCHPAD.md`, priority-based findings classification (`Critical Issues`, `High Priority`, `Medium Priority`, `Low Priority`), remediation plan generation with user confirmation requirements, and integration with operational modes including `PLAN mode` and `DESIGN mode`. The system enables developers to maintain code quality consistency across the project through automated analysis workflows triggered by natural language commands.

##### Main Components

The workflow contains six primary operational sections: trigger detection mechanism responding to `Do your magic` command variations, scope determination logic supporting default VSCode visible files and custom file/directory specifications, five-step workflow execution including magic mode initiation, compliance analysis performance, findings presentation, and remediation planning, three-component analysis framework covering documentation standards checking, code quality analysis, and reference validation, implementation guidelines specifying analysis depth requirements and communication protocols, and integration specifications with existing operational modes and project standards. The workflow supports flexible scope targeting from single files to directory-wide analysis with structured output formatting and user confirmation requirements for remediation actions.

###### Architecture & Design

The architecture implements a trigger-response workflow pattern with structured analysis phases and priority-based output organization. The design uses command-pattern activation through natural language trigger detection, scope-flexible analysis supporting both default editor context and explicit file/directory targeting, and hierarchical analysis framework with three specialized components for comprehensive code evaluation. The system employs structured output formatting with consistent analysis reporting templates, priority-based findings classification enabling focused remediation efforts, and integration-aware design respecting existing operational mode constraints. The workflow follows a confirmation-required remediation pattern preventing automatic code modifications without explicit user approval, ensuring safe operation within development environments.

####### Implementation Approach

The implementation uses natural language trigger detection for workflow activation, context-aware scope determination leveraging VSCode editor state for default targeting, and systematic analysis execution through predefined evaluation criteria. The approach employs template-based output formatting with structured analysis reporting including specific line references and concrete examples, priority-based findings organization enabling efficient issue triage, and comprehensive standards validation against multiple project documentation sources. The system implements confirmation-gated remediation with explicit user approval requirements, multi-mode integration supporting workflow execution within existing operational constraints, and iterative analysis capabilities allowing re-verification of implemented fixes.

######## External Dependencies & Integration Points

**→ References:**
- `JESSE_CODE_COMMENTS.md` - code documentation standards and file header requirements for compliance verification
- `JESSE_CODE_GENERATION.md` - code generation standards and best practices for quality assessment
- `JESSE_MARKDOWN.md` - markdown formatting standards for documentation validation
- `JESSE_SCRATCHPAD.md` - scratchpad usage standards and reference validation rules
- `VSCode` editor integration - visible file detection and scope determination for default analysis targeting

**← Referenced By:**
- Development workflows - consume compliance analysis results for code quality maintenance
- Code review processes - integrate findings for systematic quality assessment
- Project maintenance activities - use remediation plans for systematic improvement efforts
- Quality assurance workflows - leverage analysis results for standards compliance verification

**⚡ System role and ecosystem integration:**
- **System Role**: Core quality assurance workflow within the Jesse Framework development ecosystem, providing automated compliance verification and remediation guidance for maintaining project standards consistency
- **Ecosystem Position**: Central development support tool integrating with editor environments and project documentation standards to enable systematic code quality maintenance
- **Integration Pattern**: Triggered by developers through natural language commands, consumes project standards documentation, and produces structured analysis reports with actionable remediation guidance

######### Edge Cases & Error Handling

The workflow handles scope determination failures by defaulting to currently visible VSCode files when custom scope specifications are invalid or inaccessible. Missing or outdated project standards documentation is addressed through graceful degradation with warnings about incomplete analysis coverage. Complex remediation scenarios trigger automatic escalation to `PLAN mode` for structured implementation planning when fixes require significant architectural changes. Analysis depth limitations are managed through clear communication about scope boundaries and analysis coverage when dealing with large directory structures or complex codebases. Integration conflicts with active operational modes are resolved through mode-aware execution that respects existing constraints while providing maximum analysis value within operational boundaries.

########## Internal Implementation Details

The trigger detection mechanism uses exact phrase matching for `Do your magic` with case-insensitive processing and support for scope specification parsing following the command. Scope determination logic implements fallback hierarchy from explicit file/directory specifications to VSCode visible files to current working directory when no context is available. Analysis execution follows structured template processing with line-specific reference generation, concrete example extraction, and priority classification based on predefined severity criteria. Output formatting uses consistent markdown structure with code block formatting for examples and structured lists for findings organization. Remediation planning employs complexity estimation algorithms and related fix grouping for efficient implementation workflows. Mode integration uses conditional execution paths that adapt workflow behavior based on active operational constraints while maintaining core analysis functionality.

########### Code Usage Examples

This example demonstrates the basic workflow trigger and response pattern for single file analysis. The structured output format provides consistent analysis reporting with clear status indicators and systematic evaluation criteria.

```
User: "Do your magic"
Assistant: ENTERING MAGIC MODE 😉! Performing deep-dive analysis on system prompt...

[COMPLIANCE ANALYSIS: current_file.py]
- Checking strict respect to documentation standards...
- Analyzing code structure against design principles...
- Verifying documentation references relevance...
```

This example shows custom scope specification for directory-wide analysis with structured findings presentation. The priority-based classification enables efficient issue triage and focused remediation efforts.

```
User: "Do your magic src/components/"
Assistant: [Analyzes all files in src/components/ directory]

Critical Issues:
- Missing file headers in 3 files (lines: src/components/auth.py:1)
- Violated design principles in authentication logic

High Priority:
- Misaligned function intents in user management module
- Complex code sections exceeding cyclomatic complexity thresholds
```

This example illustrates the remediation confirmation workflow with priority-based action planning. The confirmation-gated approach ensures safe operation by requiring explicit user approval before implementing any code modifications.

```
Remediation Plan:
1. Critical: Add missing file headers (Est: 30 min)
2. High: Refactor complex authentication logic (Est: 2 hours)
3. Medium: Update outdated dependency references (Est: 45 min)

CRITICAL: Do you want me to implement these recommendations? [Awaiting confirmation]
```