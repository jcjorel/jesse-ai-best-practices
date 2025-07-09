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
# CLI frontend for jesse-cli command providing simple file indexing interface.
# Handles argument parsing, validation, and user interaction for the jesse-cli index-file command.
###############################################################################
# [Source file design principles]
# Pure CLI interface with argument parsing and user interaction responsibilities only
# Clear separation between frontend (CLI) and backend (LLM processing) concerns
# Simple command structure with straightforward error handling and user feedback
# Leverage existing cli_utils for validation and consistent user experience
###############################################################################
# [Source file constraints]
# Must provide clear error messages for common failure scenarios
# Should validate inputs before calling backend to catch issues early
# Must handle async backend calls properly in CLI context
# Exit codes should follow standard CLI conventions (0 for success, 1 for error)
###############################################################################
# [Dependencies]
# <system>: asyncio, sys, click
# <codebase>: jesse-cli/cli_utils (CLI formatting and AWS credential utilities)
# <codebase>: jesse_framework_mcp/llm/simple_file_indexer (Backend file indexing functionality)
###############################################################################
# [GenAI tool change history]
# 2025-07-09T23:07:00Z : Initial implementation of CLI frontend for jesse-cli by CodeAssistant
# * Created main entry point with argparse for index-file subcommand
# * Implemented async handling for backend calls with proper error management
# * Added file validation and AWS credential checking before backend processing
# * Included clear user feedback and standard CLI exit code handling
###############################################################################

#!/usr/bin/env python3
"""
jesse-cli index-file command - Frontend CLI Interface

Provides simple command line interface for file indexing using Claude 4 Sonnet.
"""

import asyncio
import sys
import click
from .cli_utils import check_aws_credentials, print_error, print_success, print_info
from jesse_framework_mcp.llm.simple_file_indexer import index_file_simple


@click.group()
def main():
    """JESSE CLI Tools - Simple file indexing with Claude 4 Sonnet"""
    pass


@main.command(name='index-file')
@click.argument('file_path', type=click.Path(exists=True, readable=True))
def index_file_command(file_path):
    """Index a source file with Claude 4 Sonnet analysis"""
    try:
        exit_code = asyncio.run(handle_index_file(str(file_path)))
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print_error("Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print_error("Unexpected error in CLI", e)
        sys.exit(1)


async def handle_index_file(file_path: str) -> int:
    """
    [Function intent]
    Handle the index-file command by validating inputs and calling backend processing.
    Provides clear user feedback throughout the process with appropriate error handling.

    [Design principles]
    Frontend validation before backend processing to catch issues early.
    Clear user feedback with progress indicators and success/error messages.
    Proper exception handling with specific error types and helpful messages.

    [Implementation details]
    Validates file path and AWS credentials before expensive backend operations.
    Calls simple_file_indexer backend with async handling and error recovery.
    Returns standard CLI exit codes for shell script integration.
    Provides informative output formatting for user experience.

    Args:
        file_path: Path to the source file to analyze

    Returns:
        Exit code: 0 for success, 1 for error
    """
    try:
        # Note: File validation now handled by Click's Path validator
        print_info(f"Validating file: {file_path}")
        
        print_info("Checking AWS credentials...")
        check_aws_credentials()
        
        # Call backend for analysis
        print_info(f"Analyzing file with Claude 4 Sonnet: {file_path}")
        result = await index_file_simple(file_path)
        
        # Display results
        print()  # Add space before results
        print(result)
        print()  # Add space after results
        print_success("File analysis completed successfully")
        
        return 0
        
    except FileNotFoundError as e:
        print_error("File not found", e)
        return 1
    except PermissionError as e:
        print_error("Permission denied", e)
        return 1
    except Exception as e:
        print_error("Failed to index file", e)
        return 1


if __name__ == "__main__":
    sys.exit(main())
