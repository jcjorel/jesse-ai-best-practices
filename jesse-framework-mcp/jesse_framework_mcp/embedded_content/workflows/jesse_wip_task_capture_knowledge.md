# WIP Task Knowledge Capture Workflow

## Workflow Purpose
Capture and structure knowledge from various sources (Perplexity queries, web resources, discoveries, patterns) for current WIP task or persistent storage.

## Execution Steps

### 1. Identify Knowledge Type
Prompt user to specify the type of knowledge being captured:
- **Perplexity Query Result**: Information obtained from Perplexity MCP server
- **Web Resource**: Valuable web page, documentation, or article
- **Pattern/Solution**: Reusable approach or solution to a problem
- **API Knowledge**: External API usage, endpoints, or integration details
- **Discovery**: New insight or finding relevant to current work
- **Tool/Resource**: Useful development tool or reference material

### 2. Determine Storage Location
Based on knowledge type and current context:
- **WIP Task Specific**: Knowledge relevant only to current active task
- **Persistent Knowledge**: Knowledge valuable for future tasks and general project work
- **Both**: Knowledge that should be captured in both locations for immediate and future reference

### 3. Gather Structured Information

#### For Perplexity Query Results:
- **Query**: Exact query text used
- **Context**: Why this search was performed
- **Key Findings**: Most important discoveries from results
- **Application**: How this knowledge applies to current work
- **Follow-up Actions**: Any actions taken based on results

#### For Web Resources:
- **URL**: Resource web address
- **Title**: Page or resource title
- **Context**: Why this resource is valuable
- **Key Information**: Most important points from resource
- **Application**: How this applies to the project

#### For Patterns/Solutions:
- **Pattern Name**: Descriptive name for the pattern
- **Context**: When this pattern applies
- **Description**: What the pattern/solution is
- **Implementation**: How to implement it
- **Benefits**: Why this approach works

#### For API Knowledge:
- **API Name**: Name of the external service/API
- **Purpose**: What this API provides
- **Key Endpoints**: Important endpoints and their functions
- **Authentication**: How to authenticate with the API
- **Usage Notes**: Important implementation details

#### For Discoveries:
- **Discovery Title**: Brief descriptive title
- **Source**: Where this discovery came from
- **Context**: Why this discovery is relevant
- **Finding**: What is now known about this topic
- **Application**: How this knowledge applies to current work

#### For Tools/Resources:
- **Tool/Resource Name**: Name of the tool or resource
- **Purpose**: What this tool does or provides
- **Usage Context**: When and how to use it
- **Benefits**: Why this tool is valuable
- **Integration Notes**: How it fits into current workflow

### 4. Format Knowledge Using Intemporal Writing
Convert all captured information to intemporal format:
- Use present tense throughout
- State facts rather than historical discoveries
- Focus on what IS known rather than what WAS learned
- Maintain consistency with existing knowledge entries

### 5. Update Appropriate Files

#### For WIP Task Knowledge:
Update current task's `WIP_TASK.md` in appropriate section:
- **Key Discoveries**: Add new discoveries with structured format
- **Patterns Identified**: Add identified patterns
- **Challenges & Solutions**: Add solutions to challenges
- **Task Resources**: Add external links, reference materials, or tools

#### For Persistent Knowledge:
Update `.knowledge/persistent-knowledge/KNOWLEDGE_BASE.md`:
- **Perplexity Query Results**: Add structured query information
- **Web Resources**: Add web resource with context
- **Patterns and Solutions**: Add reusable patterns
- **External APIs**: Add API knowledge and usage information

### 6. Check Knowledge Consistency
Verify captured knowledge doesn't contradict existing information:
- Compare with existing entries in same category
- Check for terminology consistency
- Resolve any conflicts by updating both sources
- Maintain single source of truth principle

### 7. Update Timestamps
Update "Last Updated" timestamps in modified files:
- WIP_TASK.md if task-specific knowledge was added
- KNOWLEDGE_BASE.md if persistent knowledge was added
- Essential Knowledge Base if significant knowledge was captured

## Knowledge Quality Standards

### Intemporal Writing Guidelines
- **Present Tense**: "This API requires authentication" not "We found the API requires authentication"
- **Factual Statements**: "The pattern works by..." not "We discovered the pattern works by..."
- **Timeless Knowledge**: Focus on principles and facts that remain true over time
- **Consistent Terminology**: Use same terms as existing knowledge entries

### Completeness Criteria
Ensure captured knowledge includes:
- Sufficient context for future understanding
- Clear application guidance
- Specific implementation details where relevant
- Cross-references to related knowledge when applicable

## Workflow Completion
- Verify knowledge is properly formatted and stored
- Confirm timestamps are updated
- Check for consistency with existing knowledge
- Display confirmation of knowledge capture with storage location

## Error Handling
- If knowledge conflicts with existing entries, prompt user for resolution
- If file updates fail, preserve knowledge in temporary location
- If formatting is incomplete, prompt for missing information
- Provide rollback options if capture process fails

## Automatic Capture Triggers
This workflow is automatically triggered when user says:
- "remember this"
- "capture this knowledge"
- "save this information"
- "document this finding"
- Similar knowledge capture phrases
