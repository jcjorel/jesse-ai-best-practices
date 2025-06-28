# Git Clone Knowledge Base: Cline AI Assistant - Complete MCP Integration Reference
*Last Updated: 2025-06-27T17:45:00Z*

## Repository Overview
**Purpose**: Autonomous AI coding assistant VSCode extension with comprehensive MCP (Model Context Protocol) integration  
**Language**: TypeScript/JavaScript (VSCode Extension)  
**License**: Apache-2.0  
**Last Activity**: Active development with regular updates  
**Clone URL**: https://github.com/cline/cline.git  

**🎯 Critical Knowledge**: This KB provides complete technical reference for developing MCP servers that leverage ALL Cline capabilities, from basic tool integration to advanced real-time communication and workflow systems.

---

# SECTION 1: MCP-Cline Integration Fundamentals

## Core MCP Architecture in Cline

### Hub-and-Spoke Connection Management
**Source**: `src/services/mcp/McpHub.ts` (1,000+ lines)

Cline implements a sophisticated MCP management system where the `McpHub` class serves as the central orchestrator for all MCP server connections:

```typescript
// Core connection structure
type McpConnection = {
  server: McpServer,      // Server metadata and state
  client: Client,         // MCP SDK client instance
  transport: Transport    // Transport layer (stdio/SSE/HTTP)
}

class McpHub {
  connections: McpConnection[] = []  // Multiple concurrent connections
  isConnecting: boolean = false      // Connection state management
}
```

### Connection Lifecycle Management
**Complete Flow**: Server Discovery → Configuration → Connection → Monitoring → Disposal

1. **Server Discovery**: Configuration-based or marketplace-driven discovery
2. **Transport Selection**: Automatic transport type selection based on configuration
3. **Client Initialization**: MCP SDK client setup with Cline-specific capabilities
4. **Connection Establishment**: Transport-specific connection with error handling
5. **Capability Fetching**: Tools, resources, and resource templates discovery
6. **Live Monitoring**: Real-time status monitoring with automatic reconnection
7. **Graceful Disposal**: Proper cleanup on server removal or shutdown

### MCP Protocol Foundation
**Client Identity**: All MCP servers receive this client identification:
```typescript
const client = new Client({
  name: "Cline",
  version: this.clientVersion  // VSCode extension version
}, {
  capabilities: {}  // Extensible capability system
});
```

**Core MCP Endpoints Used by Cline**:
- `tools/list` - Tool discovery and registration
- `tools/call` - Tool execution with timeout management
- `resources/list` - Resource discovery for workflow integration
- `resources/read` - Resource content retrieval
- `resources/templates/list` - Dynamic resource template discovery

---

# SECTION 2: Transport Layer Deep Dive

## Three Transport Types with Complete Configuration

### 1. STDIO Transport (Development & Local Servers)
**Best for**: Local development, process-based MCP servers, hot-reload scenarios

**Configuration Schema**:
```json
{
  "type": "stdio",
  "command": "node",                    // Executable command
  "args": ["build/index.js"],          // Command arguments
  "cwd": "/path/to/server",            // Working directory
  "env": {                             // Environment variables
    "API_KEY": "secret_value",
    "NODE_ENV": "development"
  },
  "autoApprove": ["tool1", "tool2"],   // Auto-approved tools
  "timeout": 30,                       // Request timeout in seconds
  "disabled": false                    // Server enabled state
}
```

**Transport Features**:
- **Process Management**: Automatic process spawning and lifecycle management
- **stderr Monitoring**: Intelligent error detection vs info logging
- **Hot Reload Support**: Automatic file watching and server restart
- **Environment Injection**: Complete environment variable control

**Error Handling**:
```typescript
transport.onerror = async (error) => {
  // Automatic error logging and connection state management
  const connection = this.findConnection(name, source);
  if (connection) {
    connection.server.status = "disconnected";
    this.appendErrorMessage(connection, error.message);
  }
  await this.notifyWebviewOfServerChanges();
};
```

### 2. SSE Transport (Server-Sent Events)
**Best for**: Remote servers, real-time communication, web-based MCP servers

**Configuration Schema**:
```json
{
  "type": "sse",
  "url": "https://api.example.com/mcp",
  "headers": {                         // Authentication headers
    "Authorization": "Bearer token123",
    "X-API-Key": "api_key_value"
  },
  "autoApprove": [],
  "timeout": 60,
  "disabled": false
}
```

**Transport Features**:
- **Reconnection Logic**: Automatic reconnection with exponential backoff
- **Credential Management**: Header-based authentication with secure storage
- **Real-time Communication**: Bidirectional communication over HTTP

**Reconnection Configuration**:
```typescript
const reconnectingEventSourceOptions = {
  max_retry_time: 5000,                // Maximum retry delay
  withCredentials: config.headers?.["Authorization"] ? true : false
};
```

### 3. StreamableHTTP Transport (REST-like Communication)
**Best for**: HTTP-based servers, cloud deployment, stateless communication

**Configuration Schema**:
```json
{
  "type": "streamableHttp", 
  "url": "https://api.example.com/mcp",
  "headers": {
    "Content-Type": "application/json",
    "Authorization": "Bearer token123"
  },
  "autoApprove": [],
  "timeout": 45,
  "disabled": false
}
```

**Transport Features**:
- **HTTP Protocol**: Standard HTTP request/response patterns
- **Header Management**: Complete HTTP header control
- **Stateless Operation**: No persistent connection requirements

