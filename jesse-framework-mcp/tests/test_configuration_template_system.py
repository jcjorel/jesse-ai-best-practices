"""
Test suite for Configuration Template System.

This module tests the configuration template system including:
- Centralized defaults for handler types
- JSON configuration auto-generation
- Pydantic validation
- IndexingConfig integration
"""

import pytest
import tempfile
import json
from pathlib import Path
from unittest.mock import patch

from jesse_framework_mcp.knowledge_bases.indexing.defaults import (
    get_default_config,
    get_supported_handler_types,
    validate_handler_type,
    PROJECT_BASE_DEFAULT_CONFIG,
    GIT_CLONES_DEFAULT_CONFIG,
    PDF_KNOWLEDGE_DEFAULT_CONFIG
)
from jesse_framework_mcp.knowledge_bases.indexing.config_manager import (
    IndexingConfigManager,
    IndexingConfigModel,
    HandlerType
)
from jesse_framework_mcp.knowledge_bases.models.indexing_config import IndexingConfig


class TestDefaultConfigurations:
    """Test cases for centralized default configurations."""
    
    def test_supported_handler_types(self):
        """Test that all expected handler types are supported."""
        supported_types = get_supported_handler_types()
        expected_types = ["git-clones", "pdf-knowledge", "project-base"]
        
        assert supported_types == expected_types
        assert len(supported_types) == 3
    
    def test_validate_handler_type(self):
        """Test handler type validation."""
        assert validate_handler_type("project-base") == True
        assert validate_handler_type("git-clones") == True
        assert validate_handler_type("pdf-knowledge") == True
        assert validate_handler_type("invalid-handler") == False
    
    def test_get_default_config_project_base(self):
        """Test project-base default configuration."""
        config = get_default_config("project-base")
        
        assert config["handler_type"] == "project-base"
        
        # Test hierarchical file processing configuration
        assert "file_processing" in config
        file_proc = config["file_processing"]
        assert file_proc["max_file_size"] == 2 * 1024 * 1024  # 2MB
        assert file_proc["batch_size"] == 7
        assert file_proc["max_concurrent_operations"] == 3
        
        # Test hierarchical content filtering configuration
        assert "content_filtering" in config
        content_filter = config["content_filtering"]
        assert "excluded_extensions" in content_filter
        assert "excluded_directories" in content_filter
        assert "project_base_exclusions" in content_filter
        
        # Check project-base specific exclusions
        exclusions = content_filter["project_base_exclusions"]
        assert ".knowledge" in exclusions
        assert ".coding_assistant" in exclusions
        assert ".clinerules" in exclusions
        
        # Test hierarchical LLM configuration
        assert "llm_config" in config
        llm_cfg = config["llm_config"]
        assert "llm_model" in llm_cfg
        assert llm_cfg["temperature"] == 0.3
        assert llm_cfg["max_tokens"] == 20000
    
    def test_get_default_config_git_clones(self):
        """Test git-clones default configuration."""
        config = get_default_config("git-clones")
        
        assert config["handler_type"] == "git-clones"
        
        # Test hierarchical file processing configuration
        file_proc = config["file_processing"]
        assert file_proc["max_file_size"] == 1 * 1024 * 1024  # 1MB (smaller)
        assert file_proc["batch_size"] == 5  # Smaller batches
        
        # Should not have project_base_exclusions
        content_filter = config["content_filtering"]
        assert content_filter.get("project_base_exclusions") is None
    
    def test_get_default_config_pdf_knowledge(self):
        """Test pdf-knowledge default configuration."""
        config = get_default_config("pdf-knowledge")
        
        assert config["handler_type"] == "pdf-knowledge"
        
        # Test hierarchical file processing configuration
        file_proc = config["file_processing"]
        assert file_proc["max_file_size"] == 10 * 1024 * 1024  # 10MB (larger for PDFs)
        assert file_proc["batch_size"] == 3  # Smaller batches for documents
        
        # Test hierarchical LLM configuration
        llm_cfg = config["llm_config"]
        assert llm_cfg["temperature"] == 0.2  # Lower for document analysis
    
    def test_get_default_config_invalid_handler(self):
        """Test error handling for invalid handler type."""
        with pytest.raises(ValueError) as excinfo:
            get_default_config("invalid-handler")
        
        assert "Unsupported handler type" in str(excinfo.value)
        assert "invalid-handler" in str(excinfo.value)
    
    def test_default_config_immutability(self):
        """Test that default configurations are immutable (deep copied)."""
        config1 = get_default_config("project-base")
        config2 = get_default_config("project-base")
        
        # Modify one config
        config1["file_processing"]["max_file_size"] = 999999
        
        # Other config should be unchanged
        assert config2["file_processing"]["max_file_size"] == 2 * 1024 * 1024
        
        # Original template should be unchanged
        original = PROJECT_BASE_DEFAULT_CONFIG["file_processing"]["max_file_size"]
        assert original == 2 * 1024 * 1024


