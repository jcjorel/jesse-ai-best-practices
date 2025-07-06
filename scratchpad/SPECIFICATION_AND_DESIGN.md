# Entity Relationship Mapping Indexing System - Specification & Design

## Document Information
- **Version**: 1.0.0
- **Date**: 2025-07-05
- **Author**: AI Assistant  
- **Status**: Design Phase
- **Scope**: Standalone indexing system with single integration test (no MCP server integration)
- **Complexity**: High - Advanced LLM integration with external context resolution

## Table of Contents
1. [Executive Summary](#1-executive-summary)
2. [Requirements](#2-requirements)
3. [System Architecture](#3-system-architecture)
4. [Detailed Component Design](#4-detailed-component-design)
5. [Data Models](#5-data-models)
6. [Processing Algorithms](#6-processing-algorithms)
7. [LLM Prompt Engineering](#7-llm-prompt-engineering)
8. [YAML Output Specification](#8-yaml-output-specification)
9. [Relationship Taxonomies](#9-relationship-taxonomies)
10. [Configuration System](#10-configuration-system)
11. [Integration Patterns](#11-integration-patterns)
12. [Implementation Plan](#12-implementation-plan)
13. [Success Criteria](#13-success-criteria)
14. [Risks and Mitigation](#14-risks-and-mitigation)

## 1. Executive Summary

This document provides a comprehensive specification for a semantic entity relationship mapping indexing engine that complements the existing knowledge indexing system. The engine performs deep analysis of source files to discover semantic entities (classes, functions, variables, concepts) and maps their relationships with precision, generating concatenable YAML files for comprehensive project analysis and cross-reference resolution.

### 1.1 Key Capabilities
- **Entity Discovery**: Advanced LLM-powered extraction of semantic entities from both code and documentation files
- **Relationship Mapping**: Precise identification and categorization of direct relationships between entities
- **External Context Resolution**: LLM-driven file path suggestion with simple file reading for dependency context
- **Concatenable Output**: YAML files designed for seamless concatenation without semantic loss
- **Taxonomy-Driven Analysis**: Specialized relationship taxonomies for code vs document analysis

### 1.2 Technical Approach
- **Architecture**: Modular design following proven patterns from existing knowledge indexing system
- **Processing**: Sequential processing with sophisticated error handling (no concurrent processing)
- **LLM Integration**: Single conversation per file with Claude 4 Sonnet via strands_agent_driver
- **Output Format**: Multi-document YAML streams with globally unique entity identifiers
- **Performance**: Sequential processing with no caching for implementation simplicity

## 2. Requirements

### 2.1 Functional Requirements

**FR-001**: Entity Discovery
- Extract semantic entities from source files (classes, functions, variables, concepts)
- Support both code files and document files
- Generate unique identifiers for each entity

**FR-002**: Relationship Mapping
- Identify direct relationships between entities (no transitive dependencies)
- Categorize relationships by type (imports, calls, inherits, references, etc.)
- Map both internal (within-file) and external (cross-file) relationships

**FR-003**: External Context Resolution
- Use LLM to suggest likely file paths for external dependencies
- Attempt to read suggested file paths in order of likelihood until finding a match
- Provide contextual information for resolved external file relationships

**FR-004**: YAML Output Generation
- Generate `.erm.yaml` files alongside existing `.analysis.md` files
- Ensure YAML files are concatenable without semantic loss
- Use globally unique entity identifiers to prevent conflicts

**FR-005**: Integration with Existing System
- Mirror the architecture patterns of the existing knowledge indexing system
- Use same discovery, filtering, and orchestration patterns
- Maintain separate configuration system

### 2.2 Non-Functional Requirements

**NFR-001**: Performance
- Process files sequentially for simplicity (no concurrent processing)
- No caching implementation for simplicity (acknowledged slower performance)

**NFR-002**: Maintainability
- Follow existing code patterns and conventions
- Use modular architecture with clear separation of concerns

**NFR-003**: Reliability
- Handle errors gracefully with detailed logging
- Continue processing when individual files fail

## 3. System Architecture

### 3.1 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                Entity Relationship Mapping System          │
├─────────────────────────────────────────────────────────────┤
│  EntityRelationshipIndexer (Main Orchestrator)             │
│  ├─ Discovery Phase                                         │
│  ├─ Entity Analysis Phase                                   │
│  ├─ Relationship Mapping Phase                              │
│  ├─ External Resolution Phase                               │
│  └─ YAML Generation Phase                                   │
├─────────────────────────────────────────────────────────────┤
│  EntityRelationshipBuilder (LLM Integration)               │
│  ├─ Entity Extraction                                       │
│  ├─ Relationship Discovery                                  │
│  └─ Context Integration                                     │  
├─────────────────────────────────────────────────────────────┤
│  ExternalDependencyResolver (LLM-Driven File Resolution)   │
│  ├─ LLM Path Suggestion                                     │
│  ├─ Sequential File Reading                                 │
│  └─ Context Extraction                                      │
├─────────────────────────────────────────────────────────────┤
│  YAML Generator (Output Formatting)                        │
│  ├─ Concatenable Structure                                  │
│  ├─ Unique ID Generation                                    │
│  └─ Multi-Document Format                                   │
└─────────────────────────────────────────────────────────────┘
```

### 3.2 Directory Structure

```
jesse-framework-mcp/jesse_framework_mcp/knowledge_bases/entity_relationship_mapping/
├── __init__.py
├── entity_relationship_indexer.py      # Main orchestrator
├── entity_relationship_builder.py      # LLM-powered analysis
├── entity_relationship_prompts.py      # Specialized prompts
├── entity_relationship_config.py       # Configuration system
├── external_dependency_resolver.py     # Strands agent integration
├── yaml_generator.py                   # YAML output formatting
├── models/
│   ├── __init__.py
│   ├── entity_models.py                # Entity data structures
│   ├── relationship_models.py          # Relationship data structures
│   └── erm_context.py                  # Processing context models
├── taxonomies/
│   ├── __init__.py
│   ├── code_relationships.py           # Code relationship taxonomy
│   └── document_relationships.py       # Document relationship taxonomy
└── tools/
    ├── __init__.py
    ├── file_reader.py                  # Simple file reading (no LLM)
    └── dependency_resolver.py          # LLM-suggested path resolution (no LLM)
```

### 3.3 Core Components

#### 3.3.1 EntityRelationshipIndexer
- **Purpose**: Main orchestrator following sequential processing strategy
- **Responsibilities**:
  - File discovery and filtering
  - Sequential processing coordination
  - Progress reporting via FastMCP Context
  - Error handling and statistics

#### 3.3.2 EntityRelationshipBuilder
- **Purpose**: LLM-powered entity and relationship discovery
- **Responsibilities**:
  - Entity extraction from file content
  - Relationship mapping and categorization
  - Integration with external context resolution
  - YAML structure preparation

#### 3.3.3 EntityRelationshipPrompts
- **Purpose**: Specialized prompts for entity/relationship analysis
- **Responsibilities**:
  - Entity discovery prompts (differentiated by file type)
  - Relationship mapping prompts
  - External context resolution prompts
  - YAML output format specifications

#### 3.3.4 ExternalDependencyResolver
- **Purpose**: LLM-driven file path resolution for external context
- **Responsibilities**:
  - Receive LLM-suggested file paths for dependencies
  - Attempt sequential file reading using suggested paths
  - Context extraction from successfully read files
  - Relationship context enrichment

#### 3.3.5 YAMLGenerator
- **Purpose**: Concatenable YAML output generation
- **Responsibilities**:
  - Globally unique entity ID generation
  - Multi-document YAML formatting
  - Cross-reference resolution
  - Validation for concatenation compatibility

## 4. Detailed Component Design

### 4.1 EntityRelationshipIndexer

```python
class EntityRelationshipIndexer:
    """
    Main orchestrator for entity relationship mapping following sequential processing.
    Mirrors HierarchicalIndexer patterns with specialized entity/relationship focus.
    """
    
    def __init__(self, config: EntityRelationshipConfig):
        self.config = config
        self.builder = EntityRelationshipBuilder(config)
        self.external_resolver = ExternalDependencyResolver(config)
        self.yaml_generator = YAMLGenerator(config)
        self._current_status = ERMIndexingStatus()
    
    async def index_entity_relationships(self, root_path: Path, ctx: Context) -> ERMIndexingStatus:
        """
        Main entry point for entity relationship indexing.
        
        Processing Phases:
        1. Discovery: Enumerate files using existing patterns
        2. Analysis: Extract entities and relationships per file
        3. Resolution: Resolve external dependencies for context
        4. Generation: Create concatenable YAML outputs
        5. Validation: Ensure output quality and consistency
        """
        
    async def _discover_files(self, root_path: Path, ctx: Context) -> List[ERMFileContext]:
        """Discover and filter files for entity relationship analysis"""
        
    async def _process_files_sequentially(self, file_contexts: List[ERMFileContext], ctx: Context) -> List[ERMFileContext]:
        """Process files one by one sequentially"""
        
    async def _generate_outputs(self, processed_contexts: List[ERMFileContext], ctx: Context) -> None:
        """Generate YAML output files for processed contexts"""
```

### 4.2 EntityRelationshipBuilder

```python
class EntityRelationshipBuilder:
    """
    LLM-powered entity and relationship discovery engine.
    Integrates with Claude 4 Sonnet via strands_agent_driver.
    """
    
    def __init__(self, config: EntityRelationshipConfig):
        self.config = config
        self.llm_driver: Optional[StrandsClaude4Driver] = None
        self.prompts = EntityRelationshipPrompts()
        self.dependency_resolver = DependencyResolverTool()  # Simple data access
        
    async def build_entity_relationships(self, file_context: ERMFileContext, ctx: Context) -> ERMFileContext:
        """
        Single conversation workflow for complete file analysis.
        Uses one LLM conversation session per file to handle all phases:
        1. Entity Discovery: Extract semantic entities from file content
        2. Relationship Mapping: Identify internal and external relationships
        3. Context Resolution: Resolve external dependencies via Strands Agent
        4. Validation: Ensure entity/relationship consistency
        5. YAML Generation: Prepare final output structure
        """
        
        # Initialize single conversation session for this file
        if not self.llm_driver:
            self.llm_driver = StrandsClaude4Driver()
        
        # Start conversation with entity discovery
        conversation_id = await self._start_conversation_session(file_context, ctx)
        
        try:
            # Phase 1: Entity extraction within conversation
            entities = await self._extract_entities_in_conversation(conversation_id, file_context, ctx)
            file_context.entities = entities
            
            # Phase 2: Relationship mapping within same conversation
            internal_rels, external_rels = await self._map_relationships_in_conversation(
                conversation_id, entities, file_context, ctx
            )
            file_context.internal_relationships = internal_rels
            file_context.external_relationships = external_rels
            
            # Phase 3: External context resolution within same conversation
            resolved_external_rels = await self._resolve_external_context_in_conversation(
                conversation_id, external_rels, file_context.project_root, ctx
            )
            file_context.external_relationships = resolved_external_rels
            
            # Phase 4: Final validation and cleanup within conversation
            await self._validate_results_in_conversation(conversation_id, file_context, ctx)
            
        except Exception as e:
            await ctx.error(f"Conversation session failed for {file_context.file_path}: {e}")
            file_context.add_error(f"Conversation session error: {str(e)}")
        finally:
            # Always close the conversation session
            await self._close_conversation_session(conversation_id, ctx)
        
        return file_context
        
    async def _start_conversation_session(self, file_context: ERMFileContext, ctx: Context) -> str:
        """Start a new conversation session for file analysis"""
        initial_prompt = self.prompts.get_conversation_start_prompt(
            file_context.file_path, 
            file_context.file_type, 
            file_context.language
        )
        
        conversation = await self.llm_driver.start_conversation(initial_prompt)
        await ctx.info(f"Started LLM conversation session for {file_context.relative_path}")
        return conversation.conversation_id
        
    async def _extract_entities_in_conversation(self, conversation_id: str, file_context: ERMFileContext, ctx: Context) -> List[Entity]:
        """Extract entities within the existing conversation session"""
        with open(file_context.file_path, 'r', encoding='utf-8') as f:
            file_content = f.read()
            
        entity_prompt = self.prompts.get_entity_discovery_prompt(
            file_context.file_path, file_content, file_context.file_type, file_context.language
        )
        
        response = await self.llm_driver.continue_conversation(conversation_id, entity_prompt)
        entities = self.prompts.parse_entity_response(response.content, file_context)
        
        await ctx.info(f"Extracted {len(entities)} entities from {file_context.relative_path}")
        return entities
        
    async def _map_relationships_in_conversation(self, conversation_id: str, entities: List[Entity], file_context: ERMFileContext, ctx: Context) -> Tuple[List[Relationship], List[Relationship]]:
        """Map relationships within the existing conversation session"""
        with open(file_context.file_path, 'r', encoding='utf-8') as f:
            file_content = f.read()
            
        relationship_prompt = self.prompts.get_relationship_mapping_prompt(
            entities, file_content, file_context
        )
        
        response = await self.llm_driver.continue_conversation(conversation_id, relationship_prompt)
        internal_rels, external_rels = self.prompts.parse_relationship_response(response.content, entities)
        
        await ctx.info(f"Mapped {len(internal_rels)} internal and {len(external_rels)} external relationships")
        return internal_rels, external_rels
        
    async def _resolve_external_context_in_conversation(self, conversation_id: str, relationships: List[Relationship], project_root: Path, ctx: Context) -> List[Relationship]:
        """Resolve external context within the existing conversation session"""
        resolved_relationships = []
        
        for relationship in relationships:
            try:
                # Get raw content via Strands Agent tools (no LLM)
                raw_content = await self.dependency_resolver.get_dependency_content(
                    relationship.target, project_root, ctx
                )
                
                # Use existing conversation to analyze context
                context_prompt = self.prompts.get_context_resolution_prompt(relationship, raw_content)
                response = await self.llm_driver.continue_conversation(conversation_id, context_prompt)
                
                # Create resolved relationship
                resolved_rel = Relationship(
                    source=relationship.source,
                    target=relationship.target,
                    relationship_type=relationship.relationship_type,
                    description=relationship.description,
                    line_number=relationship.line_number,
                    external_context=response.content,
                    resolution_method="file_read"
                )
                resolved_relationships.append(resolved_rel)
                
            except Exception as e:
                # Handle failures gracefully
                failed_rel = Relationship(
                    source=relationship.source,
                    target=relationship.target,
                    relationship_type=relationship.relationship_type,
                    description=relationship.description,
                    external_context=f"Resolution failed: {str(e)}",
                    resolution_method="failed"
                )
                resolved_relationships.append(failed_rel)
                
        return resolved_relationships
        
    async def _validate_results_in_conversation(self, conversation_id: str, file_context: ERMFileContext, ctx: Context) -> None:
        """Validate and finalize results within the conversation session"""
        validation_prompt = self.prompts.get_validation_prompt(file_context)
        response = await self.llm_driver.continue_conversation(conversation_id, validation_prompt)
        
        # Process any validation feedback
        validation_feedback = self.prompts.parse_validation_response(response.content)
        if validation_feedback.warnings:
            for warning in validation_feedback.warnings:
                file_context.add_warning(warning)
        if validation_feedback.errors:
            for error in validation_feedback.errors:
                file_context.add_error(error)
                
    async def _close_conversation_session(self, conversation_id: str, ctx: Context) -> None:
        """Close the conversation session and clean up resources"""
        await self.llm_driver.close_conversation(conversation_id)
        await ctx.info(f"Closed LLM conversation session {conversation_id}")
```

### 4.3 LLM-Driven External Resolution (in tools/ directory)

```python
# tools/file_reader.py
class FileReaderTool:
    """Simple tool for reading raw file content based on LLM-suggested paths"""
    
    async def read_file_content(self, file_path: Path, project_root: Path, ctx: Context) -> str:
        """Read raw file content - no analysis or summarization"""
        try:
            if not file_path.is_absolute():
                file_path = project_root / file_path
                
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
                
        except Exception as e:
            await ctx.warning(f"Failed to read file {file_path}: {e}")
            raise FileNotFoundError(f"Could not read file {file_path}: {str(e)}")

# tools/dependency_resolver.py
class DependencyResolverTool:
    """
    LLM-driven dependency resolution orchestrator.
    
    This tool works with the LLM to resolve external dependencies:
    1. LLM suggests multiple candidate file paths for a dependency
    2. Tool attempts to read each suggested path in order
    3. Returns content of first successfully read file
    4. No hardcoded heuristics - relies entirely on LLM intelligence
    """
    
    def __init__(self):
        self.file_reader = FileReaderTool()
    
    async def get_dependency_content(self, suggested_paths: List[str], project_root: Path, ctx: Context) -> str:
        """
        Attempt to resolve dependency using LLM-suggested file paths.
        
        Args:
            suggested_paths: List of file paths suggested by LLM, ordered by likelihood
            project_root: Project root directory for resolving relative paths
            ctx: FastMCP context for logging
            
        Returns:
            Content of first successfully read file
            
        Raises:
            FileNotFoundError: If none of the suggested paths can be read
        """
        if not suggested_paths:
            raise FileNotFoundError("No file paths suggested by LLM")
        
        last_error = None
        
        for path_candidate in suggested_paths:
            try:
                file_path = Path(path_candidate)
                content = await self.file_reader.read_file_content(file_path, project_root, ctx)
                await ctx.info(f"Successfully resolved dependency using path: {path_candidate}")
                return content
                
            except FileNotFoundError as e:
                last_error = str(e)
                await ctx.debug(f"Failed to read candidate path {path_candidate}: {e}")
                continue
        
        # All paths failed
        error_msg = f"Failed to resolve dependency using any suggested paths: {suggested_paths}. Last error: {last_error}"
        await ctx.warning(error_msg)
        raise FileNotFoundError(error_msg)
    
    async def get_dependency_content_with_single_target(self, dependency_target: str, project_root: Path, ctx: Context) -> str:
        """
        Legacy interface for backward compatibility.
        Treats single dependency target as a single-item suggested paths list.
        
        Args:
            dependency_target: Single dependency target (usually from relationship.target)
            project_root: Project root directory
            ctx: FastMCP context
            
        Returns:
            Content of the file if successfully read
        """
        # For backward compatibility, treat single target as single-item list
        return await self.get_dependency_content([dependency_target], project_root, ctx)
```

### 4.4 Updated External Context Resolution Flow

The new LLM-driven approach changes the external resolution workflow:

```python
# In EntityRelationshipBuilder._resolve_external_context_in_conversation()
async def _resolve_external_context_in_conversation(self, conversation_id: str, relationships: List[Relationship], project_root: Path, ctx: Context) -> List[Relationship]:
    """Enhanced external context resolution using LLM-suggested paths"""
    resolved_relationships = []
    
    for relationship in relationships:
        try:
            # Step 1: Ask LLM to suggest likely file paths for the dependency
            path_suggestion_prompt = self.prompts.get_path_suggestion_prompt(relationship, project_root)
            response = await self.llm_driver.continue_conversation(conversation_id, path_suggestion_prompt)
            
            # Step 2: Parse LLM response to extract suggested file paths
            suggested_paths = self.prompts.parse_path_suggestions(response.content)
            
            # Step 3: Use dependency resolver to attempt reading suggested paths
            raw_content = await self.dependency_resolver.get_dependency_content(
                suggested_paths, project_root, ctx
            )
            
            # Step 4: Use LLM to analyze the successfully read content
            context_prompt = self.prompts.get_context_resolution_prompt(relationship, raw_content)
            context_response = await self.llm_driver.continue_conversation(conversation_id, context_prompt)
            
            # Step 5: Create resolved relationship with context
            resolved_rel = Relationship(
                source=relationship.source,
                target=relationship.target,
                relationship_type=relationship.relationship_type,
                description=relationship.description,
                line_number=relationship.line_number,
                external_context=context_response.content,
                resolution_method="file_read",
                target_file=suggested_paths[0] if suggested_paths else None  # First successful path
            )
            resolved_relationships.append(resolved_rel)
            
        except Exception as e:
            # Handle failures gracefully - create relationship with error context
            failed_rel = Relationship(
                source=relationship.source,
                target=relationship.target,
                relationship_type=relationship.relationship_type,
                description=relationship.description,
                line_number=relationship.line_number,
                external_context=f"Resolution failed: {str(e)}",
                resolution_method="failed"
            )
            resolved_relationships.append(failed_rel)
            
    return resolved_relationships
```

## 5. Data Models

### 5.1 Entity Model

```python
@dataclass
class Entity:
    """
    Represents a discovered semantic entity with comprehensive metadata.
    Supports both code and document entities with extensible metadata.
    """
    # Core Identity
    id: str                           # Globally unique: "file_path:entity_name"
    type: EntityType                 # Entity classification
    name: str                        # Entity name
    
    # Location Information
    line_number: Optional[int]       # Source line number
    column_number: Optional[int]     # Source column number
    end_line_number: Optional[int]   # End line for multi-line entities
    
    # Descriptive Information  
    description: str                 # Brief description (max 50 chars)
    scope: EntityScope              # Visibility scope
    source_file: str                # Relative path to source file
    
    # Hierarchical Structure
    parent_entity: Optional[str]    # Parent entity ID if nested
    child_entities: List[str]       # Child entity IDs
    
    # Language-Specific Metadata
    metadata: EntityMetadata        # Extensible metadata container
    
    # Processing Information
    extraction_confidence: float    # LLM extraction confidence (0.0-1.0)
    validation_status: ValidationStatus
```

### 5.2 Entity Type System

```python
class EntityType(Enum):
    """Comprehensive entity type classification"""
    
    # Code Entities - Classes & Objects
    CLASS = "class"
    ABSTRACT_CLASS = "abstract_class"
    INTERFACE = "interface"
    ENUM = "enum"
    STRUCT = "struct"
    TRAIT = "trait"
    
    # Code Entities - Functions & Methods
    FUNCTION = "function"
    METHOD = "method"
    STATIC_METHOD = "static_method"
    CLASS_METHOD = "class_method"
    PROPERTY = "property"
    GETTER = "getter"
    SETTER = "setter"
    
    # Code Entities - Variables & Constants
    VARIABLE = "variable"
    CONSTANT = "constant"
    PARAMETER = "parameter"
    LOCAL_VARIABLE = "local_variable"
    INSTANCE_VARIABLE = "instance_variable"
    CLASS_VARIABLE = "class_variable"
    
    # Code Entities - Modules & Packages
    MODULE = "module"
    PACKAGE = "package"
    NAMESPACE = "namespace"
    
    # Code Entities - Special
    DECORATOR = "decorator"
    ANNOTATION = "annotation"
    LAMBDA = "lambda"
    GENERATOR = "generator"
    
    # Document Entities
    CONCEPT = "concept"
    DEFINITION = "definition"
    EXAMPLE = "example"
    SECTION = "section"
    REFERENCE = "reference"
    
    # Configuration Entities
    CONFIG_KEY = "config_key"
    ENV_VARIABLE = "env_variable"
    CLI_ARGUMENT = "cli_argument"
```

### 5.3 Entity Metadata System

```python
@dataclass
class EntityMetadata:
    """Extensible metadata container for entities"""
    
    # Common Metadata
    tags: List[str] = field(default_factory=list)
    annotations: List[str] = field(default_factory=list)
    decorators: List[str] = field(default_factory=list)
    
    # Function/Method Specific
    parameters: List[Dict[str, Any]] = field(default_factory=list)
    return_type: Optional[str] = None
    exceptions: List[str] = field(default_factory=list)
    is_async: bool = False
    is_generator: bool = False
    
    # Class Specific
    base_classes: List[str] = field(default_factory=list)
    interfaces: List[str] = field(default_factory=list)
    is_abstract: bool = False
    
    # Variable Specific
    data_type: Optional[str] = None
    default_value: Optional[str] = None
    is_mutable: bool = True
    
    # Documentation - Removed docstring for token optimization
    examples: List[str] = field(default_factory=list)
    
    # Custom Extensions
    custom: Dict[str, Any] = field(default_factory=dict)
```

### 5.4 Relationship Model

```python
@dataclass
class Relationship:
    """
    Represents a relationship between entities with comprehensive context.
    Supports both internal and external relationships with resolution tracking.
    """
    # Core Relationship
    source: str                      # Source entity ID
    target: str                     # Target entity ID  
    relationship_type: RelationshipType
    
    # Descriptive Information
    description: str                # Human-readable description
    context: Optional[str]          # Additional context
    
    # Location Information
    line_number: Optional[int]      # Where relationship occurs
    column_number: Optional[int]    # Column position
    
    # External Resolution
    external_context: Optional[str] # Context from external resolution
    resolution_method: Optional[str] # How context was obtained
    target_file: Optional[str]      # Target file for external relationships
    resolution_confidence: float = 1.0  # Resolution confidence (0.0-1.0)
    
    # Relationship Metadata
    strength: RelationshipStrength  # Relationship strength/importance
    direction: RelationshipDirection # Relationship directionality
    multiplicity: RelationshipMultiplicity  # One-to-one, one-to-many, etc.
    
    # Processing Information
    validation_status: ValidationStatus
    processing_notes: List[str] = field(default_factory=list)
```

### 5.5 Processing Context Models

```python
@dataclass
class ERMFileContext:
    """
    Comprehensive processing context for entity relationship mapping.
    Tracks complete file processing lifecycle and results.
    """
    # File Information
    file_path: Path
    relative_path: str
    file_size: int
    last_modified: datetime
    
    # Content Classification
    file_type: str                  # code, document, config, etc.
    language: Optional[str]         # Programming language if applicable
    content_encoding: str = "utf-8"
    
    # Discovered Entities and Relationships
    entities: List[Entity] = field(default_factory=list)
    internal_relationships: List[Relationship] = field(default_factory=list)
    external_relationships: List[Relationship] = field(default_factory=list)
    
    # Processing Information
    processing_status: ProcessingStatus
    processing_start_time: Optional[datetime] = None
    processing_end_time: Optional[datetime] = None
    processing_duration: Optional[float] = None
    
    # Context Information
    project_root: Path
    output_file_path: Optional[Path] = None
    
    # Quality Metrics
    entity_extraction_confidence: float = 0.0
    relationship_mapping_confidence: float = 0.0
    external_resolution_success_rate: float = 0.0
    
    # Error Tracking
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
```

## 6. LLM Prompt Engineering

### 6.1 Entity Discovery Prompts

```python
class EntityDiscoveryPrompts:
    """
    Specialized prompts for entity discovery with language-specific optimization.
    """
    
    def get_python_entity_prompt(self, file_path: Path, file_content: str) -> str:
        """Optimized prompt for Python entity discovery"""
        return f"""
TASK: Extract semantic entities from Python source code file.

FILE INFORMATION:
- Path: {file_path}
- Language: Python
- Size: {len(file_content)} characters

ENTITY TYPES TO EXTRACT:
1. Classes (including abstract classes, dataclasses, enums)
2. Functions (including methods, static methods, class methods, properties)
3. Variables (including constants, class variables, instance variables)
4. Modules and packages (import statements)
5. Decorators and annotations
6. Lambda functions and generators

OUTPUT FORMAT:
Return entities as JSON array with this exact structure:
```json
[
  {{
    "name": "EntityName",
    "type": "class|function|variable|module|decorator|lambda|generator",
    "line_number": 123,
    "column_number": 4,
    "end_line_number": 150,
    "description": "Brief description (max 50 chars)",
    "scope": "public|private|protected",
    "metadata": {{
      "parameters": [
        {{"name": "param1", "type": "str", "default": null}},
        {{"name": "param2", "type": "int", "default": "0"}}
      ],
      "return_type": "Optional[str]",
      "decorators": ["@property", "@staticmethod"],
      "base_classes": ["BaseClass", "Mixin"],
      "is_async": false,
      "is_generator": false
    }}
  }}
]
```

ANALYSIS GUIDELINES:
- Focus on semantically meaningful entities, not trivial variables
- Include line and column numbers for precise location
- Extract comprehensive metadata for functions and classes
- Identify inheritance relationships and decorators
- Pay attention to async functions and generators

PYTHON SOURCE CODE:
```python
{file_content}
```

Extract all semantic entities following the specified format:
"""

    def get_document_entity_prompt(self, file_path: Path, file_content: str) -> str:
        """Optimized prompt for document entity discovery (Markdown, etc.)"""
        return f"""
TASK: Extract semantic entities from documentation file.

FILE INFORMATION:
- Path: {file_path}
- Type: Documentation
- Size: {len(file_content)} characters

ENTITY TYPES TO EXTRACT:
1. Concepts (key ideas, principles, patterns)
2. Definitions (terms being defined)
3. Examples (code examples, use cases)
4. Sections (major document sections)
5. References (links to external resources)
6. Configuration keys (if config documentation)

OUTPUT FORMAT:
Return entities as JSON array:
```json
[
  {{
    "name": "EntityName",
    "type": "concept|definition|example|section|reference|config_key",
    "line_number": 123,
    "description": "What this entity represents or defines",
    "scope": "public",
    "metadata": {{
      "section_level": 2,
      "tags": ["configuration", "advanced"],
      "referenced_urls": ["https://example.com"],
      "code_language": "python",
      "example_type": "usage|configuration|tutorial"
    }}
  }}
]
```

DOCUMENT CONTENT:
```
{file_content}
```

Extract all semantic entities following the specified format:
"""
```

### 6.2 Relationship Mapping Prompts

```python
class RelationshipMappingPrompts:
    """
    Specialized prompts for relationship discovery between entities.
    """
    
    def get_internal_relationship_prompt(self, entities: List[Entity], file_content: str, file_context: ERMFileContext) -> str:
        """Generate prompt for internal relationship mapping"""
        entities_context = self._format_entities_for_prompt(entities)
        
        return f"""
TASK: Identify relationships between entities within the same file.

FILE CONTEXT:
- File: {file_context.relative_path}
- Language: {file_context.language}
- Entity Count: {len(entities)}

DISCOVERED ENTITIES:
{entities_context}

RELATIONSHIP TYPES TO IDENTIFY:
**Structural Relationships:**
- contains: Class contains method/property
- inherits: Class inherits from another class
- implements: Class implements interface

**Behavioral Relationships:**
- calls: Function/method calls another function/method
- instantiates: Code creates instance of class
- accesses: Code accesses variable/property
- modifies: Code modifies variable/property

**Data Relationships:**
- reads: Code reads from data source
- writes: Code writes to data source
- transforms: Code transforms data
- validates: Code validates data

OUTPUT FORMAT:
Return relationships as JSON array:
```json
[
  {{
    "source": "file_path:EntityName",
    "target": "file_path:EntityName", 
    "relationship_type": "contains|inherits|calls|instantiates|accesses|modifies|reads|writes|transforms|validates",
    "description": "Clear description of the relationship",
    "line_number": 123,
    "strength": "critical|important|normal|weak",
    "direction": "unidirectional|bidirectional"
  }}
]
```

ANALYSIS GUIDELINES:
- Only identify DIRECT relationships (no transitive dependencies)
- Include precise line numbers where relationships occur
- Focus on semantically meaningful relationships
- Use entity IDs exactly as provided in the entities list

SOURCE CODE FOR ANALYSIS:
```
{file_content}
```

Identify all internal relationships:
"""
        
    def _format_entities_for_prompt(self, entities: List[Entity]) -> str:
        """Format entities list for inclusion in prompts"""
        formatted_entities = []
        for entity in entities:
            formatted_entities.append(f"- {entity.id} ({entity.type.value}): {entity.description}")
        return "\n".join(formatted_entities)

### 6.3 External Path Resolution Prompts

```python
class ExternalPathResolutionPrompts:
    """
    Specialized prompts for LLM-driven external dependency path resolution.
    """
    
    def get_path_suggestion_prompt(self, relationship: Relationship, project_root: Path) -> str:
        """Generate prompt for LLM to suggest likely file paths for external dependency"""
        return f"""
TASK: Suggest likely file paths for external dependency resolution.

DEPENDENCY CONTEXT:
- Source Entity: {relationship.source}
- Target Dependency: {relationship.target}
- Relationship Type: {relationship.relationship_type}
- Description: {relationship.description}
- Project Root: {project_root}

ANALYSIS REQUIREMENTS:
Based on the dependency target "{relationship.target}", suggest 3-5 most likely file paths where this dependency might be located within the project. Consider common project structure patterns:

**Python Projects:**
- models/ directory for data models
- src/ directory for source code
- app/ directory for application code
- lib/ or libs/ for libraries
- utils/ or utilities/ for utility modules

**General Patterns:**
- Nested module structures (e.g., src/models/, app/services/)
- Different file extensions (.py, .js, .ts, etc.)
- Singular vs plural directory names
- Underscore vs hyphen naming conventions

OUTPUT FORMAT:
Return suggested paths as JSON array, ordered by likelihood (most likely first):
```json
{{
  "suggested_paths": [
    "models/user.py",
    "src/models/user.py", 
    "app/models/user.py",
    "src/user.py",
    "lib/user.py"
  ],
  "reasoning": "Target 'User' is likely a data model, so checking models/ directories first, then common source directories"
}}
```

GUIDELINES:
- Provide 3-5 realistic path suggestions
- Order by likelihood (most likely first)
- Consider the relationship type when suggesting paths
- Include brief reasoning for your suggestions
- Use relative paths from project root
- Consider common naming conventions for the project type

Generate path suggestions for the dependency:
"""
    
    def parse_path_suggestions(self, llm_response: str) -> List[str]:
        """Parse LLM response to extract suggested file paths"""
        try:
            import json
            import re
            
            # Try to extract JSON from the response
            json_match = re.search(r'```json\s*(\{.*?\})\s*```', llm_response, re.DOTALL)
            if json_match:
                json_str = json_match.group(1)
                parsed = json.loads(json_str)
                return parsed.get("suggested_paths", [])
            
            # Fallback: Look for array-like patterns
            array_match = re.search(r'\[(.*?)\]', llm_response, re.DOTALL)
            if array_match:
                array_content = array_match.group(1)
                # Extract quoted strings
                paths = re.findall(r'"([^"]+)"', array_content)
                return paths
            
            # Last resort: Look for file-like patterns in the text
            file_patterns = re.findall(r'\b[\w/]+\.[\w]+\b', llm_response)
            return file_patterns[:5]  # Limit to 5 paths
            
        except Exception as e:
            # Return empty list if parsing fails
            return []
    
    def get_context_resolution_prompt(self, relationship: Relationship, file_content: str) -> str:
        """Generate prompt for LLM to analyze external file content for relationship context"""
        truncated_content = file_content[:2000] if len(file_content) > 2000 else file_content
        
        return f"""
TASK: Analyze external file content to provide relationship context.

RELATIONSHIP CONTEXT:
- Source: {relationship.source}
- Target: {relationship.target}
- Type: {relationship.relationship_type}
- Description: {relationship.description}

EXTERNAL FILE CONTENT:
```
{truncated_content}
```

ANALYSIS REQUIREMENTS:
Analyze the file content and provide a brief context summary (max 200 characters) that explains:
1. What the target entity is (class, function, variable, etc.)
2. Key characteristics relevant to the relationship
3. Important details that help understand the dependency

OUTPUT FORMAT:
Return a concise summary focusing on the target entity:
```
Brief description of target entity and its relevance to the relationship
```

GUIDELINES:
- Keep response under 200 characters
- Focus on the target entity mentioned in the relationship
- Include key details like class fields, function parameters, or variable types
- Be concise but informative
- If target entity is not found, note "Target not found in file"

Provide context for the relationship:
"""
```

## 7. YAML Output Specification

### 7.1 Token-Optimized Structure

```yaml
---
metadata:
  source_file: "src/services/user_service.py"
  analysis_timestamp: "2025-07-05T21:28:00Z"
  file_type: "code"
  language: "python"
  analyzer_version: "1.0.0"
  project_root: "/path/to/project"

entities:
  - id: "src/services/user_service.py:UserService"
    type: "class"
    name: "UserService"
    line_number: 15
    description: "User management service"
    scope: "public"
    source_file: "src/services/user_service.py"
    metadata:
      parameters: []
      return_type: null
      decorators: []

  - id: "src/services/user_service.py:get_user_by_id"
    type: "method"
    name: "get_user_by_id"
    line_number: 23
    description: "Retrieve user by ID"
    scope: "public"
    parent_entity: "src/services/user_service.py:UserService"
    metadata:
      parameters: [{"name": "user_id", "type": "int"}, {"name": "include_deleted", "type": "bool", "default": "False"}]
      return_type: "Optional[User]"

relationships:
  internal:
    - source: "src/services/user_service.py:UserService"
      target: "src/services/user_service.py:get_user_by_id"
      relationship_type: "contains"
      description: "Class contains method"
      line_number: 23
      strength: "critical"
      direction: "unidirectional"
      
  external:
    - source: "src/services/user_service.py:get_user_by_id"
      target: "models/user.py:User"
      relationship_type: "uses"
      description: "Method returns User type"
      line_number: 23
      external_context: "User model class with fields: id, username, email, created_at, is_deleted"
      resolution_method: "file_read"
```

### 7.2 Concatenation Compatibility

- **Multi-Document Stream**: Uses `---` separators for valid YAML stream
- **Globally Unique IDs**: Prevents conflicts when concatenated (`file_path:entity_name`)
- **Self-Contained Metadata**: Each document includes complete context
- **Resolvable References**: External relationships use absolute paths

## 8. Relationship Taxonomies

### 8.1 Code Relationships

```python
class CodeRelationshipType(Enum):
    # Structural
    IMPORTS = "imports"
    INHERITS = "inherits"
    IMPLEMENTS = "implements"
    COMPOSES = "composes"
    CONTAINS = "contains"
    
    # Behavioral  
    CALLS = "calls"
    INSTANTIATES = "instantiates"
    ACCESSES = "accesses"
    MODIFIES = "modifies"
    
    # Data
    READS = "reads"
    WRITES = "writes"
    TRANSFORMS = "transforms"
    VALIDATES = "validates"
    
    # Dependency
    DEPENDS_ON = "depends_on"
    REQUIRES = "requires"
    USES = "uses"
```

### 8.2 Document Relationships

```python
class DocumentRelationshipType(Enum):
    # Reference
    REFERENCES = "references"
    LINKS_TO = "links_to"
    CITES = "cites"
    MENTIONS = "mentions"
    
    # Semantic
    DEFINES = "defines"
    DESCRIBES = "describes"
    EXPLAINS = "explains"
    ELABORATES = "elaborates"
    
    # Structural
    PART_OF = "part_of"
    CONTAINS = "contains"
    INCLUDES = "includes"
    EXTENDS = "extends"
    
    # Logical
    RELATES_TO = "relates_to"
    CONFLICTS_WITH = "conflicts_with"
    SUPPORTS = "supports"
```

## 9. Configuration System

### 9.1 Configuration Structure

```python
@dataclass(frozen=True)
class EntityRelationshipConfig:
    """Configuration for entity relationship mapping system"""
    
    # Handler Identification
    handler_type: str = "entity-relationship-mapping"
    description: str = "Entity relationship mapping configuration"
    
    # File Processing
    max_file_size: int = 2 * 1024 * 1024
    batch_size: int = 5  # Smaller due to complexity
    
    # Content Filtering
    excluded_extensions: Set[str] = field(default_factory=lambda: {
        '.pyc', '.pyo', '.git', '__pycache__',
        '.DS_Store', '.env', '.log', '.tmp'
    })
    excluded_directories: Set[str] = field(default_factory=lambda: {
        '.git', '__pycache__', '.pytest_cache',
        '.mypy_cache', 'node_modules', '.venv', 'venv'
    })
    
    # LLM Configuration
    llm_model: str = "claude-3-5-sonnet-20241022"
    temperature: float = 0.2  # Lower for deterministic extraction
    max_tokens: int = 15000
    
    # Entity/Relationship Analysis
    max_entities_per_file: int = 50
    max_relationships_per_entity: int = 20
    resolve_external_dependencies: bool = True
    
    # External Resolution
    max_external_context_length: int = 200  # Token optimized
    external_resolution_timeout: int = 30
    
    # Output Configuration
    output_file_suffix: str = ".erm.yaml"
    yaml_output_directory: Optional[Path] = None
    
    # Error Handling
    max_retries: int = 3
    retry_delay_seconds: float = 1.0
    continue_on_file_errors: bool = True
```

## 10. Integration Patterns

### 10.1 Existing System Integration

- **File Discovery**: Reuse existing file enumeration and filtering logic
- **Progress Reporting**: Same FastMCP Context integration patterns
- **Error Handling**: Same error handling conventions and logging
- **Project Structure**: Follow existing project organization

### 10.2 Strands Agent Tools Integration

All Strands Agent functionality is contained within the `tools/` directory for simple data retrieval only. **Important**: Strands Agent tools provide raw data access without LLM capabilities - all analysis and summarization is handled by the main EntityRelationshipBuilder.

## 11. Implementation Plan

### Phase 1: Core Models and Configuration
1. Entity and relationship data models
2. Configuration system
3. Processing context models
4. Relationship taxonomies

### Phase 2: YAML Generation System
1. Entity ID generation utilities
2. YAML structure templates
3. Concatenation validation
4. Output formatting

### Phase 3: LLM Integration
1. Entity relationship prompts
2. Entity relationship builder
3. External dependency resolver
4. Strands agent integration

### Phase 4: Main Orchestrator
1. Entity relationship indexer
2. Processing workflow coordination
3. Progress reporting integration
4. Error handling and statistics

### Phase 5: Testing and Validation
1. Unit tests for core components
2. Single autonomous integration test for standalone operation
3. YAML concatenation validation
4. Performance testing

## 12. Success Criteria

- **Functional**: Successfully generates `.erm.yaml` files for processed files
- **Concatenation**: Generated YAML files can be concatenated without semantic loss
- **Integration**: Runs alongside existing knowledge indexing without conflicts
- **Performance**: Processes files with acceptable performance (no caching requirement)
- **Reliability**: Handles errors gracefully and continues processing
- **Maintainability**: Code follows existing patterns and conventions

## 13. Risks and Mitigation

### Risk 1: Performance Impact
- **Risk**: External dependency resolution may be slow
- **Mitigation**: Configurable timeouts and sequential processing

### Risk 2: LLM Accuracy
- **Risk**: Entity/relationship extraction may be inaccurate
- **Mitigation**: Structured prompts and validation logic

### Risk 3: YAML Concatenation Issues
- **Risk**: Generated YAML may not concatenate properly
- **Mitigation**: Comprehensive validation and testing

### Risk 4: Integration Conflicts
- **Risk**: May interfere with existing knowledge indexing
- **Mitigation**: Separate configuration and isolated processing

---

**Document End**

This specification provides the foundation for implementing the Entity Relationship Mapping Indexing System. Implementation should proceed according to the phases outlined, with regular validation against the success criteria.
