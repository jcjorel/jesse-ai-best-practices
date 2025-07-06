<!-- CACHE_METADATA_START -->
<!-- Source File: {PROJECT_ROOT}/jesse-framework-mcp/jesse_framework_mcp/embedded_content/workflows/jesse_amazon_prfaq_coach.md -->
<!-- Cached On: 2025-07-06T12:06:46.672167 -->
<!-- Source Modified: 2025-06-26T15:49:42.702307 -->
<!-- Cache Version: 1.0 -->
<!-- CACHE_METADATA_END -->

#### Functional Intent & Features

This workflow documentation provides a comprehensive Amazon PR/FAQ coaching system implementing the authentic Amazon Working Backwards methodology, designed to guide users through creating professional PR/FAQ documents using real Amazon templates, examples, and coaching frameworks extracted from internal Amazon sources. The system delivers mandatory knowledge base loading with selective exclusions, context window management protocols preventing session interruption, and complete 5-stage Working Backwards methodology implementation (`LISTEN`, `DEFINE`, `INVENT`, `REFINE`, `TEST & ITERATE`). Key semantic entities include `Context Window Management Protocol` with 80% capacity monitoring, `working_backwards/current/` directory structure for session state preservation, `JESSE_KNOWLEDGE_MANAGEMENT.md` mandatory loading, `MCP Perplexity` research integration, Amazon's `7-paragraph Press Release Structure`, comprehensive `FAQ Organization System` with 11 essential internal questions, `Customer Focus Scoring System` for quality assessment, `Believability Assessment Framework` for testimonial validation, Amazon's `Top 10 Writing Guidelines` implementation, and complete `Working Backwards Assessment` with customer research methods, problem definition templates, solution evaluation matrices, experience design frameworks, and comprehensive success metrics enabling authentic Amazon-style strategic document creation with professional coaching guidance.

##### Main Components

The workflow contains fourteen primary sections organized into coaching methodology, document creation, and quality assessment components. Core sections include initial setup with experience assessment routing, Working Backwards Assessment implementing the 5-stage methodology, PR/FAQ Document Creation using Amazon's complete framework, Advanced Writing Quality Assessment with Amazon's top 10 guidelines, Knowledge Base Integration for persistent storage, and specialized modes including Examples Library with 20+ real Amazon examples, Methodology Learning Mode for comprehensive education, and Iterative Coaching Mode for section-by-section guidance. The system incorporates mandatory protocols including Context Window Management with graceful halt procedures, Knowledge Base Loading with selective exclusions, and comprehensive quality validation frameworks ensuring authentic Amazon communication standards.

###### Architecture & Design

The architecture implements a session-aware coaching pattern with proactive context management and state preservation mechanisms preventing workflow interruption. The design employs a multi-modal coaching approach supporting different user experience levels through routing to specialized coaching paths based on initial assessment. The system uses mandatory knowledge loading protocols with intentional exclusions of WIP tasks and available knowledge bases to maintain clean coaching focus. The architectural pattern includes comprehensive state management through `working_backwards/current/` directory structure, enabling seamless session resumption and progress preservation. The design incorporates Amazon's authentic methodology frameworks with real examples and templates, ensuring professional-grade output quality through systematic validation and assessment protocols.

####### Implementation Approach

The implementation uses proactive context window monitoring with checkpoint validation at critical workflow stages, triggering graceful halt procedures at 80% capacity to preserve session state and enable seamless continuation. The approach employs systematic knowledge base loading following JESSE Framework protocols while intentionally excluding WIP task and available knowledge base context to maintain coaching focus. The system implements Amazon's complete 5-stage Working Backwards methodology with detailed coaching frameworks, customer research integration through MCP Perplexity calls, and comprehensive document creation using authentic Amazon templates. Quality assurance employs Amazon's top 10 writing guidelines with automated assessment tools including customer focus scoring, believability frameworks, and readability analysis ensuring professional document standards.

######## External Dependencies & Integration Points

**→ References:**
- `.clinerules/JESSE_KNOWLEDGE_MANAGEMENT.md` - mandatory system rules and essential knowledge loading for coaching context
- `.knowledge/persistent-knowledge/KNOWLEDGE_BASE.md` - accumulated project knowledge integration for coaching enhancement
- `working_backwards/current/` - dedicated directory structure for session state management and document preservation
- `MCP Perplexity` - external research integration for customer insights, market data, and competitive analysis
- `https://github.com/cline/cline` - Cline conversation system for session management and coaching delivery
- Amazon internal PR/FAQ examples - authentic templates and frameworks for professional document creation
- Amazon Working Backwards methodology - 5-stage customer-focused development process implementation