### Legacy Transport Support
**Backward Compatibility**: Cline supports legacy `transportType` field:
- `"transportType": "stdio"` → `"type": "stdio"`
- `"transportType": "sse"` → `"type": "sse"`  
- `"transportType": "http"` → `"type": "streamableHttp"`

---

# SECTION 3: Real-Time Communication System

## Advanced Notification Architecture

### MCP Notification Protocol
**Critical Discovery**: Cline implements sophisticated real-time notification system for MCP servers to communicate status, progress, and information directly to active tasks.

**Notification Schema**:
```typescript
const NotificationMessageSchema = z.object({
  method: z.literal("notifications/message"),
  params: z.object({
    level: z.enum(["debug", "info", "warning", "error"]).optional(),
    logger: z.string().optional(),    // Component identifier
    data: z.string().optional(),      // Message content
    message: z.string().optional()   // Alternative message field
  }).optional()
});
```

### Real-Time Task Integration
**Active Task Callback System**: When Cline is running a task, MCP servers can send real-time updates:

```typescript
// MCP Server Implementation Example
await client.notification({
  method: "notifications/message",
  params: {
    level: "info",
    logger: "TaskProcessor", 
    data: "Processing file 5 of 10...",
    message: "Task progress update"
  }
});
```

**Cline Integration Flow**:
1. **Active Task Detection**: Cline sets notification callback when task is running
2. **Real-Time Routing**: Notifications immediately sent to active task context
3. **Task Integration**: Messages appear in Cline's task output in real-time
4. **Fallback Storage**: When no active task, notifications stored for later retrieval

### Notification Handling in Cline
```typescript
// Server-side notification handler setup
connection.client.setNotificationHandler(NotificationMessageSchema, async (notification) => {
  const params = notification.params || {};
  const level = params.level || "info";
  const data = params.data || params.message || "";
  const logger = params.logger || "";
  
  const message = logger ? `[${logger}] ${data}` : data;
  
  // Direct callback to active task
  if (this.notificationCallback) {
    this.notificationCallback(name, level, message);
  } else {
    // Store for later retrieval
    this.pendingNotifications.push({
      serverName: name,
      level,
      message,
      timestamp: Date.now()
    });
  }
});
```

### Notification Levels and Behavior
- **debug**: Development information, typically filtered
- **info**: General status updates, shown to user
- **warning**: Important notices, highlighted in UI
- **error**: Error conditions, prominently displayed

### Fallback Notification Handler
```typescript
// Catch-all for unhandled notification types
connection.client.fallbackNotificationHandler = async (notification) => {
  // Shows in VS Code information messages
  vscode.window.showInformationMessage(
    `MCP ${name}: ${notification.method || "unknown"} - ${JSON.stringify(notification.params || {})}`
  );
};
```

---

# SECTION 4: Tool Integration Patterns

## Complete Tool System Architecture

### Tool Discovery and Registration
**Discovery Process**: Cline automatically fetches tool lists when servers connect:

```typescript
// Automatic tool discovery on connection
const response = await connection.client.request(
  { method: "tools/list" }, 
  ListToolsResultSchema,
  { timeout: DEFAULT_REQUEST_TIMEOUT_MS }
);

// Tool structure with auto-approval integration
const tools = (response?.tools || []).map((tool) => ({
  ...tool,
  autoApprove: autoApproveConfig.includes(tool.name)  // Per-tool permissions
}));
```

### Tool Execution Flow with Complete Error Handling
**Full Execution Cycle**:

```typescript
async callTool(serverName: string, toolName: string, toolArguments?: Record<string, unknown>): Promise<McpToolCallResponse> {
  // 1. Connection validation
  const connection = this.connections.find((conn) => conn.server.name === serverName);
  if (!connection) {
    throw new Error(`No connection found for server: ${serverName}. Please make sure to use MCP servers available under 'Connected MCP Servers'.`);
  }
  
  // 2. Server status validation
  if (connection.server.disabled) {
    throw new Error(`Server "${serverName}" is disabled and cannot be used`);
  }
  
  // 3. Dynamic timeout configuration
  let timeout = secondsToMs(DEFAULT_MCP_TIMEOUT_SECONDS);
  try {
    const config = JSON.parse(connection.server.config);
    const parsedConfig = ServerConfigSchema.parse(config);
    timeout = secondsToMs(parsedConfig.timeout);
  } catch (error) {
    console.error(`Failed to parse timeout configuration for server ${serverName}: ${error}`);
  }
  
  // 4. Tool execution with comprehensive error handling
  const result = await connection.client.request({
    method: "tools/call",
    params: {
      name: toolName,
      arguments: toolArguments
    }
  }, CallToolResultSchema, { timeout });
  
  return {
    ...result,
    content: result.content ?? []  // Ensure content array exists
  };
}
```

### Permission System Architecture
**Tool-Level Auto-Approval**: Granular permission control per tool per server:

**Settings Storage**:
```json
{
  "mcpServers": {
    "server-name": {
      "autoApprove": ["safe_tool1", "safe_tool2"],  // Auto-approved tools
      // Other server config...
    }
  }
}
```

**Runtime Permission Checking**:
```typescript
// Dynamic permission updates
async toggleToolAutoApprove(serverName: string, toolNames: string[], shouldAllow: boolean): Promise<void> {
  const autoApprove = config.mcpServers[serverName].autoApprove;
  
  for (const toolName of toolNames) {
    const toolIndex = autoApprove.indexOf(toolName);
    
    if (shouldAllow && toolIndex === -1) {
      autoApprove.push(toolName);          // Add to auto-approve
    } else if (!shouldAllow && toolIndex !== -1) {
      autoApprove.splice(toolIndex, 1);   // Remove from auto-approve
    }
  }
  
  // Update in-memory server state
  connection.server.tools = connection.server.tools.map((tool) => ({
    ...tool,
    autoApprove: autoApprove.includes(tool.name)
  }));
}
```

