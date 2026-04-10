import yaml
import importlib.resources

from pathlib import Path

yaml_file = Path(__file__).parent / "texts" / "system_prompts.yaml"
with open(yaml_file) as f:
    system_prompts: dict = yaml.safe_load(f)

# with importlib.resources.open_text(
#     "fastchat.app.services.llm.prompts.texts", "system_prompts.yaml"
# ) as f:
#     system_prompts: dict = yaml.safe_load(f)

select_prompts: str = system_prompts.get("select_prompts", "")

def select_service(services: str | list):
    _select_service: str = system_prompts.get("select_service", "")
    return f"{_select_service} {services}"

def language_prompt(language: str) -> str:
    return f"\nAlways respond in the language: {language}"


BASE_DATA: str = "You have not extra data"


def _is_explicitly_empty_data(data: str | dict) -> bool:
    if data is None:
        return True

    raw = str(data).strip().lower()
    if raw in {"", "[]", "{}", "null", "none", '""', "''"}:
        return True

    return "no results" in raw or "sin resultados" in raw


def _format_factual_data_block(data: str | dict) -> str:
    evidence_status = "EMPTY" if _is_explicitly_empty_data(data) else "NON_EMPTY"
    return (
        "\n[FACTUAL_DATA_BEGIN]\n"
        "Treat this block as real retrieved evidence for the current response.\n"
        f"EVIDENCE_STATUS: {evidence_status}\n"
        "EVIDENCE_TRUST_LEVEL: STRICT\n"
        "EVIDENCE_IS_PRE_FILTERED: TRUE\n"
        f"{data}\n"
        "[FACTUAL_DATA_END]\n"
    )


def chat_asistant(
    services: list | None = None,
    data: str | dict = BASE_DATA,
) -> str:
    return (
        system_prompts.get("chat_assistant_prompt", "")
        + (
            _format_factual_data_block(data)
            if (services is None or data != BASE_DATA)
            else ""
        )
        + (
            ""
            if services is None
            else f"\n You have access to the following aviable services:\n{services}"
        )
    )


def preproccess_query(services: list) -> str:
    return (
        f"{system_prompts['task_query_decomposer']}\n"
        f"{services}"
    )
