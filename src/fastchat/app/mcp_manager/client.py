from .servers import Servers
from .connections.session_data import get_session_data
from .connections.services import Tool, Resource, Prompt
from ...config.logger import logger


class ClientManagerMCP:
    def __init__(self, app_name: str = "fastchat-mcp"):
        self.app_name: str = app_name
        self.tools: dict[str:Tool] | None = {}
        self.resources: dict[str:Resource] | None = {}
        self.prompts: dict[str:Prompt] | None = {}
        self.refresh_data()
        self.__services: list[dict] = []
        """Lista de servicios en forma de string para pasarse al LLM"""
        self.__prompts_context: list[dict] = []
        """Lista de prompts en forma de string para pasarse al LLM"""

    def call_tool(self, name: str, args: dict) -> str | None:
        return self.tools[name](args)

    def read_resource(self, name: str, args: dict) -> str | None:
        return self.resources[name](args)

    def get_prompt(self, name: str, args: dict) -> dict:
        self.prompts[name](args)

    def refresh_data(self):
        """
        Inicializa o refresca la lista de herramientas, recursos o promps que sirve cada uno de los servidores, y lo organiza en forma de diccionario
        donde cada valor posee informacion de cada servicio ademas de la direccion desde la cual se sirve
        """
        self.tools, self.resources, self.prompts = ({}, {}, {})
        mcp_servers: dict[str, dict] = Servers().mcp_servers

        for server_key in mcp_servers.keys():
            server = {"key": server_key} | mcp_servers[server_key]
            try:
                session: dict = get_session_data(
                    server["httpstream-url"],
                    server["oauth_client"],
                    headers=server.get("headers", None),
                )
            except Exception as e:
                logger.warning(
                    f"Failed to establish connection with server {server_key}. Cause: {e}"
                )
                continue

            for tool in session["tools"]:
                self.tools[f"{server_key}_{tool.name}"] = Tool(
                    http=server["httpstream-url"], data=tool, server=server
                )
            for resource in session["resources"]:
                self.resources[f"{server_key}_{resource.name}"] = Resource(
                    http=server["httpstream-url"], data=resource, server=server
                )

            for prompt in session["prompts"]:
                self.prompts[f"{server_key}_{prompt.name}"] = Prompt(
                    http=server["httpstream-url"], data=prompt, server=server
                )

    def service_type(self, service_key: str) -> str:
        if service_key in self.tools.keys():
            return "tool"
        if service_key in self.resources.keys():
            return "resource"

    def get_services(self) -> list[dict[str, any]]:
        if len(self.__services) != len(self.tools) + len(self.resources):
            services = self.tools | self.resources
            self.__services = [
                {service: str(services[service])} for service in services.keys()
            ]

        return self.__services

    def get_prompts(self) -> list[dict[str, any]]:
        if len(self.__prompts_context) != len(self.prompts):
            self.__prompts_context = [
                {key: str(self.prompts[key])} for key in self.prompts.keys()
            ]
        return self.__prompts_context
