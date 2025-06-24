# Git Clones Index
*Last Updated: 2025-06-19T23:39:30Z*

This directory contains external git repositories cloned for reference and their associated knowledge base files.

## Available Repositories

### aws-sdk-python
- **Purpose**: AWS SDK for Python (Boto3) reference for Nova Sonic API integration
- **Knowledge Base**: `aws-sdk-python_kb.md`
- **Focus Areas**: Bedrock Runtime client, Nova Sonic model integration, experimental SDK features
- **Last Updated**: 2025-06-19T17:14:56Z

### amazon-nova-samples
- **Purpose**: Official AWS samples for Amazon Nova models including Nova Sonic speech-to-speech
- **Knowledge Base**: `amazon-nova-samples_kb.md`
- **Focus Areas**: Nova Sonic implementation patterns, bidirectional streaming, tool integration, production examples
- **Last Updated**: 2025-06-19T22:35:00Z

### aws-nova-userguide
- **Purpose**: Complete AWS Nova User Guide documentation including comprehensive Nova Sonic reference
- **Knowledge Base**: `aws_nova_userguide_kb.md`
- **Focus Areas**: Nova Sonic architecture, bidirectional streaming API, speech-to-speech examples, prompting best practices, tool integration
- **Source**: AWS Nova User Guide PDF (44.49MB, 24,333 lines extracted)
- **Last Updated**: 2025-06-19T23:39:30Z

## Usage Guidelines
- Each cloned repository has a corresponding `[repo-name]_kb.md` knowledge base file
- Knowledge base files contain structured information about the repository
- Large files (>4000 lines) are indexed in knowledge base files rather than read directly
- Use `/wip_task_add_git_clone.md` workflow to add new repositories

## Directory Structure
```
git-clones/
├── README.md                    # This index file
├── [repo-name-1]/              # Actual git clone (gitignored)
├── [repo-name-1]_kb.md         # Knowledge base for repo-name-1
├── [repo-name-2]/              # Actual git clone (gitignored)
└── [repo-name-2]_kb.md         # Knowledge base for repo-name-2
