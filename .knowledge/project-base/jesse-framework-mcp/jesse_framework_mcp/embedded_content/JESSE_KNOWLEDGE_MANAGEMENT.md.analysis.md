<!-- CACHE_METADATA_START -->
<!-- Source File: {PROJECT_ROOT}/jesse-framework-mcp/jesse_framework_mcp/embedded_content/JESSE_KNOWLEDGE_MANAGEMENT.md -->
<!-- Cached On: 2025-07-06T12:19:55.154901 -->
<!-- Source Modified: 2025-06-26T13:02:23.573514 -->
<!-- Cache Version: 1.0 -->
<!-- CACHE_METADATA_END -->

#### Functional Intent & Features

This file serves as the central knowledge management system configuration for the Jesse Framework MCP project, establishing mandatory session initialization protocols, comprehensive knowledge capture mechanisms, and integrated workflow orchestration across all development activities. The system provides automated knowledge base loading, WIP task management, and Git repository integration through structured file organization and workflow automation. Key semantic entities include `Cline` session management via `https://github.com/cline/cline`, mandatory 6-step initialization sequence with verification checkpoints, `.knowledge/persistent-knowledge/KNOWLEDGE_BASE.md` persistent storage, `.knowledge/work-in-progress/` task directory structure, `.knowledge/git-clones/` repository storage with exclusive location policy, `${USER_HOME_DIR}/Cline/Rules/` preferred installation location, `/jesse_wip_task_*.md` workflow command syntax, `intemporal writing` format requirements for present-tense knowledge capture, automatic external knowledge capture from `Perplexity MCP server` and web browsing, Git branch integration with comprehensive merge strategies, `.gitignore` requirements for git clone management, and Essential Knowledge Base section containing current task status, project context, and quick access links enabling comprehensive development workflow coordination and knowledge preservation.

##### Main Components

The document contains four primary sections establishing comprehensive knowledge management governance: System Directives defining mandatory session initialization protocols with 6-step execution sequence and enforcement mechanisms, Installation Location and Preferences specifying preferred global installation at `${USER_HOME_DIR}/Cline/Rules/` versus project-level deployment options, Operational Modes Integration covering ACT/PLAN/DESIGN mode enhancements with knowledge capture coordination, and Workflow Commands providing `/[workflow-name].md` syntax for invoking specialized knowledge management operations. Supporting components include Session Initialization Enforcement Protocol with immediate compliance checking, Knowledge Capture Rules for automatic external knowledge integration, Git Branch Integration Policy with comprehensive branch management features, Git Clone Storage Policy enforcing exclusive `.knowledge/git-clones/` location usage, and Essential Knowledge Base section containing current WIP task status, project context, and navigation links for active development coordination.

###### Architecture & Design

The architecture implements a mandatory initialization-driven knowledge management pattern with comprehensive session boundary detection and automatic knowledge loading protocols. The design employs hierarchical file organization with specialized directories for different knowledge types, global versus project-level installation flexibility, and workflow-based operation orchestration through markdown command syntax. The system uses automatic knowledge capture mechanisms for external research integration, comprehensive Git branch tracking with merge assistance capabilities, and single-source-of-truth principles preventing knowledge duplication. The architectural pattern includes enforcement mechanisms with self-verification protocols, error reporting systems, and compliance checking ensuring mandatory initialization completion before user request processing while maintaining separation between global framework rules and project-specific knowledge content.

####### Implementation Approach

The implementation uses mandatory 6-step session initialization with verification checkpoints and failure action protocols ensuring comprehensive knowledge loading before user request processing. The approach employs automatic knowledge capture triggered by external research activities, structured file organization with standardized naming conventions, and workflow integration through markdown command parsing. Knowledge management implements intemporal writing format conversion, consistency maintenance across multiple knowledge sources, and automatic test result capture with standardized logging formats. Git integration uses comprehensive branch tracking, merge strategy selection, and exclusive repository storage policies with `.gitignore` enforcement. Quality assurance employs self-enforcement mechanisms, session boundary detection, and compliance verification protocols ensuring mandatory initialization completion and knowledge consistency maintenance.

######## External Dependencies & Integration Points

