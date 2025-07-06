<!-- CACHE_METADATA_START -->
<!-- Source File: {PROJECT_ROOT}/jesse-framework-mcp/jesse_framework_mcp/embedded_content/workflows/jesse_wip_task_process_large_file.md -->
<!-- Cached On: 2025-07-06T11:46:20.671676 -->
<!-- Source Modified: 2025-06-24T19:31:39.891821 -->
<!-- Cache Version: 1.0 -->
<!-- CACHE_METADATA_END -->

#### Functional Intent & Features

This file defines the comprehensive `WIP Task Process Large File Workflow` for handling files exceeding 4000 lines from git clones that surpass context window limits, providing detailed indexing and structured access patterns for efficient future reference within the Jesse Framework ecosystem. The workflow delivers systematic large file processing through ten execution steps including file identification, structure indexing, access pattern generation, and comprehensive documentation creation. Key semantic entities include the 4000-line threshold specification, `.knowledge/persistent-knowledge/KNOWLEDGE_BASE.md` integration for file tracking, `Large Files Requiring Processing` section identification, priority-based processing with `**before any other tasks**` markers, `wc -l` command for line counting verification, comprehensive file structure indexing with function/class mapping and section identification, access pattern generation using `sed` and `grep` commands, `[repo-name]_kb.md` documentation targets, `ISO timestamp` formatting for processing records, quality assurance protocols with accuracy verification requirements, command-line tool integration for validation, and post-processing actions including knowledge base updates and processing summaries. The system enables developers to efficiently process and access large codebase files while maintaining structured documentation and creating reusable access patterns for complex file navigation.

##### Main Components

The workflow contains ten primary execution steps: file identification from persistent knowledge base with priority assessment, file selection with user interaction and processing confirmation, file size verification using `wc -l` and accessibility checking, comprehensive file structure indexing including line-by-line analysis and function mapping, access pattern generation with `sed` and `grep` command creation, code pattern and architecture analysis for high-level insights, detailed file documentation generation in repository knowledge bases, index accuracy verification using command-line validation, knowledge base file updates across multiple storage locations, and processing summary generation with statistics and recommendations. Supporting components include file analysis techniques for different programming languages, pattern recognition for design and architectural patterns, dependency mapping for external and internal references, workflow completion verification procedures, comprehensive error handling for accessibility and processing failures, and quality assurance protocols ensuring accuracy and completeness before marking files as processed.

###### Architecture & Design

The architecture implements a comprehensive file processing pipeline with structured indexing and documentation generation patterns. The design uses priority-based file selection from persistent knowledge tracking, systematic structure analysis with line-number precision indexing, and multi-format access pattern generation supporting various extraction methods. The system employs language-specific analysis techniques for different file types, comprehensive documentation templates with structured markdown formatting, and validation protocols ensuring accuracy through command-line tool verification. The workflow follows a quality-first approach with accuracy checking, completeness verification, and usability testing before completion, while maintaining integration with existing knowledge management systems through multiple knowledge base updates and cross-referencing capabilities.

####### Implementation Approach

The implementation uses systematic file identification through knowledge base scanning with priority-based selection algorithms, comprehensive structure analysis employing line-by-line scanning with function and class mapping, and access pattern generation creating `sed` and `grep` command templates for efficient content extraction. The approach employs language-specific analysis techniques with pattern recognition for architectural insights, structured documentation generation using markdown templates with dynamic content insertion, and validation protocols using command-line tools for accuracy verification. File processing operations implement chunk definition with logical boundaries, dependency mapping with location tracking, and integration point identification for system understanding. Quality assurance uses statistical sampling for accuracy verification and comprehensive testing of generated access patterns.

######## External Dependencies & Integration Points

**→ References:**
- `.knowledge/persistent-knowledge/KNOWLEDGE_BASE.md` - persistent knowledge repository tracking files requiring processing with priority markers
- `[repo-name]_kb.md` files - repository-specific knowledge bases requiring detailed file documentation updates
- `wc -l` command-line tool - line counting utility for file size verification and threshold validation
- `sed` command-line tool - stream editor for content extraction pattern generation and validation
- `grep` command-line tool - pattern matching utility for content search and function identification
- `Essential Knowledge Base` - central knowledge coordination requiring updates for critical project information