**← Referenced By:**
- Strategic planning workflows - processes requiring customer-focused vision document creation
- Product development teams - groups needing authentic Amazon-style PR/FAQ documents for stakeholder communication
- Project management systems - workflows incorporating Working Backwards methodology for customer-centric planning
- Knowledge management processes - systems capturing and preserving strategic planning insights and methodologies
- Stakeholder review processes - procedures requiring professional PR/FAQ documents for decision-making and approval

**⚡ System role and ecosystem integration:**
- **System Role**: Comprehensive strategic planning coach implementing authentic Amazon Working Backwards methodology for creating professional customer-focused vision documents within the Jesse Framework MCP ecosystem
- **Ecosystem Position**: Specialized coaching workflow that operates independently of development tasks while integrating with knowledge management and session state preservation systems
- **Integration Pattern**: Used by product teams and strategic planners through direct workflow invocation, integrated with MCP Perplexity for external research, coordinated with Jesse Framework knowledge management for context loading, and designed for seamless session continuation across multiple coaching interactions

######### Edge Cases & Error Handling

The workflow handles context window exhaustion through proactive monitoring and graceful halt procedures, preserving all session state and enabling seamless resumption in fresh sessions. Missing or corrupted working backwards directory structures trigger automatic initialization with proper file creation and state management setup. Knowledge base loading failures provide fallback mechanisms while maintaining coaching functionality with reduced context. MCP Perplexity research failures continue coaching workflow while noting research limitations and providing alternative guidance approaches. User experience level mismatches are handled through dynamic routing and coaching approach adjustment based on demonstrated capability and needs. The system addresses incomplete Working Backwards stage completion through validation checkpoints and guided remediation before proceeding to subsequent stages.

########## Internal Implementation Details

The workflow uses bash scripting for working backwards directory initialization and state management, creating structured file organization for session preservation and progress tracking. Context monitoring employs percentage-based capacity assessment with checkpoint validation at critical workflow stages, implementing immediate state saving and session termination protocols when approaching limits. Knowledge base loading implements selective exclusion logic intentionally avoiding WIP task and available knowledge base context while maintaining essential system knowledge and working backwards context. Quality assessment employs multi-dimensional scoring systems including customer focus rating scales, believability assessment frameworks, and readability analysis tools ensuring professional document standards. Session resumption mechanisms reconstruct coaching context from preserved state files, enabling seamless continuation of complex multi-stage coaching processes.

########### Code Usage Examples

This example demonstrates the mandatory knowledge base loading protocol with selective exclusions for clean coaching context:

```bash
# Execute mandatory knowledge base loading with coaching-specific exclusions
# Load system rules and essential knowledge
cat .clinerules/JESSE_KNOWLEDGE_MANAGEMENT.md
cat .knowledge/persistent-knowledge/KNOWLEDGE_BASE.md

# Load existing working backwards context if available
for file in working_backwards/current/*.md; do 
  if [ -f "$file" ]; then 
    echo "=== BEGIN FILE: $file ==="; 
    cat "$file"; 
    echo "=== END FILE: $file ==="; 
  fi; 
done

# Intentionally exclude WIP task and available KB context for clean coaching focus
```

This example shows the context window management protocol with graceful halt and state preservation:

```bash
# Context window monitoring and graceful halt procedure at 80% capacity
echo "## Coaching Session State - $(date -u +"%Y-%m-%dT%H:%M:%SZ")" >> working_backwards/current/coaching_session_state.md
echo "**Context Halt Triggered**: 80% capacity reached" >> working_backwards/current/coaching_session_state.md
echo "**Current Phase**: [Document current coaching phase]" >> working_backwards/current/coaching_session_state.md
echo "**Completed Stages**: [List completed stages]" >> working_backwards/current/coaching_session_state.md
echo "**Next Steps**: [Document specific next actions]" >> working_backwards/current/coaching_session_state.md
```

This example illustrates the Working Backwards Assessment implementation with Amazon's problem definition template:

```markdown
# Amazon's mandatory problem definition template for Stage 2 (DEFINE)
Today, [specific customer segment] have to [current limitation/friction/manual process] 
when [specific triggering situation]. 

This means [quantified impact/consequence for customer], making it difficult to 
[specific customer goal/desired outcome].

Customers need a way to [specific needed capability] so they can 
[desired business/personal result].

Supporting Evidence:
- Data Source 1: [Specific evidence with numbers - e.g., "73% of surveyed customers report..."]
- Data Source 2: [Quantified impact - e.g., "Average time spent is 45 minutes per task"]  
- Data Source 3: [Customer quotes - e.g., "As one customer told us, 'I waste 2 hours daily on...'"]
```