**→ References:**
- `Cline` conversation system via `https://github.com/cline/cline` - session management and initialization trigger detection
- `.knowledge/persistent-knowledge/KNOWLEDGE_BASE.md` - persistent knowledge storage requiring mandatory loading
- `.knowledge/work-in-progress/[current_task]/` - WIP task files including `WIP_TASK.md` and `PROGRESS.md`
- `.knowledge/git-clones/[repo-name]_kb.md` - git clone knowledge bases for external repository integration
- `.knowledge/pdf-knowledge/[PDF-name]_kb.md` - PDF knowledge bases for document integration
- `${USER_HOME_DIR}/Cline/Rules/` - preferred global installation location for framework files
- `Perplexity MCP server` - external research service for automatic knowledge capture
- Git repository system - branch management and merge assistance integration

**← Referenced By:**
- All Jesse Framework workflows - consume knowledge management protocols for session initialization and knowledge capture
- Development session processes - require mandatory initialization sequence completion before operation
- WIP task management workflows - reference current task status and knowledge base integration
- Git workflow operations - use branch integration policies and merge assistance capabilities
- Knowledge capture workflows - apply automatic external knowledge integration and intemporal writing standards
- Installation and deployment processes - follow location preferences and file separation protocols

**⚡ System role and ecosystem integration:**
- **System Role**: Central orchestration hub for the Jesse Framework MCP ecosystem, providing mandatory session initialization, comprehensive knowledge management, and workflow coordination across all development activities
- **Ecosystem Position**: Core infrastructure component that establishes the foundation for all Jesse Framework operations, ensuring consistent knowledge loading, task management, and development workflow coordination
- **Integration Pattern**: Enforced by all Jesse Framework components through mandatory initialization requirements, integrated with Cline session management for automatic activation, coordinated with external research services for knowledge capture, and designed for both global and project-level deployment flexibility while maintaining consistent operational behavior

######### Edge Cases & Error Handling

The system addresses initialization failures through immediate error reporting and mandatory step completion verification before proceeding with user requests. Missing knowledge base files trigger automatic creation with basic structure while preserving system functionality. Git repository detection failures provide graceful fallback with non-Git workflow operation while maintaining full knowledge management capabilities. Session boundary detection handles context reset scenarios and fresh IDE restarts through comprehensive initialization trigger recognition. Knowledge capture failures preserve existing content while noting integration limitations and providing alternative capture mechanisms. Installation location conflicts receive explicit user choice presentation with clear option differentiation and verification protocols ensuring proper file separation and functionality maintenance.

########## Internal Implementation Details

The mandatory initialization sequence uses 6-step verification protocol with checkpoint validation and failure action specification for each step. Knowledge capture implements automatic trigger detection for external research activities with structured information appending to appropriate knowledge files. Git integration uses comprehensive branch tracking with status management, merge strategy selection algorithms, and exclusive storage policy enforcement through `.gitignore` rule management. File organization employs hierarchical directory structures with standardized naming conventions and location-specific behavior patterns. Session enforcement uses self-verification mechanisms with immediate compliance checking and mandatory sequence execution when initialization gaps are detected. Installation management implements user choice presentation with explicit option verification and file separation protocols ensuring consistent behavior across deployment scenarios.

########### Code Usage Examples

This example demonstrates the mandatory session initialization sequence that must be executed at the start of every Cline session:

```markdown
# Mandatory 6-step initialization sequence for every new session
1. Read JESSE_KNOWLEDGE_MANAGEMENT.md completely
2. Read .knowledge/persistent-knowledge/KNOWLEDGE_BASE.md
3. Load all referenced git clone and PDF knowledge bases
4. Load current WIP task files if active task exists
5. Display brief context summary with loaded resources
6. Confirm successful initialization before processing user requests
```

This example shows the automatic knowledge capture format for external research integration:

```markdown
# Automatic knowledge capture from Perplexity MCP server and web browsing
# If active WIP task exists: append to WIP_TASK.md
# If no active task: append to KNOWLEDGE_BASE.md
# No manual trigger required - happens automatically during research
```

This example illustrates the Git clone storage policy with exclusive location enforcement:

```gitignore
# Required .gitignore rules for git clone management
# Knowledge Management System - Git Clones
# Ignore actual git clone directories but keep knowledge base files
.knowledge/git-clones/*/
!.knowledge/git-clones/*.md
!.knowledge/git-clones/README.md
```

This example demonstrates the workflow command syntax for invoking knowledge management operations:

```bash
# Workflow invocation using markdown command syntax
/jesse_wip_task_create.md          # Create new WIP task
/jesse_wip_task_switch.md          # Switch between existing tasks
/jesse_wip_kb_git_clone_import.md  # Import external repository
/jesse_wip_task_complete.md        # Complete current task with knowledge extraction
```