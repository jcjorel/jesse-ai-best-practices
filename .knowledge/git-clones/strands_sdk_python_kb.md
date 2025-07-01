# Git Clone Knowledge Base: Strands Agents SDK Python
*Last Updated: 2025-06-30T17:05:00Z*

## Repository Overview
**Purpose**: Model-driven Python SDK for building AI agents with just a few lines of code, developed by AWS
**Language**: Python 3.10+
**License**: Apache License 2.0
**Status**: Public Preview (APIs may change)
**Clone URL**: https://github.com/strands-agents/sdk-python
**Stars**: 1,843 (highly popular)
**Key Insight**: Production-ready framework with comprehensive multi-model support and native MCP integration

## Directory Structure

### Core Framework (`src/strands/`)
**Purpose**: Main SDK implementation with modular architecture
**Key Components**:
- `agent/`: Core agent implementation and conversation management
- `event_loop/`: Agentic event loop with streaming support
- `handlers/`: Model provider handlers and integrations
- `models/`: Multi-provider model implementations
- `tools/`: Tool system including MCP support
- `types/`: Type definitions and data structures
- `multiagent/`: Multi-agent system support
- `telemetry/`: Observability and monitoring

### Agent System (`src/strands/agent/`)
**Purpose**: Core agent logic and conversation management
**Key Files**:
- `agent.py`: Main Agent class implementation
- `agent_result.py`: Agent response handling
- `conversation_manager/`: Memory management strategies
  - `summarizing_conversation_manager.py`: Summarization-based memory
  - `sliding_window_conversation_manager.py`: Window-based memory
  - `null_conversation_manager.py`: No memory persistence
**Patterns**: Pluggable conversation management with multiple memory strategies

### Event Loop (`src/strands/event_loop/`)
**Purpose**: Manages the agentic loop - plan, reason, act, reflect cycle
**Key Files**:
- `event_loop.py`: Core event loop implementation
- `message_processor.py`: Message processing and routing
- `streaming.py`: Real-time streaming support
**Patterns**: Iterative processing with error handling, retries, and observability

### Model Providers (`src/strands/models/` & `src/strands/handlers/`)
**Purpose**: Multi-provider model support with unified interface
**Supported Providers**:
- Amazon Bedrock (default)
- Anthropic
- LiteLLM (gateway to 100+ models)
- LlamaAPI
- Ollama (local models)
- OpenAI
- Custom providers
**Patterns**: Provider abstraction with consistent API across different models

### Tools System (`src/strands/tools/`)
**Purpose**: Tool integration including MCP protocol support
**Key Features**:
- Python decorator-based tools (@tool)
- Native MCP (Model Context Protocol) client
- Built-in tools via strands-agents-tools package
- Custom tool development support
**Integration**: Direct MCP server integration for thousands of pre-built tools

### Multi-Agent Support (`src/strands/multiagent/`)
**Purpose**: Agent-to-agent communication and coordination
**Key Components**:
- `a2a/`: Agent-to-agent communication protocols
**Patterns**: Distributed agent systems with inter-agent messaging

## Usage Knowledge

### Core Agent Creation Pattern
```python
from strands import Agent
from strands_tools import calculator

# Simple agent with tools
agent = Agent(tools=[calculator])
response = agent("What is the square root of 1764")
```

### Custom Tool Development
```python
from strands import Agent, tool

@tool
def word_count(text: str) -> int:
    """Count words in text. Docstring is used by LLM."""
    return len(text.split())

agent = Agent(tools=[word_count])
```

### MCP Integration Pattern
```python
from strands.tools.mcp import MCPClient
from mcp import stdio_client, StdioServerParameters

# Connect to MCP server
aws_docs_client = MCPClient(
    lambda: stdio_client(StdioServerParameters(
        command="uvx", 
        args=["awslabs.aws-documentation-mcp-server@latest"]
    ))
)

with aws_docs_client:
    agent = Agent(tools=aws_docs_client.list_tools_sync())
```

### Multi-Model Support
```python
from strands.models import BedrockModel
from strands.models.ollama import OllamaModel

# Bedrock with streaming
bedrock_model = BedrockModel(
    model_id="us.amazon.nova-pro-v1:0",
    temperature=0.3,
    streaming=True
)

# Local Ollama model
ollama_model = OllamaModel(
    host="http://localhost:11434",
    model_id="llama3"
)
```

## Architecture Insights

### Model-Driven Approach
- **LLM as Brain**: Uses foundation models for decision-making and reasoning
- **Prompt-Based**: Natural language prompts define agent objectives
- **Event Loop**: Iterative cycle of planning, reasoning, acting, reflecting
- **Error Handling**: Automatic retry logic and context overflow management

### Key Architectural Patterns
- **Provider Abstraction**: Unified interface across different model providers
- **Pluggable Memory**: Multiple conversation management strategies
- **Tool Ecosystem**: Extensible tool system with MCP protocol support
- **Streaming Support**: Real-time response streaming capabilities
- **Observability**: Built-in tracing and telemetry for debugging

### Integration Points
- **MCP Protocol**: Native support for Model Context Protocol servers
- **Multi-Provider**: Seamless switching between different model providers
- **Tool Ecosystem**: Access to thousands of pre-built tools
- **Conversation Management**: Flexible memory and context handling
- **Multi-Agent**: Agent-to-agent communication capabilities

## Development Patterns

### Testing Structure
- `tests/`: Unit tests mirroring src structure
- `tests-integ/`: Integration tests for end-to-end scenarios
- Comprehensive test coverage for all major components

### Build Configuration
- `pyproject.toml`: Modern Python packaging with dependencies
- `.pre-commit-config.yaml`: Code quality automation
- GitHub Actions workflows for CI/CD
- Style guide with code formatting standards

### Framework Extensibility
- **Custom Providers**: Implement custom model providers
- **Custom Tools**: Python decorator-based tool creation
- **Custom Handlers**: Extend model provider handling
- **Plugin Architecture**: Modular design for extensions

## Large Files Requiring Processing
*None identified - all files are reasonably sized for direct analysis*

## Reference Links
- **Repository**: https://github.com/strands-agents/sdk-python
- **Documentation**: https://strandsagents.com/
- **PyPI Package**: https://pypi.org/project/strands-agents/
- **Tools Package**: https://github.com/strands-agents/tools
- **Samples**: https://github.com/strands-agents/samples
- **MCP Server**: https://github.com/strands-agents/mcp-server

## JESSE Framework Integration Value
- **MCP Implementation Reference**: Production-ready MCP client implementation
- **Multi-Provider Architecture**: Patterns for supporting multiple model providers
- **Agent Design Patterns**: Event loop and conversation management approaches
- **Tool Integration**: Decorator-based tool system and MCP protocol usage
- **Error Handling**: Robust error handling and retry mechanisms
- **Streaming Support**: Real-time response streaming implementation
- **Multi-Agent Patterns**: Agent-to-agent communication architectures
