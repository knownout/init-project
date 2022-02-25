import json
import re
import typing
from utils.configuration import Configuration


def parse_definitions(template_config: dict[str, typing.Any], config: Configuration):
    if "define" in template_config:
        storage = dict(template_config["define"])
    else:
        storage = {}

    for definition in filter(lambda x: x not in ["files", "define"], template_config.keys()):
        if definition == "template":
            storage["TemplateName"] = template_config["template"]

        elif definition == "author":
            if config.get_property("author"):
                storage["Author"] = config.get_property("author")

            else:
                storage["Author"] = template_config["author"]

        elif definition == "version":
            storage["TemplateVersion"] = template_config["version"]

        else:
            definition_name = "Template" + definition[0].upper() + definition[1:]
            storage[definition_name] = template_config[definition]

    if "TemplateAuthor" not in storage and config.get_property("default-author"):
        storage["Author"] = config.get_property("default-author")

    files_config_raw = json.dumps(template_config["files"])
    for definition in storage:
        files_config_raw = files_config_raw.replace("#" + definition, storage[definition])

    empty_definitions = list(set(re.findall(r"#[A-Z][A-z]+", files_config_raw)))

    re_words = re.compile(r"[A-Z][a-z]+")
    for empty_definition in empty_definitions:
        readable_name = " ".join(re_words.findall(empty_definition)).lower()
        readable_name = readable_name[0].upper() + readable_name[1:]

        value = input(f"{readable_name}: ")

        files_config_raw = files_config_raw.replace(empty_definition, value or readable_name)
        storage[empty_definition[1:]] = value or readable_name

    template_config["defines"] = storage
    template_config["files"] = json.loads(files_config_raw)

    return template_config
