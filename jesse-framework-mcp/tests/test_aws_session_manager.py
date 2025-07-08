#!/usr/bin/env python3
"""
Test suite for centralized AWS session management

This test suite validates the AWSSessionManager implementation and its integration
with the Strands Agent driver. It tests credential detection, region resolution,
connection validation, and integration patterns.

Usage:
    python -m pytest tests/test_aws_session_manager.py -v
"""

import asyncio
import os
import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from pathlib import Path
import tempfile
import configparser

# Add the project root to Python path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from jesse_framework_mcp.helpers.aws_session_manager import (
    AWSSessionManager,
    AWSConnectionInfo,
    AWSCredentialInfo,
    AWSConfigurationError,
    AWSConnectionError
)
from jesse_framework_mcp.llm.strands_agent_driver.models import Claude4SonnetConfig
from fastmcp import Context


class MockFastMCPContext:
    """Mock FastMCP Context for testing"""
    
    def __init__(self):
        self.logs = []
    
    async def info(self, message: str):
        self.logs.append(('info', message))
    
    async def error(self, message: str):
        self.logs.append(('error', message))
    
    async def warning(self, message: str):
        self.logs.append(('warning', message))


class TestAWSSessionManager:
    """Test suite for AWSSessionManager core functionality"""
    
    def setup_method(self):
        """Reset singleton state before each test"""
        # Reset singleton state
        AWSSessionManager._instance = None
        AWSSessionManager._initialized = False
        AWSSessionManager._validation_result = None
    
    @pytest.mark.asyncio
    async def test_singleton_pattern(self):
        """Test that AWSSessionManager follows singleton pattern"""
        manager1 = AWSSessionManager()
        manager2 = AWSSessionManager()
        
        # Should be the same instance
        assert manager1 is manager2
        assert id(manager1) == id(manager2)
    
    @pytest.mark.asyncio
    async def test_region_detection_env_aws_region(self):
        """Test region detection from AWS_REGION environment variable"""
        with patch.dict(os.environ, {'AWS_REGION': 'us-west-2'}, clear=False):
            manager = AWSSessionManager()
            region = await manager.get_region()
            assert region == 'us-west-2'
    
    @pytest.mark.asyncio
    async def test_region_detection_env_aws_default_region(self):
        """Test region detection from AWS_DEFAULT_REGION environment variable"""
        with patch.dict(os.environ, {}, clear=True):
            with patch.dict(os.environ, {'AWS_DEFAULT_REGION': 'eu-central-1'}):
                manager = AWSSessionManager()
                region = await manager.get_region()
                assert region == 'eu-central-1'
    
    @pytest.mark.asyncio
    async def test_region_detection_from_config_file(self):
        """Test region detection from ~/.aws/config file"""
        # Create temporary config file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.config', delete=False) as f:
            f.write('[default]\nregion = ap-southeast-1\n')
            config_path = f.name
        
        try:
            with patch.dict(os.environ, {}, clear=True):
                # Mock the config file path directly
                with patch.object(Path, 'exists', return_value=True):
                    with patch('configparser.ConfigParser.read') as mock_read:
                        with patch('configparser.ConfigParser.has_section', return_value=True):
                            with patch('configparser.ConfigParser.has_option', return_value=True):
                                with patch('configparser.ConfigParser.get', return_value='ap-southeast-1'):
                                    manager = AWSSessionManager()
                                    region = await manager.get_region()
                                    assert region == 'ap-southeast-1'
        finally:
            os.unlink(config_path)
    
    @pytest.mark.asyncio
    async def test_region_detection_failure(self):
        """Test region detection failure when no configuration found"""
        with patch.dict(os.environ, {}, clear=True):
            with patch('pathlib.Path.exists', return_value=False):
                manager = AWSSessionManager()
                
                with pytest.raises(AWSConfigurationError) as exc_info:
                    await manager.get_region()
                
                assert "No AWS region found" in str(exc_info.value)
    
    @pytest.mark.asyncio
    async def test_profile_detection_env_override(self):
        """Test profile detection with AWS_PROFILE environment override"""
        with patch.dict(os.environ, {'AWS_PROFILE': 'test-profile'}):
            with patch.object(AWSSessionManager, '_profile_exists', return_value=True):
                manager = AWSSessionManager()
                profile = await manager.get_profile_name()
                assert profile == 'test-profile'
    
    @pytest.mark.asyncio
    async def test_profile_detection_jesse_bedrock_access(self):
        """Test profile detection with jesse_bedrock_access preferred profile"""
        with patch.dict(os.environ, {}, clear=True):
            async def mock_profile_exists(profile_name):
                return profile_name == 'jesse_bedrock_access'
            
            with patch.object(AWSSessionManager, '_profile_exists', side_effect=mock_profile_exists):
                manager = AWSSessionManager()
                profile = await manager.get_profile_name()
                assert profile == 'jesse_bedrock_access'
    
    @pytest.mark.asyncio
    async def test_profile_detection_default_fallback(self):
        """Test profile detection fallback to default profile"""
        with patch.dict(os.environ, {}, clear=True):
            async def mock_profile_exists(profile_name):
                return profile_name == 'default'
            
            with patch.object(AWSSessionManager, '_profile_exists', side_effect=mock_profile_exists):
                manager = AWSSessionManager()
                profile = await manager.get_profile_name()
                assert profile == 'default'
    
    @pytest.mark.asyncio
    async def test_profile_detection_none_for_env_credentials(self):
        """Test profile detection returns None when no profiles exist (env credentials)"""
        with patch.dict(os.environ, {}, clear=True):
            with patch.object(AWSSessionManager, '_profile_exists', return_value=False):
                manager = AWSSessionManager()
                profile = await manager.get_profile_name()
                assert profile is None
    
    @pytest.mark.asyncio
    async def test_env_credentials_detection(self):
        """Test environment credentials detection"""
        manager = AWSSessionManager()
        
        # Test with both required env vars
        with patch.dict(os.environ, {
            'AWS_ACCESS_KEY_ID': 'test-key',
            'AWS_SECRET_ACCESS_KEY': 'test-secret'
        }):
            assert manager._has_env_credentials() is True
        
        # Test with missing secret key
        with patch.dict(os.environ, {'AWS_ACCESS_KEY_ID': 'test-key'}, clear=True):
            assert manager._has_env_credentials() is False
        
        # Test with no env vars
        with patch.dict(os.environ, {}, clear=True):
            assert manager._has_env_credentials() is False
    
    @pytest.mark.asyncio
    async def test_credential_detection_hierarchy(self):
        """Test complete credential detection hierarchy"""
        ctx = MockFastMCPContext()
        manager = AWSSessionManager()
        
        # Test environment credentials (highest priority)
        with patch.dict(os.environ, {
            'AWS_ACCESS_KEY_ID': 'test-key',
            'AWS_SECRET_ACCESS_KEY': 'test-secret'
        }):
            credential_info = await manager._detect_credentials(ctx)
            assert credential_info.credential_source == 'env_vars'
            assert credential_info.has_env_credentials is True
            assert credential_info.profile_name is None
    
    @pytest.mark.asyncio
    async def test_credential_detection_no_credentials_failure(self):
        """Test credential detection failure when no credentials found"""
        ctx = MockFastMCPContext()
        manager = AWSSessionManager()
        
        with patch.dict(os.environ, {}, clear=True):
            with patch.object(manager, '_has_env_credentials', return_value=False):
                with patch.object(manager, '_profile_exists', return_value=False):
                    with pytest.raises(AWSConfigurationError) as exc_info:
                        await manager._detect_credentials(ctx)
                    
                    assert "No valid AWS credentials found" in str(exc_info.value)
    
    @pytest.mark.asyncio
    async def test_connection_validation_success(self):
        """Test successful AWS connection validation"""
        ctx = MockFastMCPContext()
        manager = AWSSessionManager()
        
        # Mock successful STS call
        mock_caller_identity = {
            'Account': '123456789012',
            'Arn': 'arn:aws:iam::123456789012:user/test-user',
            'UserId': 'AIDATEST123456789'
        }
        
        with patch.object(manager, '_detect_credentials') as mock_detect_creds:
            mock_detect_creds.return_value = AWSCredentialInfo(
                has_env_credentials=True,
                profile_name=None,
                credential_source='env_vars',
                profile_path=None
            )
            
            with patch.object(manager, 'get_region', return_value='us-east-1'):
                with patch.object(manager, '_create_boto3_session') as mock_create_session:
                    mock_session = MagicMock()
                    mock_sts_client = MagicMock()
                    mock_sts_client.get_caller_identity.return_value = mock_caller_identity
                    mock_session.client.return_value = mock_sts_client
                    mock_create_session.return_value = mock_session
                    
                    connection_info = await manager.validate_connection_once(ctx)
                    
                    assert connection_info.region == 'us-east-1'
                    assert connection_info.credential_source == 'env_vars'
                    assert connection_info.account_id == '123456789012'
                    assert connection_info.connection_validated is True
    
    @pytest.mark.asyncio
    async def test_connection_validation_failure(self):
        """Test AWS connection validation failure"""
        ctx = MockFastMCPContext()
        manager = AWSSessionManager()
        
        with patch.object(manager, '_detect_credentials') as mock_detect_creds:
            mock_detect_creds.return_value = AWSCredentialInfo(
                has_env_credentials=True,
                profile_name=None,
                credential_source='env_vars',
                profile_path=None
            )
            
            with patch.object(manager, 'get_region', return_value='us-east-1'):
                with patch.object(manager, '_create_boto3_session') as mock_create_session:
                    mock_session = MagicMock()
                    mock_sts_client = MagicMock()
                    mock_sts_client.get_caller_identity.side_effect = Exception("Access Denied")
                    mock_session.client.return_value = mock_sts_client
                    mock_create_session.return_value = mock_session
                    
                    with pytest.raises(AWSConnectionError) as exc_info:
                        await manager.validate_connection_once(ctx)
                    
                    assert "Unexpected AWS validation error" in str(exc_info.value)
    
    @pytest.mark.asyncio
    async def test_singleton_validation_once(self):
        """Test that connection validation only happens once per singleton instance"""
        ctx = MockFastMCPContext()
        manager = AWSSessionManager()
        
        # Mock successful validation
        mock_connection_info = AWSConnectionInfo(
            region='us-east-1',
            profile_used=None,
            credential_source='env_vars',
            caller_identity={'Account': '123456789012', 'Arn': 'test-arn'},
            account_id='123456789012',
            user_arn='test-arn',
            connection_validated=True
        )
        
        with patch.object(manager, '_detect_credentials') as mock_detect_creds:
            with patch.object(manager, 'get_region', return_value='us-east-1'):
                with patch.object(manager, '_create_boto3_session') as mock_create_session:
                    mock_session = MagicMock()
                    mock_sts_client = MagicMock()
                    mock_sts_client.get_caller_identity.return_value = {
                        'Account': '123456789012',
                        'Arn': 'test-arn',
                        'UserId': 'test-user'
                    }
                    mock_session.client.return_value = mock_sts_client
                    mock_create_session.return_value = mock_session
                    mock_detect_creds.return_value = AWSCredentialInfo(
                        has_env_credentials=True,
                        profile_name=None,
                        credential_source='env_vars',
                        profile_path=None
                    )
                    
                    # First call should perform validation
                    result1 = await manager.validate_connection_once(ctx)
                    
                    # Second call should return cached result without validation
                    result2 = await manager.validate_connection_once(ctx)
                    
                    # Should be the same object
                    assert result1 is result2
                    
                    # STS should only be called once
                    assert mock_sts_client.get_caller_identity.call_count == 1


