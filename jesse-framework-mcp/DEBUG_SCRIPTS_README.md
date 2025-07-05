# Debug Scripts for Pipeline Issue Investigation

This directory contains comprehensive debug scripts to investigate the ValidationExceptions and content corruption issues reported in the knowledge generation pipeline.

## 🚨 Problem Description

Based on the screenshot, the system is experiencing:
- ValidationExceptions with "content field...is empty" messages
- Cache files containing content from other files (content mixing)
- Random failures during knowledge generation
- Multiple retry attempts failing

## 🔍 Investigation Strategy

The debug scripts test three main hypotheses:

### 1. Cache Integrity Issues (`debug_cache_integrity.py`)
- **Tests**: Content mixing, corrupted metadata, missing delimiters, empty cache files
- **Detects**: Duplicate content across cache files, suspicious patterns, metadata corruption
- **Output**: Detailed integrity report with specific file issues

### 2. Race Conditions (`debug_race_conditions.py`) 
- **Tests**: Concurrent read/write operations, cache structure preparation races, content extraction during writes
- **Simulates**: Multiple workers accessing same cache files simultaneously
- **Output**: Race condition detection report with specific failure scenarios

### 3. LLM Validation Issues (`debug_llm_validation.py`)
- **Tests**: Empty prompt generation, conversation ID collisions, content extraction failures
- **Validates**: Prompt building, template processing, response handling
- **Output**: LLM validation report with specific validation failures

## 🚀 Usage Instructions

### Quick Diagnosis (Recommended)
Run the master script that executes all tests:

```bash
cd jesse-framework-mcp
python debug_pipeline_issues.py
```

This will:
- Execute all three debug scripts sequentially
- Generate a consolidated report
- Save detailed results to `debug_pipeline_results.json`
- Return appropriate exit codes for CI/CD integration

### Individual Test Scripts

#### Cache Integrity Analysis
```bash
python debug_cache_integrity.py
```
- Scans `.knowledge/project-base/` for cache files
- Reports corruption, content mixing, and metadata issues
- Exit code 0 = healthy, 1+ = issues detected

#### Race Condition Testing
```bash
python debug_race_conditions.py
```
- Creates temporary test environment
- Simulates concurrent cache operations
- Exit code 0 = no races, 1+ = race conditions detected

#### LLM Validation Testing
```bash
python debug_llm_validation.py
```
- Tests prompt generation with edge cases
- Validates conversation management
- Exit code 0 = no validation issues, 1+ = validation problems

## 📊 Understanding Results

### Exit Codes
- **0**: All tests passed, no issues detected
- **1**: Minor issues detected, pipeline mostly functional
- **2**: Serious issues detected, immediate attention required
- **3**: Script execution failure, check environment

### Report Sections

Each script generates detailed reports with:
- **Issue Summary**: Count and type of problems detected
- **Specific Failures**: Detailed information about each issue
- **Recommendations**: Actionable steps to fix identified problems

### Common Issues and Solutions

#### Cache Integrity Issues
```
❌ DUPLICATE CONTENT detected (3 files):
   - .knowledge/project-base/src/file1.py.analysis.md
   - .knowledge/project-base/src/file2.py.analysis.md
```
**Solution**: Clear cache and implement atomic operations

#### Race Conditions
```
❌ CONTENT CORRUPTION in worker 2:
   Expected: "Analysis content from worker 2"
   Actual: "Analysis content from worker 1"
```
**Solution**: Add file locking for cache operations

#### LLM Validation Issues
```
❌ Empty prompt for empty_content test case:
   Content length: 0, Prompt length: 45
```
**Solution**: Add content validation before prompt generation

## 🔧 Environment Requirements

- Python 3.8+
- All jesse-framework-mcp dependencies installed
- Access to `.knowledge/` directory for cache analysis
- Sufficient disk space for temporary test files

## 📁 Generated Files

During execution, the scripts may create:
- `debug_pipeline_results.json` - Detailed test results
- Temporary test directories (automatically cleaned up)
- Debug log files in the knowledge directory

## 🎯 Next Steps

Based on the debug results:

1. **If no issues detected**: Investigate external factors (AWS credentials, network, etc.)
2. **If cache issues found**: Clear cache and implement fixes in `file_analysis_cache.py`
3. **If race conditions detected**: Add locking mechanisms to concurrent operations
4. **If LLM validation issues**: Improve input validation and error handling

## 🚨 Important Notes

- These scripts are **read-only** for existing cache files
- Race condition tests use temporary directories
- No production data is modified during testing
- Scripts include automatic cleanup procedures

Run the master script first for a comprehensive analysis, then use individual scripts for detailed investigation of specific issue categories.