### Timeout Management System
**Configurable Timeouts**: Per-server timeout configuration with validation:

```typescript
// Timeout validation schema
const BaseConfigSchema = z.object({
  timeout: z.number().min(MIN_MCP_TIMEOUT_SECONDS).optional().default(DEFAULT_MCP_TIMEOUT_SECONDS)
});

// Dynamic timeout updates
async updateServerTimeout(serverName: string, timeout: number): Promise<McpServer[]> {
  // Schema validation
  const setConfigResult = BaseConfigSchema.shape.timeout.safeParse(timeout);
  if (!setConfigResult.success) {
    throw new Error(`Invalid timeout value: ${timeout}. Must be at minimum ${MIN_MCP_TIMEOUT_SECONDS} seconds.`);
  }
  
  // Configuration update and server reconnection
  config.mcpServers[serverName] = { ...config.mcpServers[serverName], timeout };
  await this.updateServerConnections(config.mcpServers);
}
```

---

# SECTION 5: Resource System Architecture

## Complete Resource Management

### Resource Discovery and Caching
**Automatic Resource Discovery**: Cline fetches resource lists on server connection:

```typescript
private async fetchResourcesList(serverName: string): Promise<McpResource[]> {
  try {
    const response = await this.connections
      .find((conn) => conn.server.name === serverName)
      ?.client.request(
        { method: "resources/list" }, 
        ListResourcesResultSchema, 
        { timeout: DEFAULT_REQUEST_TIMEOUT_MS }
      );
    return response?.resources || [];
  } catch (error) {
    return [];  // Graceful fallback for servers without resources
  }
}
```

### Resource Template System
**Dynamic Resource Generation**: Support for parameterized resources:

```typescript
private async fetchResourceTemplatesList(serverName: string): Promise<McpResourceTemplate[]> {
  try {
    const response = await this.connections
      .find((conn) => conn.server.name === serverName)
      ?.client.request(
        { method: "resources/templates/list" }, 
        ListResourceTemplatesResultSchema,
        { timeout: DEFAULT_REQUEST_TIMEOUT_MS }
      );
    return response?.resourceTemplates || [];
  } catch (error) {
    return [];  // Graceful fallback for servers without templates
  }
}
```

### Resource Content Retrieval
**On-Demand Resource Reading**:

```typescript
async readResource(serverName: string, uri: string): Promise<McpResourceResponse> {
  const connection = this.connections.find((conn) => conn.server.name === serverName);
  if (!connection) {
    throw new Error(`No connection found for server: ${serverName}`);
  }
  if (connection.server.disabled) {
    throw new Error(`Server "${serverName}" is disabled`);
  }
  
  return await connection.client.request({
    method: "resources/read",
    params: { uri }
  }, ReadResourceResultSchema);
}
```

### Workflow Integration System
**🔥 Critical Discovery**: Resources become Cline slash commands through sophisticated integration:

**Integration Flow**:
1. **Resource Discovery**: MCP server exposes resources via `resources/list`
2. **Workflow Detection**: Resources with workflow-like names become available as slash commands
3. **Command Processing**: `/workflow-name` triggers resource content retrieval
4. **Content Injection**: Resource content injected as explicit instructions

**Slash Command Integration**:
```typescript
// From src/core/slash-commands/index.ts
const matchingWorkflow = enabledWorkflows.find((workflow) => workflow.fileName === commandName);

if (matchingWorkflow) {
  const workflowContent = (await fs.readFile(matchingWorkflow.fullPath, "utf8")).trim();
  const processedText = 
    `<explicit_instructions type="${matchingWorkflow.fileName}">\n${workflowContent}\n</explicit_instructions>\n` +
    textWithoutSlashCommand;
  return { processedText, needsClinerulesFileCheck: false };
}
```

**MCP Resource → Slash Command Bridge**:
```typescript
// Example MCP server resource that becomes slash command
{
  "resources": [
    {
      "uri": "file://workflows/workflow_name.md",
      "name": "workflow_name.md",           // This becomes /workflow_name
      "mimeType": "text/markdown",
      "description": "Workflow description"
    }
  ]
}
```

---

# SECTION 6: Configuration Management System

## Complete Settings Architecture

### Zod Schema System
**Comprehensive Validation**: Cline uses sophisticated schema validation for all MCP configurations:

```typescript
// Base configuration schema
export const BaseConfigSchema = z.object({
  autoApprove: z.array(z.string()).default([]),              // Tool permissions
  disabled: z.boolean().optional(),                          // Server state
  timeout: z.number().min(MIN_MCP_TIMEOUT_SECONDS).optional().default(DEFAULT_MCP_TIMEOUT_SECONDS)
});

// Transport-specific schemas with transformation
const ServerConfigSchema = z.union([
  // STDIO Configuration
  BaseConfigSchema.extend({
    type: z.literal("stdio").optional(),
    command: z.string(),                                      // Required for stdio
    args: z.array(z.string()).optional(),
    cwd: z.string().optional(),
    env: z.record(z.string()).optional(),
  }).transform((data) => ({
    ...data,
    type: data.type || "stdio" as "stdio"                    // Default type inference
  })),
  
  // SSE Configuration  
  BaseConfigSchema.extend({
    type: z.literal("sse").optional(),
    url: z.string().url("URL must be a valid URL format"),   // Required for SSE
    headers: z.record(z.string()).optional(),
  }).transform((data) => ({
    ...data, 
    type: data.type || "sse" as "sse"
  })),
  
  // StreamableHTTP Configuration
  BaseConfigSchema.extend({
    type: z.literal("streamableHttp").optional(),
    url: z.string().url("URL must be a valid URL format"),   // Required for HTTP
    headers: z.record(z.string()).optional(),
  }).transform((data) => ({
    ...data,
    type: data.type || "streamableHttp" as "streamableHttp"
  }))
]);

// Complete settings schema
export const McpSettingsSchema = z.object({
  mcpServers: z.record(ServerConfigSchema)
});
```

