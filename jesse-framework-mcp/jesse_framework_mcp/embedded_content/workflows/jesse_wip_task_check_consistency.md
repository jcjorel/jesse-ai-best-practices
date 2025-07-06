# WIP Task Knowledge Consistency Check Workflow

## Workflow Purpose
Verify knowledge consistency across all knowledge management files, identifying and resolving contradictions to maintain single source of truth principle.

## Execution Steps

### 1. Scan Essential Knowledge Base
Read `.clinerules/JESSE_KNOWLEDGE_MANAGEMENT.md` Essential Knowledge Base section:
- Extract all knowledge entries and facts
- Identify key terminology and definitions
- Note project context and component descriptions
- Record git clone information and purposes

### 2. Scan Persistent Knowledge Base
Read `.knowledge/persistent-knowledge/KNOWLEDGE_BASE.md`:
- Extract all patterns, solutions, and API knowledge
- Identify external resource information
- Note Perplexity query results and findings
- Record web resource descriptions and applications

### 3. Scan Active WIP Task Knowledge
If active WIP task exists, read WIP_TASK.md:
- Extract task learnings and discoveries
- Identify patterns and solutions documented
- Note challenges and their solutions
- Record tools, APIs, and resources mentioned

### 4. Scan Git Clone Knowledge Bases
For each git clone knowledge base file:
- Read repository descriptions and purposes
- Extract usage knowledge and insights
- Note integration points and patterns
- Record API information and architectural details

### 5. Identify Potential Conflicts
Compare knowledge across all sources for:
- **Terminology Inconsistencies**: Same concepts described with different terms
- **Contradictory Facts**: Conflicting statements about APIs, tools, or patterns
- **Duplicate Information**: Same knowledge stored in multiple locations with variations
- **Outdated References**: References to archived tasks or removed components
- **Missing Cross-References**: Related knowledge that should reference each other

### 6. Categorize Conflicts by Severity
Classify identified conflicts:
- **Critical**: Direct contradictions that could cause implementation errors
- **Major**: Terminology inconsistencies that could cause confusion
- **Minor**: Formatting inconsistencies or missing cross-references
- **Informational**: Duplicate information that should be consolidated

### 7. Present Conflicts to User
For each identified conflict, display:
- **Conflict Type**: Category and severity level
- **Conflicting Sources**: Which files contain contradictory information
- **Specific Content**: Exact text from each source showing the conflict
- **Impact Assessment**: How this conflict could affect development work
- **Resolution Options**: Suggested approaches to resolve the conflict

### 8. Gather Resolution Decisions
For each conflict, prompt user to choose resolution approach:
- **Update Source A**: Modify first source to match second source
- **Update Source B**: Modify second source to match first source
- **Create New Standard**: Establish new consistent terminology/fact across both sources
- **Consolidate Information**: Merge duplicate information into single authoritative source
- **Add Cross-Reference**: Link related information without changing content
- **Skip**: Leave conflict unresolved (with justification)

### 9. Implement Resolutions
For each approved resolution:
- Update specified files with consistent information
- Maintain intemporal writing style in all updates
- Preserve essential context and meaning
- Add cross-references where appropriate
- Update timestamps in modified files

### 10. Verify Resolution Success
After implementing changes:
- Re-scan updated files for consistency
- Verify no new conflicts were introduced
- Confirm all cross-references are valid
- Check that intemporal writing standards are maintained

### 11. Generate Consistency Report
Create comprehensive report including:
- **Total Conflicts Found**: Number and severity breakdown
- **Conflicts Resolved**: Number and types of resolutions applied
- **Files Modified**: List of files updated during consistency check
- **Remaining Issues**: Any unresolved conflicts with justification
- **Recommendations**: Suggestions for preventing future inconsistencies

## Consistency Check Categories

### Terminology Consistency
Check for consistent use of:
- **Project Component Names**: Backend services, APIs, tools
- **Technical Terms**: Architecture patterns, data formats, protocols
- **Process Names**: Workflows, procedures, methodologies
- **Tool Names**: Development tools, frameworks, libraries

### Factual Consistency
Verify consistency of:
- **API Information**: Endpoints, authentication methods, data formats
- **Configuration Details**: Default values, required parameters, options
- **Process Steps**: Workflow procedures, installation steps, usage patterns
- **Integration Points**: How components connect and interact

### Reference Consistency
Ensure valid:
- **File References**: Links to existing files and directories
- **Cross-References**: Links between related knowledge entries
- **External Links**: URLs and external resource references
- **Task References**: Links to active, archived, or completed tasks

## Automated Consistency Rules

### Intemporal Writing Verification
Ensure all knowledge entries follow intemporal standards:
- Present tense usage throughout
- Factual statements rather than historical references
- Consistent terminology across all sources
- Timeless knowledge focus

### Cross-Reference Validation
Verify all internal references:
- File paths point to existing files
- Task references point to valid tasks
- Git clone references match available repositories
- Documentation links are accessible

### Duplicate Detection
Identify and flag:
- Identical information in multiple locations
- Similar patterns or solutions with different descriptions
- Redundant API documentation across files
- Overlapping resource descriptions

## Workflow Completion
- Display comprehensive consistency report
- Confirm all approved resolutions are implemented
- Verify no new conflicts were introduced
- Update all file timestamps appropriately
- Provide recommendations for maintaining consistency

## Error Handling
- If files are missing or corrupted, note in report and continue with available files
- If resolution implementation fails, preserve original content and log error
- If cross-reference validation fails, mark references as potentially broken
- Provide rollback options if consistency check introduces new problems

## Preventive Recommendations
Based on consistency check results, suggest:
- **Terminology Standards**: Establish project glossary for consistent terms
- **Knowledge Templates**: Standardized formats for capturing similar knowledge
- **Regular Checks**: Schedule periodic consistency verification
- **Cross-Reference Maintenance**: Procedures for keeping references current
- **Knowledge Consolidation**: Strategies for reducing information duplication

## Post-Check Actions
After successful consistency check:
- Schedule next consistency verification
- Update knowledge capture workflows with identified standards
- Document any new terminology or factual standards established
- Provide training on maintaining consistency for future knowledge capture
