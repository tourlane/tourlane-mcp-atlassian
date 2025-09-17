# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**MCP Atlassian** is a Model Context Protocol (MCP) server that integrates Atlassian products (Jira and Confluence) with AI language models. It supports both Cloud and Server/Data Center deployments and provides secure, contextual AI interactions with Atlassian tools.

## Technology Stack

- **Language:** Python 3.10+
- **Framework:** FastMCP for MCP server implementation
- **Key Dependencies:**
  - `atlassian-python-api` - Atlassian API client
  - `mcp` - Model Context Protocol implementation
  - `fastmcp` - Fast MCP server framework
  - `httpx` - HTTP client
  - `click` - CLI framework
  - `pydantic` - Data validation
  - `starlette` - ASGI framework for HTTP transports

## Architecture

### Core Components

The codebase is organized into several key modules:

1. **Entry Point** (`src/mcp_atlassian/__init__.py`): Main CLI interface with Click commands, handles configuration and server startup
2. **Servers** (`src/mcp_atlassian/servers/`):
   - `main.py` - Main FastMCP server setup and lifecycle management
   - `jira.py` - Jira-specific MCP tool implementations
   - `confluence.py` - Confluence-specific MCP tool implementations
   - `dependencies.py` - Shared dependency injection and configuration
3. **Service Clients** (`src/mcp_atlassian/jira/`, `src/mcp_atlassian/confluence/`): API clients and business logic for each service
4. **Models** (`src/mcp_atlassian/models/`): Pydantic models for data validation
5. **Utilities** (`src/mcp_atlassian/utils/`): Cross-cutting concerns like logging, environment handling, OAuth setup

### Authentication Architecture

The server supports multiple authentication methods:
- **API Token** (Cloud): Username + API token
- **Personal Access Token** (Server/Data Center): PAT-based authentication
- **OAuth 2.0** (Cloud): Full OAuth flow with token refresh capabilities
- **Multi-user HTTP Transport**: Per-request authentication via headers

### Transport Layer

Three transport modes are supported:
- **STDIO**: Standard MCP transport for IDE integration
- **SSE**: Server-Sent Events HTTP transport
- **Streamable-HTTP**: Bidirectional HTTP transport

## Development Commands

### Setup and Environment

```bash
# Install dependencies (requires uv)
uv sync
uv sync --frozen --all-extras --dev

# Activate virtual environment
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate.ps1  # Windows

# Set up pre-commit hooks
pre-commit install

# Set up environment variables
cp .env.example .env
```

### Testing

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=mcp_atlassian

# Run specific test files
uv run pytest tests/unit/servers/
uv run pytest tests/integration/
```

### Code Quality

```bash
# Run all pre-commit checks
pre-commit run --all-files

# Individual tools
uv run ruff check .          # Linting
uv run ruff format .         # Formatting
uv run mypy src/             # Type checking (disabled by default, use pyright)
```

### Running the Server

```bash
# STDIO transport (for IDE integration)
uv run mcp-atlassian

# HTTP transports for testing
uv run mcp-atlassian --transport sse --port 9000 -vv
uv run mcp-atlassian --transport streamable-http --port 9000 -vv

# OAuth setup wizard
uv run mcp-atlassian --oauth-setup -v

# Using environment file
uv run mcp-atlassian --env-file .env.production
```

### Docker Development

```bash
# Build image
docker build -t mcp-atlassian .

# Run with environment file
docker run --rm --env-file .env mcp-atlassian

# Run with HTTP transport
docker run --rm -p 9000:9000 --env-file .env mcp-atlassian --transport sse --port 9000
```

## Code Structure and Patterns

### Configuration Management

Configuration follows a precedence pattern:
1. CLI arguments (highest precedence)
2. Environment variables
3. .env file
4. Default values

Configuration classes use Pydantic for validation and are located in `config.py` files within each service module.

### Tool Registration

MCP tools are registered in the server modules (`servers/jira.py`, `servers/confluence.py`) using the FastMCP framework. Tools are automatically filtered based on:
- `ENABLED_TOOLS` environment variable
- `READ_ONLY_MODE` flag
- Service availability (determined by configuration presence)

### Error Handling

- Custom exceptions inherit from base classes
- HTTP errors are handled gracefully with appropriate MCP error responses
- Sensitive information is masked in logs using `mask_sensitive()` utility

### Async Patterns

The codebase extensively uses Python's async/await patterns:
- All MCP tools are async functions
- HTTP clients use `httpx` for async requests
- Context managers handle resource lifecycle

## Important Development Notes

### Authentication Testing

When testing authentication, use the mock environment variables:
- Set `CONFLUENCE_URL`, `JIRA_URL` to test endpoints
- Use `--oauth-setup` for OAuth flow testing
- HTTP transports support per-request authentication headers

### Pre-commit Hooks

The project uses pre-commit hooks for code quality:
- `ruff` for formatting and linting (88 character line limit)
- `prettier` for YAML/JSON formatting
- `pyright` for type checking (preferred over mypy)
- Various file validation checks

### Testing Considerations

- Unit tests are in `tests/unit/`
- Integration tests require real Atlassian credentials
- Use `conftest.py` fixtures for test setup
- Mock external API calls in unit tests

### Environment Configuration

Key environment variables:
- `MCP_VERBOSE`, `MCP_VERY_VERBOSE` - Logging levels
- `MCP_LOGGING_STDOUT` - Log to stdout instead of stderr
- `READ_ONLY_MODE` - Disable write operations
- `ENABLED_TOOLS` - Filter available tools
- Service-specific variables follow pattern: `SERVICE_SETTING` (e.g., `JIRA_URL`, `CONFLUENCE_API_TOKEN`)

## Build and Distribution

The project uses modern Python packaging:
- `pyproject.toml` for project configuration
- `uv` for dependency management
- `hatchling` for building
- `uv-dynamic-versioning` for Git-based versioning
- Docker multi-stage builds for distribution

## Code Style Guidelines

- Follow the existing patterns for new MCP tools
- Use type hints extensively (required by pre-commit)
- Add docstrings to all public functions using Google style
- Keep line length to 88 characters
- Use `ruff` for consistent formatting