<!-- CACHE_METADATA_START -->
<!-- Source File: {PROJECT_ROOT}/.knowledge/git-clones/cline/buf.yaml -->
<!-- Cached On: 2025-07-09T04:43:16.973427 -->
<!-- Source Modified: 2025-06-27T12:14:47.909889 -->
<!-- Cache Version: 1.0 -->
<!-- CACHE_METADATA_END -->

#### Functional Intent & Features

This file serves as a `buf` configuration for Protocol Buffer linting and code generation within the `cline` project, specifically targeting the `proto/` directory module named `cline/cline/lint`. The configuration establishes standardized protobuf development practices while accommodating project-specific naming conventions through strategic lint rule exceptions. Key semantic entities include `STANDARD` lint ruleset, `RPC_PASCAL_CASE`, `PACKAGE_DIRECTORY_MATCH`, `RPC_REQUEST_RESPONSE_UNIQUE`, `RPC_REQUEST_STANDARD_NAME`, `RPC_RESPONSE_STANDARD_NAME`, `PACKAGE_VERSION_SUFFIX`, `ENUM_VALUE_PREFIX`, and `ENUM_ZERO_VALUE_SUFFIX` exceptions. The configuration uses `v2` schema version and implements selective compliance with protobuf best practices while preserving existing codebase patterns.

##### Main Components

The configuration contains two primary sections: a `modules` declaration defining the protobuf source location and module name, and a comprehensive `lint` configuration section. The modules section specifies a single module at `proto` path with identifier `cline/cline/lint`. The lint section establishes `STANDARD` ruleset usage with eight specific rule exceptions addressing naming conventions, directory structure requirements, and message uniqueness constraints.

###### Architecture & Design

The configuration follows a permissive linting approach, applying industry-standard protobuf conventions while selectively disabling rules that conflict with established project patterns. The design prioritizes backward compatibility and existing code preservation over strict adherence to all standard conventions. The modular structure separates path definitions from linting rules, enabling clear separation of concerns between source organization and code quality enforcement.

####### Implementation Approach

The implementation uses `buf`'s exception-based configuration strategy, starting with comprehensive `STANDARD` ruleset coverage and explicitly removing incompatible rules. Each exception targets specific naming and structural conventions: camelCase RPC naming instead of PascalCase, flexible package directory structures, non-unique request messages, relaxed request/response naming suffixes, version-agnostic package names, and flexible enum naming patterns. A commented `breaking` section indicates potential future wire format compatibility checking.

######## External Dependencies & Integration Points

**→ Inbound:**
- `proto/` directory - contains Protocol Buffer definition files for linting analysis
- `buf` CLI tool (external library) - provides linting engine and rule enforcement
- `STANDARD` ruleset (external library) - buf's predefined comprehensive linting rules

######### Edge Cases & Error Handling

The configuration handles conflicts between standard protobuf conventions and existing codebase patterns through explicit rule exceptions rather than code modifications. Edge cases include scenarios where RPCs use camelCase naming, packages don't match directory structures, request/response messages share names across services, and enums don't follow standard prefixing conventions. The commented breaking change detection suggests awareness of potential wire format compatibility issues during development.

########## Internal Implementation Details

The `v2` configuration schema enables advanced module definitions and granular lint control. The `cline/cline/lint` module name suggests a nested package structure within the broader cline ecosystem. Each exception rule corresponds to specific protobuf style guide violations that would otherwise prevent successful linting. The breaking change section remains disabled, indicating current focus on development velocity over strict compatibility guarantees.

########### Code Usage Examples

To apply this configuration, developers run `buf lint` in the project root, which processes all `.proto` files in the `proto/` directory according to the specified rules:

```bash
buf lint
```

The configuration allows protobuf definitions like:

```protobuf
service MyService {
  rpc getUserData(GetUserRequest) returns (UserResponse);
}
```

This RPC naming (camelCase `getUserData`) would normally violate `RPC_PASCAL_CASE` but is permitted through the exception configuration.