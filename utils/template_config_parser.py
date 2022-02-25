import json
import re
import typing
from utils.configuration import Configuration


def parse_definitions(template_config: dict[str, typing.Any], config: Configuration):
    """
    Mathod for parsing definitions from template configuration file
    :param template_config: template config
    :param config: script config
    :return: processed template config with extracted definitions
    """

    # Get or create definitions storage
    if "define" in template_config:
        storage = dict(template_config["define"])
    else:
        storage = {}

    # Extract definitions from config keys
    for definition in filter(lambda x: x not in ["files", "define"], template_config.keys()):
        # If key is template, define as TemplateName
        if definition == "template":
            storage["TemplateName"] = template_config["template"]

        # If key is author...
        elif definition == "author":
            # Check if author key defined in script config
            if config.get_property("author"):
                storage["Author"] = config.get_property("author")

            # ... or get it from template config
            else:
                storage["Author"] = template_config["author"]

        # Transform other keys to variables
        else:
            definition_name = "Template" + definition[0].upper() + definition[1:]
            storage[definition_name] = template_config[definition]

    # If author variable not defined but script config has default-author...
    if "Author" not in storage and config.get_property("default-author"):
        storage["Author"] = config.get_property("default-author")

    # Get template config files section as string
    files_config_raw = json.dumps(template_config["files"])

    # Inject variable values
    for definition in storage:
        files_config_raw = files_config_raw.replace("#" + definition, storage[definition])

    # Get variables without defined values
    empty_definitions = list(set(re.findall(r"#[A-Z][A-z]+", files_config_raw)))

    # Require variable values from user
    re_words = re.compile(r"[A-Z][a-z]+")
    for empty_definition in empty_definitions:
        readable_name = " ".join(re_words.findall(empty_definition)).lower()
        readable_name = readable_name[0].upper() + readable_name[1:]

        value = input(f"{readable_name}: ")

        files_config_raw = files_config_raw.replace(empty_definition, value or readable_name)
        storage[empty_definition[1:]] = value or readable_name

    # Rewrite definitions storage
    template_config["defines"] = storage

    # Rewrite files container
    template_config["files"] = json.loads(files_config_raw)

    return template_config
