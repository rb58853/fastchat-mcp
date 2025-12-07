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

select_service: str = system_prompts.get("select_service", "")
select_prompts: str = system_prompts.get("select_prompts", "")


def language_prompt(language: str) -> str:
    return f"\nAlways respond in the language: {language}"


BASE_DATA: str = "You have not extra data"


def chat_asistant(
    services: list | None = None,
    data: str | dict = BASE_DATA,
) -> str:
    return (
        system_prompts.get("chat_assistant_prompt", "")
        + (str(data) if (services is None or data != BASE_DATA) else "")
        + (
            ""
            if services is None
            else f"\n You have access to the following aviable services:\n{services}"
        )
    )


def preproccess_query(services: list) -> str:
    return f'{system_prompts["task_query_decomposer"]}"\n"{services})'
