# Git Clone Knowledge Bases Index

This directory contains knowledge bases extracted from external git repositories that provide context and patterns relevant to the JESSE Framework development.

## Storage Policy
**CRITICAL**: All git clones are stored **EXCLUSIVELY** in this directory (`<project_root>/.knowledge/git-clones/`).

- **Single Location Rule**: Git clones must **NEVER** exist anywhere else in the project structure
- **No Exceptions**: This policy has no exceptions - all external repositories are cloned only to `.knowledge/git-clones/`
- **Centralized Management**: This ensures consistent knowledge management and prevents scattered repository copies
- **Version Control Separation**: Keeps external repository content separate from project codebase through .gitignore rules

## Directory Structure
```
.knowledge/git-clones/
├── README.md                        # This index file
├── [repo-name]/                     # Actual git clone (ignored by .gitignore)
├── [repo-name]_kb.md               # Knowledge base extracted from repo (tracked)
└── [another-repo]_kb.md            # Additional knowledge bases (tracked)
```

## Available Knowledge Bases
*No git clone knowledge bases have been imported yet*

## How to Add Git Clone Knowledge Bases
Use the Git Clone Import workflow to add external repositories:

```bash
/jesse_wip_kb_git_clone_import.md
```

This workflow will:
1. Prompt for repository URL and focus areas
2. Clone repository to `.knowledge/git-clones/[repo-name]/`
3. Create knowledge base file `[repo-name]_kb.md`
4. Index important files and patterns
5. Update main knowledge base with reference

## .gitignore Protection
When any git clone is added to the knowledge base, the project `.gitignore` file contains these protective rules:

```
# Knowledge Management System - Git Clones
# Ignore actual git clone directories but keep knowledge base files
.knowledge/git-clones/*/
!.knowledge/git-clones/*.md
!.knowledge/git-clones/README.md
```

This ensures that:
- Actual git clone directories are ignored and not committed to the project repository
- Knowledge base files (`[repo-name]_kb.md`) are preserved and version controlled
- This index file (`README.md`) is maintained in version control
- External repository content remains separate from project codebase
