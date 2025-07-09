"""
Test suite for the new clean knowledge bases indexer implementation.

This test suite provides comprehensive coverage for all components of the new
indexer architecture including models, handlers, discovery, planning, execution,
and end-to-end integration testing.

Test Structure:
- test_models.py: Data models and validation testing
- test_handlers.py: Handler interface and implementations
- test_discovery.py: Discovery engine and validation
- test_decisions.py: Decision making and task generation
- test_planning.py: Task planning and dependency resolution
- test_knowledge.py: Knowledge building tasks and LLM integration
- test_execution.py: Task execution and result handling
- test_core.py: Core indexer orchestration
- test_integration.py: End-to-end integration testing

Usage:
    # Run all new indexer tests
    pytest jesse_framework_mcp/knowledge_bases/indexer/tests/
    
    # Run specific test file
    pytest jesse_framework_mcp/knowledge_bases/indexer/tests/test_models.py
    
    # Run with coverage
    pytest --cov=jesse_framework_mcp.knowledge_bases.indexer jesse_framework_mcp/knowledge_bases/indexer/tests/
"""

import sys
from pathlib import Path

# Add project root to path for imports
project_root = Path(__file__).parent.parent.parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# Test utilities and fixtures
import pytest
import asyncio
import tempfile
from unittest.mock import Mock, AsyncMock, patch

# Test modules will be imported as they are created
__all__ = []
