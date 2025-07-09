<!-- CACHE_METADATA_START -->
<!-- Source File: {PROJECT_ROOT}/.knowledge/git-clones/cline/esbuild.js -->
<!-- Cached On: 2025-07-09T04:56:05.036707 -->
<!-- Source Modified: 2025-06-27T12:14:47.917888 -->
<!-- Cache Version: 1.0 -->
<!-- CACHE_METADATA_END -->

#### Functional Intent & Features

This file serves as an `esbuild` bundler configuration script that automates TypeScript compilation and asset bundling for both VSCode extension and standalone application builds through customizable build pipelines. The script provides dual build target support via `extensionConfig` and `standaloneConfig` objects, TypeScript path alias resolution through `aliasResolverPlugin` with mappings for `@`, `@api`, `@core`, `@integrations`, `@services`, `@shared`, `@utils`, and `@packages`, and automated WASM file copying via `copyWasmFiles` plugin for Tree-sitter language parsers. Key semantic entities include `esbuild` bundler, `aliasResolverPlugin` custom plugin, `esbuildProblemMatcherPlugin` error reporter, `copyWasmFiles` asset plugin, `baseConfig` shared configuration, `extensionConfig` VSCode build, `standaloneConfig` independent build, `main()` async function, `process.argv` command line parsing, `--production`, `--watch`, `--standalone` flags, `tree-sitter.wasm` parser, and language-specific WASM files for `typescript`, `tsx`, `python`, `rust`, `javascript`, `go`, `cpp`, `c`, `c_sharp`, `ruby`, `java`, `php`, `swift`, and `kotlin`. The configuration implements comprehensive build automation through plugin-based architecture, enabling development and production builds with watch mode support and asset management.

##### Main Components

The script contains seven primary components: command line argument processing using `process.argv.includes()` for `--production`, `--watch`, and `--standalone` flags, TypeScript path alias resolution plugin `aliasResolverPlugin` with file system-based module resolution, build problem matcher plugin `esbuildProblemMatcherPlugin` providing console output for build events, WASM file copying plugin `copyWasmFiles` handling Tree-sitter parser assets, shared base configuration `baseConfig` with common build settings, target-specific configurations `extensionConfig` and `standaloneConfig` for different deployment scenarios, and main execution function `main()` orchestrating the build process with context management and error handling.

###### Architecture & Design

The architecture follows a plugin-based build system design that separates concerns through modular esbuild plugins and configuration inheritance. The design implements dual build targets using configuration composition where `baseConfig` provides shared settings and target-specific configs extend with unique requirements. The architecture uses custom plugin development through esbuild's plugin API with `setup()` functions and lifecycle hooks like `onResolve`, `onStart`, and `onEnd`. The structure provides flexible build modes through command line flag detection and conditional configuration application, enabling development, production, and watch mode variations.

####### Implementation Approach

The implementation uses esbuild's context API with `esbuild.context()` for build management and `watch()` or `rebuild()` methods for execution control. The approach employs custom plugin development using regular expressions for alias matching and file system operations for module resolution. Path alias resolution uses `Object.entries()` iteration with `RegExp` pattern matching and `fs.existsSync()` validation for module discovery. The strategy includes asset management through post-build file copying using `fs.copyFileSync()` for WASM files and directory traversal for language-specific parsers. Error handling uses async/await patterns with `.catch()` for build process management.

######## External Dependencies & Integration Points

**→ Inbound:**
- `esbuild` (external library) - JavaScript bundler providing compilation, minification, and plugin architecture
- `fs` (external library) - Node.js file system module for file operations and asset copying
- `path` (external library) - Node.js path manipulation module for cross-platform path resolution
- `tsconfig.json` - TypeScript compiler configuration referenced by build process
- `src/extension.ts` - VSCode extension entry point for extension build target
- `src/standalone/standalone.ts` - standalone application entry point for independent builds
- `node_modules/web-tree-sitter/` directory - Tree-sitter WASM runtime files
- `node_modules/tree-sitter-wasms/out/` directory - language-specific parser WASM files
- `vscode` (external library) - VSCode extension API excluded from bundling
- `@grpc/reflection` (external library) - gRPC reflection service excluded from standalone bundle
- `grpc-health-check` (external library) - gRPC health checking excluded from standalone bundle

######### Edge Cases & Error Handling

The script handles missing module resolution through fallback mechanisms in `aliasResolverPlugin` where failed path resolution returns the original path for esbuild error handling. Edge cases include directory vs file resolution using `fs.statSync()` and `stats.isDirectory()` checks with index file discovery across multiple extensions. The framework manages build errors through `esbuildProblemMatcherPlugin` with structured error reporting including file location and error text. Asset copying handles missing WASM files through direct file system operations without explicit error checking, relying on Node.js built-in error propagation.

########## Internal Implementation Details

The `aliasResolverPlugin` uses `build.onResolve()` with regex filters to intercept module resolution and applies file system checks with extension fallbacks for `.ts`, `.tsx`, `.js`, and `.jsx` files. The `copyWasmFiles` plugin executes during `build.onEnd()` lifecycle, copying Tree-sitter runtime and language-specific WASM files to the destination directory. Configuration objects use spread operator inheritance with `...baseConfig` for shared settings and target-specific overrides for `entryPoints`, `outfile`, and `external` dependencies. The `main()` function uses conditional configuration selection based on `standalone` flag and manages build context lifecycle with proper disposal.

########### Code Usage Examples

To execute a development build with watch mode, developers run the script with appropriate flags:

```bash
node esbuild.js --watch
```

This command starts the build process in watch mode, automatically rebuilding when source files change and providing console output for build status and errors.

For creating a production standalone build, developers combine multiple flags:

```bash
node esbuild.js --production --standalone
```

This example demonstrates production build configuration with minification enabled and standalone target selection, generating optimized bundles for independent deployment scenarios.