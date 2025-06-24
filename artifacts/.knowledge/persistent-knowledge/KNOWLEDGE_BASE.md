# Project Knowledge Base
*Last Updated: 2025-06-21T06:00:30Z*

## Session-Specific Knowledge Loading Strategy
**LAZY LOADING APPROACH**: Knowledge bases related to the current session task are loaded on-demand when specifically needed, rather than automatically at session initialization. This approach:

- **Reduces Context Window Usage**: Only loads relevant knowledge bases for the current task
- **Improves Performance**: Avoids loading unnecessary external repository content
- **Maintains Focus**: Keeps session context aligned with current work objectives
- **Enables Selective Access**: Allows targeted knowledge base consultation when specific expertise is required

**Loading Triggers**: Knowledge bases are loaded when:
- User explicitly requests information from a specific repository or PDF
- Current task requires specific external API or framework knowledge
- Implementation needs reference patterns from external sources
- Debugging requires consultation of external documentation

**Available Knowledge Sources**:
- Git Clone Knowledge Bases: `.knowledge/git-clones/[repo-name]_kb.md`
- PDF Knowledge Bases: `.knowledge/pdf-knowledge/[source-name]/[source-name]_kb.md`
- Essential Knowledge Base: Always loaded (this file)

## PDF Knowledge Usage Requirements
**CRITICAL**: When using knowledge from imported PDF knowledge bases, you MUST also open and read the associated PDF chunk files to get full clarity and complete context about the knowledge. PDF chunk files are always located in `.knowledge/pdf-knowledge/[source-name]/pdf_chunks/<PDF-chunk-filename>`.

**Mandatory Process**:
1. **Reference PDF Knowledge Base**: First consult `.knowledge/pdf-knowledge/[source-name]/[source-name]_kb.md` for indexed knowledge
2. **Access Original Chunks**: Always open and read the corresponding PDF chunk files referenced in the knowledge base entry
3. **Verify Context**: Cross-reference the chunk content with the summarized knowledge to ensure complete understanding
4. **Use Complete Information**: Base decisions and implementations on the full context from both the knowledge base summary and the original PDF chunks

**PDF Chunk Naming Convention**: PDF chunks are stored with specific naming pattern:
- **Location**: `<project_root>/.knowledge/pdf-knowledge/<imported_pdf_name>/pdf_chunks/`
- **Naming Format**: `<imported_pdf_name>_pages_<page_number_start>_<page_number_end>.pdf`
- **Example**: `.knowledge/pdf-knowledge/nova_user_guide/pdf_chunks/nova_user_guide_pages_001_020.pdf`

**Locating PDF Chunks**: To find the correct PDF chunk(s) to read:
1. Identify the imported PDF name from the knowledge base entry
2. Navigate to `<project_root>/.knowledge/pdf-knowledge/<imported_pdf_name>/pdf_chunks/`
3. Look for files matching pattern `<imported_pdf_name>_pages_<start>_<end>.pdf`
4. Select chunks based on the page range containing the information you need

**Why This Is Required**:
- Knowledge base entries are summaries and may not contain all critical details
- PDF chunks contain the complete original context and nuanced information
- Implementation decisions require full understanding of the source material
- Error prevention through comprehensive information access

## Knowledge Entry Requirements
**MANDATORY**: All knowledge entries must include one or more trust sources to enable deep-dive verification and validation. Trust sources can be:
- Complete relative file paths to codebase files (e.g., `nova-sonic-speech-app/backend/services/nova_sonic_service.py`)
- Git cloned repository references (e.g., `.knowledge/git-clones/aws-sdk-python_kb.md`)
- Web URLs with specific sections (e.g., `https://docs.aws.amazon.com/bedrock/latest/userguide/nova-sonic.html#streaming`)
- Documentation file references (e.g., `doc/DESIGN.md#architecture-overview`)

**Format**: Each knowledge entry must end with:
```
**Trust Sources**:
- [Source Type]: [Complete path/URL/reference]
- [Source Type]: [Complete path/URL/reference]
```

## Project Purpose
Nova Sonic UI is a speech-to-text application that integrates with AWS Nova Sonic services to provide real-time audio transcription capabilities. The project features a FastAPI backend with WebM/Opus audio processing, comprehensive testing infrastructure, and Docker containerization for deployment flexibility.

**Trust Sources**:
- Codebase: `nova-sonic-speech-app/README.md`
- Codebase: `nova-sonic-speech-app/documentation/ARCHITECTURE.md`

## Perplexity Query Results
*No Perplexity queries recorded yet*

