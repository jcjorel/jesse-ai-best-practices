# WIP Task Add Git Clone Workflow

## Workflow Purpose
Add external git repository to the knowledge base for reference, creating structured documentation and integration with the knowledge management system.

## Execution Steps

### 1. Gather Repository Information
Prompt user for the following information:
- **Repository URL**: Full git clone URL (https or ssh)
- **Repository Purpose**: Why this repository is valuable for the project
- **Key Areas of Interest**: Specific directories, files, or concepts to focus on
- **Integration Context**: How this repository relates to current work

### 2. Generate Repository Name
Create standardized repository name for directory structure:
- Extract repository name from URL
- Convert to lowercase with underscores for special characters
- Ensure name doesn't conflict with existing clones
- Example: `https://github.com/user/my-repo` → `my_repo`

### 3. Clone Repository
Execute git clone operation:
- Clone repository to `.knowledge/git-clones/[repo-name]/`
- Verify clone was successful
- Check repository size and structure
- Identify large files that may need special processing

### 4. Generate Repository Overview
Use Perplexity MCP server to research repository:
- Query: "What is [repository-name] and what does it do?"
- Query: "What are the key features and architecture of [repository-name]?"
- Gather information about:
  - Repository purpose and functionality
  - Primary programming language
  - Key architectural patterns
  - Important directories and files
  - License and activity level

### 5. Analyze Repository Structure
Scan cloned repository to identify:
- **Directory Structure**: Map out key directories and their purposes
- **Key Files**: Identify important configuration, documentation, and source files
- **Large Files**: Files exceeding 4000 lines that need special processing
- **Documentation**: README files, docs directories, and other documentation
- **Patterns**: Notable code patterns or architectural approaches

### 6. Create Knowledge Base File
Generate `[repo-name]_kb.md` with structured information:

```markdown
# Git Clone Knowledge Base: [Repository Name]
*Last Updated: [ISO timestamp]*

## Repository Overview
**Purpose**: [Repository purpose from Perplexity research]
**Language**: [Primary programming language]
**License**: [License type]
**Last Activity**: [Recent activity summary]
**Clone URL**: [Original repository URL]

## Directory Structure
### [Directory Name]
**Purpose**: [What this directory contains]
**Key Files**:
- `[filename]`: [File purpose and significance]
- `[filename]`: [File purpose and significance]
**Patterns**: [Important patterns or conventions found]

### [Another Directory]
**Purpose**: [What this directory contains]
**Key Files**:
- `[filename]`: [File purpose and significance]
**Patterns**: [Important patterns or conventions found]

## Usage Knowledge
### Key Insights
- [Important insight about using this repository]
- [Another insight gained from analyzing the structure]

### Integration Points
- [How this repository integrates with other systems]
- [Important APIs or interfaces it provides]

## Large Files Requiring Processing
### [Large File Name] ([line count] lines)
**Purpose**: [What this file does]
**Priority**: [Processing priority level]
**Access Pattern**: [How to read this file in chunks]

## Reference Links
- **Repository**: [Clone URL]
- **Documentation**: [Links to key documentation files]
- **Examples**: [Links to example files or directories]
```

### 7. Update Git Clones Index
Update `.knowledge/git-clones/README.md`:
- Add new repository to "Available Repositories" section
- Include repository name, purpose, and key information
- Update last modified timestamp

### 8. Update Essential Knowledge Base
Update `.clinerules/JESSE_KNOWLEDGE_MANAGEMENT.md` Essential Knowledge Base:
- Add repository to "Available Git Clones" section
- Include repository purpose and key files
- Update timestamp

### 9. Process Large Files (if any)
For files exceeding 4000 lines:
- Mark in `KNOWLEDGE_BASE.md` as requiring processing
- Set priority based on relevance to current work
- Add to "Large Files Requiring Processing" section
- Recommend using `/jesse_wip_task_process_large_file.md` for detailed processing

## Repository Analysis Guidelines

### Directory Mapping
For each significant directory, document:
- **Purpose**: What the directory contains and its role
- **Key Files**: Most important files with brief descriptions
- **Patterns**: Notable code patterns, naming conventions, or architectural approaches
- **Dependencies**: How this directory relates to others

### File Significance Assessment
Prioritize documentation of:
- Configuration files (package.json, requirements.txt, etc.)
- Main entry points and core modules
- Documentation files (README, docs, examples)
- Test files and test patterns
- Build and deployment scripts

### Knowledge Extraction
Focus on extracting:
- **Architectural Patterns**: How the repository is structured and organized
- **Integration Patterns**: How components interact with each other
- **Best Practices**: Notable approaches to common problems
- **API Patterns**: How external interfaces are designed and implemented

## Workflow Completion
- Verify repository is successfully cloned
- Confirm knowledge base file is created with comprehensive information
- Verify git clones index is updated
- Check Essential Knowledge Base reflects new repository
- Display summary of available repository resources

## Error Handling
- If git clone fails, verify URL and network connectivity
- If repository is too large, offer to clone specific branches or shallow clone
- If Perplexity research fails, create knowledge base with manual analysis
- If knowledge base creation fails, preserve clone and retry documentation
- Handle cases where repository requires authentication

## Security Considerations
- Only clone from trusted sources
- Verify repository authenticity before cloning
- Do not clone repositories with sensitive information
- Add cloned repositories to .gitignore to prevent accidental commits
- Warn user about potential security implications of external code

## Post-Addition Actions
After successful repository addition:
- Suggest exploring key files identified in knowledge base
- Recommend processing large files if any were identified
- Offer to capture specific knowledge from repository using capture workflow
- Provide quick access links to repository and knowledge base file
