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
# Pure AWS session management providing centralized credential detection,
# region resolution, and connection validation for the entire MCP server.
# Completely independent of any specific AWS service integrations.
###############################################################################
# [Source file design principles]
# - Pure AWS session management with no service-specific knowledge
# - Singleton pattern with one-time startup validation
# - Hierarchical credential and region detection following AWS standards
# - Clean separation of concerns - only AWS primitives, no Strands/Bedrock knowledge
# - Comprehensive error handling with descriptive failure messages
###############################################################################
# [Source file constraints]
# - Must support AWS credential hierarchy: env vars → jesse_bedrock_access → default → fail
# - Region detection: AWS_REGION → AWS_DEFAULT_REGION → ~/.aws/config → fail
# - One-time connection validation per program lifetime using STS get-caller-identity
# - Must provide generic AWS configuration consumable by any AWS service integration
###############################################################################
# [Dependencies]
# system:boto3 - AWS SDK for Python session management and STS operations
# system:configparser - INI file parsing for ~/.aws/config
# system:pathlib.Path - Cross-platform filesystem operations
# system:os - Environment variable access
# system:asyncio - Async operations support
# system:typing - Type annotations
# system:dataclasses - Configuration data models
# codebase:fastmcp.Context - FastMCP Context for async logging operations
###############################################################################
# [GenAI tool change history]
# 2025-07-08T14:54:50Z : Initial AWS session manager implementation by CodeAssistant
# * Created pure AWS session management layer with no service-specific dependencies
# * Implemented hierarchical credential detection (env vars → jesse_bedrock_access → default)
# * Added comprehensive region resolution (AWS_REGION → AWS_DEFAULT_REGION → ~/.aws/config)
# * Singleton pattern with one-time STS connection validation
###############################################################################

import asyncio
import os
import boto3
from botocore.exceptions import ClientError, NoCredentialsError, ProfileNotFound
from configparser import ConfigParser
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Any, Optional, Tuple
import logging

from fastmcp import Context

logger = logging.getLogger(__name__)


class AWSConfigurationError(Exception):
    """Raised when AWS configuration is invalid or incomplete"""
    pass


class AWSConnectionError(Exception):
    """Raised when AWS connection validation fails"""
    pass


@dataclass
class AWSConnectionInfo:
    """Pure AWS connection information"""
    region: str
    profile_used: Optional[str]
    credential_source: str  # "env_vars" | "jesse_profile" | "default_profile"
    caller_identity: Dict[str, Any]
    account_id: str
    user_arn: str
    connection_validated: bool


@dataclass
class AWSCredentialInfo:
    """AWS credential detection results"""
    has_env_credentials: bool
    profile_name: Optional[str]
    credential_source: str
    profile_path: Optional[str]


