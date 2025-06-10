from setuptools import setup, find_packages
from pathlib import Path
import os

long_description = """
# Python MCP Client
Python client, based on [`fastmcp`](https://github.com/modelcontextprotocol/python-sdk), for connecting to MCP servers through multiple protocols, specifically designed to work with integrated language models.

## Table of Contents

* [Overview](#overview)
* [Installation](#installation)
* [Implemented Models](#implemented-models)
* [Implemented Transfer Protocols](#implemented-transfer-protocols)
* [System Requirements](#system-requirements)
* [Usage Example](#usage-example)
* [License](#license)

## Overview

This package provides a Python interface to connect to MCP servers in an easy, intuitive, and configurable way. It offers a modular architecture that allows for easy extension of new transfer protocols and language models. Currently includes support for HTTPStream and GPT-4 mini, with expansion capability for more options in the future.

## Installation

To install the MCP client, you can use pip:

```bash
pip install mcp-client-py
```

## Implemented Models

The client currently supports the following language models:

| Model | Technical Description |
| --- | --- |
| gpt4o-mini | Optimized implementation of the GPT-4 model that provides a balance between computational performance and resource efficiency. This model is specifically designed to operate in environments with memory constraints while maintaining superior predictive quality. |

## Implemented Transfer Protocols

Protocols for communication with MCP servers:

| Protocol | Status | Technical Characteristics |
| --- | --- | --- |
| HTTPStream | Implemented | Asynchronous HTTP-based protocol that enables continuous data streaming. Characterized by low memory consumption and real-time processing capability for partial responses. |
| SSE (Server-Sent Events) | Not Implemented | Unidirectional protocol that allows the server to send multiple updated events through a single HTTP connection. Designed specifically for applications requiring real-time updates from the server. |
| stdio | Not Implemented | Standard input/output interface that facilitates direct communication between processes. Will provide a lightweight alternative for local environments and unit testing. |

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

    ```python
    # .env
    # OpenAI Authentication
    OPENAI_API_KEY=<YOUR OPENAI-API-KEY>
    ```

* **`config.json` file**: The `config.json` file defines the configuration of available MCP servers. It must be created in the project root directory with the following structure:

    ```json
    {
        "mcp_servers": {
            "example_server": {
                "http": "http://0.0.0.0:8000/server/mcp",
                "name": "Example mcp server",
                "description": "A simple example MCP server"
            }
        }
    }
    ```

### Software Requirements

* Python 3.11+
* openai package
* fastmcp package

## Usage Example

```python
#example.local.py
```

<!-- ## Contribución

Las contribuciones son bienvenidas. Para agregar nuevos protocolos o modelos, sigue estas directrices:

1. Crea una rama feature desde main
2. Implementa las nuevas características siguiendo el patrón existente
3. Incluye documentación actualizada
4. Realiza pruebas unitarias
5. Envía una pull request con explicación detallada -->

<!-- ## Contacto

Para reportar bugs o solicitar funcionalidades, abre un issue en el repositorio. -->

## License

MIT License. See [`license`](license).

"""

setup(
    name="fastmcpclient",
    version="0.0.1",
    packages=find_packages(),
    author="Raúl Beltrán Gómez",
    author_email="rb58853@gmail.com",
    description="Python client, based on fastmcp, for connecting to MCP servers through multiple protocols, specifically designed to work with integrated language models.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rb58853/python-mcp-client",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.11",
)
