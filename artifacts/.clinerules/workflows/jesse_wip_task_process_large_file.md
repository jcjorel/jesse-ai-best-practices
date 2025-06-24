# WIP Task Process Large File Workflow

## Workflow Purpose
Process large files (>4000 lines) from git clones that exceed context window limits, creating detailed indexes and access patterns for future reference.

## Execution Steps

### 1. Identify Files for Processing
Check `.knowledge/persistent-knowledge/KNOWLEDGE_BASE.md` for files marked as requiring processing:
- Look for "Large Files Requiring Processing" section
- Identify files marked with priority "**before any other tasks**"
- Display list of files awaiting processing with their details:
  - File path and repository
  - Estimated line count
  - Processing priority level
  - Reason for processing requirement

### 2. Select File for Processing
If multiple files require processing:
- Present prioritized list to user
- Allow user to select specific file or process highest priority
- Display file information and estimated processing time
- Confirm user wants to proceed with processing

### 3. Verify File Size and Accessibility
Before processing, verify file details:
- Use `wc -l` to count exact number of lines
- Confirm file exceeds 4000 line threshold
- Check file is readable and not binary
- Estimate processing complexity based on file type

### 4. Create File Structure Index
Generate comprehensive file index:
- **Line-by-Line Analysis**: Scan file to identify structural elements
- **Function/Class Mapping**: Create index of all functions, classes, and methods with line numbers
- **Section Identification**: Identify major sections, modules, or logical divisions
- **Import/Dependency Mapping**: Track all imports and dependencies with locations
- **Comment Block Analysis**: Identify documentation blocks and their purposes

### 5. Generate Access Patterns
Create efficient access methods for future reference:
- **Chunk Definitions**: Define logical chunks with start/end line numbers
- **Sed Commands**: Generate `sed` commands for extracting specific sections
- **Grep Patterns**: Create `grep` commands for finding specific content
- **Function Extractors**: Commands to extract individual functions or classes
- **Section Navigators**: Commands to jump to specific file sections

### 6. Analyze Code Patterns and Architecture
Extract high-level insights:
- **Architectural Patterns**: Identify design patterns and architectural approaches
- **Code Organization**: Document how code is structured and organized
- **Key Abstractions**: Identify main classes, interfaces, and abstractions
- **Integration Points**: Find external dependencies and integration patterns
- **Configuration Patterns**: Locate configuration handling and parameter management

### 7. Create Detailed File Documentation
Generate comprehensive documentation in corresponding `[repo-name]_kb.md`:

```markdown
## Large File: [filename] ([line_count] lines)
*Last Processed: [ISO timestamp]*

### File Overview
**Purpose**: [What this file does based on analysis]
**Language**: [Programming language]
**Architecture**: [Key architectural patterns identified]
**Complexity**: [High/Medium/Low based on analysis]

### Structure Index
#### Functions/Methods ([count] total)
- `function_name()` (lines [start]-[end]): [Brief description]
- `class_name.method()` (lines [start]-[end]): [Brief description]
- `another_function()` (lines [start]-[end]): [Brief description]

#### Major Sections
- **Imports/Dependencies** (lines 1-[end]): [Description of imports]
- **Configuration** (lines [start]-[end]): [Configuration handling]
- **Core Logic** (lines [start]-[end]): [Main business logic]
- **Utilities** (lines [start]-[end]): [Helper functions]
- **Exports** (lines [start]-[end]): [Module exports]

#### Key Classes/Interfaces
- `ClassName` (lines [start]-[end]): [Class purpose and key methods]
- `InterfaceName` (lines [start]-[end]): [Interface definition and usage]

### Access Patterns
#### Extract Specific Function
```bash
sed -n '[start_line],[end_line]p' [file_path]
```

#### Find Function Definitions
```bash
grep -n "^function\|^def\|^class" [file_path]
```

#### Extract Section
```bash
sed -n '[section_start],[section_end]p' [file_path]
```

#### Search for Pattern
```bash
grep -n "[pattern]" [file_path]
```

### Integration Knowledge
**Dependencies**: [Key dependencies and their purposes]
**Exports**: [What this file provides to other modules]
**Integration Points**: [How this file connects to rest of system]
**Configuration**: [Configuration parameters and defaults]

### Usage Recommendations
**When to Reference**: [Scenarios where this file is relevant]
**Key Sections**: [Most important parts for different use cases]
**Common Patterns**: [Reusable patterns found in this file]
**Gotchas**: [Important limitations or considerations]
```

### 8. Verify Index Accuracy
Validate generated index using command-line tools:
- Use `grep` to verify function/class line numbers are accurate
- Test `sed` commands to ensure they extract correct content
- Verify section boundaries align with actual file structure
- Check that all major components are properly indexed

### 9. Update Knowledge Base Files
Update relevant knowledge management files:
- **Repository Knowledge Base**: Add detailed file documentation
- **Persistent Knowledge Base**: Remove file from "requiring processing" list
- **Essential Knowledge Base**: Update if file contains critical project information
- Mark file as "processed" with timestamp

### 10. Generate Processing Summary
Create summary of processing results:
- **File Statistics**: Line count, function count, class count
- **Processing Time**: Time taken to analyze and index
- **Key Discoveries**: Most important insights from file analysis
- **Access Efficiency**: How much the indexing improves future access
- **Recommendations**: Suggestions for using the indexed information

## File Analysis Techniques

### Structural Analysis
For different file types, use appropriate analysis methods:
- **Python**: Look for class definitions, function definitions, imports
- **JavaScript**: Identify functions, classes, modules, exports
- **Java**: Find classes, interfaces, methods, packages
- **C/C++**: Locate functions, classes, headers, includes
- **Configuration**: Identify sections, parameters, defaults

### Pattern Recognition
Identify common patterns:
- **Design Patterns**: Singleton, Factory, Observer, etc.
- **Architectural Patterns**: MVC, MVP, Repository, etc.
- **Integration Patterns**: API clients, database access, event handling
- **Configuration Patterns**: Environment variables, config files, defaults

### Dependency Mapping
Track dependencies systematically:
- **External Libraries**: Third-party dependencies and their usage
- **Internal Modules**: References to other project files
- **System Dependencies**: OS-level or environment dependencies
- **Configuration Dependencies**: Required configuration parameters

## Workflow Completion
- Verify file is fully indexed with accurate line references
- Confirm all access patterns work correctly
- Update knowledge base files with comprehensive documentation
- Mark file as processed in persistent knowledge base
- Display processing summary and usage recommendations

## Error Handling
- If file is not accessible, mark as "processing failed" with reason
- If file is binary or encrypted, note limitation and skip detailed analysis
- If line counting fails, estimate based on file size and continue
- If indexing is incomplete, preserve partial results and note limitations
- Provide fallback options if automated analysis fails

## Quality Assurance
Before marking file as processed:
- **Accuracy Check**: Verify at least 5 random line references are correct
- **Completeness Check**: Ensure all major functions/classes are indexed
- **Usability Check**: Test that access patterns work as documented
- **Documentation Check**: Verify generated documentation is clear and useful

## Post-Processing Actions
After successful file processing:
- Suggest immediate applications of the indexed knowledge
- Recommend related files that might benefit from similar processing
- Update project documentation if file contains architectural insights
- Schedule periodic re-processing if file is actively maintained
