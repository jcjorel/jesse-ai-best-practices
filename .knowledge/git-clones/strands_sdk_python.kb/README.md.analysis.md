<!-- CACHE_METADATA_START -->
<!-- Source File: {PROJECT_ROOT}/.knowledge/git-clones/strands_sdk_python/README.md -->
<!-- Cached On: 2025-07-07T22:32:35.667582 -->
<!-- Source Modified: 2025-06-30T17:02:52.895757 -->
<!-- Cache Version: 1.0 -->
<!-- CACHE_METADATA_END -->

#### Functional Intent & Features

Strands Agents SDK serves as a model-driven framework for building AI agents with minimal code complexity, providing lightweight agent orchestration, multi-provider model support, and native `MCP` (Model Context Protocol) integration. The SDK enables rapid development of conversational assistants and autonomous workflows through its `Agent` class, `@tool` decorator system, and built-in streaming capabilities. Key semantic entities include `strands.Agent`, `strands.tool`, `strands.models.BedrockModel`, `strands.tools.mcp.MCPClient`, `strands_tools.calculator`, `BedrockModel`, `OllamaModel`, `LlamaAPIModel`, and integration with `Amazon Bedrock`, `Anthropic`, `LiteLLM`, `Ollama`, `OpenAI` providers. The framework implements a customizable agent loop architecture supporting both local development and production deployment scenarios.

##### Main Components

The SDK consists of core agent orchestration through the `Agent` class, model provider abstractions including `BedrockModel`, `OllamaModel`, and `LlamaAPIModel`, tool integration system via `@tool` decorators and `MCPClient`, and the optional `strands-agents-tools` package containing pre-built utilities like `calculator`. The architecture separates model providers from agent logic, enabling seamless switching between `Amazon Bedrock`, `Anthropic`, `LiteLLM`, `Ollama`, and `OpenAI` services while maintaining consistent agent behavior patterns.

###### Architecture & Design

The framework follows a model-agnostic design pattern where agents operate independently of specific LLM providers through abstracted model interfaces. The `MCPClient` implements the Model Context Protocol specification for standardized tool integration, while the agent loop architecture provides customizable execution flows. The system employs decorator-based tool registration using `@tool` annotations, enabling Python functions to be automatically converted into agent-callable tools with automatic schema generation from docstrings and type hints.

####### Implementation Approach

The SDK implements streaming support through provider-specific streaming flags, tool execution via Python function introspection and automatic schema generation, and multi-agent coordination through shared tool registries. The `MCPClient` uses `stdio_client` with `StdioServerParameters` for external tool server communication, while model providers implement consistent interfaces for temperature control, model selection, and response handling. Agent initialization patterns support both simple single-tool scenarios and complex multi-provider configurations.

######## External Dependencies & Integration Points

**→ Inbound:**
- `mcp` (external library) - Model Context Protocol client implementation for tool server communication
- `uvx` (external command) - Package execution for MCP server instantiation
- `awslabs.aws-documentation-mcp-server` - AWS documentation MCP server integration
- AWS credentials and model access configuration for `us-west-2` region
- Python 3.10+ runtime environment requirement

**← Outbound:**
- `strandsagents.com` - Documentation and API reference hosting
- `pypi.org/project/strands-agents/` - Package distribution and version management
- `github.com/strands-agents/` - Source code repositories and sample collections

**⚡ Integration:**
The SDK serves as a central orchestration layer connecting LLM providers, tool systems, and MCP servers through standardized interfaces, enabling developers to build agent systems without vendor lock-in while maintaining access to thousands of pre-built MCP tools.

######### Edge Cases & Error Handling

The framework requires AWS credentials configuration and Claude 3.7 Sonnet model access in `us-west-2` region for default `BedrockModel` operation, with fallback guidance for alternative provider configuration. MCP server integration may fail if `uvx` command execution encounters permission or network issues, requiring proper error handling in `MCPClient` initialization. Model provider switching requires careful attention to parameter compatibility, as different providers support varying temperature ranges, streaming capabilities, and model identifier formats.

########## Internal Implementation Details

The agent loop maintains conversation state through message history management, while tool execution results are automatically formatted for LLM consumption. The `@tool` decorator performs runtime introspection to extract function signatures, parameter types, and docstring content for automatic schema generation. Model provider implementations handle authentication, request formatting, and response parsing specific to each service's API requirements, with streaming responses managed through provider-specific callback mechanisms.

########### Code Usage Examples

Basic agent creation with calculator tool integration:
```python
from strands import Agent
from strands_tools import calculator
agent = Agent(tools=[calculator])
response = agent("What is the square root of 1764")
```

Custom tool definition using decorator pattern:
```python
from strands import Agent, tool

@tool
def word_count(text: str) -> int:
    """Count words in text.

    This docstring is used by the LLM to understand the tool's purpose.
    """
    return len(text.split())

agent = Agent(tools=[word_count])
response = agent("How many words are in this sentence?")
```

MCP server integration for AWS documentation access:
```python
from strands import Agent
from strands.tools.mcp import MCPClient
from mcp import stdio_client, StdioServerParameters

aws_docs_client = MCPClient(
    lambda: stdio_client(StdioServerParameters(command="uvx", args=["awslabs.aws-documentation-mcp-server@latest"]))
)

with aws_docs_client:
   agent = Agent(tools=aws_docs_client.list_tools_sync())
   response = agent("Tell me about Amazon Bedrock and how to use it with Python")
```