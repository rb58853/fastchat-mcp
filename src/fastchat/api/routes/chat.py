import json
import asyncio
from fastauth import websocket_middleware, TokenType
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from ..settings import FastappSettings
from ...config.logger import logger
from ...app.chat.chat import Fastchat
from ...config.llm_config import ConfigModel

router = APIRouter(prefix="/chat", tags=["chating"])
STREAM_END_MARKER: str = "--eof"
ADITIONAL_SERVERS_PREFIX: str = "__fastchat_additional_servers__:"

#TODO: Change logic to authorize tokens pass is_unauthotized for validate in the next message

@router.websocket("/user")
@websocket_middleware(token_type=TokenType.ACCESS)
async def access_websocket(
    websocket: WebSocket,
    chat_id: str = None,
    model: str = ConfigModel.DEFAULT_MODEL_NAME,
    is_unauthotized: bool = False,
):
    await websocket_chat(
        websocket=websocket,
        chat_id=chat_id,
        model=model,
        is_unauthotized=is_unauthotized,
    )


@router.websocket("/admin")
@websocket_middleware(token_type=TokenType.MASTER)
async def master_websocket(
    websocket: WebSocket,
    chat_id: str = None,
    model: str = ConfigModel.DEFAULT_MODEL_NAME,
    is_unauthotized: bool = False,
):
    await websocket_chat(
        websocket=websocket,
        chat_id=chat_id,
        model=model,
        is_unauthotized=is_unauthotized,
    )


async def websocket_chat(
    websocket: WebSocket,
    chat_id: str = None,
    model: str = ConfigModel.DEFAULT_MODEL_NAME,
    is_unauthotized: bool = False,
):
    await websocket.accept()
    await websocket.send_json(
        {
            "status": "success",
            "detail": "Connected: Connection Accepted",
        }
    )
    aditional_servers_by_headers: dict = parse_aditional_servers_header(
        websocket.headers.get("aditional_servers")
    )

    # Optional parser for browser clients that cannot send custom websocket headers.
    # If the first message is not an additional-servers payload, it is treated as a regular query.
    pending_query: str | None = None
    aditional_servers_by_message: dict = {}
    try:
        first_message = await asyncio.wait_for(websocket.receive_text(), timeout=2.0)
        is_aditional_servers_message, parsed_servers = parse_aditional_servers_message(
            first_message
        )
        if is_aditional_servers_message:
            aditional_servers_by_message = parsed_servers
        else:
            pending_query = first_message
    except asyncio.TimeoutError:
        pass

    aditional_servers: dict = {
        **aditional_servers_by_headers,
        **aditional_servers_by_message,
    }

    history: list = get_history(chat_id)

    chat = Fastchat(
        id=chat_id,
        model=model,
        extra_reponse_system_prompts=FastappSettings.extra_reponse_system_prompts,
        extra_selection_system_prompts=FastappSettings.extra_selection_system_prompts,
        aditional_servers=aditional_servers,
        len_context=FastappSettings.len_context,
        history=history,
    )

    logger.info(f"Initilaized chat with id = {chat_id}")
    await chat.initialize(print_logo=False)

    try:
        while True:
            # Espera mensaje del usuario, típicamente texto (puedes cambiarlo si envías JSON)
            if pending_query is not None:
                query = pending_query
                pending_query = None
            else:
                query = await websocket.receive_text()
            # response = chat(query)

            # Enviar respuesta al cliente (puede ser texto o JSON)
            async for step in chat(query):
                await websocket.send_json(step.json)
            await websocket.send_text(STREAM_END_MARKER)

    except WebSocketDisconnect:
        # Cierra conexión limpia si el cliente se desconecta
        pass


def get_history(chat_id: str) -> list:
    """Select history from database using chat_id"""
    return []


def parse_aditional_servers_header(aditional_servers: str | None) -> dict:
    if (
        aditional_servers is None
        or aditional_servers == ""
        or aditional_servers == "None"
    ):
        return {}

    try:
        aditional_servers = aditional_servers.replace("'", '"')
        parsed = json.loads(aditional_servers)
        return parsed if isinstance(parsed, dict) else {}
    except Exception:
        return {}


def parse_aditional_servers_message(message: str) -> tuple[bool, dict]:
    message = message.strip()
    payload: str | None = None

    if message.startswith(ADITIONAL_SERVERS_PREFIX):
        payload = message[len(ADITIONAL_SERVERS_PREFIX) :].strip()
    else:
        # Alternative JSON envelope syntax for browser clients.
        # Example:
        # {"type":"additional_servers","data":{...}}
        try:
            parsed_message = json.loads(message)
            if (
                isinstance(parsed_message, dict)
                and parsed_message.get("type") == "additional_servers"
            ):
                data = parsed_message.get("data", {})
                if isinstance(data, dict):
                    return True, data
                logger.warning("Ignored additional_servers message: 'data' must be a JSON object")
                return True, {}
        except Exception:
            return False, {}

    if payload is None:
        return False, {}

    try:
        parsed_payload = json.loads(payload)
        if isinstance(parsed_payload, dict):
            return True, parsed_payload
        logger.warning("Ignored additional_servers message: payload must be a JSON object")
        return True, {}
    except Exception:
        logger.warning("Ignored additional_servers message: invalid JSON payload")
        return True, {}
