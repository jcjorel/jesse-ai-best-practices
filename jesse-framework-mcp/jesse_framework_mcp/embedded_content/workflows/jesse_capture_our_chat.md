# Capture Our Chat Workflow

## Purpose
Capture the complete current conversation between the user and assistant, saving it as a formatted markdown file for future reference. This workflow creates a permanent record of the conversation, including all exchanges, code changes, and task completion results.

## Trigger
When user includes "capture our chat" anywhere in their request.

## Workflow Steps

### 1. Identify Chat Topic
Extract the main topic of the conversation by:
- Analyzing the initial user request and overall conversation theme
- If topic is unclear, use the primary task or feature being discussed
- Convert topic to snake_case format for file naming

### 2. Generate Timestamp
Create timestamp in exact format: `YYYYMMDD-HHmm`
- Use current time at moment of capture request
- Ensure precise format compliance for consistency

### 3. Construct File Path
Build complete file path:
```
<project_root>/.coding_assistant/captured_chats/YYYYMMDD-HHmm-<Chat_topic_in_snake_case>.md
```

### 4. Format Conversation Content

#### User Message Formatting
Highlight all user messages using YAML distinctive code blocks:
```yaml
User: [User's message content here]
```

#### Assistant Message Formatting
Include assistant responses in standard markdown format without special blocks.

#### Code Block Preservation
- Maintain all code blocks with proper language syntax highlighting
- Preserve indentation and formatting exactly as shown in conversation

#### Tool Use Documentation
Include all tool uses and their results as they appeared in the conversation.

### 5. Content Structure

#### File Header
Start with a clear header:
```markdown
# Chat Capture: [Topic Description]
**Date**: YYYY-MM-DD HH:mm
**Topic**: [Human-readable topic description]

---
```

#### Conversation Body
- Include complete conversation from start to current point
- Maintain chronological order
- Preserve all context including error messages, tool outputs, and corrections

#### File Footer
End with exactly:
```markdown
---

**Task Completion Result**: [Final result or status of the task]

End of chat capture
```

### 6. Recreation Handling
If "capture our chat" is requested again in the SAME conversation:
- **ALWAYS create a new file** with updated timestamp
- **DO NOT overwrite** the previous capture
- Include all conversation up to the new capture point
- This ensures progressive snapshots of ongoing conversations

### 7. Confirmation Response
After successful capture, respond with:
```
✅ Chat captured successfully!
📄 File: <project_root>/.coding_assistant/captured_chats/YYYYMMDD-HHmm-<topic>.md
📝 Topic: [Human-readable topic]
💾 Size: [Approximate conversation length]
```

## Implementation Guidelines

### File System Operations
- Create the captured_chats directory if it doesn't exist
- Handle file writing errors gracefully
- Ensure proper permissions for file creation

### Content Completeness
- **CRITICAL**: Include ENTIRE conversation without truncation
- Capture must include final task completion result
- Never omit parts of the conversation for brevity

### Special Considerations
- Captured files are ephemeral documents, not authoritative sources
- Files in captured_chats/ should NEVER be read back as context

### Error Handling
- If file writing fails, notify user immediately
- Provide alternative (e.g., display content for manual save)
- Never silently fail the capture operation

## Example Usage

### Simple Capture
```
User: "Please capture our chat"
Assistant: [Captures entire conversation with topic extracted from context]
```

### Capture with Context
```
User: "We've finished the authentication implementation. Capture our chat."
Assistant: [Captures with topic "authentication_implementation"]
```

### Multiple Captures
```
User: "Capture our chat" (at 14:30)
Assistant: [Creates: 20250624-1430-feature_development.md]

User: "We made more progress, capture our chat again" (at 15:45)
Assistant: [Creates NEW file: 20250624-1545-feature_development.md]
```

## Related Standards
- Markdown file management: `JESSE_MARKDOWN.md` Section 5.2
- General markdown standards: `JESSE_MARKDOWN.md`
- File naming conventions: `JESSE_MARKDOWN.md` Section 2

## Important Reminders
1. Captured chat files are **write-only** - never read them back
2. Always create new files for subsequent captures in same conversation
3. Include complete conversation without summarization
4. End file properly with task result and "End of chat capture"
5. Use YAML blocks consistently for all user messages
