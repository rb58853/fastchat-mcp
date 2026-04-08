from collections.abc import Generator

from .....mcp_manager.client import ClientManagerMCP
from ...prompts import system_prompts, user_prompts
from ......config.llm_config import ConfigModel
from ......config.logger import logger
from ...llm import LLM
from litellm import completion
import json


class LiteLLMModel(LLM):
    """
    ## LiteLLMModel
    ### Args:
    - `model`: modelo de gpt que a usar
    - `max_history_len`: largo maximo del historial que se para como input al modelo
    """

    def __init__(
        self,
        model=ConfigModel.DEFAULT_MODEL_NAME,
        max_history_len: int = 10,
        chat_history: list = [],
    ):
        super().__init__()
        self.client = completion
        """Cliente secuencial de LiteLLM"""
        self.async_client = None
        """Referencia reservada para compatibilidad con limpieza asincrona"""
        self.base_url: str | None = ConfigModel.LITELLM_BASE_URL
        self.max_len_history: int = max_history_len
        """Maxima cantidad de mensajes previos que se le pasan como input"""
        self.chat_history: list[list[dict[str, str]]] = chat_history
        """Historial del chat asociado a esta instancia del modelo, en forma lista de listas, por ejemplo 
        ```
        chat_history: str = [
            [
                {"role": "user", "content": "query1"},
                {"role": "assistant", "content": "response1"}
            ],
            [
                {"role": "user", "content": "query2"},
                {"role": "assistant", "content": "response2"}
            ]
        ]
        ```
        """
        self.model: str = model
        self.current_price: float = 0

    def __completion(self, messages: list[dict[str, str]], **kwargs):
        completion_args = {
            "model": self.model,
            "messages": messages,
            "drop_params": True,
            **kwargs,
        }
        if self.base_url:
            completion_args["base_url"] = self.base_url
        return self.client(**completion_args)

    def __get_price(self, usage) -> float:
        """
        ### Args
            - `usage`: uso de la api retornado en el completion respuesta del llamado a la api de gpt
        ### Outs:
            - `price`: precio final del llamado a la api.
        """
        try:
            input_tokens: int = (
                usage.get("prompt_tokens", 0)
                if isinstance(usage, dict)
                else getattr(usage, "prompt_tokens", 0)
            )
            output_tokens: int = (
                usage.get("completion_tokens", 0)
                if isinstance(usage, dict)
                else getattr(usage, "completion_tokens", 0)
            )

            input_price: float = ConfigModel.MODEL_PRICE[self.model]["input"]
            output_price: float = ConfigModel.MODEL_PRICE[self.model]["output"]
            price: float = input_tokens * input_price + output_tokens * output_price

            # Aumenta el valor asociado al costo de uso de la API en esta instancia
            self.current_price += price
            return price
        except Exception:
            logger.warning(f"Can't calculate usage price from: {self.model}")
            return 0.0

    def append_chat_history(self):
        """Agrega una historia vacia para crear el espacio"""
        self.chat_history.append([])
        self.chat_history[-1].append({})

    def append_service_data_to_history(self, data: str, role: str = "system"):
        """
        Agrega datos recuperados de un servicio MCP al historial de chat.
        Esto permite que las siguientes subtareas tengan acceso a los datos
        recuperados en pasos anteriores.

        Args:
            data (str): Los datos recuperados del servicio
            role (str): El rol del mensaje (default: "system" para datos contextuales)
        """
        if self.chat_history and len(self.chat_history[-1]) > 0:
            # Si el último elemento está vacío, reemplazarlo con los datos
            if not self.chat_history[-1][-1]:
                self.chat_history[-1][-1] = {"role": role, "content": data}
            else:
                # Sino, agregarlo como un nuevo elemento
                self.chat_history[-1].append({"role": role, "content": data})
        else:
            # Si no hay historial, crear uno
            self.chat_history.append([{"role": role, "content": data}])

    def __call_stream_completion(
        self,
        system_message: str,
        query: str,
        extra_messages: list[dict[str, str]] = [],
    ):
        """ """
        self.chat_history[-1][0] = {"role": "user", "content": query}
        messages: list[dict[str, str]] = [{"role": "system", "content": system_message}]

        for message in extra_messages:
            if message["role"] == "system":
                messages.append(message)
        messages += [
            message
            for messages in self.chat_history[-self.max_len_history : -1]
            for message in messages
        ]
        for message in extra_messages:
            if message["role"] == "user" or message["role"] == "assistant":
                messages.append(message)
        messages.append(self.chat_history[-1][0])

        stream = self.__completion(
            messages=messages,
            stream=True,
        )
        return stream

    def __call_completion(
        self,
        system_message: str,
        query: str,
        json_format: bool = False,
        extra_messages: list[dict[str, str]] = [],
    ):
        """ """
        
        self.chat_history[-1][0] = {"role": "user", "content": query}
        messages: list[dict[str, str]] = [{"role": "system", "content": system_message}]

        for message in extra_messages:
            if message["role"] == "system":
                messages.append(message)
        messages += [
            message
            for messages in self.chat_history[-self.max_len_history : -1]
            for message in messages
        ]
        for message in extra_messages:
            if message["role"] == "user" or message["role"] == "assistant":
                messages.append(message)
        messages.append(self.chat_history[-1][0])

        if json_format:
            completion = self.__completion(
                messages=messages,
                response_format={"type": "json_object"},
            )
        else:

            completion = self.__completion(
                messages=messages,
            )
        self.__get_price(completion.usage)
        return completion.choices[0].message.content

    def preprocess_query(
        self,
        query: str,
        extra_messages: list[dict[str, str]] = [],
    ) -> dict:
        system_message: str = system_prompts.preproccess_query(
            services=self.client_manager_mcp.get_services()
        )
        messages: list[dict[str, str]] = [{"role": "system", "content": system_message}]
        for message in extra_messages:
            if message["role"] == "system":
                messages.append(message)
        messages += [
            message
            for messages in self.chat_history[-self.max_len_history : -1]
            for message in messages
        ]
        for message in extra_messages:
            if message["role"] == "user" or message["role"] == "assistant":
                messages.append(message)
        
        messages.append({"role": "user", "content": query})

        completion = self.__completion(
            messages=messages,
            response_format={"type": "json_object"},
        )
        self.__get_price(completion.usage)
        response = completion.choices[0].message.content
        return json.loads(response)

    def select_prompts(self, query: str, extra_messages: list[dict[str, str]]) -> str:
        system_message: str = system_prompts.select_prompts
        prompts = self.client_manager_mcp.get_prompts()
        if prompts is None or len(prompts) == 0:
            return json.dumps({"prompt_services": []})

        extra_messages: list[dict[str, str]] = extra_messages + [
            {
                "role": "user",
                "content": user_prompts.exposed_prompts(prompts),
            }
        ]

        return self.__call_completion(
            system_message=system_message,
            query=query,
            json_format=True,
            extra_messages=extra_messages,
        )

    def select_service(
        self,
        query: str,
        extra_messages: list[dict[str, str]] = [],
    ) -> str:
        services = self.client_manager_mcp.get_services()
        if services is None or len(services) == 0:
            return json.dumps({"service": "", "args": {}})

        system_message: str = system_prompts.select_service(services=services)

        query: str = query
        return self.__call_completion(
            system_message=system_message,
            query=query,
            json_format=True,
            extra_messages=extra_messages,
        )

    def simple_query(
        self,
        query: str,
        use_services_contex: bool = False,
        extra_messages: list[dict[str, str]] = [],
    ) -> Generator[str, None]:
        system_message: str = system_prompts.chat_asistant(
            self.client_manager_mcp.get_services() if use_services_contex else None
        ) + system_prompts.language_prompt(self.current_language)
        # response = self.__call_completion(system_message=system_message, query=query)

        stream = self.__call_stream_completion(
            system_message=system_message,
            query=query,
            extra_messages=extra_messages,
        )

        response: str = ""
        for chunk in stream:
            content = chunk.choices[0].delta.content
            response += content if content is not None else ""
            yield content

        # Se agrega la respuesta a la historia
        self.chat_history[-1].append({"role": "assistant", "content": response})
        return response

    def final_response(
        self,
        query: str,
        data: str | dict,
        extra_messages: list[dict[str, str]] = [],
    ) -> Generator[str, None]:
        system_message: str = system_prompts.chat_asistant(
            data=data
        ) + system_prompts.language_prompt(self.current_language)
        user_message = query
        # user_message = user_prompts.query_and_data(query=query, data=data)

        stream = self.__call_stream_completion(
            system_message=system_message,
            query=user_message,
            extra_messages=extra_messages,
        )

        response: str = ""
        for chunk in stream:
            content = chunk.choices[0].delta.content
            response += content if content is not None else ""
            yield content

        # Se agrega la respuesta a la historia
        self.chat_history[-1].append({"role": "assistant", "content": response})
        return response

    async def close(self) -> None:
        """
        Closes and cleans up all model resources including LiteLLM references and chat history.

        This method performs the following cleanup operations:
        - Clears LiteLLM client references
        - Clears the chat history to free memory
        - Nullifies client references to prevent memory leaks

        Called by the parent Fastchat cleanup process to ensure proper resource management.
        """
        try:
            # Clear LiteLLM client references
            if hasattr(self, "client") and self.client is not None:
                self.client = None
            if hasattr(self, "async_client") and self.async_client is not None:
                self.async_client = None
            if hasattr(self, "api_key"):
                self.api_key = None
            if hasattr(self, "base_url"):
                self.base_url = None

            # Clear chat history to free memory
            if hasattr(self, "chat_history"):
                self.chat_history.clear()

            # Clear client manager reference
            if hasattr(self, "client_manager_mcp"):
                self.client_manager_mcp = None

        except Exception as e:
            logger.error(f"Error during LiteLLMModel cleanup: {e}")
            raise
