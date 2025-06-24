# Git Clones Index
*Last Updated: YYYY-MM-DDThh:mm:ssZ*

This directory contains external git repositories cloned for reference and their associated knowledge base files.

⚠️ **IMPORTANT**: The repository entries below are TEMPLATE EXAMPLES ONLY. They **MUST** be completely removed and replaced with actual repository information when adding the first real git clone to this project.

## Available Repositories

### example-framework-repo
- **Purpose**: Example framework or library repository for understanding implementation patterns
- **Knowledge Base**: `example-framework-repo_kb.md`
- **Focus Areas**: Core API patterns, integration examples, best practices documentation
- **Last Updated**: YYYY-MM-DDThh:mm:ssZ

### third-party-integration-samples
- **Purpose**: Official samples and examples for third-party service integration
- **Knowledge Base**: `third-party-integration-samples_kb.md`
- **Focus Areas**: Authentication patterns, API usage examples, error handling, production-ready implementations
- **Last Updated**: YYYY-MM-DDThh:mm:ssZ

### documentation-source-repo
- **Purpose**: Complete documentation source or user guide repository for comprehensive reference
- **Knowledge Base**: `documentation-source-repo_kb.md`
- **Focus Areas**: Architecture patterns, API reference, configuration examples, troubleshooting guides
- **Source**: [Description of source type - git repo, PDF conversion, etc.]
- **Last Updated**: YYYY-MM-DDThh:mm:ssZ

## Template Guidelines
When adding new repositories, follow this format:
- **Repository name**: Use the actual git repository name (lowercase with hyphens)
- **Purpose**: One-line clear description of why this repository was cloned
- **Knowledge Base**: Always `[repo-name]_kb.md`
- **Focus Areas**: 3-5 specific areas of interest from the repository
- **Source**: Include if from PDF, documentation, or special source
- **Last Updated**: Use precise timestamp format YYYY-MM-DDThh:mm:ssZ

## Usage Guidelines
- Each cloned repository has a corresponding `[repo-name]_kb.md` knowledge base file
- Knowledge base files contain structured information about the repository
- Large files (>4000 lines) are indexed in knowledge base files rather than read directly
- Use `/jesse_wip_kb_git_clone_import.md` workflow to add new repositories

## Directory Structure
```
git-clones/
├── README.md                    # This index file
├── [repo-name-1]/              # Actual git clone (gitignored)
├── [repo-name-1]_kb.md         # Knowledge base for repo-name-1
├── [repo-name-2]/              # Actual git clone (gitignored)
└── [repo-name-2]_kb.md         # Knowledge base for repo-name-2
```

## Notes for Implementation
- Replace template entries above with actual repository information
- Maintain the same structure and formatting for consistency
- Always include the timestamp in the exact format shown
- Focus areas should be specific and actionable, not generic
- Knowledge base filenames must exactly match the repository name with `_kb.md` suffix