class AWSSessionManager:
    """
    [Class intent]
    Singleton AWS session manager providing pure AWS operations with no service-specific knowledge.
    Handles credential detection, region resolution, and connection validation for the entire MCP server.
    
    [Design principles]
    Singleton pattern ensures one-time connection validation per program lifetime.
    Clean separation of AWS primitives from service integrations (Strands, Bedrock, etc).
    Hierarchical credential and region detection following AWS standard practices.
    
    [Implementation details]
    Uses boto3 sessions for AWS operations and STS get-caller-identity for validation.
    Caches validation results to avoid repeated STS calls during program lifetime.
    Provides generic AWS configuration consumable by any AWS service integration.
    """
    
    _instance: Optional['AWSSessionManager'] = None
    _initialized: bool = False
    _validation_result: Optional[AWSConnectionInfo] = None
    _lock = asyncio.Lock()
    
    def __new__(cls) -> 'AWSSessionManager':
        """
        [Class method intent]
        Ensure singleton instance creation for consistent AWS session management.
        
        [Design principles]
        Singleton pattern prevents multiple AWS validation attempts during program lifetime.
        
        [Implementation details]
        Creates single instance stored in class variable, returns same instance on subsequent calls.
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    async def validate_connection_once(self, ctx: Context) -> AWSConnectionInfo:
        """
        [Function intent]
        Perform one-time AWS connection validation using STS get-caller-identity with comprehensive error handling.
        
        [Design principles]
        Single validation per program lifetime to avoid repeated expensive STS calls.
        Comprehensive credential and region detection with clear error reporting.
        
        [Implementation details]
        Uses asyncio lock to prevent concurrent validation attempts.
        Caches successful validation results for subsequent access.
        Raises descriptive errors for configuration or connection failures.
        
        Args:
            ctx: FastMCP Context for logging and progress reporting
            
        Returns:
            AWSConnectionInfo with validated connection details
            
        Raises:
            AWSConnectionError: When connection validation fails
            AWSConfigurationError: When AWS configuration is invalid
        """
        if self._initialized:
            if self._validation_result is None:
                raise AWSConnectionError("AWS connection validation failed at startup")
            return self._validation_result
        
        async with self._lock:
            if self._initialized:
                if self._validation_result is None:
                    raise AWSConnectionError("AWS connection validation failed at startup")
                return self._validation_result
            
            try:
                await ctx.info("Validating AWS connection (one-time startup check)...")
                
                # Detect credentials and region using hierarchical approach
                credential_info = await self._detect_credentials(ctx)
                region = await self.get_region()
                
                await ctx.info(f"Using AWS region: {region}")
                await ctx.info(f"Using credential source: {credential_info.credential_source}")
                if credential_info.profile_name:
                    await ctx.info(f"Using AWS profile: {credential_info.profile_name}")
                
                # Create session and test connectivity
                session = await self._create_boto3_session(region, credential_info.profile_name)
                sts_client = session.client('sts')
                
                # Perform STS get-caller-identity test
                await ctx.info("Testing AWS connectivity with STS get-caller-identity...")
                caller_identity = sts_client.get_caller_identity()
                
                # Cache successful result
                self._validation_result = AWSConnectionInfo(
                    region=region,
                    profile_used=credential_info.profile_name,
                    credential_source=credential_info.credential_source,
                    caller_identity=caller_identity,
                    account_id=caller_identity['Account'],
                    user_arn=caller_identity['Arn'],
                    connection_validated=True
                )
                
                await ctx.info(f"✅ AWS connection validated successfully")
                await ctx.info(f"   Account: {caller_identity['Account']}")
                await ctx.info(f"   User/Role: {caller_identity['Arn']}")
                await ctx.info(f"   Region: {region}")
                await ctx.info(f"   Credential Source: {credential_info.credential_source}")
                
            except (NoCredentialsError, ClientError) as e:
                error_msg = f"AWS authentication failed: {str(e)}"
                await ctx.error(error_msg)
                self._validation_result = None
                raise AWSConnectionError(error_msg) from e
            
            except AWSConfigurationError as e:
                await ctx.error(f"AWS configuration error: {str(e)}")
                self._validation_result = None
                raise
            
            except Exception as e:
                error_msg = f"Unexpected AWS validation error: {str(e)}"
                await ctx.error(error_msg)
                self._validation_result = None
                raise AWSConnectionError(error_msg) from e
            
            finally:
                self._initialized = True
            
            return self._validation_result
    
    async def get_region(self) -> str:
        """
        [Function intent]
        Detect AWS region using standard AWS resolution hierarchy with comprehensive fallback logic.
        
        [Design principles]
        Follows AWS standard region detection order without hard-coded fallbacks.
        Provides clear error messages when no region configuration is found.
        
        [Implementation details]
        Checks AWS_REGION, AWS_DEFAULT_REGION environment variables, then parses ~/.aws/config.
        Raises descriptive error if no region found rather than using hard-coded fallback.
        
        Returns:
            Detected AWS region string
            
        Raises:
            AWSConfigurationError: When no region found in environment or AWS config
        """
        # 1. AWS_REGION environment variable (highest priority)
        if region := os.getenv("AWS_REGION"):
            logger.debug(f"Using region from AWS_REGION: {region}")
            return region
        
        # 2. AWS_DEFAULT_REGION environment variable
        if region := os.getenv("AWS_DEFAULT_REGION"):
            logger.debug(f"Using region from AWS_DEFAULT_REGION: {region}")
            return region
        
        # 3. Parse ~/.aws/config [default] section
        try:
            if region := await self._parse_config_default_region():
                logger.debug(f"Using region from ~/.aws/config: {region}")
                return region
        except Exception as e:
            logger.debug(f"Failed to parse ~/.aws/config for region: {e}")
        
        # 4. No region found - fail with descriptive error
        raise AWSConfigurationError(
            "No AWS region found. Please set AWS_REGION environment variable or configure region in ~/.aws/config [default] section"
        )
    
    async def get_profile_name(self) -> Optional[str]:
        """
        [Function intent]
        Detect AWS profile using hierarchical preference with jesse_bedrock_access as preferred default.
        
        [Design principles]
        Environment variable override takes precedence, followed by preferred profile, then AWS standard default.
        Returns None when using environment credentials rather than profile-based authentication.
        
        [Implementation details]
        Checks AWS_PROFILE environment variable, then jesse_bedrock_access profile, then default profile.
        Validates profile existence before returning profile name.
        
        Returns:
            AWS profile name if using profile-based credentials, None for environment credentials
        """
        # 1. AWS_PROFILE environment variable (explicit user override)
        if profile := os.getenv("AWS_PROFILE"):
            if await self._profile_exists(profile):
                logger.debug(f"Using profile from AWS_PROFILE: {profile}")
                return profile
            else:
                logger.warning(f"AWS_PROFILE profile '{profile}' not found, falling back to detection")
        
        # 2. jesse_bedrock_access profile (preferred default)
        if await self._profile_exists("jesse_bedrock_access"):
            logger.debug("Using preferred profile: jesse_bedrock_access")
            return "jesse_bedrock_access"
        
        # 3. default profile (AWS standard)
        if await self._profile_exists("default"):
            logger.debug("Using standard default profile")
            return "default"
        
        # 4. No profile available - assume environment credentials
        logger.debug("No AWS profile found, assuming environment credentials")
        return None
    
    async def get_boto3_session(self) -> boto3.Session:
        """
        [Function intent]
        Create validated boto3 session using detected AWS configuration for direct AWS service access.
        
        [Design principles]
        Ensures connection validation has been performed before providing session.
        Uses detected region and profile configuration consistently.
        
        [Implementation details]
        Requires prior connection validation to ensure session will work.
        Creates session with detected profile and region configuration.
        
        Returns:
            Configured and validated boto3.Session instance
            
        Raises:
            AWSConnectionError: When connection not validated or session creation fails
        """
        if not self._initialized or self._validation_result is None:
            raise AWSConnectionError("AWS connection must be validated before creating session")
        
        try:
            region = self._validation_result.region
            profile = self._validation_result.profile_used
            
            return await self._create_boto3_session(region, profile)
        except Exception as e:
            raise AWSConnectionError(f"Failed to create boto3 session: {e}") from e
    
    async def get_caller_identity(self) -> Dict[str, Any]:
        """
        [Function intent]
        Get cached AWS caller identity information from previous validation without additional STS calls.
        
        [Design principles]
        Returns cached identity information to avoid repeated expensive STS operations.
        Provides account and user details for logging and debugging purposes.
        
        [Implementation details]
        Returns cached caller identity from initial connection validation.
        Includes Account ID, ARN, and User ID from STS get-caller-identity response.
        
        Returns:
            Dictionary containing STS caller identity information
            
        Raises:
            AWSConnectionError: When connection not validated
        """
        if not self._initialized or self._validation_result is None:
            raise AWSConnectionError("AWS connection must be validated before accessing caller identity")
        
        return self._validation_result.caller_identity
    
    async def get_aws_config(self) -> Dict[str, Any]:
        """
        [Function intent]
        Get comprehensive AWS configuration suitable for any AWS service integration with all validation details.
        
        [Design principles]
        Provides generic AWS configuration that any AWS service consumer can use.
        Includes both configuration details and ready-to-use boto3 session.
        
        [Implementation details]
        Returns dictionary with region, profile, session, and identity information.
        All values are from validated connection, ensuring they work correctly.
        
        Returns:
            Dictionary containing comprehensive AWS configuration
            
        Raises:
            AWSConnectionError: When connection not validated
        """
        if not self._initialized or self._validation_result is None:
            raise AWSConnectionError("AWS connection must be validated before accessing configuration")
        
        return {
            "region": self._validation_result.region,
            "profile": self._validation_result.profile_used,
            "boto3_session": await self.get_boto3_session(),
            "account_id": self._validation_result.account_id,
            "user_arn": self._validation_result.user_arn,
            "credential_source": self._validation_result.credential_source,
            "caller_identity": self._validation_result.caller_identity
        }
    
    # Private helper methods
    
    async def _detect_credentials(self, ctx: Context) -> AWSCredentialInfo:
        """
        [Function intent]
        Detect AWS credentials using hierarchical approach with comprehensive source tracking.
        
        [Design principles]
        Follows credential hierarchy: environment variables, jesse_bedrock_access profile, default profile.
        Provides clear source tracking for debugging and logging purposes.
        
        [Implementation details]
        Checks for environment credentials first, then preferred profile, then default profile.
        Returns comprehensive credential information including source and profile details.
        
        Args:
            ctx: FastMCP Context for logging
            
        Returns:
            AWSCredentialInfo with detected credential details
            
        Raises:
            AWSConfigurationError: When no valid credentials found
        """
        # 1. Environment variables (highest priority)
        if self._has_env_credentials():
            await ctx.info("Using AWS credentials from environment variables")
            return AWSCredentialInfo(
                has_env_credentials=True,
                profile_name=None,
                credential_source="env_vars",
                profile_path=None
            )
        
        # 2. jesse_bedrock_access profile (preferred default)
        if await self._profile_exists("jesse_bedrock_access"):
            await ctx.info("Using AWS profile: jesse_bedrock_access")
            return AWSCredentialInfo(
                has_env_credentials=False,
                profile_name="jesse_bedrock_access",
                credential_source="jesse_profile",
                profile_path=str(Path.home() / ".aws" / "credentials")
            )
        
        # 3. default profile (AWS standard)
        if await self._profile_exists("default"):
            await ctx.info("Using AWS profile: default")
            return AWSCredentialInfo(
                has_env_credentials=False,
                profile_name="default",
                credential_source="default_profile",
                profile_path=str(Path.home() / ".aws" / "credentials")
            )
        
        # 4. No credentials found
        raise AWSConfigurationError(
            "No valid AWS credentials found. Please either:\n"
            "1. Set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables, OR\n"
            "2. Configure 'jesse_bedrock_access' AWS profile, OR\n"
            "3. Configure 'default' AWS profile"
        )
    
    def _has_env_credentials(self) -> bool:
        """
        [Function intent]
        Check if AWS credentials are available in environment variables for credential detection.
        
        [Design principles]
        Simple boolean check for environment credential availability.
        Does not validate credential correctness, only presence.
        
        [Implementation details]
        Checks for required AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables.
        AWS_SESSION_TOKEN is optional for temporary credentials.
        
        Returns:
            True if environment credentials are present, False otherwise
        """
        return bool(
            os.getenv("AWS_ACCESS_KEY_ID") and 
            os.getenv("AWS_SECRET_ACCESS_KEY")
        )
    
    async def _profile_exists(self, profile_name: str) -> bool:
        """
        [Function intent]
        Check if AWS profile exists in credentials or config files for profile validation.
        
        [Design principles]
        Validates profile existence without attempting to use credentials.
        Checks both ~/.aws/credentials and ~/.aws/config locations.
        
        [Implementation details]
        Uses boto3 Session to attempt profile loading and catches ProfileNotFound exception.
        Provides safe profile existence check without credential validation.
        
        Args:
            profile_name: AWS profile name to check
            
        Returns:
            True if profile exists, False otherwise
        """
        try:
            # Attempt to create session with profile to test existence
            boto3.Session(profile_name=profile_name)
            return True
        except ProfileNotFound:
            return False
        except Exception:
            # Other exceptions might indicate profile exists but has issues
            return True
    
    async def _parse_config_default_region(self) -> Optional[str]:
        """
        [Function intent]
        Parse ~/.aws/config file to extract default region configuration following AWS config format.
        
        [Design principles]
        Handles AWS config file parsing robustly with proper error handling.
        Returns None rather than raising exceptions for missing files or sections.
        
        [Implementation details]
        Uses ConfigParser to parse INI-style AWS config file format.
        Looks for [default] section and extracts region value.
        
        Returns:
            Region string from [default] section, or None if not found
        """
        config_path = Path.home() / ".aws" / "config"
        
        if not config_path.exists():
            logger.debug("~/.aws/config file not found")
            return None
        
        try:
            config = ConfigParser()
            config.read(config_path)
            
            # Check [default] section for region
            if config.has_section('default') and config.has_option('default', 'region'):
                region = config.get('default', 'region').strip()
                if region:
                    return region
            
            logger.debug("No region found in ~/.aws/config [default] section")
            return None
            
        except Exception as e:
            logger.debug(f"Failed to parse ~/.aws/config: {e}")
            return None
    
    async def _create_boto3_session(self, region: str, profile: Optional[str]) -> boto3.Session:
        """
        [Function intent]
        Create boto3 session with specified region and optional profile for AWS service access.
        
        [Design principles]
        Centralizes boto3 session creation with consistent configuration.
        Handles both profile-based and environment credential scenarios.
        
        [Implementation details]
        Creates session with profile if specified, otherwise uses environment credentials.
        Always sets region_name for consistent regional operations.
        
        Args:
            region: AWS region for session
            profile: Optional AWS profile name
            
        Returns:
            Configured boto3.Session instance
            
        Raises:
            Exception: When session creation fails
        """
        if profile:
            return boto3.Session(profile_name=profile, region_name=region)
        else:
            return boto3.Session(region_name=region)
