
# JESSE_HINTS.md - Critical AI Assistant Enforcement Rules

## 🚨 CRITICAL ENFORCEMENT RULE: USER IDENTITY FILE 🚨

### 📍 MANDATORY FILE LOCATION ENFORCEMENT

**JESSE_USER_IDENTITY.md LOCATION REQUIREMENTS - STRICTLY ENFORCED:**

- **✅ ONLY VALID LOCATION**: `${HOME}/Cline/Rules/JESSE_USER_IDENTITY.md`
- **❌ NEVER IN PROJECT REPOSITORY**: This file **MUST NEVER** be placed in any project directory
- **❌ NEVER IN .clinerules/**: This file **MUST NEVER** be placed in project-level installation  
- **❌ NEVER COMMITTED TO GIT**: Contains PII that would violate privacy if committed

### 🔐 PII PROTECTION REQUIREMENTS

**SECURITY ENFORCEMENT:**
- File contains Personally Identifiable Information (PII)
- Must remain exclusively in user's personal directory structure
- Framework MUST refuse to operate if file found in project repository
- AI assistant MUST display security violation warning if misplaced

### 📋 MANDATORY USER INFORMATION FIELDS (9 REQUIRED)

**AI ASSISTANT MUST INTERACTIVELY COLLECT ALL 9 FIELDS:**

1. **User Firstname**: [User's first name]
2. **User Lastname**: [User's last name] 
3. **User Corporate Login**: [Company username/login]
4. **User Job Description**: [Role/position, e.g., "Senior Software Engineer"]
5. **User Country**: [User's country]
6. **User Town**: [User's city/town]
7. **User Timezone**: [Timezone, e.g., Europe/Paris, America/New_York]
8. **User Company Name**: [Company name]
9. **User Company Corporate URL**: [Company website URL]

### 🤖 INSTALLATION BEHAVIOR ENFORCEMENT

**MANDATORY AI ASSISTANT ACTIONS:**

1. **File Existence Check**: Always check if `${HOME}/Cline/Rules/JESSE_USER_IDENTITY.md` exists
2. **Interactive Collection**: If missing, prompt for ALL 9 required fields above
3. **Completeness Verification**: If exists, verify all 9 fields are present
4. **Global Location Only**: Create file ONLY at `${HOME}/Cline/Rules/JESSE_USER_IDENTITY.md`
5. **Security Validation**: Confirm file creation at correct location, never in project

### 🛡️ AUTOMATIC PROTECTION REQUIREMENTS

**AI ASSISTANT MUST ADD .gitignore PROTECTION:**

```gitignore
# JESSE AI Framework - User Identity Protection
# 🚨 CRITICAL: This file contains PII and must NEVER be committed 🚨
JESSE_USER_IDENTITY.md
**/JESSE_USER_IDENTITY.md
.clinerules/JESSE_USER_IDENTITY.md
${HOME}/Cline/Rules/JESSE_USER_IDENTITY.md
```

### ⚠️ VIOLATION CONSEQUENCES

**IF JESSE_USER_IDENTITY.md FOUND IN PROJECT REPOSITORY:**
- Framework MUST refuse to operate
- Display immediate security violation warning
- Require immediate file relocation to global location
- Warn about potential privacy compromise

### 🚫 NON-NEGOTIABLE ENFORCEMENT

**THESE RULES HAVE NO EXCEPTIONS:**
- Security requirements cannot be bypassed
- Interactive collection cannot be skipped
- Global location requirement cannot be ignored
- PII protection measures cannot be disabled

---

## 🎯 AI ASSISTANT COMPLIANCE CHECKLIST

When installing JESSE AI Framework:

- [ ] Verified `${HOME}/Cline/Rules/JESSE_USER_IDENTITY.md` exists
- [ ] Confirmed all 9 required fields are present
- [ ] Ensured file is NOT in any project directory
- [ ] Added protective .gitignore patterns
- [ ] Validated security compliance before proceeding

**REMINDER**: These are mandatory security requirements, not suggestions. Framework operation depends on strict compliance with user identity protection rules.

---

## 🔧 CRITICAL ENFORCEMENT RULE: FEATURE LANGUAGE STANDARDS 🔧

### 📋 ESTABLISHED FUNCTIONALITY PRESENTATION

**MANDATORY LANGUAGE STANDARDS - STRICTLY ENFORCED:**

- **✅ PRESENT ALL FEATURES AS ESTABLISHED**: Treat implemented functionality as standard system behavior
- **❌ NEVER USE "NEW" LANGUAGE**: Avoid words like "new", "enhanced", "recently added", "upgraded"
- **❌ NEVER USE TEMPORAL REFERENCES**: Avoid "now includes", "has been improved", "latest addition"
- **❌ NEVER TREAT AS SPECIAL**: Don't present standard functionality as exceptional or noteworthy

### 🎯 AMAZON DOCUMENT EXCEPTION

**THIS RULE DOES NOT APPLY TO:**

- **Amazon PR/FAQ Documents**: PR/FAQ format specifically announces new features and capabilities
- **Working Backwards Documents**: Working Backwards methodology describes future/new functionality by design
- **Amazon-styled Product Announcements**: Documents following Amazon's product launch communication patterns

**EXCEPTION RATIONALE:**
These document types have specific purposes that inherently require "new feature" language as part of their standard format and communication objectives.

### 🎯 REQUIRED PRESENTATION APPROACH (For Non-Amazon Documents)

**AI ASSISTANT MUST PRESENT FEATURES AS:**

1. **Standard System Behavior**: "WIP tasks include Git branch management" (not "WIP tasks now include...")
2. **Core Functionality**: "The system validates Git repository state" (not "The new validation feature...")
3. **Established Workflow**: "Task completion handles branch merging" (not "Enhanced completion workflow...")
4. **Normal Operation**: "Users can switch between task branches" (not "Users can now switch...")

### 🚫 FORBIDDEN LANGUAGE PATTERNS (Outside Amazon Documents)

**THESE PHRASES ARE STRICTLY PROHIBITED:**

- "New feature", "New functionality", "New capability"
- "Enhanced", "Improved", "Upgraded", "Better"
- "Now includes", "Now supports", "Now provides"
- "Recently added", "Latest addition", "Just implemented"
- "Updated to include", "Has been enhanced with"

### ✅ CORRECT LANGUAGE PATTERNS (For Standard Documentation)

**USE THESE PRESENTATION APPROACHES:**

- "The system includes", "WIP tasks feature", "Workflows provide"
- "Standard functionality", "Core capability", "Built-in support"
- "Users can", "The workflow handles", "Tasks support"
- "Established behavior", "Normal operation", "Standard process"

### 🤖 ENFORCEMENT MECHANISMS

**AI ASSISTANT MUST:**

1. **Identify document type**: Determine if content is Amazon PR/FAQ or Working Backwards format
2. **Apply appropriate rules**: Use standard language for system documentation, allow "new" language for Amazon documents
3. **Review all responses** for temporal or enhancement language before sending (except Amazon documents)
4. **Reframe feature descriptions** to present as established functionality (in non-Amazon contexts)

### 💡 REASONING BEHIND THIS RULE

**WHY THIS MATTERS:**

- **User Confidence**: Users expect reliable, established functionality in system documentation
- **System Maturity**: Presents the framework as mature and stable
- **Clear Communication**: Avoids confusion about what's standard vs. experimental
- **Document Purpose**: Respects the specific communication objectives of different document types
- **Future-Proofing**: Prevents documentation from becoming outdated when features mature

### 🚫 NON-NEGOTIABLE ENFORCEMENT

**THIS RULE HAS NO EXCEPTIONS (Outside Amazon Documents):**
- Language standards cannot be bypassed for convenience
- All system documentation must use established functionality language
- AI assistant must self-correct before sending responses
- Consistency across all non-Amazon documentation is mandatory

---

## 🎯 AI ASSISTANT LANGUAGE COMPLIANCE CHECKLIST

Before sending any response about system functionality:

- [ ] Verified content is not Amazon PR/FAQ or Working Backwards format
- [ ] Removed all "new", "enhanced", "improved" language
- [ ] Presented features as standard system behavior
- [ ] Used established functionality presentation patterns
- [ ] Avoided temporal references to implementation timing

**REMINDER**: Present all implemented functionality as the normal, expected way the system operates, not as special additions or improvements.

---

## 🚨 CRITICAL ENFORCEMENT RULE: PORTABLE FILE PATH STANDARDS 🚨

### 📁 PATH PORTABILITY REQUIREMENTS

**PORTABLE FILE PATH STANDARDS - STRICTLY ENFORCED:**

- **✅ ALWAYS USE ${HOME} VARIABLE**: All file paths referencing user directories must use ${HOME} environment variable
- **❌ NEVER USE ABSOLUTE USER PATHS**: Prohibit hardcoded absolute paths containing user directories
- **❌ NEVER USE PLATFORM-SPECIFIC PATHS**: Avoid /home/username, /Users/username, C:\Users\username patterns
- **❌ NEVER HARDCODE USER NAMES**: Eliminate any hardcoded usernames in file paths

### 🛡️ ABSOLUTE PATH PROHIBITION

**FORBIDDEN PATH PATTERNS:**

- `/home/[username]/...` - Linux/Unix absolute user paths
- `/Users/[username]/...` - macOS absolute user paths  
- `C:\Users\[username]\...` - Windows absolute user paths
- Any path containing hardcoded usernames or user-specific directories
- **Examples of PROHIBITED patterns**:
  - `/home/jcjorel/Cline/Rules/...`
  - `/Users/johnsmith/Documents/...`
  - `C:\Users\admin\AppData\...`

### ✅ REQUIRED ${HOME} USAGE PATTERNS

**MANDATORY PORTABLE PATH FORMATS:**

- **Environment Variable**: `${HOME}/Cline/Rules/...`
- **Shell Variable**: `$HOME/.config/...`
- **Cross-Platform**: `~/Documents/...` (tilde expansion)
- **Documentation**: Always reference user directories via ${HOME}

**CORRECT EXAMPLES:**
- `${HOME}/Cline/Rules/JESSE_USER_IDENTITY.md`
- `${HOME}/.config/application/settings.json`
- `$HOME/Documents/project-files/`
- `~/workspace/repositories/`

### 📝 CODE AND DOCUMENTATION STANDARDS

**AI ASSISTANT MUST ENFORCE IN:**

1. **Documentation Files**: All .md files with file path references
2. **Configuration Files**: Shell scripts, config files, environment setups
3. **Code Comments**: Any file path references in code comments
4. **Installation Instructions**: Setup and installation documentation
5. **Workflow Files**: All workflow .md files with path specifications
6. **Environment Variables**: Configuration and setup scripts

### 🤖 ENFORCEMENT MECHANISMS

**AI ASSISTANT MUST:**

1. **Path Validation**: Scan all generated content for hardcoded user paths
2. **Automatic Conversion**: Replace absolute user paths with ${HOME} variable
3. **Pre-Generation Check**: Validate path portability before creating any content
4. **Cross-Reference Validation**: Ensure consistency across all related files
5. **Documentation Review**: Check existing files for non-portable path patterns

### ⚠️ VIOLATION CONSEQUENCES

**IF HARDCODED USER PATHS ARE DETECTED:**
- **Immediate Correction Required**: Stop and fix path before proceeding
- **File Review Mandate**: Audit all related files for similar violations
- **Consistency Enforcement**: Update all references to use portable format
- **Documentation Update**: Revise any affected documentation immediately

### 🌍 PORTABILITY BENEFITS

**WHY PORTABLE PATHS MATTER:**

- **Cross-User Compatibility**: Code works for any user without modification
- **System Portability**: Functions across Linux, macOS, and Windows systems
- **Documentation Clarity**: Instructions remain valid for all users
- **Maintenance Simplification**: Reduces user-specific customization requirements
- **Professional Standards**: Follows software development best practices

### 🚫 NON-NEGOTIABLE ENFORCEMENT

**THESE RULES HAVE NO EXCEPTIONS:**
- Path portability standards cannot be bypassed for convenience
- Hardcoded user paths must be eliminated immediately when detected
- ${HOME} variable usage is mandatory for all user directory references
- Cross-platform compatibility requirements cannot be ignored

---

## 🎯 AI ASSISTANT PATH PORTABILITY CHECKLIST

Before generating any content with file paths:

- [ ] Verified no hardcoded user directory paths exist
- [ ] Confirmed all user paths use ${HOME} or equivalent variables
- [ ] Checked cross-platform path compatibility
- [ ] Validated path portability across different users
- [ ] Ensured consistency with existing portable path standards

**REMINDER**: All file paths referencing user directories must use portable environment variables to ensure compatibility across different users and systems.