**← Referenced By:**
- Git clone processing workflows - consume large file processing results for comprehensive repository analysis
- Development workflows - reference indexed large files for implementation guidance and pattern understanding
- Knowledge management workflows - use processed file documentation for cross-referencing and consistency maintenance
- Code analysis workflows - leverage structural indexes and access patterns for efficient large file navigation

**⚡ System role and ecosystem integration:**
- **System Role**: Specialized large file processing workflow within the Jesse Framework knowledge management ecosystem, serving as the primary mechanism for handling files exceeding context window limits through structured indexing and access pattern generation
- **Ecosystem Position**: Core processing component bridging git clone repositories with knowledge management systems through comprehensive file analysis and documentation generation
- **Integration Pattern**: Triggered by priority-based file identification from persistent knowledge tracking, consumes command-line tools for analysis and validation, produces structured documentation and access patterns for consumption by development and knowledge management workflows

######### Edge Cases & Error Handling

The workflow handles inaccessible files by marking them as `processing failed` with specific reason documentation and preservation of partial analysis results. Binary or encrypted files trigger limitation notation with analysis skipping while maintaining processing records for future reference. Line counting failures implement estimation based on file size with continued processing using approximate metrics. Incomplete indexing scenarios preserve partial results with limitation documentation and fallback option provision for manual completion. Automated analysis failures provide alternative processing methods with user guidance for manual intervention. File permission issues during processing implement graceful degradation with alternative access strategies and clear error reporting for resolution guidance.

########## Internal Implementation Details

The file identification mechanism scans `.knowledge/persistent-knowledge/KNOWLEDGE_BASE.md` for `Large Files Requiring Processing` sections with priority parsing and file detail extraction. Structure indexing implements line-by-line scanning with function definition detection, class boundary identification, and section mapping using language-specific patterns. Access pattern generation creates command templates with line number substitution, content extraction optimization, and validation command generation. Documentation generation uses structured markdown templates with dynamic content insertion, line reference formatting, and cross-reference linking. Quality assurance implements statistical sampling with random line reference validation, completeness checking through major component verification, and usability testing with access pattern execution. Knowledge base updates target multiple files with section-specific insertion and timestamp maintenance for accurate change tracking.

########### Code Usage Examples

This example demonstrates file identification and priority assessment from the persistent knowledge base. The structured approach ensures systematic processing of large files based on priority markers and processing requirements.

```bash
# Check for files requiring processing with priority assessment
grep -A 10 "Large Files Requiring Processing" .knowledge/persistent-knowledge/KNOWLEDGE_BASE.md
```

This example shows line counting verification and file accessibility checking before processing initiation. The validation ensures accurate threshold assessment and processing feasibility determination.

```bash
# Verify file size and accessibility for processing threshold validation
wc -l /path/to/large/file.py
test -r /path/to/large/file.py && echo "File accessible" || echo "Access denied"
```

This example illustrates comprehensive structure indexing with function and class mapping. The systematic analysis creates detailed indexes with precise line number references for efficient future access.

```bash
# Generate function and class index with line numbers for structure mapping
grep -n "^def \|^class \|^function " /path/to/large/file.py > structure_index.txt
```

This example demonstrates access pattern generation with `sed` and `grep` command creation. The templates enable efficient content extraction and navigation for large file sections.

```bash
# Extract specific function using generated sed command for content access
sed -n '150,200p' /path/to/large/file.py  # Extract lines 150-200
grep -n "specific_pattern" /path/to/large/file.py  # Find pattern occurrences
```

This example shows the structured documentation template for comprehensive file analysis results. The markdown format ensures consistent documentation with detailed access patterns and architectural insights.

```markdown
## Large File: example_service.py (5500 lines)
*Last Processed: 2024-01-15T10:30:00Z*

### Structure Index
#### Functions/Methods (45 total)
- `initialize_service()` (lines 50-75): Service initialization and configuration
- `ServiceClass.process_request()` (lines 200-350): Main request processing logic

### Access Patterns
#### Extract Specific Function
```bash
sed -n '50,75p' example_service.py
```

#### Find Function Definitions
```bash
grep -n "^def \|^class " example_service.py
```
```