# Monorepo Structure

## B1. ASCII Tree

```
dofus-bot/
├── core/
│   ├── src/
│   │   ├── lua_bindings.rs
│   │   ├── mitm_parser.rs
│   │   ├── scheduler.rs
│   │   └── main.rs
│   ├── Cargo.toml
│   ├── Cargo.lock
│   └── tests/
│       └── unit_tests.rs
├── orchestrator/
│   ├── src/
│   │   ├── api/
│   │   │   ├── specs/
│   │   │   │   ├── bot_api.yaml
│   │   │   │   └── sandbox_rpc.proto
│   │   ├── config/
│   │   │   ├── sandbox.yml
│   │   │   └── app.yml
│   │   ├── sandbox/
│   │   │   ├── runner.py
│   │   │   ├── policies/
│   │   │   │   ├── seccomp.json
│   │   │   │   ├── cgroup.conf
│   │   │   │   └── firejail.profile
│   │   │   └── socket.py
│   │   ├── main.py
│   │   └── utils.py
│   ├── requirements.txt
│   ├── pyproject.toml
│   └── tests/
│       └── integration_tests.py
├── ui/
│   ├── src/
│   │   ├── components/
│   │   │   ├── App.svelte
│   │   │   └── Dashboard.svelte
│   │   ├── stores/
│   │   │   └── state.js
│   │   ├── main.js
│   │   └── app.html
│   ├── package.json
│   ├── rollup.config.js
│   └── tests/
│       └── e2e_tests.js
├── scripts/
│   ├── templates/
│   │   ├── lua/
│   │   │   └── sample_script.lua
│   │   └── python/
│   │       └── sample_plugin.py
│   ├── build.sh
│   └── deploy.sh
├── infra/
│   ├── docker/
│   │   ├── Dockerfile.core
│   │   ├── Dockerfile.orchestrator
│   │   └── docker-compose.yml
│   ├── k8s/
│   │   └── deployment.yaml
│   └── ansible/
│       └── playbook.yml
├── tests/
│   ├── sandbox/
│   │   └── test_filesystem_block.py
│   ├── e2e/
│   │   └── full_flow_test.py
│   └── unit/
│       └── core_tests.rs
├── docs/
│   ├── diagrams/
│   │   ├── component-diagram.puml
│   │   ├── sequence-mitm.puml
│   │   ├── sequence-ui_automation.puml
│   │   ├── sandbox-flow.puml
│   │   ├── component-diagram.svg
│   │   ├── sequence-mitm.svg
│   │   ├── sequence-ui_automation.svg
│   │   ├── sandbox-flow.svg
│   │   └── README.md
│   ├── repo_tree.md
│   └── REPO_GUIDE.md
├── ci/
│   ├── gh-actions/
│   │   ├── build.yml
│   │   ├── test.yml
│   │   └── release.yml
│   └── scripts/
│       └── ci_setup.sh
├── packaging/
│   ├── windows/
│   │   └── build_msi.sh
│   ├── linux/
│   │   └── build_appimage.sh
│   └── macos/
│       └── build_dmg.sh
├── examples/
│   ├── pcap/
│   │   └── sample.pcap
│   ├── scripts/
│   │   ├── lua_example.lua
│   │   └── python_example.py
│   └── configs/
│       └── sample_config.yml
├── README.md
├── LICENSE
└── .gitignore
```

## B2. File/Folder Descriptions