### Live Configuration Reloading
**File Watching System**: Automatic configuration updates without restart:

```typescript
// gRPC-based file watching
const cancelSubscription = getHostBridgeProvider().watchServiceClient.subscribeToFile(
  SubscribeToFileRequest.create({
    metadata: Metadata.create({}),
    path: settingsPath
  }),
  {
    onResponse: async (response) => {
      if (response.type === FileChangeEvent_ChangeType.CHANGED) {
        const settings = await this.readAndValidateMcpSettingsFile();
        if (settings) {
          await this.updateServerConnections(settings.mcpServers);
          vscode.window.showInformationMessage("MCP servers updated");
        }
      }
    },
    onError: (error) => console.error("Error watching MCP settings file:", error),
    onComplete: () => console.log("MCP settings file watch completed")
  }
);
```

### Settings File Management
**Default Settings Structure**:
```json
{
  "mcpServers": {
    "example-server": {
      "type": "stdio",
      "command": "node",
      "args": ["build/index.js"],
      "cwd": "/path/to/server",
      "env": {
        "NODE_ENV": "production"
      },
      "autoApprove": ["safe_tool"],
      "timeout": 30,
      "disabled": false
    }
  }
}
```

### Legacy Support System
**Backward Compatibility**: Automatic migration from old configuration formats:

```typescript
// Legacy field support with transformation
.transform((data) => {
  // Support both type and transportType fields
  const finalType = data.type || (data.transportType === "stdio" ? "stdio" : undefined) || "stdio";
  return {
    ...data,
    type: finalType as "stdio",
    transportType: undefined  // Remove legacy field
  };
})
```

---

# SECTION 7: Development Workflow Integration

## Hot-Reload System for MCP Development

### Automatic File Watching
**Development-Time Features**: Cline provides sophisticated development support for MCP server creators:

```typescript
// Automatic file watching for stdio servers
private setupFileWatcher(name: string, config: Extract<McpServerConfig, { type: "stdio" }>) {
  const filePath = config.args?.find((arg: string) => arg.includes("build/index.js"));
  if (filePath) {
    const watcher = chokidar.watch(filePath, {
      // Configuration for atomic writes and change detection
    });
    
    watcher.on("change", () => {
      console.log(`Detected change in ${filePath}. Restarting server ${name}...`);
      this.restartConnection(name);  // Automatic server restart
    });
    
    this.fileWatchers.set(name, watcher);
  }
}
```

### Development Restart Flow
**Graceful Server Restart**: Complete restart cycle for development:

```typescript
async restartConnection(serverName: string): Promise<void> {
  this.isConnecting = true;
  
  const connection = this.connections.find((conn) => conn.server.name === serverName);
  const config = connection?.server.config;
  
  if (config) {
    // User notification
    vscode.window.showInformationMessage(`Restarting ${serverName} MCP server...`);
    
    // Update UI state
    connection.server.status = "connecting";
    connection.server.error = "";
    await this.notifyWebviewOfServerChanges();
    
    // Artificial delay for UX
    await setTimeoutPromise(500);
    
    try {
      // Clean shutdown and restart
      await this.deleteConnection(serverName);
      await this.connectToServer(serverName, JSON.parse(config), "internal");
      vscode.window.showInformationMessage(`${serverName} MCP server connected`);
    } catch (error) {
      console.error(`Failed to restart connection for ${serverName}:`, error);
      vscode.window.showErrorMessage(`Failed to connect to ${serverName} MCP server`);
    }
  }
  
  await this.notifyWebviewOfServerChanges();
  this.isConnecting = false;
}
```

### Development Best Practices
**Recommended Development Flow**:
1. **stdio Transport**: Use for local development with automatic restart
2. **Build File Watching**: Point to compiled JavaScript files for hot-reload
3. **Error Monitoring**: Monitor stderr for development debugging
4. **Configuration Testing**: Use validation schemas for configuration testing

---

# SECTION 8: Advanced Integration Patterns

## Multi-Server Connection Management

### Concurrent Connection Architecture
**Scalable Design**: Cline manages multiple MCP servers simultaneously:

```typescript
class McpHub {
  connections: McpConnection[] = []  // Array of concurrent connections
  
  // Server sorting based on configuration order
  private getSortedMcpServers(serverOrder: string[]): McpServer[] {
    return [...this.connections]
      .sort((a, b) => {
        const indexA = serverOrder.indexOf(a.server.name);
        const indexB = serverOrder.indexOf(b.server.name);
        return indexA - indexB;
      })
      .map((connection) => connection.server);
  }
}
```

### Connection State Management
**Sophisticated State Tracking**: Each connection maintains detailed state:

