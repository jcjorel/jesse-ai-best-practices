###############################################################################
# IMPORTANT: This header comment is designed for GenAI code review and maintenance
# Any GenAI tool working with this file MUST preserve and update this header
###############################################################################
# [GenAI coding tool directive]
# - Maintain this header with all modifications
# - Update History section with each change
# - Keep only the 4 most recent records in the history section. Sort from newer to older.
# - Preserve Intent, Design, and Constraints sections
# - Use this header as context for code reviews and modifications
# - Ensure all changes align with the design principles
# - Respect system prompt directives at all times
###############################################################################
# [Source file intent]
# Simple File Indexer Backend providing ultra-simple file indexing using Claude 4 Sonnet
# directly via Strands driver. No complex prompts or indexing systems - just basic file analysis
# for the jesse-cli command line interface.
###############################################################################
# [Source file design principles]
# Ultra-simple implementation with minimal dependencies and clear flow
# Direct Claude 4 interaction without service layers, complex prompt engineering, or MCP context
# Focus on clarity and ease of use over advanced features
# Reusable backend that other parts of the framework can utilize
###############################################################################
# [Source file constraints]
# Must work outside of MCP context for standalone CLI usage
# Should not depend on complex indexing or knowledge base systems
# Must provide clear error messages for troubleshooting
# File reading must handle both text and binary files gracefully
###############################################################################
# [Dependencies]
# <system>: asyncio, logging, pathlib
# <codebase>: jesse_framework_mcp/llm/strands_agent_driver (Strands Claude 4 driver and config)
# <codebase>: jesse_framework_mcp/llm/strands_agent_driver/exceptions (Driver-specific exceptions)
###############################################################################
# [GenAI tool change history]
# 2025-07-09T23:07:00Z : Initial implementation of simple file indexer backend by CodeAssistant
# * Created ultra-simple file indexing function using Claude 4 Sonnet directly
# * Implemented basic prompt for file analysis without complex indexing workflows
# * Added proper error handling for file reading and AWS Bedrock connectivity
# * Included support for both text and binary file reading with encoding fallback
###############################################################################

"""
Simple File Indexer Backend

Ultra-simple file indexing using Claude 4 Sonnet directly via Strands driver.
No complex prompts or indexing systems - just basic file analysis.
"""

import asyncio
import logging
from pathlib import Path
from typing import Optional

from .strands_agent_driver import StrandsClaude4Driver, Claude4SonnetConfig
from .strands_agent_driver.exceptions import StrandsDriverError, BedrockConnectionError

logger = logging.getLogger(__name__)


async def index_file_simple(file_path: str) -> str:
    """
    [Function intent]
    Simple file indexing - read file, send to Claude 4 with basic prompt, return analysis.
    Provides straightforward file analysis without complex indexing workflows or MCP context.

    [Design principles]
    Ultra-simple implementation with minimal dependencies and clear flow.
    Direct Claude 4 interaction without service layers or complex prompt engineering.
    Focus on clarity and ease of use over advanced features.
    Clear error handling with specific exception types for different failure modes.

    [Implementation details]
    Reads file content and creates basic analysis prompt for file understanding.
    Uses default Claude 4 Sonnet configuration for reliable, fast analysis.
    Returns raw Claude response for maximum flexibility in output handling.
    Handles both text and binary files with encoding fallback mechanism.
    Creates unique conversation ID to avoid conflicts in driver's conversation management.

    Args:
        file_path: Path to the source file to analyze

    Returns:
        Claude 4 analysis result as string

    Raises:
        FileNotFoundError: When file doesn't exist
        PermissionError: When file isn't readable
        StrandsDriverError: When Claude 4 analysis fails
        BedrockConnectionError: When AWS Bedrock connection fails
    """
    # Read file content
    path = Path(file_path)
    
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        # Handle binary files gracefully
        with open(path, 'r', encoding='latin-1') as f:
            content = f.read()
    
    # Create simple, clear indexing prompt
    prompt = f"""Please analyze this source file and provide a concise summary including:

1. **Purpose**: What this file does and its role
2. **Key Components**: Main functions, classes, or important sections  
3. **Dependencies**: What it imports or relies on
4. **Architecture Notes**: How it might fit into a larger system

File: {path.name}
Size: {len(content)} characters

```
{content}
```

Provide a clear, structured analysis:"""

    # Use Claude 4 driver directly with simple configuration
    config = Claude4SonnetConfig()  # Default, simple config
    
    try:
        async with StrandsClaude4Driver(config) as driver:
            conversation_id = f"simple_index_{path.name}_{id(path)}"
            response = await driver.send_message(prompt, conversation_id, use_cache=False)
            
            logger.info(f"Successfully indexed file: {file_path}")
            return response.content
            
    except (StrandsDriverError, BedrockConnectionError) as e:
        logger.error(f"Claude 4 indexing failed for {file_path}: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error indexing {file_path}: {e}")
        raise RuntimeError(f"File indexing failed: {e}")
