"""
CLI Utilities

Shared utilities for JESSE CLI commands including error handling and common functions.
"""

import sys
import logging
import os
from pathlib import Path
from typing import Optional


def setup_logging(verbose: bool = False) -> None:
    """
    Setup logging for CLI operations.
    
    Args:
        verbose: Enable verbose logging output
    """
    level = logging.DEBUG if verbose else logging.WARNING
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )


def validate_file_path(file_path: str) -> Path:
    """
    Validate that a file path exists and is readable.
    
    Args:
        file_path: Path to the file to validate
        
    Returns:
        Path object for the validated file
        
    Raises:
        SystemExit: On validation failure with appropriate error message
    """
    path = Path(file_path).resolve()
    
    if not path.exists():
        print(f"❌ Error: File not found: {file_path}", file=sys.stderr)
        sys.exit(1)
    
    if not path.is_file():
        print(f"❌ Error: Path is not a file: {file_path}", file=sys.stderr)
        sys.exit(1)
    
    try:
        # Test readability
        with open(path, 'r', encoding='utf-8') as f:
            f.read(1)  # Try to read first character
    except PermissionError:
        print(f"❌ Error: Permission denied reading file: {file_path}", file=sys.stderr)
        sys.exit(1)
    except UnicodeDecodeError:
        # Binary files are OK, will be handled by the service
        pass
    except Exception as e:
        print(f"❌ Error: Unable to read file {file_path}: {e}", file=sys.stderr)
        sys.exit(1)
    
    return path


def check_aws_credentials() -> None:
    """
    Check if AWS credentials are available and warn if not found.
    """
    has_credentials = (
        os.getenv("AWS_ACCESS_KEY_ID") or 
        os.getenv("AWS_PROFILE") or
        Path.home().joinpath(".aws/credentials").exists()
    )
    
    if not has_credentials:
        print("⚠️  Warning: No AWS credentials detected", file=sys.stderr)
        print("   Set AWS_ACCESS_KEY_ID/AWS_SECRET_ACCESS_KEY or AWS_PROFILE", file=sys.stderr)
        print("   This CLI requires AWS Bedrock access for Claude 4 Sonnet", file=sys.stderr)
        print()


def print_error(message: str, error: Optional[Exception] = None) -> None:
    """
    Print a formatted error message.
    
    Args:
        message: Main error message
        error: Optional exception for additional details
    """
    print(f"❌ Error: {message}", file=sys.stderr)
    if error and hasattr(error, '__class__'):
        print(f"   Details: {error.__class__.__name__}: {error}", file=sys.stderr)


def print_success(message: str) -> None:
    """
    Print a formatted success message.
    
    Args:
        message: Success message
    """
    print(f"✅ {message}")


def print_info(message: str) -> None:
    """
    Print a formatted info message.
    
    Args:
        message: Info message
    """
    print(f"ℹ️  {message}")