```typescript
type McpConnection = {
  server: {
    name: string,
    config: string,        // Serialized configuration
    status: "connecting" | "connected" | "disconnected",
    disabled: boolean,
    error?: string,        // Error accumulation
    tools?: McpTool[],     // Cached tool list
    resources?: McpResource[],           // Cached resource list
    resourceTemplates?: McpResourceTemplate[]  // Cached templates
  },
  client: Client,          // MCP SDK client
  transport: Transport     // Active transport connection
};
```

### Error Recovery Strategies
**Comprehensive Error Handling**: Multi-layered error recovery:

1. **Transport-Level Recovery**: Automatic reconnection for transport failures
2. **Request-Level Timeout**: Per-request timeout with graceful failure
3. **Server-Level Fallback**: Server disable/enable for persistent failures
4. **User-Level Notification**: Clear error communication to users

## Marketplace Integration Architecture

### MCP Server Discovery
**Marketplace Integration**: Built-in support for MCP server discovery and installation:

```typescript
// Marketplace catalog subscription
async refreshMcpMarketplace(): Promise<void> {
  // Marketplace integration for server discovery
}

async subscribeToMcpMarketplaceCatalog(): Promise<void> {
  // Live marketplace updates
}

async downloadMcp(): Promise<void> {
  // Automatic MCP server installation
}
```

### Remote Server Management
**Dynamic Server Addition**: Runtime server configuration:

```typescript
async addRemoteServer(serverName: string, serverUrl: string): Promise<McpServer[]> {
  // URL validation
  const urlValidation = z.string().url().safeParse(serverUrl);
  if (!urlValidation.success) {
    throw new Error(`Invalid server URL: ${serverUrl}. Please provide a valid URL.`);
  }
  
  // Duplicate name checking
  if (settings.mcpServers[serverName]) {
    throw new Error(`An MCP server with the name "${serverName}" already exists`);
  }
  
  // Dynamic server configuration
  const serverConfig = {
    url: serverUrl,
    disabled: false,
    autoApprove: []
  };
  
  // Live configuration update
  settings.mcpServers[serverName] = parsedConfig;
  await fs.writeFile(settingsPath, JSON.stringify(settings, null, 2));
  await this.updateServerConnections(settings.mcpServers);
}
```

---

# SECTION 9: Complete Implementation Examples

## 1. Minimal MCP Server Example
**Basic functional MCP server that integrates with Cline**:

```typescript
// minimal-server.ts
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";

const server = new Server(
  { name: "minimal-server", version: "1.0.0" },
  { capabilities: { tools: {} } }
);

// Tool registration
server.setRequestHandler("tools/list", async () => ({
  tools: [{
    name: "hello",
    description: "Say hello",
    inputSchema: {
      type: "object",
      properties: {
        name: { type: "string", description: "Name to greet" }
      }
    }
  }]
}));

// Tool execution
server.setRequestHandler("tools/call", async (request) => {
  if (request.params.name === "hello") {
    const name = request.params.arguments?.name || "World";
    return {
      content: [{ type: "text", text: `Hello, ${name}!` }]
    };
  }
  throw new Error(`Unknown tool: ${request.params.name}`);
});

// Transport setup
const transport = new StdioServerTransport();
server.connect(transport);
```

**Cline Configuration**:
```json
{
  "mcpServers": {
    "minimal-server": {
      "type": "stdio", 
      "command": "node",
      "args": ["minimal-server.js"],
      "autoApprove": ["hello"]
    }
  }
}
```

## 2. Workflow-Enabled MCP Server
**MCP server that provides workflow resources for Cline slash commands**:

```typescript
// workflow-server.ts
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import * as fs from "fs/promises";

const server = new Server(
  { name: "workflow-server", version: "1.0.0" },
  { capabilities: { resources: {} } }
);

// Resource list - these become slash commands in Cline
server.setRequestHandler("resources/list", async () => ({
  resources: [
    {
      uri: "workflow://deploy",
      name: "deploy.md",  // Becomes /deploy slash command
      mimeType: "text/markdown",
      description: "Deployment workflow"
    },
    {
      uri: "workflow://test", 
      name: "test.md",    // Becomes /test slash command
      mimeType: "text/markdown",
      description: "Testing workflow"
    }
  ]
}));

// Resource content retrieval
server.setRequestHandler("resources/read", async (request) => {
  const uri = request.params.uri;
  
  if (uri === "workflow://deploy") {
    return {
      contents: [{
        uri,
        mimeType: "text/markdown",
        text: `# Deployment Workflow
        
1. Run tests: \`npm test\`
2. Build application: \`npm run build\`
3. Deploy to staging: \`npm run deploy:staging\`
4. Run smoke tests
5. Deploy to production: \`npm run deploy:prod\`

Execute these steps carefully and confirm each step before proceeding.`
      }]
    };
  }
  
  if (uri === "workflow://test") {
    return {
      contents: [{
        uri,
        mimeType: "text/markdown", 
        text: `# Testing Workflow

1. Run unit tests: \`npm run test:unit\`
2. Run integration tests: \`npm run test:integration\`
3. Run e2e tests: \`npm run test:e2e\`
4. Generate coverage report: \`npm run test:coverage\`
5. Review test results and coverage

Ensure all tests pass before proceeding with deployment.`
      }]
    };
  }
  
  throw new Error(`Unknown resource: ${uri}`);
});

const transport = new StdioServerTransport();
server.connect(transport);
```

## 3. Notification-Rich MCP Server
**MCP server with real-time communication to Cline tasks**:

```typescript
// notification-server.ts
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";

const server = new Server(
  { name: "notification-server", version: "1.0.0" },
  { capabilities: { tools: {} } }
);

