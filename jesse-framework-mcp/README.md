# JESSE Framework MCP Server

A Model Context Protocol (MCP) server that provides complete JESSE AI Framework initialization, replacing the manual 6-step session setup with a single MCP tool call.

## Overview

The JESSE Framework MCP Server embeds all JESSE framework rules and workflows at build time, providing:

- **Complete Session Initialization**: Single `jesse_start_session` call replaces manual file loading
- **Embedded Framework**: All JESSE rules and workflows packaged within the server
- **Project Knowledge Integration**: Automatic loading from `.knowledge/` directory
- **Lazy Loading**: Optional knowledge base loading based on task relevance
- **Session Logging**: Usage tracking for analytics and debugging

## Features

### 🚀 Core Tools

- **`jesse_start_session`**: Complete JESSE framework initialization
  - Loads embedded JESSE rules and workflows
  - Scans project `.knowledge/` directory
  - Provides knowledge base inventory for lazy loading
  - Optionally includes WIP task context

- **`jesse_load_knowledge_base`**: Lazy loading of specific knowledge bases
  - LLM-driven selection of relevant knowledge
  - Loads from `.knowledge/git-clones/` and `.knowledge/pdf-knowledge/`
  - Efficient context window management

### 📦 Self-Contained Distribution

- **Build-Time Embedding**: JESSE content copied from `artifacts/` during packaging
- **No Installation Dependencies**: Works without JESSE framework installation
- **Version Control**: JESSE rules version-locked with MCP server
- **Portable**: Runs in any project directory

## Installation

### Prerequisites

- Python 3.8 or higher
- UV package manager (recommended) or pip

### Install from PyPI

```bash
# Using UV (recommended)
uv add jesse-framework-mcp

# Using pip
pip install jesse-framework-mcp
```

### Install from Source

```bash
# Clone the repository (must be within JESSE framework project)
git clone <repository-url>
cd jesse-framework-mcp

# Build and install with UV
uv build
uv pip install dist/jesse_framework_mcp-*.whl

# Or with pip
pip install -e .
```

## Usage

### Cline Integration

Add to your Cline MCP configuration:

```json
{
  "mcpServers": {
    "jesse-framework": {
      "command": "uv",
      "args": ["run", "jesse-framework-mcp"],
      "transport": "stdio"
    }
  }
}
```

Or with pip installation:

```json
{
  "mcpServers": {
    "jesse-framework": {
      "command": "jesse-framework-mcp",
      "transport": "stdio"
    }
  }
}
```

### Direct Usage

```bash
# Run MCP server directly (for testing)
jesse-framework-mcp
```

### Tool Usage in Cline

```javascript
// Complete JESSE framework initialization
const context = await mcpClient.callTool("jesse_start_session", {
    user_prompt: "Help me implement authentication",
    load_wip_tasks: true
});

// Lazy load specific knowledge bases
const kbContent = await mcpClient.callTool("jesse_load_knowledge_base", {
    kb_names: ["fastapi_kb", "aws_cdk_kb"]
});
```

## Architecture

### Build-Time Content Embedding

```
Build Process:
artifacts/.clinerules/        →  embedded_content/
├── JESSE_*.md               →  ├── JESSE_*.md
└── workflows/               →  └── workflows/
    └── *.md                     └── *.md

Runtime Loading:
embedded_content/  +  .knowledge/  →  Complete Context
```

### Session Initialization Flow

```
jesse_start_session()
├── Log user prompt (analytics only)
├── Load embedded JESSE rules
├── Load embedded workflows  
├── Load project knowledge (.knowledge/)
├── Generate KB inventory
├── Load WIP task context (optional)
└── Return complete formatted context
```

### Knowledge Base Structure

```
.knowledge/
├── persistent-knowledge/
│   └── KNOWLEDGE_BASE.md
├── git-clones/
│   ├── repo1_kb.md
│   └── repo2_kb.md
├── pdf-knowledge/
│   ├── doc1_kb.md
│   └── doc2_kb.md
└── work-in-progress/
    └── current_task/
        ├── WIP_TASK.md
        └── PROGRESS.md
```

## Development

### Building from Source

**Note**: Must be built within the JESSE framework project hierarchy to access `artifacts/` directory.

```bash
# Ensure you're in the JESSE framework project
cd /path/to/jesse-ai-best-practices

# Navigate to MCP server directory
cd jesse-framework-mcp

# Build (copies content from ../artifacts/)
uv build

# Install locally for testing
uv pip install dist/jesse_framework_mcp-*.whl
```

### Testing the Build Script

```bash
# Test content copying without building
cd jesse-framework-mcp
python build_scripts/copy_jesse_content.py
```

### Development Dependencies

```bash
# Install development dependencies
uv sync --dev

# Run tests
uv run pytest

# Format code
uv run black .
uv run isort .

# Type checking
uv run mypy .
```

## Configuration

### Session Logging

The server logs all sessions to `.coding_assistant/jesse/session.log`:

```json
{
  "session_id": "a1b2c3d4",
  "timestamp": "2025-06-27T01:30:00.000Z",
  "user_prompt": "Help me debug the API",
  "load_wip_tasks": true,
  "event": "session_start"
}
```

### Knowledge Base Discovery

The server automatically discovers knowledge bases in:

- `.knowledge/git-clones/*_kb.md`
- `.knowledge/pdf-knowledge/*_kb.md`

Inventory includes size estimates for context window management.

## Troubleshooting

### Build Issues

**Error**: `Could not locate JESSE project with artifacts/ directory`
- **Solution**: Ensure build is run from within JESSE framework project hierarchy

**Error**: `Required JESSE rule file not found`
- **Solution**: Verify all JESSE_*.md files exist in `artifacts/.clinerules/`

### Runtime Issues

**Error**: `Failed to load embedded JESSE rules`
- **Solution**: Rebuild package to ensure content was properly embedded

**Error**: `Knowledge base 'xyz_kb' not found`
- **Solution**: Verify KB file exists in `.knowledge/git-clones/` or `.knowledge/pdf-knowledge/`

### Logging Issues

**Warning**: `Failed to log session`
- **Impact**: Non-blocking, session continues normally
- **Solution**: Check write permissions for `.coding_assistant/jesse/` directory

## License

MIT License - see LICENSE file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes following JESSE coding standards
4. Add tests for new functionality
5. Submit a pull request

## Support

- **Issues**: Report bugs via GitHub issues
- **Documentation**: See JESSE framework documentation
- **Community**: Join JESSE framework discussions
