# Fastchat MCP

![alt text](/doc/images/fastchat.png)

<div align = center>

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/pypi/v/fastchat-mcp?color=%2334D058&label=Version)](https://pypi.org/project/fastchat-mcp)
[![PyPI Downloads](https://static.pepy.tech/badge/fastchat-mcp)](https://pepy.tech/projects/fastchat-mcp)
[![Stars](https://img.shields.io/github/stars/rb58853/fastchat-mcp?style=flat&logo=github)](https://github.com/rb58853/fastchat-mcp/stargazers)
[![Forks](https://img.shields.io/github/forks/rb58853/fastchat-mcp?style=flat&logo=github)](https://github.com/rb58853/fastchat-mcp/network/members)
[![Watchers](https://img.shields.io/github/watchers/rb58853/fastchat-mcp?style=flat&logo=github)](https://github.com/rb58853/fastchat-mcp)
[![Contributors](https://img.shields.io/github/contributors/rb58853/fastchat-mcp)](https://github.com/rb58853/fastchat-mcp/graphs/contributors)
[![MSeeP](https://img.shields.io/badge/MSeep-4.3-lima)](https://mseep.ai/app/rb58853-fastchat-mcp)
[![MCP](https://img.shields.io/badge/MCP-Client-orange)](https://modelcontextprotocol.io/quickstart/client)
[![Commit activity](https://img.shields.io/github/commit-activity/m/rb58853/fastchat-mcp)](https://github.com/rb58853/fastchat-mcp/commits)
[![Last commit](https://img.shields.io/github/last-commit/rb58853/fastchat-mcp.svg?style=flat)](https://github.com/rb58853/fastchat-mcp/commits)
[![Version](https://img.shields.io/pypi/v/fastauth-api?color=%234D58&label=fastauth-api)](https://github.com/rb58853/fastauth-api)

</div>

Python chat client, based on [`mcp[cli]`](https://github.com/modelcontextprotocol/python-sdk), for connecting to MCP servers through multiple protocols, specifically designed to work with integrated language models. **Fastchat-mcp** is a very simple way to interact with MCP servers using custom chats through natural language.

## Table of Contents

* [Overview](#overview)
* [Installation](#installation)
* [LLM Implementation](#llm-implementation)
  * [LLM Providers](#llm-providers)
  * [LLM Models](#llm-models)
* [Implemented Transfer Protocols](#implemented-transfer-protocols)
* [System Requirements](#system-requirements)
* [Configuration](#file-fastchatconfigjson)
* [Aditional Configuration](#additional-configuration)
* [API & Websocket Integration](#api--websocket-integration)
* [Usage Example](#usage-example)
* [Version History](#version-history)
* [Project Status](#project-status)
* [Flow](./doc/FLOW.md)
* [License](#license)

## Overview

This package provides a Python interface to connect to MCP servers in an easy, intuitive, and configurable way. It features a modular architecture that allows for the seamless addition of new transfer protocols and language models (LLM) providers. Currently, it supports the HTTPStream and Stdio transport protocols and uses LiteLLM as the LLM gateway, enabling model usage across multiple providers.

## Installation

To install the MCP client, you can use pip:

```bash
pip install fastchat-mcp
```

## LLM Implementation

### LLM Providers

The client currently supports the following language model gateway:

| Provider | Status | Technical Description |
| ---      | ---    |---                    |
| LiteLLM   | Implemented |LiteLLM provides a unified interface for multiple LLM providers, allowing you to use models from OpenAI, Anthropic, Google, Azure, Bedrock, Groq, and others through a common API.|

>🚨 **CONFIGURATION NOTE** The runtime provider is `LiteLLM`, and model/provider selection is controlled by the `model` identifier and environment variables.

**Default Provider (`LiteLLM`):** LiteLLM acts as a unified adapter to route requests to many LLM vendors while preserving a consistent interface in Fastchat.

### LLM Models

This project can use any model supported by LiteLLM, providing flexibility to choose the model that best fits your specific needs. To explore providers and model naming conventions, consult the official [LiteLLM provider documentation](https://docs.litellm.ai/docs/providers).

To select a model, you should create a chat instance like this:

```python
from fastchat import Fastchat
chat = Fastchat(model="my-model-id", ...)
```

#### Supported Model Examples

The following table contains examples of model identifiers that can be passed to the core. Each model must be prefixed with its provider identifier:

| Provider | Model Examples | Use Case |
| --- | --- | --- |
| **OpenAI** | `gpt-4o`, `gpt-4-turbo`, `gpt-5-nano` | General purpose, advanced reasoning |
| **Anthropic** | `anthropic/claude-3-7-sonnet`, `anthropic/claude-3-opus` | Enterprise, complex reasoning |
| **Google** | `gemini/gemini-2.5-pro`, `gemini/gemini-2-flash-preview`, `gemini/gemini-3-flash-preview` | Multimodal, versatile |
| **Groq** | `groq/llama-3.1-8b-instant`, `groq/llama-3.1-70b-versatile`, `groq/meta-llama/llama-4-scout-17b-16e-instruct` | Fast inference, cost-effective |
| **Mistral** | `mistral/mistral-large`, `mistral/mistral-tiny` | Efficient, multilingual |
| **Meta (Llama)** | `ollama/llama2`, `ollama/mistral` | Self-hosted, local inference |
| **Azure** | `azure/gpt-4-deployment`, `azure/<your-deployment-name>` | Enterprise, Azure integration |
| **AWS Bedrock** | `bedrock/anthropic.claude-3-sonnet`, `bedrock/meta.llama2-13b` | AWS ecosystem |

**Usage Examples:**

```python
from fastchat import Fastchat

# OpenAI models (requires OPENAI_API_KEY)
chat = Fastchat(model="gpt-4o", ...)

# Groq models (requires GROQ_API_KEY)
chat = Fastchat(model="groq/llama-3.1-70b-versatile", ...)

# Google Gemini models (requires GEMINI_API_KEY)
chat = Fastchat(model="gemini/gemini-2-flash-preview", ...)

# Anthropic Claude models (requires ANTHROPIC_API_KEY)
chat = Fastchat(model="anthropic/claude-3-7-sonnet", ...)

# Mistral models (requires MISTRAL_API_KEY)
chat = Fastchat(model="mistral/mistral-large", ...)
```

**Default Model (`"groq/openai/gpt-oss-120b"`):** The 120B open-source model is a powerful, cost-effective option that provides excellent performance and reasoning capabilities. Served through Groq's fast inference platform, it delivers low-latency responses ideal for production applications. This model combines the strength of a large parameter count with competitive pricing and speed, making it suitable for complex tasks, code generation, and detailed analysis while maintaining cost efficiency.

## Implemented Transfer Protocols

Protocols for communication with MCP servers:

| Protocol | Status | Technical Characteristics |
| --- | --- | --- |
| stdio | Implemented | Standard input/output interface that facilitates direct communication between processes.|
| HTTPStream | Implemented | Asynchronous HTTP-based protocol that enables continuous data streaming.|
| SSE (Server-Sent Events) | Not Implemented | Unidirectional protocol that allows the server to send multiple updated events through a single HTTP connection.|

>🚨 **CRITICAL CONFIGURATION NOTE** Currently, this project don't work with `SSE (Server-Sent Events)` protocol.

## System Requirements

### Environmental Configuration

* **`.env` file**: The `.env` file contains the authentication credentials necessary for integration with external services. This file must be created in the project root directory with the following format:

    #### Basic Configuration

    ```env
    # .env

    # Cryptography key for token data storage (OAuth2)
    CRIPTOGRAFY_KEY=<any-cryptography-key>
    ```

    #### LLM Provider API Keys

    The following environment variables configure authentication with different LLM providers. Add only the keys for the providers you plan to use:

    ```env
    # OpenAI
    OPENAI_API_KEY=<your-openai-api-key>

    # Anthropic (Claude)
    ANTHROPIC_API_KEY=<your-anthropic-api-key>

    # Google (Gemini)
    GEMINI_API_KEY=<your-google-api-key>

    # Groq
    GROQ_API_KEY=<your-groq-api-key>

    # Mistral
    MISTRAL_API_KEY=<your-mistral-api-key>

    # Azure OpenAI
    AZURE_API_KEY=<your-azure-api-key>
    AZURE_API_BASE=<your-azure-endpoint>
    AZURE_API_VERSION=<your-azure-api-version>

    # AWS Bedrock (requires AWS credentials)
    AWS_ACCESS_KEY_ID=<your-aws-access-key>
    AWS_SECRET_ACCESS_KEY=<your-aws-secret-key>
    AWS_REGION_NAME=<your-aws-region>

    # Local/Ollama models (if using local inference)
    OLLAMA_BASE_URL=http://localhost:11434
    ```

    #### LiteLLM Configuration (Optional)

    ```env
    # Set a default routing API key (optional)
    LITELLM_API_KEY=<your-default-provider-key>

    # Set a custom base URL (for OpenAI-compatible APIs)
    LITELLM_BASE_URL=<optional-openai-compatible-base-url>
    ```

    #### How to Add API Keys

    1. Create a `.env` file in the project root directory (same level as `fastchat.config.json`):
       ```bash
       touch .env
       ```

    2. Add the API key for your selected provider:
       ```env
       # Example: Using Groq
       GROQ_API_KEY=gsk_your_actual_groq_api_key_here
       
       # Example: Using Google Gemini
       GEMINI_API_KEY=your_actual_gemini_api_key_here
       ```

    3. The application will automatically load these credentials when initializing the chat:
       ```python
       from fastchat import Fastchat
       
       # This will use the GROQ_API_KEY from .env
       chat = Fastchat(model="groq/llama-3.1-70b-versatile", ...)
       ```

    4. **⚠️ Security Note:** Never commit the `.env` file to version control. Add it to your `.gitignore`:
       ```bash
       echo ".env" >> .gitignore
       ```

* **`fastchat.config.json` file**: The `fastchat.config.json` file defines the configuration of available MCP servers. It must be created in the project root directory with this [structure](#file-fastchatconfigjson)

### Dependencies

* `Python = ">=3.11"`
* `litellm`
* `mcp[cli]`
* `mcp-oauth`

## File `fastchat.config.json`

This file defines the **configuration of available MCP servers** (Model Context Protocol) in the project.
It must be placed in the root directory of the repository. Its main purpose is to inform the application which servers can be used and how to connect to them.

### General Structure

The file is JSON formatted and follows this main structure:

```json
{
    "app_name": "fastchat-mcp",
    "mcp_servers": {
    "..."
    }
}
```

* **`app_name`**: The identifiable name of the application or project using these MCP servers.
* **`mcp_servers`**: An object listing one or more configured MCP servers, each with its unique key.

### Server Definition

Each MCP server inside `"mcp_servers"` has a custom configuration with these common properties:

* **Server key** (e.g., `"example_public_server"`, `"github"`, etc.): internal name identifying this server.
  
* **`protocol`**: Protocol or communication method. It can be:
  * `"httpstream"`: Communication via HTTP streaming.
  * `"stdio"`: Communication based on standard input/output (local command execution).

### Server Configuration Examples

#### 1. Public HTTP Stream Server

```json
"example_public_server": {
    "protocol": "httpstream",
    "httpstream-url": "http://127.0.0.1:8000/public-example-server/mcp",
    "name": "example-public-server",
    "description": "Example public server."
}
```

* **`httpstream-url`**: Base URL where the MCP HTTP streaming server is exposed.
* No authentication required (public access).
* `"name"` and `"description"` provide descriptive labels for users.

#### 2. Private HTTP Stream Server with Authentication

```json
"example_private_mcp": {
    "protocol": "httpstream",
    "httpstream-url": "http://127.0.0.1:8000/private-example-server/mcp",
    "name": "example-private-server",
    "description": "Example private server with oauth required.",
    "auth": {
        "required": true,
        "post_body": {
            "username": "user",
            "password": "password"
        }
    }
}
```

* Adds an `"auth"` object on top of basic config:
  * **`required`**: `true` indicates authentication is needed.
  * **`post_body`**: Data sent for authentication (username and password here).
* Suitable for servers secured with OAuth2.

#### 3. GitHub Server with Authentication Headers

```json
"github": {
    "protocol": "httpstream",
    "httpstream-url": "https://api.githubcopilot.com/mcp",
    "name": "github",
    "description": "This server specializes in github operations.",
    "headers": {
        "Authorization": "Bearer {your-github-access-token}"
    }
}
```

* Uses a custom HTTP header `"Authorization"` for token-based authentication.
* Perfect for sending API keys or tokens in headers to access the server.

#### 4. Local Server using STDIO protocol

```json
"my-stdio-server": {
    "protocol": "stdio",
    "name": "my-stdio-server",
    "config": {
        "command": "npx",
        "args": [
            "-y",
            "@modelcontextprotocol/example-stdio-server"
        ]
    }
}
```

* Does not use HTTP; communication happens by executing local commands.
* `"config"` specifies the command and arguments to run the MCP server. This key value(or body) has the same Claude Desktop sintaxis.
* Useful for local integrations or development testing without networking.

### Database Configuration

Database connection settings are defined in the `fastchat.config.file`. If the connection is established successfully, the conversation flow will automatically handle sending and retrieving data from the specified endpoints.

```json
{
    "...": "...",

    "db_conection": {
        "root_path": "http://127.0.0.1:6543/fastchatdb",
        "headers": {
            "example_autorization_token": "<your_token_here>",
            "other_header": "value",
            "...": "..."
        },
        "base_body": {
            "company_id": "<your_company_id>",
            "example_body_param": "<your_value_here>",
            "other_body_param": "value",
            "...": "..."
        },
        "base_query": {
            "company_id": "<your_company_id>",
            "example_query_param": "<your_value_here>",
            "other_query_param": "value",
            "...": "..."
        },
        "endpoints": {
            "save_message": {
                "path": "/message/save"
            },
            "load_history": {
                "path": "/history/load"
            }
        }
    }
}
```

[See more about database](./doc/DATABASE.md)

### Notes

> ⚠️ Place this file in the **project root** so the application can detect it automatically.
>
>💡 If you need an httpstream MCP server to test the code, you can use [simple-mcp-server](https://github.com/rb58853/simple-mcp-server).
>
> ✍️ If you need help configuring a specific server or using this configuration in your code, feel free to open discussion for help!

[see config.example.json](config.example.json)

---

## Additional Configuration

### System Prompts

As an advanced configuration, system prompts can be supplied to modify the behavior of responses. Prompts should be provided as lists; multiple system prompts can be supplied.

#### Args

* `extra_reponse_system_prompts`: List of string prompts used as additional system prompts in the final responses.
* `extra_selection_system_prompts`: List of string prompts used as additional system prompts for the resource/service selection step exposed by connected MCP servers.

Example:

```python
chat = Fastchat(
    extra_reponse_system_prompts=[
        "You are an NPC street vendor for an RPG game. You must behave as such and respond according to your character. You specialize in selling medieval weaponry, such as swords, armor, shields, and more. Address anyone who speaks to you as if they were an adventurer in a medieval fantasy world."
    ]
)
```

[See example here](./doc/USAGE.md#customizing-system-prompts)

### Additional MCP Servers

In addition to the servers defined in the configuration file, you can pass extra MCP servers via parameters. These are provided as a dictionary with the same structure as the configuration file, under the key `"mcp-servers"`.

#### Args

* `additional_servers`: Additional servers to be supplied to the Fastchat component, following the same format as the configuration file, for example:

```python
my_servers = {
  "github": {
    "protocol": "httpstream",
    "httpstream-url": "https://api.githubcopilot.com/mcp",
    "name": "github",
    "description": "This server specializes in github operations.",
    "headers": {
      "Authorization": "Bearer {your-github-token}"
    }
  },
  "other_server": {"...": "..."}
}
chat = Fastchat(additional_servers=my_servers)
```

> Note: Servers defined in the `.config` file are concatenated with those passed as parameters; it is compatible to use both methods to add MCP servers.

> API: The websocket exposed by the API supports additional servers passed through the `additional_servers` parameter.

### Browser-compatible additional servers injection (WebSocket)

Some browser WebSocket clients do not allow custom headers. For this scenario, the API now supports sending additional servers in the first WebSocket message.

How it works:

1. The API reads `aditional_servers` from headers (if available).
2. Optionally, the API reads the first client message and checks whether it is an additional-servers payload.
3. Final additional servers are the merge of both sources:
    * header-provided servers
    * first-message servers (overwrite repeated keys)
4. If the first message is not an additional-servers payload, it is processed as the normal user query.

Supported payload formats for the first message:

```text
__fastchat_additional_servers__:{"my_server":{"protocol":"httpstream","httpstream-url":"http://127.0.0.1:9000/mcp","name":"my_server","description":"My browser-injected server"}}
```

```json
{
    "type": "additional_servers",
    "data": {
        "my_server": {
            "protocol": "httpstream",
            "httpstream-url": "http://127.0.0.1:9000/mcp",
            "name": "my_server",
            "description": "My browser-injected server"
        }
    }
}
```

Typical browser flow:

1. Open WebSocket (`/chat/user` or `/chat/admin`) with URL query params.
2. Optionally send the first message with one of the payload formats above.
3. Send the user query as plain text.
4. Read streamed JSON steps until `--eof`.

## API & WebSocket Integration

Fastchat MCP provides an API extension with support for WebSocket connections secured via JWT token-based authentication. It offers two primary real-time messaging endpoints: one for users authenticated by an `ACCESS TOKEN`, and another for administrators requiring a `MASTER TOKEN`.

This system ensures continuous token validation on every connection, enabling a message flow that combines plain text with segmented JSON streams to efficiently and securely handle fragmented responses.

Configuration centralizes sensitive keys and external service endpoints through JSON configuration files or environment variables, seamlessly integrating with the FastAPI architecture and facilitating token persistence via a configurable REST backend.

### fastchat.config.json

```json
{
    "...": "...",
    
    "auth_middleware": {
        "database_api_path": "http://127.0.0.1:6789/mydb/data",
        "headers": {
            "header_key": "header_value",
            "other_header": "header_value",
            "...": "..."
        }
    }
}
```

[Learn more about the API](./doc/API_WEBSOCKET.md)

## Usage Example

```python
#example1.py
from fastchat import TerminalChat
chat = TerminalChat()
chat.open()
```

<https://github.com/user-attachments/assets/1fcb0db8-5798-4745-8711-4b93198e36cc>

```python
#example2.py
from fastchat import Fastchat
import asyncio

async def chating():
    chat: Fastchat = Fastchat()
    await chat.initialize()
    while True:
        query = input("> ")
        if query == "":
            break
        async for step in chat(query):
            print(f"<< {step.json}")
            
asyncio.run(chating())  
```

[see more usage examples](./doc/USAGE.md)

<!-- Alternatively, you may test this service using the following [template available on GitHub](https://github.com/rb58853/template-fastchat-mcp):

```shell
# clone repo
git clone https://github.com/rb58853/template-fastchat-mcp.git
# change to project dir
cd template-fastchat-mcp
# install dependencies
pip install -r requirements.txt
# open in vscode
code .
``` -->

## Version History

### Last Version Features

* 💬 Fully functional streaming chat by passing a query; see [`Fastchat`](./src/fastchat/services/llm/chat/chat.py).
* ⚙️ Integration with `Tools`, `Resources`, and `Prompts` from MCP servers, achieving a well-integrated client workflow with each of these services. [Check flow](./doc/FLOW.md)
* 🔐 Simple authentication system using [mcp-oauth](https://github.com/rb58853/mcp-oauth) and [this environmental configuration](#2-private-http-stream-server-with-authentication). Also integrate [headers authorization](#3-github-server-with-authentication-headers).
* 👾 LiteLLM as integrated LLM gateway using any supported model identifier.
* 📡 Support for the httpstream transport protocol.
* 📟 Support for the stdio transport protocol.
* 💻 Easy console usage via [`TerminalChat().open()`](./src/fastchat/dev.py); see [example1](#usage-example) for the use case.
* 💡 Response management and MCP service selection control through system prompts that can be passed to the chat. [see example](./doc/USAGE.md#customizing-system-prompts)
* 🗃 **Data persistence integrated into the workflow:** database connections established through APIs defined in the `fastchat.config.json`. [see more](#database-configuration)

[See more in changelog](./doc//CHANGELOG.md)

## Project Status
>
>⚠️ **Important Notice:** This project is currently in active development phase. As a result, errors or unexpected behaviors may occur during usage.
>
> Future versions are expected to include additional features such as voice systems, quick integrations with databases, built-in websocket support for frontend connections, among other useful functionalities. We invite you to **follow this repository (watch)** to stay updated on the latest news and improvements implemented.

* ✅ Quick integrations with databases
* ✅ Built-in websocket support for frontend connections
* ⏳ Voice systems
* 💡 And more

## License

MIT License. See [`license`](LICENSE)

---
<div align = center>

#### If you find this project helpful, please don’t forget to ⭐ star the [repository](https://github.com/rb58853/fastchat-mcp)

</div>

<!-- or [buy me a ☕ coffee](buymeacoffee.com/rb58853).** -->