## Web Resources
*No web resources captured yet*

## PDF Large Files Requiring Processing
*No large PDF files marked for processing*

## Patterns and Solutions

### Real-Time Audio Processing with asyncio Integration
**Pattern**: Bridge callback-based audio APIs with asyncio using queues for simultaneous recording and playback
**Context**: Real-time audio applications require consistent timing with async operations integration
**Implementation**:
- Use asyncio.Queue to bridge sounddevice callbacks with async generators
- Separate threads for recording callbacks and playback queue processing
- 40ms audio chunks (640 samples at 16kHz) for consistent real-time processing
- Zero-copy operations using numpy views for efficient audio data handling
**Benefits**: Enables real-time audio processing in asyncio applications without blocking event loop

**Trust Sources**:
- Codebase: `nova-sonic-speech-app/services/audio_device_manager.py`
- Implementation: AudioDeviceManager class with callback-to-async bridging

### Audio Performance Statistics Collection
**Pattern**: Accurate callback timing measurement with burst filtering and initialization bias elimination
**Context**: Audio callback statistics require filtering out system artifacts for accurate performance measurement
**Implementation**:
- Filter burst intervals (<10ms) which are audio system artifacts, not real callback intervals
- Exclude first callback from statistics to eliminate initialization bias
- Use nanosecond precision timing with separate tracking for processing, queue, and total times
- Implement Welford's algorithm for stable variance calculation in real-time
**Benefits**: Provides accurate performance metrics for audio optimization and troubleshooting

**Trust Sources**:
- Codebase: `nova-sonic-speech-app/services/audio_device_manager.py`
- Implementation: CallbackStats class with burst filtering logic

### Queue-Based Audio Playback with Blocking Mode
**Pattern**: Non-blocking audio playback with optional blocking completion using sentinel values
**Context**: Audio playback requires both responsive non-blocking operation and completion confirmation capability
**Implementation**:
- Background thread processes playback queue continuously
- Sentinel values (None) signal completion points for blocking mode
- threading.Event with asyncio.run_in_executor for async-compatible blocking
- Queue-based architecture prevents audio dropouts during playback
**Benefits**: Flexible playback control with both fire-and-forget and wait-for-completion modes

**Trust Sources**:
- Codebase: `nova-sonic-speech-app/services/audio_device_manager.py`
- Implementation: AudioDeviceManager playback methods with sentinel pattern

### Per-Chunk Sample Rate Switching for Multi-Source Audio
**Pattern**: AudioChunk metadata with per-chunk sample rate switching maintaining strict FIFO order
**Context**: Applications using multiple audio sources with different sample rates (Polly 16kHz, Nova Sonic 24kHz)
**Implementation**:
- AudioChunk class encapsulates audio data with sample rate metadata and completion tracking
- Playback worker recreates OutputStream only when chunk sample rate differs from current stream rate
- Maintains strict FIFO processing order regardless of sample rate changes
- Per-chunk completion events enable precise blocking synchronization for specific audio chunks
**Benefits**: Seamless multi-source audio support without reordering, minimal stream recreation overhead

**Trust Sources**:
- Codebase: `nova-sonic-speech-app/services/audio_device_manager.py`
- Production Test: `nova-sonic-speech-app/tests/test_autonomous_nova_sonic_conversation.py` execution log

### Precise Blocking Audio Playback with Chunk-Specific Completion
**Pattern**: UUID-based completion tracking for precise blocking synchronization in queue-based audio playback
**Context**: Need to wait for specific audio chunks to complete playback, not just any chunk completion
**Implementation**:
- Each AudioChunk gets unique UUID and optional threading.Event for blocking mode
- Playback worker signals completion after successful audio playback for each chunk
- Blocking mode waits for the specific chunk's completion event with timeout
- Works correctly even when multiple audio chunks are queued
**Benefits**: Precise synchronization control, eliminates race conditions in blocking audio playback

**Trust Sources**:
- Codebase: `nova-sonic-speech-app/services/audio_device_manager.py`
- Production Test: Successful blocking synchronization in Nova Sonic conversation test

### Immediate Audio Buffer Clearing with Graceful Current Chunk Handling
**Pattern**: Thread-safe queue clearing while preserving current playback and properly handling blocking chunks
**Context**: Need responsive audio control to immediately stop queued audio without disrupting current playback
**Implementation**:
- Iterates through playback queue extracting all items without stopping playback thread
- Signals completion events for any blocking chunks to unblock waiting callers
- Allows current ~40ms audio chunk to finish naturally before clearing takes effect
- Returns count of cleared items for caller feedback and debugging
**Benefits**: Non-destructive responsive audio control, prevents audio overlap in conversation systems

