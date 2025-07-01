# Git Clone Knowledge Base: Strands Agent Builder
*Last Updated: 2025-06-30T17:14:41Z*

## Repository Overview
**Purpose**: Interactive command-line tool for building, testing, and extending custom AI agents and tools
**Language**: Python 3.10+
**License**: Apache License 2.0
**Status**: Public Preview - APIs may change
**Clone URL**: https://github.com/strands-agents/agent-builder
**Stars**: 174 (popular developer tool)
**Size**: 87.17 KiB (lightweight CLI tool)
**Key Insight**: Production-ready developer experience tool with rich CLI interface and optimized model configurations

## Repository Structure

### CLI Application (`src/strands_agents_builder/`)
**Purpose**: Main CLI application for interactive agent development
**Core Components**:
- `strands.py`: Main CLI interface and command processing
- `tools.py`: Integrated tool management and loading
- `handlers/callback_handler.py`: Event handling and streaming responses
- `models/`: Model provider implementations (Bedrock, Ollama)
- `utils/`: Utility modules for KB, welcome text, and model management

### Model Providers (`src/strands_agents_builder/models/`)
**Purpose**: Pluggable model provider system
**Available Providers**:
- `bedrock.py`: AWS Bedrock integration with optimized defaults
- `ollama.py`: Local Ollama model support
- Custom provider support via `.models/` directory

### Utilities (`src/strands_agents_builder/utils/`)
**Purpose**: Supporting functionality for the CLI tool
**Key Utilities**:
- `kb_utils.py`: Knowledge base interactions
- `model_utils.py`: Model configuration and management
- `welcome_utils.py`: User onboarding and help text

### Configuration Files
**`.prompt`**: Default system prompt (11,264 bytes - comprehensive)
**`pyproject.toml`**: Package configuration with CLI entry points
**`tools/`**: Additional tooling and scripts

## Key Features & Capabilities

### Interactive Development Environment
**Command-line Interface**: Rich terminal interface with streaming responses
**Hot-reloading**: Instant testing of custom tools and agents
**Nested Agents**: Create specialized agents with focused capabilities
**Dynamic Tool Loading**: Extend functionality at runtime

### Comprehensive Tool Integration
**24+ Built-in Tools**: Complete toolkit for agent development
**Tool Categories**:
- **Development**: `editor`, `python_repl`, `shell`, `load_tool`
- **AI & Reasoning**: `use_llm`, `think`, `swarm`, `strand`
- **AWS Integration**: `use_aws`, `generate_image`, `nova_reels`, `retrieve`
- **Communication**: `http_request`, `slack`, `speak`
- **Data Management**: `memory`, `store_in_kb`, `journal`
- **Utilities**: `calculator`, `current_time`, `environment`, `cron`

### Knowledge Base Integration
**Persistent Storage**: Amazon Bedrock Knowledge Bases for tools and configurations
**Iterative Development**: Load and enhance previous creations
**Session Continuity**: Maintain development history across sessions
**Tool Sharing**: Store and retrieve custom tool implementations

### Advanced Model Configuration
**Optimized Defaults**: Maxed-out settings for Claude Sonnet 4
**Key Configurations**:
- Model: `us.anthropic.claude-sonnet-4-20250514-v1:0`
- Max Tokens: 32,768 (maximum output)
- Timeouts: 15 minutes for complex operations
- Retries: Adaptive backoff with 3 max attempts
- Thinking Budget: 2,048 tokens for reasoning
- Interleaved Thinking: Real-time reasoning capability

## Usage Patterns

### Quick Start Pattern
```bash
# Install globally
pipx install strands-agents-builder

# Interactive development
strands

# One-shot tool creation
strands "Create a sentiment analyzer tool and test it"
```

### Knowledge Base Integration Pattern
```bash
# With specific KB
strands --kb YOUR_KB_ID "Load my calculator tool and add scientific functions"

# With environment default
export STRANDS_KNOWLEDGE_BASE_ID="YOUR_KB_ID"
strands "Find my recent agent and optimize it"
```

### Custom Model Provider Pattern
```bash
# Built-in providers
strands --model-provider ollama --model-config '{"model_id": "llama2"}'

# Custom provider
# Create .models/custom_model.py with instance() function
strands --model-provider custom_model --model-config config.json
```

### Pipeline Integration Pattern
```bash
# Pipe specifications
cat agent-spec.txt | strands "Build agent from these specifications"

# Environment customization
export STRANDS_SYSTEM_PROMPT="You are a Python expert."
strands
```

## Configuration Management