// Long-running tool with progress notifications
server.setRequestHandler("tools/call", async (request) => {
  if (request.params.name === "long_task") {
    const steps = 10;
for (let i = 1; i <= steps; i++) {
      // Send progress notification to Cline
      await server.notification({
        method: "notifications/message",
        params: {
          level: "info",
          logger: "TaskProcessor",
          data: `Processing step ${i} of ${steps}...`,
          message: `Task progress: ${Math.round((i/steps) * 100)}%`
        }
      });
      
      // Simulate work
      await new Promise(resolve => setTimeout(resolve, 1000));
    }
    
    // Final completion notification
    await server.notification({
      method: "notifications/message", 
      params: {
        level: "info",
        logger: "TaskProcessor",
        data: "Task completed successfully!",
        message: "All processing steps finished"
      }
    });
    
    return {
      content: [{ 
        type: "text", 
        text: `Completed ${steps} processing steps with real-time progress updates.` 
      }]
    };
  }
  
  throw new Error(`Unknown tool: ${request.params.name}`);
});

// Tool registration with notification capability
server.setRequestHandler("tools/list", async () => ({
  tools: [{
    name: "long_task",
    description: "Execute long-running task with real-time progress notifications",
    inputSchema: {
      type: "object",
      properties: {}
    }
  }]
}));

const transport = new StdioServerTransport();
server.connect(transport);
```

**Key Features**:
- **Real-Time Progress**: Updates sent during tool execution
- **Structured Notifications**: Consistent level and logger identification
- **Active Task Integration**: Messages appear directly in Cline's task output
- **Progress Tracking**: Percentage completion and step-by-step updates

## 4. Multi-Transport Production Server
**Production-ready MCP server supporting all transport types**:

```typescript
// production-server.ts
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import express from "express";

// Environment-based transport selection
const serverConfig = {
  name: "production-server",
  version: "2.0.0",
  capabilities: {
    tools: {},
    resources: {},
    notifications: {}
  }
};

const server = new Server(serverConfig.name, serverConfig);

// Advanced tool with error handling and notifications
server.setRequestHandler("tools/call", async (request) => {
  const toolName = request.params.name;
  
  try {
    // Send start notification
    await server.notification({
      method: "notifications/message",
      params: {
        level: "info",
        logger: "ToolExecutor",
        data: `Starting execution of ${toolName}`,
      }
    });

    switch (toolName) {
      case "analyze_codebase":
        return await analyzeCodebase(request.params.arguments);
      case "deploy_application":
        return await deployApplication(request.params.arguments);
      case "run_tests":
        return await runTests(request.params.arguments);
      default:
        throw new Error(`Unknown tool: ${toolName}`);
    }
  } catch (error) {
    // Send error notification
    await server.notification({
      method: "notifications/message",
      params: {
        level: "error",
        logger: "ToolExecutor",
        data: `Tool ${toolName} failed: ${error.message}`,
      }
    });
    throw error;
  }
});

// Resource system with templates
server.setRequestHandler("resources/templates/list", async () => ({
  resourceTemplates: [{
    uriTemplate: "project://{project_id}/analysis",
    name: "Project Analysis Template",
    description: "Generate analysis for any project",
    mimeType: "application/json"
  }]
}));

// Dynamic resource generation
server.setRequestHandler("resources/read", async (request) => {
  const uri = request.params.uri;
  const match = uri.match(/project:\/\/(.+)\/analysis/);
  
  if (match) {
    const projectId = match[1];
    const analysis = await generateProjectAnalysis(projectId);
    
    return {
      contents: [{
        uri,
        mimeType: "application/json",
        text: JSON.stringify(analysis, null, 2)
      }]
    };
  }
  
  throw new Error(`Unknown resource: ${uri}`);
});

// Environment-specific transport setup
if (process.env.MCP_TRANSPORT === "stdio") {
  const transport = new StdioServerTransport();
  server.connect(transport);
} else {
  // HTTP/SSE server setup for cloud deployment
  const app = express();
  app.use(express.json());
  
  // MCP over HTTP endpoint
  app.post("/mcp", async (req, res) => {
    try {
      const response = await server.handleRequest(req.body);
      res.json(response);
    } catch (error) {
      res.status(500).json({ error: error.message });
    }
  });
  
  const port = process.env.PORT || 3000;
  app.listen(port, () => {
    console.log(`MCP server listening on port ${port}`);
  });
}