**Trust Sources**:
- Codebase: `nova-sonic-speech-app/services/audio_device_manager.py`
- Production Test: Automatic buffer clearing in Nova Sonic conversation preventing audio overlap

### Nova Sonic JSON Event Streaming Protocol
**Pattern**: AWS Nova Sonic requires structured JSON event sequence for bidirectional streaming
**Context**: Nova Sonic bidirectional streaming API uses event-driven architecture, not raw PCM streaming
**Implementation**: 
- Event sequence: sessionStart → promptStart → SYSTEM content → USER audio → contentEnd → promptEnd → sessionEnd
- Audio chunks: 32ms chunks (1024 bytes at 16kHz, 16-bit, mono) with base64 encoding
- SYSTEM role content is mandatory before any USER content
**Benefits**: Provides structured communication with clear error messages and proper event handling

**Trust Sources**:
- Git Clone: `.knowledge/git-clones/amazon-nova-samples_kb.md`
- Codebase: `nova-sonic-speech-app/tests/debug_nova_sonic_event_stream.py`

### AWS Experimental SDK Credential Chain Integration
**Pattern**: Convert boto3 session credentials to AWS Experimental SDK compatible format
**Context**: AWS Experimental SDK requires specific credential resolver that differs from standard boto3 approach
**Implementation**:
- Use boto3.Session() to get standard AWS credentials
- Convert to AWSCredentialsIdentity with access_key, secret_key, and session_token
- Create StaticCredentialsResolver with credentials parameter
- Configure BedrockRuntimeClient with aws_credentials_identity_resolver
**Benefits**: Enables AWS CLI profiles, environment variables, and IAM roles to work with experimental SDK

**Trust Sources**:
- Git Clone: `.knowledge/git-clones/aws-sdk-python_kb.md`
- Codebase: `nova-sonic-speech-app/tests/debug_nova_sonic_experimental_sdk.py`

### Amazon Nova Samples Workshop Event Streaming
**Pattern**: Complete 10-event JSON streaming sequence for Nova Sonic bidirectional communication
**Context**: Production-ready Nova Sonic implementation requires exact event sequence from amazon-nova-samples
**Implementation**:
- Generate unique IDs for prompt_name, system_content_name, audio_content_name
- Send JSON events as bytes via BidirectionalInputPayloadPart.bytes_
- Include audioInputConfiguration and audioOutputConfiguration with proper media types
- Use 16kHz input, 24kHz output LPCM configuration
**Benefits**: Follows official AWS samples patterns for production-ready Nova Sonic integration

**Trust Sources**:
- Git Clone: `.knowledge/git-clones/amazon-nova-samples_kb.md`
- Web URL: `https://github.com/aws-samples/amazon-nova-samples/blob/main/speech-to-speech/sample-codes/console-python/nova_sonic.py`

### Aggressive Timeout Management for Streaming APIs
**Pattern**: Wrap streaming response collection in nested async functions with multiple timeout layers
**Context**: Streaming APIs can hang indefinitely without proper timeout management
**Implementation**:
- Primary timeout: asyncio.wait_for() around entire response collection (10s)
- Secondary timeout: Safety limits on chunk count and processing time
- Graceful degradation: Return empty results on timeout, allow test to continue
**Benefits**: Prevents indefinite hanging while maintaining robust error handling

**Trust Sources**:
- Codebase: `nova-sonic-speech-app/tests/test_autonomous_nova_sonic_conversation.py`
- Codebase: `nova-sonic-speech-app/tests/debug_nova_sonic_experimental_sdk.py`

## Development Environment
### Virtual Environment
**Location**: `nova-sonic-speech-app/venv`
**Usage**: Must be activated before executing any Python commands in the project
**Activation Command**: `source nova-sonic-speech-app/venv/bin/activate`
**Purpose**: Isolates project dependencies from system Python environment

**Trust Sources**:
- Codebase: `nova-sonic-speech-app/README.md`
- Codebase: `nova-sonic-speech-app/backend/requirements.txt`

## External APIs
### AWS Nova Sonic
**Purpose**: Provides speech-to-text transcription services
**Key Endpoints**: Real-time streaming transcription API
**Authentication**: AWS credentials via boto3
**Usage Notes**: Supports WebM/Opus audio format with streaming capabilities

