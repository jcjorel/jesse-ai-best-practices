
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