async function analyzeCodebase(args: any) {
  // Implementation with progress notifications
  const files = await getProjectFiles(args.projectPath);
  const totalFiles = files.length;
  
  for (let i = 0; i < totalFiles; i++) {
    await server.notification({
      method: "notifications/message",
      params: {
        level: "info",
        logger: "CodeAnalyzer",
        data: `Analyzing file ${i + 1} of ${totalFiles}: ${files[i]}`,
      }
    });
    
    // Analyze file logic here
  }
  
  return {
    content: [{
      type: "text",
      text: `Analysis complete: ${totalFiles} files processed`
    }]
  };
}
```

**Production Configuration Examples**:

**STDIO (Development)**:
```json
{
  "type": "stdio",
  "command": "node",
  "args": ["dist/production-server.js"],
  "env": {"MCP_TRANSPORT": "stdio"},
  "timeout": 60
}
```

**HTTP (Cloud)**:
```json
{
  "type": "streamableHttp",
  "url": "https://mcp.company.com/api",
  "headers": {"Authorization": "Bearer prod-token"},
  "timeout": 120
}
```

---

# SECTION 10: Production Deployment Patterns

## Configuration Best Practices

### Security Configuration
**Authentication and Authorization**:
```json
{
  "mcpServers": {
    "production-server": {
      "type": "streamableHttp",
      "url": "https://secure-mcp.company.com/api",
      "headers": {
        "Authorization": "Bearer ${MCP_API_TOKEN}",
        "X-Client-ID": "${MCP_CLIENT_ID}",
        "X-Environment": "production"
      },
      "autoApprove": [],  // No auto-approval in production
      "timeout": 60,
      "disabled": false
    }
  }
}
```

### Performance Optimization
**Timeout and Connection Management**:
- **Development**: 30-60 seconds for interactive development
- **Production**: 120+ seconds for complex operations
- **Batch Operations**: 300+ seconds for large-scale processing

**Resource Caching Strategy**:
- Cache resource lists for 5 minutes
- Cache resource content for 1 minute
- Invalidate cache on server reconnection

### Monitoring and Observability
**Comprehensive Logging Integration**:
```typescript
// Enhanced notification system for production monitoring
await server.notification({
  method: "notifications/message",
  params: {
    level: "info",
    logger: "MetricsCollector",
    data: JSON.stringify({
      event: "tool_execution",
      tool: toolName,
      duration: executionTime,
      success: true,
      timestamp: new Date().toISOString()
    })
  }
});
```

### Error Recovery Patterns
**Multi-Level Fallback System**:
1. **Tool-Level**: Graceful degradation for individual tool failures
2. **Server-Level**: Automatic server restart and reconnection
3. **System-Level**: Alternative server or offline mode
4. **User-Level**: Clear error communication and manual override options

## Deployment Architecture Patterns

### Local Development
```bash
# Development MCP server with hot reload
npm run dev
# Cline configuration: stdio transport with file watching
```

### Staging Environment
```bash
# Containerized MCP server
docker run -p 8080:8080 mcp-server:staging
# Cline configuration: HTTP transport with staging credentials
```

### Production Environment
```bash
# Kubernetes deployment with load balancing
kubectl apply -f mcp-server-deployment.yaml
# Cline configuration: HTTPS transport with production security
```

---

# SECTION 11: Advanced Technical Insights

## MCP Protocol Extensions

### Custom Notification Types
**Beyond Standard Notifications**: Cline's extensible notification system supports custom notification types:

```typescript
// Custom notification for file operations
await server.notification({
  method: "notifications/file_operation",
  params: {
    operation: "create",
    path: "/path/to/file",
    size: 1024,
    checksum: "abc123"
  }
});

// Custom notification for deployment status
await server.notification({
  method: "notifications/deployment",
  params: {
    environment: "production",
    status: "deploying",
    progress: 45,
    eta: "2 minutes"
  }
});
```

### Resource URI Patterns
**Advanced URI Schemes**: Sophisticated URI patterns for dynamic resources:

```typescript
// Template-based resources
"uriTemplate": "git://repo/{owner}/{repo}/branch/{branch}/file/{path}"
"uriTemplate": "database://table/{table}/query/{query_id}"
"uriTemplate": "api://service/{service}/endpoint/{endpoint}/version/{version}"

// Query-based resources  
"uriTemplate": "search://index/{index}?q={query}&limit={limit}"
"uriTemplate": "metrics://service/{service}/timerange/{start}/{end}"
```

### Tool Composition Patterns
**Complex Tool Orchestration**: MCP servers can implement sophisticated tool composition:

```typescript
server.setRequestHandler("tools/call", async (request) => {
  if (request.params.name === "deploy_full_stack") {
    // Composite tool that orchestrates multiple sub-tools
    const steps = [
      "run_tests",
      "build_application", 
      "deploy_backend",
      "deploy_frontend",
      "run_smoke_tests"
    ];
    
    const results = [];
    for (const step of steps) {
      await server.notification({
        method: "notifications/message",
        params: {
          level: "info",
          logger: "DeploymentOrchestrator",
          data: `Executing step: ${step}`
        }
      });
      
      const result = await executeSubTool(step, request.params.arguments);
      results.push({ step, result });
    }
    
    return {
      content: [{
        type: "text",
        text: `Full stack deployment completed: ${results.length} steps executed`
      }]
    };
  }
});
```

## Performance Optimization Techniques

### Connection Pooling
**Efficient Resource Management**: For HTTP-based MCP servers:

```typescript
// Connection pool for database access
const pool = new Pool({
  host: 'localhost',
  database: 'mcp_data',
  max: 20,        // Maximum connections
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 2000,
});

// Reuse connections across tool calls
server.setRequestHandler("tools/call", async (request) => {
  const client = await pool.connect();
  try {
    const result = await executeToolWithDB(client, request);
    return result;
  } finally {
    client.release();
  }
});
```

### Caching Strategies
**Smart Caching for Performance**:

```typescript
const cache = new Map();
const CACHE_TTL = 5 * 60 * 1000; // 5 minutes

