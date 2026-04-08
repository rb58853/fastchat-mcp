# Version History 🚀

## fastchat-mcp

### v2.0.0 ⚡

- ✨ Added support for using multiple LLM providers and model identifiers through LiteLLM routing.
- 🚀 Updated default model to `groq/openai/gpt-oss-120b` for faster inference and improved response speed.
- 🧠 Applied small chat-history flow improvements so data recovered in previous steps can be reused in following steps.
- 🧹 Removed obsolete `llm_provider` parameter from API/chat configuration and related documentation.

### v1.2.5 🚀

- 🚀 Improvement of the prompt engine in system prompts  
- 🛠️ Fix Fastauth-integration

### v1.2.4 📝

- 🚀 Improvement of the prompt engine in system prompts  
- 🛠️ Fixing minor issues (await in resource & extra_selection_prompts in `TerminalChat`)

### v1.2.0 🧹

- **🔧 Client Cleanup**: `FastChatMCPClient.cleanup()` method for proper MCP connection termination
- **🧠 LLM Cleanup**: `LLMManager.cleanup()` for model and tokenizer memory release
- **📦 Context Manager Support**: Automatic cleanup using `async with` statements
- **🛡️ Resource Safety**: Prevents memory leaks in long-running applications

### v1.1.3 📡

- ✅ Full **WebSocket integration** with authentication, middleware, and security.  
- 🔑 Integration with an **external API** to generate, store, and load tokens connected to a database.  
- ⚙️ **Simple, fast, and flexible configuration** of the middleware system directly from the configuration file.  
- 🧩 **Basic tokenization** implemented — future updates will extend this to support more advanced payloads.  
  - For customizing tokenization settings, please check the [example implementation](../examples/custom_api/api.py).  

### v1.1.2 🗃

- 💬 The chat flow now handles connections to endpoints that interact with databases.  
- ⚙️ Database usage is **optional**, fully **configurable**, and designed to be **easy to understand and manage**. [Learn more](DATABASE.md)

### v1.1.1 🧩

- ✨ It is now possible to add additional system prompts to the `Fastchat` module, enabling customization of response style and query processing. *[See example](./USAGE.md#customizing-system-prompts)*  

- 🧩 You can now connect additional servers to the `Fastchat` class with a straightforward configuration process. *[See example](../README.md#additional-mcp-servers)*  

### v1.1.0 📡

- 🔄 **Shift from Sequential to Asynchronous Code**: Chat initialization must now be performed asynchronously using: `await chat.initialize();`.

- 🌐 **New WebSocket API**: Added a basic API that provides a WebSocket endpoint at: `"https://127.0.0.1:8000/chat/ws"`. Currently in **beta** stage, without an authentication system.

- 🚀 **Default Language Model**: The default model is now **`gpt-5-nano`** — faster, cheaper, and more accurate in completions.

### v1.0.1 🔧

- 📝 Improved logging and terminal output for local chat.
- 🎯 Enhanced prompt configuration for selecting prompts from the MCP.

### v1.0.0 📟

- 📟 The Stdio connection protocol has been implemented. The system now supports stdio-type connections.
- 👾 Access has been granted to utilize any OpenAI language model. Currently, only OpenAI is supported as the LLM provider.
- ⚙️ Rename config file from `config.json` to `fastchat.config.json`

### v0.1.3 ⌛️

- 🔧 Renamed the package to `fastchat-mcp`.
- 💬 Enabled real-time chat responses using streaming for final outputs.
- 🛠️ Refined parameter handling for tools, adding support for multi-typed arguments.

---
---
---

## mcp-llm-client

> ## Note
>
> Versions prior to `v0.1.3` specifically used the `mcp-llm-client` package. Starting from version `v0.1.3`, the package for this repository has been renamed to `fastchat-mcp`.

### v0.1.2 🔧

- 🐞 **Bug fixed:** A small error originating from the `dev` development branch has been resolved.
- ✅ Now, if an MCP server is detected, **no error will be thrown because of this**.

---

### v0.1.1 ⚙️

- 🔐 **Full integration with the new OAuth system:** Enhanced security and compatibility.
- ⚙️ **Advanced customization:** You can now add **custom headers** directly from the configuration.
- 🏷️ **Improved flexibility:** Support for passing `app_name` from the configuration for better identification.

---

### v0.1.0 ✨

- 🌟 Full integration of prompts from MCP servers into the client workflow.
- ⚙️ Enhancement of prompt engineering within the repository.
- 🔗 Exclusive integration with `mcp.types.PromptMessage`.

---

### v0.0.8 🎯

- 🚀 The prompts for language models (LLMs) were optimized to deliver responses that are more closely aligned with the MCP context.
- 🔄 The service extraction step was merged with the argument creation step, enabling both services and arguments to be identified in a single stage.

---

### v0.0.7 🔐

- 🛡️ A simple authorization system based on user credential authentication (username and password) was integrated. For further reference, please see [mcp-oauth](https://github.com/rb58853/mcp-oauth).

---

### v0.0.6 📡

- 📥 The exposed services have been added to the context of all queries, including those that do not require the use of a specific service. This approach allows for general inquiries regarding the available services.

---

### v0.0.5 🧩

- 📑 The LLM system is structured in steps, with each step being returned to the client making the query. This approach allows for the identification of the current stage within the query process.
- 🌐 Efficient language detection has been implemented for queries, enabling responses to be provided based on the detected language.
- 💬 The `open_local_chat()` function has been added, making it easy to use a local chat.

---

### v0.0.4 📦

- 📥 Package dependencies are incorporated during its initial installation process.

---

### v0.0.1 🛠️

- 🚀 Initial implementation of `Fastchat` client
- 🔗 Complete integration of `httpstream` protocol ([fasmcp](https://github.com/modelcontextprotocol/python-sdk))
- 🌍 Connectivity with multiple servers
- 🔧 Simplified fastchat.config.json file for connection management
- ⚡ Efficient processing of multiple simultaneous requests to tools and resources within a single query
- 🔓 Simple connection without authorization (compatible only with servers that do not require authentication)
