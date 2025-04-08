# Bithumb MCP Server
[![MCP Server](https://badge.mcpx.dev?type=server)](https://modelcontextprotocol.io/introduction)
[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

This is a Model Context Protocol (MCP) server for Bithumb, allowing LLMs like Claude to interact with the Bithumb trading API. It enables trading stocks, checking positions, fetching market data, and managing your account - all through natural language.

It relies on Bithumb API v2.1.0. Will soon to have support for v2.1.5 which is currently in beta version.

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
This should automatically configure your `claude_desktop_config.json` file.

## Example Queries
* What's my current account balance?
* Get me a snapshot for SUI
* Show me the price history for SUI over the last 100 days
* Buy 10000 KRW worth of SUI at a limit price of 2600 KRW
* Analyse the orderbook and give me a rough estimate of the chances for the price of SUI going up or down. 
* Cancel all my open orders.

## !! NOTICE !!
This MCP server will have access to real trades. The developers of this server will not be held accountable for mistakes or bad decision making.

## License
This project is licensed under the [MIT License](https://github.com/kahngjoonkoh/pybithumb2/blob/main/LICENSE). See the [LICENSE](https://github.com/kahngjoonkoh/pybithumb2/blob/main/LICENSE) file for more details.
