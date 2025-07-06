#!/usr/bin/env python3
"""
Test to verify that scratchpad directory is excluded from all indexing handlers.
"""

import tempfile
from pathlib import Path

from jesse_framework_mcp.knowledge_bases.indexing.defaults import (
    get_default_config, 
    get_supported_handler_types,
    BASE_EXCLUDED_DIRECTORIES
)
from jesse_framework_mcp.knowledge_bases.models.indexing_config import IndexingConfig


def test_scratchpad_in_base_exclusions():
    """Test that scratchpad is included in base excluded directories."""
    assert 'scratchpad' in BASE_EXCLUDED_DIRECTORIES
    print("✅ 'scratchpad' found in BASE_EXCLUDED_DIRECTORIES")


def test_scratchpad_excluded_in_all_handlers():
    """Test that scratchpad directory is excluded in all supported handler types."""
    handler_types = get_supported_handler_types()
    
    for handler_type in handler_types:
        # Get default configuration for this handler
        config_dict = get_default_config(handler_type)
        
        # Verify scratchpad is in excluded directories
        excluded_dirs = config_dict['content_filtering']['excluded_directories']
        assert 'scratchpad' in excluded_dirs, f"scratchpad not found in {handler_type} excluded directories"
        print(f"✅ Handler '{handler_type}': scratchpad found in excluded directories")


def test_indexing_config_excludes_scratchpad():
    """Test that IndexingConfig properly excludes scratchpad directory."""
    handler_types = get_supported_handler_types()
    
    for handler_type in handler_types:
        # Create IndexingConfig from default configuration
        config_dict = get_default_config(handler_type)
        config = IndexingConfig.from_dict(config_dict)
        
        # Create a mock scratchpad directory path
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            scratchpad_path = temp_path / 'scratchpad'
            scratchpad_path.mkdir()
            
            # Test that should_process_directory returns False for scratchpad
            should_process = config.should_process_directory(scratchpad_path)
            assert not should_process, f"Handler '{handler_type}' should NOT process scratchpad directory"
            print(f"✅ Handler '{handler_type}': should_process_directory(scratchpad) = {should_process}")


def test_scratchpad_exclusion_with_different_paths():
    """Test scratchpad exclusion with different path structures."""
    config = IndexingConfig.from_dict(get_default_config('project-base'))
    
    test_paths = [
        'scratchpad',
        'project/scratchpad',
        'deep/nested/scratchpad',
        'absolute/path/scratchpad'  # Changed from /absolute/path/scratchpad to avoid permission issues
    ]
    
    for path_str in test_paths:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Create the directory structure
            full_path = temp_path / path_str
            full_path.mkdir(parents=True)
            
            # Test the scratchpad directory specifically
            scratchpad_dir = full_path if full_path.name == 'scratchpad' else full_path / 'scratchpad'
            if not scratchpad_dir.exists():
                scratchpad_dir.mkdir()
            
            should_process = config.should_process_directory(scratchpad_dir)
            assert not should_process, f"scratchpad directory should be excluded at path: {scratchpad_dir}"
            print(f"✅ Path '{scratchpad_dir}': correctly excluded")


if __name__ == "__main__":
    # Run the tests
    print("Testing scratchpad directory exclusion...")
    print()
    
    test_scratchpad_in_base_exclusions()
    print()
    
    test_scratchpad_excluded_in_all_handlers()
    print()
    
    test_indexing_config_excludes_scratchpad()
    print()
    
    test_scratchpad_exclusion_with_different_paths()
    print()
    
    print("🎉 All tests passed! The scratchpad directory is properly excluded from all indexing handlers.")