### Environment Variables
**Core Configuration**:
- `STRANDS_MODEL_ID`: Claude model selection
- `STRANDS_MAX_TOKENS`: Output token limit (default: 32,768)
- `STRANDS_BUDGET_TOKENS`: Thinking token budget (default: 2,048)
- `STRANDS_SYSTEM_PROMPT`: Custom system prompt override

**Feature Toggles**:
- `STRANDS_TOOL_CONSOLE_MODE`: Rich UI mode (default: enabled)
- `BYPASS_TOOL_CONSENT`: Skip confirmation prompts
- `STRANDS_KNOWLEDGE_BASE_ID`: Default KB for persistence

**Advanced Settings**:
- `STRANDS_THINKING_TYPE`: Reasoning capability control
- `STRANDS_ANTHROPIC_BETA`: Beta feature access
- `STRANDS_CACHE_TOOLS`: Tool caching strategy
- `STRANDS_CACHE_PROMPT`: Prompt caching strategy

### System Prompt Customization
**File-based**: `.prompt` file in working directory
**Environment**: `STRANDS_SYSTEM_PROMPT` variable override
**Default**: Comprehensive 11KB prompt for agent development

## Developer Experience Features

### Rich CLI Interface
- Streaming responses with real-time feedback
- Color-coded output and syntax highlighting
- Progress indicators for long-running operations
- Interactive help and command completion

### Development Workflow
- **Create**: Build new tools and agents interactively
- **Test**: Immediate testing with hot-reloading
- **Extend**: Enhance existing tools with new capabilities
- **Persist**: Save work to knowledge base for future use

### Error Handling & Resilience
- Comprehensive error handling with helpful messages
- Automatic retries with adaptive backoff
- Graceful degradation for missing dependencies
- User-friendly troubleshooting guidance

## Advanced Capabilities

### Multi-Agent Orchestration
**Swarm Intelligence**: Coordinate multiple AI agents
**Nested Agents**: Create specialized sub-agents
**Workflow Orchestration**: Sequence complex operations
**Agent Graphs**: Visualize agent relationships

### Knowledge Management
**Semantic Storage**: Bedrock Knowledge Bases integration
**Retrieval Augmented Generation**: Context-aware responses
**Memory Persistence**: Agent memory across sessions
**Tool Library**: Reusable tool implementations

### AWS Integration
**Native AWS Support**: Direct service integration
**Bedrock Optimization**: Optimized for AWS Bedrock models
**Knowledge Bases**: First-class KB support
**Service Orchestration**: Multi-service workflows

## Architecture Insights

### Modular Design
- **Plugin Architecture**: Extensible model providers
- **Tool System**: Pluggable tool ecosystem
- **Handler Pattern**: Event-driven response processing
- **Configuration Layer**: Flexible environment-based config

### Performance Optimization
- **Streaming**: Real-time response streaming
- **Caching**: Tool and prompt caching strategies
- **Timeout Management**: Configurable timeout handling
- **Resource Management**: Efficient memory usage

### User Experience Focus
- **Interactive Design**: Conversational interface
- **Rich Output**: Formatted and colored terminal output
- **Context Awareness**: Maintains session context
- **Help Integration**: Built-in help and documentation

## Development Workflow Integration

### IDE Integration
- Terminal-based development workflow
- Pipe-friendly for script integration
- Environment variable configuration
- File-based prompt management

### CI/CD Compatibility
- Command-line interface for automation
- Configuration via environment variables
- Scriptable tool creation and testing
- Knowledge base integration for persistence

### Team Collaboration
- Shared knowledge base for team tools
- Standardized agent development patterns
- Reusable tool library creation
- Consistent development environment

## Reference Links
- **Repository**: https://github.com/strands-agents/agent-builder
- **PyPI Package**: https://pypi.org/project/strands-agents-builder/
- **Documentation**: https://strandsagents.com/
- **SDK Integration**: https://github.com/strands-agents/sdk-python
- **Tools Package**: https://github.com/strands-agents/tools

## JESSE Framework Integration Value
- **Developer Experience**: Comprehensive CLI tool design patterns
- **Interactive Development**: Real-time feedback and streaming response handling
- **Configuration Management**: Environment variable based configuration systems
- **Tool Ecosystem**: Extensible plugin architecture for tools and capabilities
- **Knowledge Persistence**: Integration patterns with knowledge bases
- **Model Provider Abstraction**: Pluggable model provider system design
- **Rich CLI Interface**: Terminal UI design with streaming and rich output
- **Error Handling**: Production-ready error handling and resilience patterns
- **Workflow Integration**: Pipeline and automation friendly design
- **Multi-Agent Patterns**: Advanced agent coordination and orchestration
- **Optimization Strategies**: Performance tuning for LLM interactions
- **User Onboarding**: Welcome system and progressive disclosure patterns
