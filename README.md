# MCP LLM client

<div align = center>

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/pypi/v/mcp-llm-client?color=%2334D058&label=Version)](https://pypi.org/project/mcp-llm-client)
[![Last commit](https://img.shields.io/github/last-commit/rb58853/python-mcp-client.svg?style=flat)](https://github.com/rb58853/python-mcp-client/commits)
[![Commit activity](https://img.shields.io/github/commit-activity/m/rb58853/python-mcp-client)](https://github.com/rb58853/python-mcp-client/commits)
[![Stars](https://img.shields.io/github/stars/rb58853/python-mcp-client?style=flat&logo=github)](https://github.com/rb58853/python-mcp-client/stargazers)
[![Forks](https://img.shields.io/github/forks/rb58853/python-mcp-client?style=flat&logo=github)](https://github.com/rb58853/python-mcp-client/network/members)
[![Watchers](https://img.shields.io/github/watchers/rb58853/python-mcp-client?style=flat&logo=github)](https://github.com/rb58853/python-mcp-client)
[![Contributors](https://img.shields.io/github/contributors/rb58853/python-mcp-client)](https://github.com/rb58853/python-mcp-client/graphs/contributors)

</div>

Python client, based on [`fastmcp`](https://github.com/modelcontextprotocol/python-sdk), for connecting to MCP servers through multiple protocols, specifically designed to work with integrated language models.

## Table of Contents

* [Overview](#overview)
* [Installation](#installation)
* [Implemented Models](#implemented-models)
* [Implemented Transfer Protocols](#implemented-transfer-protocols)
* [System Requirements](#system-requirements)
* [Usage Example](#usage-example)
* [Version History](#version-history)
* [Project Status](#project-status)
* [License](#license)

## Overview

This package provides a Python interface to connect to MCP servers in an easy, intuitive, and configurable way. It offers a modular architecture that allows for easy extension of new transfer protocols and language models. Currently includes support for HTTPStream and GPT-4 mini, with expansion capability for more options in the future.

## Installation

To install the MCP client, you can use pip:

```bash
pip install mcp-llm-client
```

## Implemented Models

The client currently supports the following language models:

| Model | Technical Description |
| --- | --- |
| gpt4o-mini | Optimized implementation of the GPT-4 model that provides a balance between computational performance and resource efficiency. This model is specifically designed to operate in environments with memory constraints while maintaining superior predictive quality. |

>🚨 **CRITICAL CONFIGURATION NOTE** Currently, this project only work with `gpt4o-mini` llm model.

## Implemented Transfer Protocols

Protocols for communication with MCP servers:

| Protocol | Status | Technical Characteristics |
| --- | --- | --- |
| HTTPStream | Implemented | Asynchronous HTTP-based protocol that enables continuous data streaming. Characterized by low memory consumption and real-time processing capability for partial responses. |
| SSE (Server-Sent Events) | Not Implemented | Unidirectional protocol that allows the server to send multiple updated events through a single HTTP connection. Designed specifically for applications requiring real-time updates from the server. |
| stdio | Not Implemented | Standard input/output interface that facilitates direct communication between processes. Will provide a lightweight alternative for local environments and unit testing. |

>🚨 **CRITICAL CONFIGURATION NOTE** Currently, this project only work with `HTTPStream` protocol.

## Future Development Planning

### Pending Language Models

* Integration of additional language models
* Implementation of dynamic model selection system
* Optimization of model loading and management

### Pending Protocols

* Complete implementation of SSE for better real-time event handling
* Development of stdio interface for local environments
* Performance optimization across all protocols

## System Requirements

### Environmental Configuration

* **`.env` file**: The `.env` file contains the authentication credentials necessary for integration with external services. This file must be created in the project root directory with the following format:

    ```env
    # .env
    # OpenAI Authentication
    OPENAI_API_KEY=<YOUR OPENAI-API-KEY>
    ```

* **`config.json` file**: The `config.json` file defines the configuration of available MCP servers. It must be created in the project root directory with the following structure:

    ```json
    {
        "mcp_servers": {
            "example_public_server": {
                "transport": "httpstream",
                "httpstream-url": "http://127.0.0.1:8000/public-example-server/mcp",
                "name": "example-public-server",
                "description": "Example public server."
            },
            "example_private_mcp": {
                "transport": "httpstream",
                "httpstream-url": "http://127.0.0.1:8000/private-example-server/mcp",
                "name": "example-private-server",
                "description": "Example private server with oauth required.",
                "auth": {
                    "required": true,
                    "server": "http://127.0.0.1:9000",
                    "secrets": {
                        "username": "user",
                        "password": "password"
                    }
                }
            }
        }
    }
    ```

    If you need an MCP server to test the code, you can use [simple-mcp-server](https://github.com/rb58853/simple-mcp-server).

### Dependencies

* `Python = ">=3.11"`
* `openai = "^1.68.2"`
* `"mcp[cli]"`
* `mcp-oauth`

## Usage Example

```python
#example1.py
from mcpclient import open_local_chat
open_local_chat()
```

```python
#example2.py
from mcpclient import Chat
chat: Chat = Chat()
while True:
    query = input("> ")
    if query == "":
        break
    for step in chat(query):
        print(f"<< {step.json}")
```

Alternatively, you may test this service using the following [template available on GitHub](https://github.com/rb58853/template_mcp_llm_client):

```shell
# clone repo
git clone https://github.com/rb58853/template_mcp_llm_client.git

# change to project dir
cd template_mcp_llm_client

# install dependencies
pip install -r requirements.txt

# open in vscode
code .
```

## Version History

### v0.0.1

* Initial implementation of `Chat` client
* Complete integration of `httpstream` protocol ([fasmcp](https://github.com/modelcontextprotocol/python-sdk))
* Connectivity with multiple servers
* Simplified config.json file for connection management
* Efficient processing of multiple simultaneous requests to tools and resources within a single query
* Simple connection without authorization (compatible only with servers that do not require authentication)

### v0.0.4

* Package dependencies are incorporated during its initial installation process.

### v0.0.5

* The LLM system is structured in steps, with each step being returned to the client making the query. This approach allows for the identification of the current stage within the query process.
* Efficient language detection has been implemented for queries, enabling responses to be provided based on the detected language.
* The `open_local_chat()` function has been added, making it easy to use a local chat.

### v0.0.6

* The exposed services have been added to the context of all queries, including those that do not require the use of a specific service. This approach allows for general inquiries regarding the available services.

### v0.0.7

* A simple authorization system based on user credential authentication (username and password) was integrated. For further reference, please see [mcp-oauth](https://github.com/rb58853/mcp-oauth).

## Project Status
>
>⚠️ **Important Notice:** This project is currently in active development phase. As a result, errors or unexpected behaviors may occur during usage

## License

MIT License. See [`license`](license).
