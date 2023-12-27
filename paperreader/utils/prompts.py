from langchain.prompts.prompt import PromptTemplate
from langchain.prompts import HumanMessagePromptTemplate, ChatPromptTemplate
from langchain.prompts.loading import _load_output_parser

from pathlib import Path
import yaml

from paperreader.config import DIR_PROMPTS


def chat_prompt_template_from_name(name: str) -> ChatPromptTemplate:
    return ChatPromptTemplate.from_messages([
        HumanMessagePromptTemplate(
            prompt=prompt_template_from_name(name)
        )
    ])


def prompt_template_from_name(name: str) -> PromptTemplate:
    file_path = Path(f"{DIR_PROMPTS}/{name}/config.yaml")
    if file_path.suffix == ".yaml":
        with open(file_path, "r") as f:
            config = yaml.safe_load(f)

        config["template_path"] = f"{DIR_PROMPTS}/{name}/template.txt"
        config["_type"] = "prompt"
    else:
        raise ValueError(f"Got unsupported file type {file_path.suffix}")

    # Load the prompt from the config now.
    return _load_prompt(config)


def _load_prompt(config: dict, name: str = None) -> PromptTemplate:
    """Load the prompt template from config."""
    # Load the template from disk if necessary.
    config = _load_template("template", config)
    config = _load_output_parser(config)

    return PromptTemplate(**config)


def _load_template(var_name: str, config: dict, name: str = None) -> dict:
    """Load template from the path if applicable."""
    # Check if template_path exists in config.
    if f"{var_name}_path" in config:
        # If it does, make sure template variable doesn't also exist.
        if var_name in config:
            raise ValueError(
                f"Both `{var_name}_path` and `{var_name}` cannot be provided."
            )
        # Pop the template path from the config.
        template_path = Path(config.pop(f"{var_name}_path"))
        # Load the template.
        if template_path.suffix == ".txt":
            with open(template_path) as f:
                template = f.read()
        else:
            raise ValueError
        # Set the template variable to the extracted variable.
        config[var_name] = template
    return config