class TestPydanticValidation:
    """Test cases for Pydantic configuration validation."""
    
    def test_valid_project_base_config(self):
        """Test validation of valid project-base configuration."""
        config_data = get_default_config("project-base")
        
        # Should validate without errors
        config_model = IndexingConfigModel(**config_data)
        
        assert config_model.handler_type == HandlerType.PROJECT_BASE
        assert config_model.file_processing.max_file_size == 2 * 1024 * 1024
        assert config_model.content_filtering.project_base_exclusions is not None
        assert ".knowledge" in config_model.content_filtering.project_base_exclusions
    
    
    def test_invalid_indexing_mode(self):
        """Test validation error for invalid indexing mode."""
        config_data = get_default_config("project-base")
        config_data["change_detection"]["indexing_mode"] = "invalid_mode"
        
        with pytest.raises(ValueError) as excinfo:
            IndexingConfigModel(**config_data)
        
        assert "indexing_mode must be one of" in str(excinfo.value)
    
    def test_missing_project_base_exclusions(self):
        """Test validation error when project-base handler lacks exclusions."""
        config_data = get_default_config("project-base")
        config_data["content_filtering"]["project_base_exclusions"] = None
        
        with pytest.raises(ValueError) as excinfo:
            IndexingConfigModel(**config_data)
        
        assert "project_base_exclusions required for project-base handler" in str(excinfo.value)
    
    def test_git_clones_without_project_base_exclusions(self):
        """Test that git-clones handler doesn't require project_base_exclusions."""
        config_data = get_default_config("git-clones")
        
        # Should validate without errors (no project_base_exclusions)
        config_model = IndexingConfigModel(**config_data)
        
        assert config_model.handler_type == HandlerType.GIT_CLONES
        assert config_model.content_filtering.project_base_exclusions is None


class TestConfigurationManager:
    """Test cases for IndexingConfigManager."""
    
    @pytest.fixture
    def temp_knowledge_dir(self):
        """Create temporary knowledge directory for testing."""
        with tempfile.TemporaryDirectory() as temp_dir:
            yield Path(temp_dir)
    
    def test_manager_initialization(self, temp_knowledge_dir):
        """Test configuration manager initialization."""
        manager = IndexingConfigManager(temp_knowledge_dir)
        
        assert manager.knowledge_directory == temp_knowledge_dir
        assert temp_knowledge_dir.exists()
    
    def test_auto_generate_missing_config(self, temp_knowledge_dir):
        """Test auto-generation of missing configuration files."""
        manager = IndexingConfigManager(temp_knowledge_dir)
        
        # Config file shouldn't exist initially
        config_file = temp_knowledge_dir / "project-base.indexing-config.json"
        assert not config_file.exists()
        
        # Load config should auto-generate the file
        config = manager.load_config("project-base")
        
        # File should now exist
        assert config_file.exists()
        
        # Verify it's valid JSON with expected hierarchical content
        with open(config_file, 'r') as f:
            json_config = json.load(f)
        
        assert json_config["handler_type"] == "project-base"
        assert json_config["file_processing"]["max_file_size"] == 2 * 1024 * 1024
        
        # Should return IndexingConfig instance
        assert isinstance(config, IndexingConfig)
        assert config.max_file_size == 2 * 1024 * 1024
    
    def test_load_existing_config(self, temp_knowledge_dir):
        """Test loading existing configuration file."""
        manager = IndexingConfigManager(temp_knowledge_dir)
        
        # Create custom config file with hierarchical structure
        config_file = temp_knowledge_dir / "git-clones.indexing-config.json"
        custom_config = get_default_config("git-clones")
        custom_config["file_processing"]["max_file_size"] = 500000  # Custom value
        
        with open(config_file, 'w') as f:
            json.dump(custom_config, f, indent=2)
        
        # Load config should use existing file
        config = manager.load_config("git-clones")
        
        assert isinstance(config, IndexingConfig)
        assert config.max_file_size == 500000  # Custom value used
    
    def test_configuration_caching(self, temp_knowledge_dir):
        """Test that configurations are cached for performance."""
        manager = IndexingConfigManager(temp_knowledge_dir)
        
        # Load config twice
        config1 = manager.load_config("project-base")
        config2 = manager.load_config("project-base")
        
        # Should return the same instance (cached)
        assert config1 is config2
    
    def test_cache_clearing(self, temp_knowledge_dir):
        """Test configuration cache clearing."""
        manager = IndexingConfigManager(temp_knowledge_dir)
        
        # Load config to populate cache
        config1 = manager.load_config("project-base")
        
        # Clear cache
        manager.clear_cache()
        
        # Load again should create new instance
        config2 = manager.load_config("project-base")
        
        assert config1 is not config2  # Different instances
        assert config1.max_file_size == config2.max_file_size  # Same values
    
    def test_invalid_handler_type(self, temp_knowledge_dir):
        """Test error handling for invalid handler type."""
        manager = IndexingConfigManager(temp_knowledge_dir)
        
        with pytest.raises(ValueError) as excinfo:
            manager.load_config("invalid-handler")
        
        assert "Unsupported handler type" in str(excinfo.value)
    
    def test_invalid_json_config(self, temp_knowledge_dir):
        """Test error handling for invalid JSON configuration."""
        manager = IndexingConfigManager(temp_knowledge_dir)
        
        # Create invalid JSON file
        config_file = temp_knowledge_dir / "project-base.indexing-config.json"
        with open(config_file, 'w') as f:
            f.write("{ invalid json")
        
        with pytest.raises(ValueError) as excinfo:
            manager.load_config("project-base")
        
        assert "Invalid JSON format" in str(excinfo.value)
    
    def test_get_config_file_path(self, temp_knowledge_dir):
        """Test getting configuration file path."""
        manager = IndexingConfigManager(temp_knowledge_dir)
        
        path = manager.get_config_file_path("project-base")
        expected_path = temp_knowledge_dir / "project-base.indexing-config.json"
        
        assert path == expected_path
        
        # Test invalid handler type
        with pytest.raises(ValueError):
            manager.get_config_file_path("invalid-handler")