- **core/**: Directory for Rust core components. Type: code. Purpose: Houses high-performance Rust modules for parsing and scheduling. Primary owner: Rust. Security notes: None.
- **core/src/**: Source code directory. Type: code. Purpose: Contains Rust source files. Primary owner: Rust. Security notes: None.
- **core/src/lua_bindings.rs**: File for Lua VM integration. Type: code. Purpose: Implements bindings between Rust and embedded Lua VM. Primary owner: Rust. Security notes: Sandboxed execution.
- **core/src/mitm_parser.rs**: File for MITM packet parsing. Type: code. Purpose: Parses intercepted network packets. Primary owner: Rust. Security notes: Requires network privileges.
- **core/src/scheduler.rs**: File for bot scheduling logic. Type: code. Purpose: Manages task scheduling and execution. Primary owner: Rust. Security notes: None.
- **core/src/main.rs**: Entry point for Rust core. Type: code. Purpose: Initializes and runs the core engine. Primary owner: Rust. Security notes: None.
- **core/Cargo.toml**: Rust package manifest. Type: config. Purpose: Defines dependencies and build settings. Primary owner: Rust. Security notes: None. Required template: Standard Cargo.toml.
- **core/Cargo.lock**: Dependency lock file. Type: config. Purpose: Locks dependency versions. Primary owner: Rust. Security notes: None.
- **core/tests/**: Test directory. Type: code. Purpose: Contains unit tests for Rust code. Primary owner: Rust. Security notes: None.
- **core/tests/unit_tests.rs**: Unit test file. Type: code. Purpose: Tests individual Rust functions. Primary owner: Rust. Security notes: None.
- **orchestrator/**: Directory for Python orchestrator. Type: code. Purpose: Coordinates between components and manages sandboxes. Primary owner: Python. Security notes: None.
- **orchestrator/src/**: Source code directory. Type: code. Purpose: Contains Python source files. Primary owner: Python. Security notes: None.
- **orchestrator/src/api/**: API definitions. Type: code. Purpose: Defines APIs for communication. Primary owner: Python. Security notes: None.
- **orchestrator/src/api/specs/**: API specification files. Type: config. Purpose: Holds OpenAPI and proto files. Primary owner: Python. Security notes: None.
- **orchestrator/src/api/specs/bot_api.yaml**: OpenAPI spec for bot API. Type: config. Purpose: Defines REST endpoints. Primary owner: Python. Security notes: None. Required template: OpenAPI 3.0 schema.
- **orchestrator/src/api/specs/sandbox_rpc.proto**: gRPC proto for sandbox RPC. Type: config. Purpose: Defines RPC messages. Primary owner: Python. Security notes: None. Required template: Protocol Buffers schema.
- **orchestrator/src/config/**: Configuration directory. Type: config. Purpose: Stores config files. Primary owner: Python. Security notes: None.
- **orchestrator/src/config/sandbox.yml**: Sandbox configuration. Type: config. Purpose: Defines sandbox limits and policies. Primary owner: Python. Security notes: Enforces resource isolation. Required template: YAML schema.
- **orchestrator/src/config/app.yml**: Application config. Type: config. Purpose: General app settings. Primary owner: Python. Security notes: None. Required template: YAML schema.
- **orchestrator/src/sandbox/**: Sandbox implementation. Type: code. Purpose: Manages Python sandbox execution. Primary owner: Python. Security notes: Isolated subprocess.
- **orchestrator/src/sandbox/runner.py**: Sandbox runner script. Type: code. Purpose: Executes Python plugins in sandbox. Primary owner: Python. Security notes: Resource limits applied.
- **orchestrator/src/sandbox/policies/**: Policy files directory. Type: config. Purpose: Contains security policies. Primary owner: Python. Security notes: Critical for sandbox security.
- **orchestrator/src/sandbox/policies/seccomp.json**: Seccomp profile. Type: config. Purpose: Restricts system calls. Primary owner: Python. Security notes: Prevents privilege escalation.
- **orchestrator/src/sandbox/policies/cgroup.conf**: Cgroup config. Type: config. Purpose: Limits resources. Primary owner: Python. Security notes: Enforces CPU/memory limits.
- **orchestrator/src/sandbox/policies/firejail.profile**: Firejail profile. Type: config. Purpose: Sandboxing rules. Primary owner: Python. Security notes: Filesystem and network isolation.
- **orchestrator/src/sandbox/socket.py**: Socket communication. Type: code. Purpose: Handles IPC via sockets. Primary owner: Python. Security notes: Localhost only.
- **orchestrator/src/main.py**: Orchestrator entry point. Type: code. Purpose: Starts the orchestrator service. Primary owner: Python. Security notes: None.
- **orchestrator/src/utils.py**: Utility functions. Type: code. Purpose: Shared helpers. Primary owner: Python. Security notes: None.
- **orchestrator/requirements.txt**: Python dependencies. Type: config. Purpose: Lists required packages. Primary owner: Python. Security notes: None.
- **orchestrator/pyproject.toml**: Python project config. Type: config. Purpose: Build and dependency management. Primary owner: Python. Security notes: None.
- **orchestrator/tests/**: Test directory. Type: code. Purpose: Integration tests. Primary owner: Python. Security notes: None.
- **orchestrator/tests/integration_tests.py**: Integration test file. Type: code. Purpose: Tests component interactions. Primary owner: Python. Security notes: None.
- **ui/**: Directory for Electron/Svelte UI. Type: code. Purpose: User interface components. Primary owner: Svelte. Security notes: None.
- **ui/src/**: Source code directory. Type: code. Purpose: Contains UI source files. Primary owner: Svelte. Security notes: None.
- **ui/src/components/**: Component files. Type: code. Purpose: Svelte components. Primary owner: Svelte. Security notes: None.
- **ui/src/components/App.svelte**: Main app component. Type: code. Purpose: Root component. Primary owner: Svelte. Security notes: None.
- **ui/src/components/Dashboard.svelte**: Dashboard component. Type: code. Purpose: Displays bot status. Primary owner: Svelte. Security notes: None.
- **ui/src/stores/**: State management. Type: code. Purpose: Svelte stores. Primary owner: Svelte. Security notes: None.
- **ui/src/stores/state.js**: State store. Type: code. Purpose: Manages app state. Primary owner: Svelte. Security notes: None.
- **ui/src/main.js**: UI entry point. Type: code. Purpose: Initializes Svelte app. Primary owner: Svelte. Security notes: None.
- **ui/src/app.html**: HTML template. Type: code. Purpose: Electron main window. Primary owner: Svelte. Security notes: None.
- **ui/package.json**: Node dependencies. Type: config. Purpose: Defines UI dependencies. Primary owner: Svelte. Security notes: None.
- **ui/rollup.config.js**: Build config. Type: config. Purpose: Rollup bundler settings. Primary owner: Svelte. Security notes: None.
- **ui/tests/**: Test directory. Type: code. Purpose: E2E tests. Primary owner: Svelte. Security notes: None.
- **ui/tests/e2e_tests.js**: E2E test file. Type: code. Purpose: Tests UI interactions. Primary owner: Svelte. Security notes: None.
- **scripts/**: Directory for build and utility scripts. Type: code. Purpose: Automation scripts. Primary owner: Shell. Security notes: None.
- **scripts/templates/**: Template directory. Type: code. Purpose: Example scripts. Primary owner: Lua/Python. Security notes: None.
- **scripts/templates/lua/**: Lua templates. Type: code. Purpose: Sample Lua scripts. Primary owner: Lua. Security notes: Sandboxed.
- **scripts/templates/lua/sample_script.lua**: Sample Lua script. Type: code. Purpose: Template for user scripts. Primary owner: Lua. Security notes: None.
- **scripts/templates/python/**: Python templates. Type: code. Purpose: Sample Python plugins. Primary owner: Python. Security notes: Sandboxed.
- **scripts/templates/python/sample_plugin.py**: Sample Python plugin. Type: code. Purpose: Template for plugins. Primary owner: Python. Security notes: None.
- **scripts/build.sh**: Build script. Type: code. Purpose: Compiles the project. Primary owner: Shell. Security notes: None.
- **scripts/deploy.sh**: Deploy script. Type: code. Purpose: Deploys the application. Primary owner: Shell. Security notes: None.
- **infra/**: Directory for infrastructure. Type: config. Purpose: Deployment configurations. Primary owner: DevOps. Security notes: None.
- **infra/docker/**: Docker files. Type: config. Purpose: Container definitions. Primary owner: DevOps. Security notes: None.
- **infra/docker/Dockerfile.core**: Core container. Type: config. Purpose: Builds Rust core image. Primary owner: DevOps. Security notes: None.
- **infra/docker/Dockerfile.orchestrator**: Orchestrator container. Type: config. Purpose: Builds Python orchestrator image. Primary owner: DevOps. Security notes: None.
- **infra/docker/docker-compose.yml**: Compose file. Type: config. Purpose: Multi-container setup. Primary owner: DevOps. Security notes: None.
- **infra/k8s/**: Kubernetes manifests. Type: config. Purpose: K8s deployments. Primary owner: DevOps. Security notes: None.
- **infra/k8s/deployment.yaml**: Deployment manifest. Type: config. Purpose: Defines pods. Primary owner: DevOps. Security notes: None.
- **infra/ansible/**: Ansible playbooks. Type: config. Purpose: Configuration management. Primary owner: DevOps. Security notes: None.
- **infra/ansible/playbook.yml**: Ansible playbook. Type: config. Purpose: Automates setup. Primary owner: DevOps. Security notes: None.
- **tests/**: Directory for all tests. Type: code. Purpose: Test suites. Primary owner: Various. Security notes: None.
- **tests/sandbox/**: Sandbox tests. Type: code. Purpose: Tests sandbox isolation. Primary owner: Python. Security notes: Validates security.
- **tests/sandbox/test_filesystem_block.py**: Filesystem block test. Type: code. Purpose: Ensures filesystem restrictions. Primary owner: Python. Security notes: None.
- **tests/e2e/**: E2E tests. Type: code. Purpose: End-to-end flows. Primary owner: Python. Security notes: None.
- **tests/e2e/full_flow_test.py**: Full flow test. Type: code. Purpose: Tests complete bot operation. Primary owner: Python. Security notes: None.
- **tests/unit/**: Unit tests. Type: code. Purpose: Unit tests for core. Primary owner: Rust. Security notes: None.
- **tests/unit/core_tests.rs**: Core unit tests. Type: code. Purpose: Tests Rust functions. Primary owner: Rust. Security notes: None.
- **docs/**: Directory for documentation. Type: docs. Purpose: Project docs. Primary owner: Markdown. Security notes: None.
- **docs/diagrams/**: Diagram files. Type: docs. Purpose: Architecture diagrams. Primary owner: PlantUML. Security notes: None.
- **docs/diagrams/component-diagram.puml**: Component diagram source. Type: docs. Purpose: PlantUML for components. Primary owner: PlantUML. Security notes: None.
- **docs/diagrams/sequence-mitm.puml**: MITM sequence source. Type: docs. Purpose: PlantUML for MITM flow. Primary owner: PlantUML. Security notes: None.
- **docs/diagrams/sequence-ui_automation.puml**: UI automation sequence source. Type: docs. Purpose: PlantUML for UI fallback. Primary owner: PlantUML. Security notes: None.
- **docs/diagrams/sandbox-flow.puml**: Sandbox flow source. Type: docs. Purpose: PlantUML for sandboxes. Primary owner: PlantUML. Security notes: None.
- **docs/diagrams/component-diagram.svg**: Component diagram SVG. Type: docs. Purpose: Rendered diagram. Primary owner: SVG. Security notes: None.
- **docs/diagrams/sequence-mitm.svg**: MITM sequence SVG. Type: docs. Purpose: Rendered diagram. Primary owner: SVG. Security notes: None.
- **docs/diagrams/sequence-ui_automation.svg**: UI automation sequence SVG. Type: docs. Purpose: Rendered diagram. Primary owner: SVG. Security notes: None.
- **docs/diagrams/sandbox-flow.svg**: Sandbox flow SVG. Type: docs. Purpose: Rendered diagram. Primary owner: SVG. Security notes: None.
- **docs/diagrams/README.md**: Diagram explanations. Type: docs. Purpose: Describes diagrams. Primary owner: Markdown. Security notes: None.
- **docs/repo_tree.md**: Repo structure doc. Type: docs. Purpose: Details file structure. Primary owner: Markdown. Security notes: None.
- **docs/REPO_GUIDE.md**: Repo guide. Type: docs. Purpose: Conventions and guidelines. Primary owner: Markdown. Security notes: None.
- **ci/**: Directory for CI/CD. Type: config. Purpose: Continuous integration. Primary owner: YAML. Security notes: None.
- **ci/gh-actions/**: GitHub Actions. Type: config. Purpose: Workflow definitions. Primary owner: YAML. Security notes: None.
- **ci/gh-actions/build.yml**: Build workflow. Type: config. Purpose: Compiles code. Primary owner: YAML. Security notes: None.
- **ci/gh-actions/test.yml**: Test workflow. Type: config. Purpose: Runs tests. Primary owner: YAML. Security notes: None.
- **ci/gh-actions/release.yml**: Release workflow. Type: config. Purpose: Handles releases. Primary owner: YAML. Security notes: None.
- **ci/scripts/**: CI scripts. Type: code. Purpose: Setup scripts. Primary owner: Shell. Security notes: None.
- **ci/scripts/ci_setup.sh**: CI setup script. Type: code. Purpose: Prepares CI environment. Primary owner: Shell. Security notes: None.
- **packaging/**: Directory for packaging. Type: code. Purpose: Build packages. Primary owner: Shell. Security notes: None.
- **packaging/windows/**: Windows packaging. Type: code. Purpose: MSI builds. Primary owner: Shell. Security notes: None.
- **packaging/windows/build_msi.sh**: MSI build script. Type: code. Purpose: Creates Windows installer. Primary owner: Shell. Security notes: None.
- **packaging/linux/**: Linux packaging. Type: code. Purpose: AppImage builds. Primary owner: Shell. Security notes: None.
- **packaging/linux/build_appimage.sh**: AppImage build script. Type: code. Purpose: Creates Linux package. Primary owner: Shell. Security notes: None.
- **packaging/macos/**: macOS packaging. Type: code. Purpose: DMG builds. Primary owner: Shell. Security notes: None.
- **packaging/macos/build_dmg.sh**: DMG build script. Type: code. Purpose: Creates macOS package. Primary owner: Shell. Security notes: None.
- **examples/**: Directory for examples. Type: docs. Purpose: Sample files. Primary owner: Various. Security notes: None.
- **examples/pcap/**: PCAP samples. Type: docs. Purpose: Example packet captures. Primary owner: PCAP. Security notes: None.
- **examples/pcap/sample.pcap**: Sample PCAP. Type: docs. Purpose: Demonstrates packet format. Primary owner: PCAP. Security notes: None.
- **examples/scripts/**: Example scripts. Type: code. Purpose: Sample user scripts. Primary owner: Lua/Python. Security notes: Sandboxed.
- **examples/scripts/lua_example.lua**: Lua example. Type: code. Purpose: Illustrates Lua scripting. Primary owner: Lua. Security notes: None.
- **examples/scripts/python_example.py**: Python example. Type: code. Purpose: Illustrates Python plugins. Primary owner: Python. Security notes: None.
- **examples/configs/**: Example configs. Type: config. Purpose: Sample configurations. Primary owner: YAML. Security notes: None.
- **examples/configs/sample_config.yml**: Sample config. Type: config. Purpose: Template for user config. Primary owner: YAML. Security notes: None.
- **README.md**: Project readme. Type: docs. Purpose: Overview and setup. Primary owner: Markdown. Security notes: None.
- **LICENSE**: License file. Type: docs. Purpose: Legal terms. Primary owner: Text. Security notes: None.
- **.gitignore**: Git ignore rules. Type: config. Purpose: Excludes files from git. Primary owner: Git. Security notes: None.

## B3. Sandbox Mapping

- Lua bindings: `core/src/lua_bindings.rs`
- Python sandbox runner: `orchestrator/src/sandbox/runner.py`
- Sandbox policy files: `orchestrator/src/sandbox/policies/seccomp.json` (seccomp syscall restrictions), `orchestrator/src/sandbox/policies/cgroup.conf` (resource limits), `orchestrator/src/sandbox/policies/firejail.profile` (filesystem/network isolation).
- Communication sockets: Unix domain socket at `/tmp/dofus_sandbox.sock` for Lua; TCP localhost port 50051 for Python gRPC.

## B4. IPC & API Placeholders

- `orchestrator/api/specs/bot_api.yaml`: OpenAPI spec for REST API. Endpoints: /start (POST), /stop (POST), /status (GET), /run_script (POST), /get_state (GET).
- `orchestrator/api/specs/sandbox_rpc.proto`: gRPC proto for sandbox RPC. Messages: ExecRequest (script, args), ExecResponse (result, error), StreamLogs (log_line).

## B5. CI / Packaging Skeleton

- `ci/gh-actions/build.yml`: Defines build pipeline for multi-language project.
- `ci/gh-actions/test.yml`: Runs unit and integration tests across components.
- `ci/gh-actions/release.yml`: Automates versioning and artifact publishing.
- `packaging/windows/build_msi.sh`: Script to build MSI installer for Windows.
- `packaging/linux/build_appimage.sh`: Script to build AppImage for Linux.
- `packaging/macos/build_dmg.sh`: Script to build DMG for macOS.

## B6. Examples & Templates

- `scripts/templates/lua/`: Directory for Lua script templates.
- `scripts/templates/python/`: Directory for Python plugin templates.
- `examples/pcap/sample.pcap`: Example packet capture file.
- `tests/sandbox/test_filesystem_block.py`: Test for sandbox filesystem blocking.