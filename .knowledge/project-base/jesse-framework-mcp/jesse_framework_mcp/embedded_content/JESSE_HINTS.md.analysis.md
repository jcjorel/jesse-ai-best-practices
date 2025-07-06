<!-- CACHE_METADATA_START -->
<!-- Source File: {PROJECT_ROOT}/jesse-framework-mcp/jesse_framework_mcp/embedded_content/JESSE_HINTS.md -->
<!-- Cached On: 2025-07-06T12:21:48.962331 -->
<!-- Source Modified: 2025-06-26T13:30:02.419243 -->
<!-- Cache Version: 1.0 -->
<!-- CACHE_METADATA_END -->

#### Functional Intent & Features

This file serves as the critical AI assistant enforcement rules document for the Jesse Framework MCP project, establishing mandatory security protocols, language standards, and path portability requirements that govern AI assistant behavior across all framework operations. The system provides comprehensive enforcement mechanisms for user identity protection, feature presentation standards, and cross-platform compatibility through strict compliance requirements and automated validation protocols. Key semantic entities include `JESSE_USER_IDENTITY.md` file location enforcement at `${HOME}/Cline/Rules/` exclusively, 9 mandatory user information fields (firstname, lastname, corporate login, job description, country, town, timezone, company name, corporate URL), `PII` protection requirements preventing repository commits, `.gitignore` protection patterns for user identity files, established functionality presentation language standards prohibiting temporal references like "new" or "enhanced", `Amazon PR/FAQ` document exceptions allowing feature announcement language, `${HOME}` environment variable requirements for portable file paths, absolute path prohibition patterns (`/home/[username]/`, `/Users/[username]/`, `C:\Users\[username]\`), and comprehensive enforcement mechanisms with violation consequences ensuring security compliance, professional presentation standards, and cross-platform portability across all Jesse Framework operations.

##### Main Components

The document contains three primary enforcement rule sections establishing comprehensive AI assistant behavior governance: User Identity File enforcement defining mandatory location requirements, PII protection protocols, and interactive collection procedures for 9 required user information fields; Feature Language Standards specifying established functionality presentation requirements, temporal reference prohibitions, and Amazon document exceptions for PR/FAQ and Working Backwards formats; and Portable File Path Standards enforcing `${HOME}` variable usage, absolute path prohibitions, and cross-platform compatibility requirements. Supporting components include mandatory AI assistant actions for file existence checking and interactive field collection, automatic protection requirements through `.gitignore` pattern addition, violation consequence specifications with framework operation refusal, enforcement mechanisms with document type identification and language pattern validation, and comprehensive compliance checklists ensuring security validation, language standard adherence, and path portability verification across all framework operations.

###### Architecture & Design

The architecture implements a multi-layered enforcement model with mandatory security protocols, language standardization mechanisms, and path portability validation ensuring consistent AI assistant behavior across all Jesse Framework operations. The design employs strict location-based security for user identity files, comprehensive language pattern enforcement with document type exceptions, and universal path portability requirements preventing platform-specific implementations. The system uses automated validation protocols with immediate violation detection, interactive user information collection with completeness verification, and cross-platform compatibility enforcement through environment variable usage. The architectural pattern includes non-negotiable enforcement mechanisms with framework operation refusal for violations, document type-aware language processing allowing Amazon format exceptions, and comprehensive compliance verification protocols ensuring security, presentation standards, and portability requirements are maintained across all AI assistant interactions.

####### Implementation Approach

The implementation uses mandatory file location validation for `JESSE_USER_IDENTITY.md` exclusively at `${HOME}/Cline/Rules/` with automatic security violation detection and framework operation refusal for misplaced files. The approach employs interactive user information collection with 9-field completeness verification, automatic `.gitignore` protection pattern addition, and comprehensive PII security enforcement. Language standardization uses document type identification distinguishing Amazon PR/FAQ formats from standard documentation, temporal reference pattern detection and prohibition, and established functionality presentation requirements. Path portability enforcement employs `${HOME}` environment variable validation, absolute path pattern detection and replacement, and cross-platform compatibility verification ensuring consistent behavior across Linux, macOS, and Windows systems.

######## External Dependencies & Integration Points

**→ References:**
- `${HOME}/Cline/Rules/JESSE_USER_IDENTITY.md` - mandatory user identity file location with exclusive placement requirements
- `.gitignore` files - automatic protection pattern addition for user identity file security
- `Amazon PR/FAQ` document formats - exception handling for feature announcement language requirements
- `Working Backwards` methodology documents - exception handling for future functionality description language
- Environment variable systems - `${HOME}`, `$HOME`, and tilde expansion for portable path references
- Cross-platform file systems - Linux, macOS, and Windows path compatibility requirements

**← Referenced By:**
- All Jesse Framework AI assistant operations - consume enforcement rules for behavior compliance and security validation
- User identity collection workflows - reference mandatory field requirements and interactive collection procedures
- Documentation generation processes - apply language standardization rules and established functionality presentation
- File path generation systems - enforce portable path standards and environment variable usage
- Security validation procedures - implement PII protection protocols and location-based enforcement mechanisms
- Installation and setup processes - verify compliance with user identity file placement and protection requirements

**⚡ System role and ecosystem integration:**
- **System Role**: Critical behavioral enforcement system for AI assistants within the Jesse Framework MCP ecosystem, establishing mandatory security, language, and portability standards that govern all framework operations
- **Ecosystem Position**: Core governance component that defines non-negotiable requirements for AI assistant behavior, ensuring consistent security protocols, professional presentation standards, and cross-platform compatibility
- **Integration Pattern**: Enforced by all AI assistant interactions through mandatory compliance checking, integrated with security validation systems for user identity protection, coordinated with documentation generation for language standardization, and applied universally across all file path operations for portability assurance

######### Edge Cases & Error Handling

The system addresses user identity file misplacement through immediate framework operation refusal with security violation warnings and mandatory relocation requirements to the global location. Missing user information fields trigger interactive collection procedures with completeness verification and mandatory field population before framework operation. Language standard violations in non-Amazon documents receive automatic correction with temporal reference removal and established functionality presentation. Path portability violations trigger immediate correction requirements with hardcoded user path replacement using `${HOME}` environment variables. The system handles Amazon document format exceptions through document type identification allowing appropriate language patterns while maintaining standard enforcement for other documentation. Installation compliance failures prevent framework operation until all security, language, and portability requirements are satisfied with comprehensive validation protocols.

########## Internal Implementation Details

The user identity enforcement system uses file existence checking at `${HOME}/Cline/Rules/JESSE_USER_IDENTITY.md` with automatic security validation and interactive field collection for 9 mandatory user information requirements. Language standardization employs pattern matching algorithms detecting temporal references and feature announcement language with document type-aware processing allowing Amazon format exceptions. Path portability validation uses environment variable detection and absolute path pattern matching with automatic replacement algorithms ensuring cross-platform compatibility. Security protection implements automatic `.gitignore` pattern addition with comprehensive PII protection protocols preventing repository commits. Enforcement mechanisms use immediate violation detection with framework operation suspension until compliance requirements are satisfied through corrective actions and verification procedures.

########### Code Usage Examples

This example demonstrates the mandatory `.gitignore` protection patterns that must be automatically added for user identity file security:

```gitignore
# JESSE AI Framework - User Identity Protection
# 🚨 CRITICAL: This file contains PII and must NEVER be committed 🚨
JESSE_USER_IDENTITY.md
**/JESSE_USER_IDENTITY.md
.clinerules/JESSE_USER_IDENTITY.md
${HOME}/Cline/Rules/JESSE_USER_IDENTITY.md
```

This example shows the correct portable path format requirements using environment variables for cross-platform compatibility:

```bash
# Correct portable path formats using environment variables
${HOME}/Cline/Rules/JESSE_USER_IDENTITY.md
$HOME/.config/application/settings.json
~/workspace/repositories/project-name/
```

This example illustrates the language standardization requirements for presenting established functionality without temporal references:

```markdown
# Correct established functionality presentation (non-Amazon documents)
The system includes Git branch management
WIP tasks feature comprehensive merge assistance
Workflows provide automated knowledge capture
Users can switch between task branches
```

This example demonstrates the interactive user information collection format for the 9 mandatory fields:

```markdown
# Interactive collection format for mandatory user identity fields
1. User Firstname: [Interactive prompt for first name]
2. User Lastname: [Interactive prompt for last name]
3. User Corporate Login: [Interactive prompt for company username]
4. User Job Description: [Interactive prompt for role/position]
5. User Country: [Interactive prompt for country]
6. User Town: [Interactive prompt for city/town]
7. User Timezone: [Interactive prompt for timezone]
8. User Company Name: [Interactive prompt for company name]
9. User Company Corporate URL: [Interactive prompt for company website]
```