**Trust Sources**:
- Codebase: `nova-sonic-speech-app/backend/services/nova_sonic_service.py`
- Codebase: `nova-sonic-speech-app/documentation/NOVA_SONIC_API.md`

## Project PR/FAQ Documents

### Press Release & FAQ
**Status**: ⚠️ **NOT YET CREATED**

**🚀 ACTION REQUIRED**: No PR/FAQ document exists for this project yet.

**To create your project's PR/FAQ document**:
1. Use the Amazon PR/FAQ Coach: `/jesse_amazon_prfaq_coach.md`  
2. The coach will guide you through Amazon's authentic Working Backwards methodology
3. Complete press release and FAQ will be automatically added to this knowledge base

**What you'll get**:
- Professional press release using Amazon's 7-paragraph structure
- Comprehensive FAQ with customer-facing and internal questions
- Working Backwards methodology completion with 5 Customer Questions
- Integration with this knowledge base for future reference

**Trust Sources**:
- Coach Workflow: `.clinerules/workflows/jesse_amazon_prfaq_coach.md`
- Working Backwards Directory: `working_backwards/`

### Working Backwards Summary

**Status**: ⚠️ **NOT YET COMPLETED**

**🚀 ACTION REQUIRED**: Project Working Backwards analysis not yet completed.

**The 5 Customer Questions Framework**:
```
❓ WHO is the customer?     → [Not yet answered - use PR/FAQ coach]
❓ WHAT is the problem?     → [Not yet answered - use PR/FAQ coach]  
❓ WHAT is the solution?    → [Not yet answered - use PR/FAQ coach]
❓ WHAT is the experience?  → [Not yet answered - use PR/FAQ coach]
❓ HOW measure success?     → [Not yet answered - use PR/FAQ coach]
```

**To complete your Working Backwards analysis**:
1. Launch the Amazon PR/FAQ Coach: `/jesse_amazon_prfaq_coach.md`
2. The coach provides authentic Amazon methodology with real examples
3. Your completed analysis will automatically populate this section

**Trust Sources**:
- Coach Workflow: `.clinerules/workflows/jesse_amazon_prfaq_coach.md`
- Amazon Examples: Real internal Amazon PR/FAQ examples included in coach
- Working Backwards Directory: `working_backwards/current/` and `working_backwards/archive/`

## Available Knowledge Sources (Lazy Loading)
**Note**: These knowledge bases are loaded on-demand when specifically needed for the current session task, following the lazy loading strategy described above.

### Git Clone Knowledge Bases
#### amazon-nova-samples
- **Repository**: https://github.com/aws-samples/amazon-nova-samples.git
- **Purpose**: Official AWS samples for Amazon Nova models including Nova Sonic speech-to-speech
- **Knowledge Base**: `.knowledge/git-clones/amazon-nova-samples_kb.md`
- **Key Resources**: Production-ready Nova Sonic implementation patterns, bidirectional streaming examples, tool integration patterns
- **Clone Date**: 2025-06-19T22:35:00Z
- **Loading Trigger**: When Nova Sonic implementation patterns or official AWS samples are needed

#### aws-sdk-python
- **Repository**: https://github.com/boto/boto3.git
- **Purpose**: AWS SDK for Python (Boto3) reference for Nova Sonic API integration
- **Knowledge Base**: `.knowledge/git-clones/aws-sdk-python_kb.md`
- **Key Resources**: Bedrock Runtime client, Nova Sonic model integration, experimental SDK features
- **Clone Date**: 2025-06-19T17:14:56Z
- **Loading Trigger**: When AWS SDK integration details or experimental SDK features are required

### PDF Knowledge Bases
#### nova-user-guide (PDF Import)
- **Source**: AWS Nova User Guide PDF Documentation (Official)
- **Purpose**: Complete AWS Nova documentation including comprehensive Nova Sonic reference
- **Knowledge Base**: `.knowledge/pdf-knowledge/nova_user_guide/nova_user_guide_kb.md`
- **Key Resources**: Nova Sonic architecture, bidirectional streaming API, speech-to-speech examples, prompting best practices, tool integration, error handling patterns
- **Import Status**: In Progress (2/26 chunks analyzed)
- **Critical Findings**: JSON event streaming approach confirmed correct, SYSTEM role requirement identified, EnvironmentCredentialsResolver pattern documented
- **Download Date**: 2025-06-20T17:36:47Z
- **Size**: 44.49MB PDF (508 pages, 26 chunks)
- **Loading Trigger**: When comprehensive Nova Sonic documentation or official AWS guidance is needed