server.setRequestHandler("resources/read", async (request) => {
  const uri = request.params.uri;
  const cacheKey = `resource:${uri}`;
  
  // Check cache first
  const cached = cache.get(cacheKey);
  if (cached && Date.now() - cached.timestamp < CACHE_TTL) {
    return cached.data;
  }
  
  // Generate resource content
  const content = await generateResourceContent(uri);
  
  // Cache the result
  cache.set(cacheKey, {
    data: content,
    timestamp: Date.now()
  });
  
  return content;
});
```

### Batch Operations
**Efficient Bulk Processing**:

```typescript
server.setRequestHandler("tools/call", async (request) => {
  if (request.params.name === "process_files_batch") {
    const files = request.params.arguments.files;
    const batchSize = 10;
    
    for (let i = 0; i < files.length; i += batchSize) {
      const batch = files.slice(i, i + batchSize);
      
      // Process batch in parallel
      const promises = batch.map(file => processFile(file));
      await Promise.all(promises);
      
      // Progress notification
      await server.notification({
        method: "notifications/message",
        params: {
          level: "info",
          logger: "BatchProcessor",
          data: `Processed ${Math.min(i + batchSize, files.length)} of ${files.length} files`
        }
      });
    }
    
    return { content: [{ type: "text", text: `Batch processing completed: ${files.length} files` }] };
  }
});
```

---

# Reference Links

- **Repository**: https://github.com/cline/cline.git
- **MCP SDK Documentation**: https://modelcontextprotocol.io/
- **Core MCP Services**: [src/services/mcp/](.knowledge/git-clones/cline/src/services/mcp/)
- **MCP Controllers**: [src/core/controller/mcp/](.knowledge/git-clones/cline/src/core/controller/mcp/)
- **Slash Commands**: [src/core/slash-commands/](.knowledge/git-clones/cline/src/core/slash-commands/)
- **Package Configuration**: [package.json](.knowledge/git-clones/cline/package.json)

## Large Files Requiring Processing
*Note: Only package-lock.json files exceed 4000 lines - these are dependency files not critical for MCP understanding*

### Standard Dependencies (Not Critical for MCP Analysis)
- `package-lock.json` (41,582 lines): Main project dependencies
- `docs/package-lock.json` (10,118 lines): Documentation dependencies  
- `webview-ui/package-lock.json` (17,214 lines): UI component dependencies

---

# MCP Implementation Learnings

## Critical Success Factors for MCP Development

### 1. Transport Selection Strategy
- **Development**: Always use `stdio` transport with automatic restart
- **Testing**: Use `stdio` for unit tests, `http` for integration tests  
- **Production**: Use `sse` or `streamableHttp` based on infrastructure
- **Hybrid**: Support multiple transports in the same server codebase

### 2. Notification Integration Mastery
- **Real-Time Updates**: Essential for long-running operations
- **Structured Logging**: Use consistent logger names and levels
- **Progress Tracking**: Include percentage and ETA when possible
- **Error Communication**: Detailed error context for debugging

### 3. Resource System Excellence
- **Workflow Integration**: Design resources to become useful slash commands
- **URI Consistency**: Use predictable URI patterns for discoverability
- **Template Support**: Implement parameterized resources for flexibility
- **Content Caching**: Cache expensive resource generation operations

### 4. Tool Design Principles
- **Single Responsibility**: Each tool should have one clear purpose
- **Comprehensive Schemas**: Detailed input validation prevents errors
- **Error Handling**: Throw descriptive errors for all failure modes
- **Progress Reporting**: Use notifications for operations > 2 seconds

### 5. Production Readiness
- **Configuration Management**: Support environment-specific configuration
- **Security First**: No auto-approval for production tools
- **Monitoring Integration**: Comprehensive logging and metrics
- **Graceful Degradation**: Handle partial failures gracefully

## Advanced Integration Patterns

### MCP Server Factory Pattern
```typescript
// Factory for creating MCP servers with different capabilities
class McpServerFactory {
  static createServer(type: 'minimal' | 'workflow' | 'notification' | 'production') {
    const baseConfig = { name: `${type}-server`, version: "1.0.0" };
    
    switch (type) {
      case 'minimal':
        return new Server(baseConfig, { capabilities: { tools: {} } });
      case 'workflow':
        return new Server(baseConfig, { capabilities: { resources: {} } });
      case 'notification':
        return new Server(baseConfig, { capabilities: { tools: {}, notifications: {} } });
      case 'production':
        return new Server(baseConfig, { 
          capabilities: { tools: {}, resources: {}, notifications: {} }
        });
    }
  }
}
```

### Middleware Pattern for MCP Tools
```typescript
// Middleware pattern for common tool functionality
const withLogging = (toolHandler) => async (request) => {
  const start = Date.now();
  try {
    const result = await toolHandler(request);
    await server.notification({
      method: "notifications/message",
      params: {
        level: "info",
        logger: "ToolMiddleware",
        data: `Tool ${request.params.name} completed in ${Date.now() - start}ms`
      }
    });
    return result;
  } catch (error) {
    await server.notification({
      method: "notifications/message", 
      params: {
        level: "error",
        logger: "ToolMiddleware",
        data: `Tool ${request.params.name} failed: ${error.message}`
      }
    });
    throw error;
  }
};

// Usage
server.setRequestHandler("tools/call", withLogging(async (request) => {
  // Tool implementation
}));
```

## Final Implementation Notes

**🎯 Key Takeaway**: Cline's MCP integration is one of the most sophisticated implementations available, providing multiple transport options, real-time notifications, workflow integration, and comprehensive development support. Building MCP servers that fully leverage these capabilities requires understanding all the architectural patterns documented in this knowledge base.

**🚀 Next Steps for MCP Developers**:
1. Start with the minimal server example for basic functionality
2. Add notification support for real-time user feedback  
3. Implement resource system for workflow integration
4. Design production-ready configuration and error handling
5. Test across all three transport types
6. Integrate with Cline's development workflow tools

This comprehensive knowledge base provides all the technical details needed to build MCP servers that seamlessly integrate with Cline's advanced capabilities, from basic tool execution to sophisticated real-time communication and workflow automation systems.