class TestStrandsIntegration:
    """Test suite for AWS session manager integration with Strands Agent driver"""
    
    def setup_method(self):
        """Reset singleton state before each test"""
        AWSSessionManager._instance = None
        AWSSessionManager._initialized = False
        AWSSessionManager._validation_result = None
    
    @pytest.mark.asyncio
    async def test_claude_config_async_aws_integration(self):
        """Test Claude4SonnetConfig async AWS integration"""
        config = Claude4SonnetConfig()
        
        # Mock AWS session manager
        mock_aws_config = {
            'region': 'us-west-2',
            'profile': 'jesse_bedrock_access',
            'boto3_session': MagicMock(),
            'account_id': '123456789012',
            'user_arn': 'test-arn',
            'credential_source': 'jesse_profile',
            'caller_identity': {'Account': '123456789012'}
        }
        
        with patch.object(AWSSessionManager, 'get_aws_config', return_value=mock_aws_config):
            kwargs = await config.to_strands_model_kwargs_async()
            
            assert kwargs['region'] == 'us-west-2'
            assert kwargs['profile'] == 'jesse_bedrock_access'
            assert kwargs['model_id'] == config.model_id
            assert kwargs['temperature'] == config.temperature
    
    @pytest.mark.asyncio
    async def test_claude_config_async_env_credentials(self):
        """Test Claude4SonnetConfig async integration with environment credentials"""
        config = Claude4SonnetConfig()
        
        # Mock AWS session manager with no profile (env credentials)
        mock_aws_config = {
            'region': 'eu-west-1',
            'profile': None,  # Environment credentials
            'boto3_session': MagicMock(),
            'account_id': '123456789012',
            'user_arn': 'test-arn',
            'credential_source': 'env_vars',
            'caller_identity': {'Account': '123456789012'}
        }
        
        with patch.object(AWSSessionManager, 'get_aws_config', return_value=mock_aws_config):
            kwargs = await config.to_strands_model_kwargs_async()
            
            assert kwargs['region'] == 'eu-west-1'
            assert 'profile' not in kwargs  # Should not include profile for env credentials
            assert kwargs['model_id'] == config.model_id
    
    @pytest.mark.asyncio
    async def test_claude_config_legacy_fallback(self):
        """Test Claude4SonnetConfig legacy method still works"""
        config = Claude4SonnetConfig()
        
        with patch.dict(os.environ, {
            'AWS_REGION': 'ap-south-1',
            'AWS_PROFILE': 'test-profile'
        }):
            kwargs = config.to_strands_model_kwargs()
            
            assert kwargs['region'] == 'ap-south-1'
            assert kwargs['profile'] == 'test-profile'
            assert kwargs['model_id'] == config.model_id


def main():
    """Run tests directly"""
    print("Running AWS Session Manager Tests...")
    
    # Run tests using pytest
    exit_code = pytest.main([
        __file__,
        '-v',
        '--tb=short',
        '--disable-warnings'
    ])
    
    return exit_code


if __name__ == "__main__":
    exit(main())
