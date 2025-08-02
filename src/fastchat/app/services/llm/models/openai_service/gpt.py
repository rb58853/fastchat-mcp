from collections.abc import Generator
from ...prompts import system_prompts, user_prompts
from ......config.llm_config import ConfigGPT
from ......config.logger import logger
from ...llm import LLM
from openai import OpenAI, AsyncOpenAI
import json


class GPT(LLM):
    """
    ## GPT
    ### Args:
    - `model`: modelo de gpt que a usar
    - `max_history_len`: largo maximo del historial que se para como input al modelo
    """

    def __init__(
        self,
        model=ConfigGPT.DEFAULT_MODEL_NAME,
        max_history_len: int = 10,
    ):
        super().__init__()
        self.client = OpenAI(api_key=ConfigGPT.OPENAI_API_KEY)
        """Cliente secuencial de GPT"""
        self.async_client = AsyncOpenAI(api_key=ConfigGPT.OPENAI_API_KEY)
        """Cliente asincrono de GPT"""
        self.max_len_history: int = max_history_len
        """Maxima cantidad de mensajes previos que se le pasan como input"""
        self.chat_history: list[list[dict[str, str]]] = []
        """Historial del chat asosiado a esta instancia de GPT, en forma lista de listas, por ejemplo 
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

    def append_chat_history(self):
        """Agrega una historia vacia para crear el espacio"""
        self.chat_history.append([])
        self.chat_history[-1].append({})

    def call_stream_completion(
        self, system_message: str, query: str, extra_messages: list[dict[str, str]] = []
    ):
        """ """
        self.chat_history[-1][0] = {"role": "user", "content": query}
        messages: list[dict[str, str]] = [{"role": "system", "content": system_message}]

        for message in extra_messages:
            if message["role"] == "system":
                messages.append(message)
        messages += [
            message
            for messages in self.chat_history[-self.max_len_history :]
            for message in messages
        ]
        for message in extra_messages:
            if message["role"] == "user" or message["role"] == "assistant":
                messages.append(message)

        stream = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            stream=True,
        )
        return stream

    def call_completion(
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
            for messages in self.chat_history[-self.max_len_history :]
            for message in messages
        ]
        for message in extra_messages:
            if message["role"] == "user" or message["role"] == "assistant":
                messages.append(message)

        if json_format:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                response_format={"type": "json_object"},
            )
        else:

            completion = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
            )
        self.__get_price(completion.usage)
        return completion.choices[0].message.content

    def preprocess_query(self, query: str) -> dict:
        system_message: str = system_prompts.preproccess_query(
            services=self.client_manager_mcp.get_services()
        )
        messages: list[dict[str, str]] = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": query},
        ]
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            response_format={"type": "json_object"},
        )
        self.__get_price(completion.usage)
        response = completion.choices[0].message.content
        return json.loads(response)

    def simple_query(
        self, query: str, use_services_contex: bool = False
    ) -> Generator[str, None]:
        system_message: str = system_prompts.chat_asistant(
            self.client_manager_mcp.get_services() if use_services_contex else None
        ) + system_prompts.language_prompt(self.current_language)
        # response = self.call_completion(system_message=system_message, query=query)

        stream = self.call_stream_completion(
            system_message=system_message,
            query=query,
        )

        response: str = ""
        for chunk in stream:
            content = chunk.choices[0].delta.content
            response += content if content is not None else ""
            yield content

        # Se agrega la respuesta a la historia
        self.chat_history[-1].append({"role": "assistant", "content": response})
        return response

    def final_response(self, query: str, data: str | dict) -> Generator[str, None]:
        system_message: (
            str
        ) = system_prompts.chat_asistant() + system_prompts.language_prompt(
            self.current_language
        )
        user_message = user_prompts.query_and_data(query=query, data=data)

        stream = self.call_stream_completion(
            system_message=system_message,
            query=user_message,
        )

        response: str = ""
        for chunk in stream:
            content = chunk.choices[0].delta.content
            response += content if content is not None else ""
            yield content

        # Se agrega la respuesta a la historia
        self.chat_history[-1].append({"role": "assistant", "content": response})
        return response

    def select_prompts(self, query: str) -> str:
        system_message: str = system_prompts.select_prompts
        prompts = self.client_manager_mcp.get_prompts()

        extra_messages: list[dict[str, str]] = [
            {
                "role": "user",
                "content": user_prompts.exposed_prompts(prompts),
            }
        ]

        return self.call_completion(
            system_message=system_message,
            query=query,
            json_format=True,
            extra_messages=extra_messages,
        )

    def select_service(
        self, query: str, extra_messages: list[dict[str, str]] = []
    ) -> str:
        """
        Funcion encargada de seleccionar los servicios utiles para el contexto de la consulta, usando los servicios expuestos por cada uno
        de los servidores
        """
        system_message: str = system_prompts.select_service
        services = self.client_manager_mcp.get_services()
        query: str = user_prompts.query_and_services(query=query, services=services)
        
        return self.call_completion(
            system_message=system_message,
            query=query,
            json_format=True,
            extra_messages=extra_messages,
        )

    def __get_price(self, usage) -> float:
        """
        ### Args
            - `usage`: uso de la api retornado en el completion respuesta del llamado a la api de gpt
        ### Outs:
            - `price`: precio final del llamado a la api.
        """
        try:
            input_tokens: int = usage.prompt_tokens
            output_tokens: int = usage.completion_tokens

            input_price: float = ConfigGPT.MODEL_PRICE[self.model]["input"]
            output_price: float = ConfigGPT.MODEL_PRICE[self.model]["output"]
            price: float = input_tokens * input_price + output_tokens * output_price

            # Aumenta el valod asociado al costo de uso de la API en esta instancia de GPT
            self.current_price += price
            return price
        except Exception as e:
            logger.warning(f"Error al calcular el precio: {e}")
            return 0.0
