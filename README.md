# Bithumb MCP Server
[![MCP Server](https://badge.mcpx.dev?type=server)](https://modelcontextprotocol.io/introduction)
[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

This is a Model Context Protocol (MCP) server for Bithumb, allowing LLMs like Claude to interact with the Bithumb trading API. It enables trading stocks, checking positions, fetching market data, and managing your account - all through natural language.

It relies on Bithumb API 2.1 which is currently in beta version.
up to date for API 2.1

## Prerequisites

## Installation
```
# Clone the repository
git clone https://https://github.com/kahngjoonkoh/bithumb-mcp

# Navigate into the project directory
cd bithumb-mcp

# Synchronize dependencies
uv sync --dev --all-extras
```

```
fastmcp install server.py \
    -e API_KEY_ID=<YOUR_API_KEY> \
    -e API_SECRET_KEY=<YOUR_API_SECRET_KEY>
```