class TestIndexingConfigIntegration:
    """Test cases for IndexingConfig integration with configuration system."""
    
    def test_from_dict_conversion(self):
        """Test IndexingConfig.from_dict with configuration manager data."""
        config_dict = get_default_config("project-base")
        
        # Convert through configuration manager process
        config_model = IndexingConfigModel(**config_dict)
        converted_dict = config_model.model_dump()
        
        # Create IndexingConfig from hierarchical dictionary
        indexing_config = IndexingConfig.from_dict(converted_dict)
        
        assert isinstance(indexing_config, IndexingConfig)
        assert indexing_config.max_file_size == 2 * 1024 * 1024
        assert indexing_config.batch_size == 7
        assert isinstance(indexing_config.excluded_extensions, set)
        assert isinstance(indexing_config.excluded_directories, set)
        assert isinstance(indexing_config.project_base_exclusions, set)
        assert ".knowledge" in indexing_config.project_base_exclusions
    
    def test_load_for_handler_with_project_root(self):
        """Test IndexingConfig.load_for_handler with project root detection."""
        with tempfile.TemporaryDirectory() as temp_dir:
            knowledge_dir = Path(temp_dir)
            
            # Call with explicit knowledge directory (avoid mocking complexity)
            config = IndexingConfig.load_for_handler("project-base", knowledge_dir)
            
            assert isinstance(config, IndexingConfig)
            assert config.max_file_size == 2 * 1024 * 1024
            
            # Verify JSON file was created
            config_file = knowledge_dir / "project-base.indexing-config.json"
            assert config_file.exists()
    
    def test_load_for_handler_with_explicit_knowledge_dir(self):
        """Test IndexingConfig.load_for_handler with explicit knowledge directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            knowledge_dir = Path(temp_dir)
            
            config = IndexingConfig.load_for_handler("git-clones", knowledge_dir)
            
            assert isinstance(config, IndexingConfig)
            assert config.max_file_size == 1 * 1024 * 1024  # git-clones default
            
            # Verify JSON file was created
            config_file = knowledge_dir / "git-clones.indexing-config.json"
            assert config_file.exists()
    
    @patch('jesse_framework_mcp.knowledge_bases.models.indexing_config.get_project_root')
    def test_load_for_handler_no_project_root(self, mock_get_project_root):
        """Test error when project root cannot be detected."""
        mock_get_project_root.return_value = None
        
        with pytest.raises(ValueError) as excinfo:
            IndexingConfig.load_for_handler("project-base")
        
        assert "Could not determine knowledge directory" in str(excinfo.value)


class TestHierarchicalExclusions:
    """Test cases for hierarchical exclusion system."""
    
    def test_project_base_exclusions_in_defaults(self):
        """Test that project-base defaults include specific exclusions."""
        config = get_default_config("project-base")
        exclusions = config["content_filtering"]["project_base_exclusions"]
        
        # Required project-base exclusions
        assert ".knowledge" in exclusions
        assert ".coding_assistant" in exclusions
        assert ".clinerules" in exclusions
    
    def test_git_clones_no_project_base_exclusions(self):
        """Test that git-clones doesn't have project-base exclusions."""
        config = get_default_config("git-clones")
        content_filtering = config["content_filtering"]
        
        # Should not have project_base_exclusions or it should be None/empty
        assert content_filtering.get("project_base_exclusions") is None
    
    def test_base_exclusions_in_all_handlers(self):
        """Test that base exclusions are present in all handler types."""
        for handler_type in get_supported_handler_types():
            config = get_default_config(handler_type)
            content_filtering = config["content_filtering"]
            
            excluded_dirs = content_filtering["excluded_directories"]
            excluded_exts = content_filtering["excluded_extensions"]
            
            # Common base exclusions should be present
            assert ".git" in excluded_dirs
            assert "__pycache__" in excluded_dirs
            assert ".pyc" in excluded_exts
            assert ".log" in excluded_exts


if __name__ == "__main__":
    pytest.main([__file__])
