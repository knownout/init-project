import json
import os
import shutil

from utils.configuration import Configuration
from utils.template_config_parser import parse_definitions

config = Configuration()


class TemplateBuilder:
    templates: list[str]
    template: str

    def __init__(self):
        if not os.path.exists(config.get_templates_path()):
            os.makedirs(config.get_templates_path())

        self.templates = self._filter_templates([
            template for template in os.listdir(config.get_templates_path())
            if os.path.isdir(os.path.join(config.get_templates_path(), template))
        ])

        if len(self.templates) < 1:
            print(f"- No valid templates found under {config.get_templates_path()}")
            return

        print(f"Found {len(self.templates)} valid templates")
        template = input(f"Select template (default: {self.templates[-1]}): ") or self.templates[-1]

        print(f"+ {template} template selected")
        location = input(
            f"Project location (default: {config.get_property('projects-location')}):\n> ") or os.path.join(
            config.get_property("projects-location"), template
        )

        if os.path.exists(location):
            print("- Location already exist")
            return

        template_config_file = open(os.path.join(config.get_templates_path(), template, "init-project.json"), "r")
        try:
            template_config = parse_definitions(json.loads(template_config_file.read()), config)

        except json.decoder.JSONDecodeError:
            print(f"- Invalid template configuration file")
            return

        template_config_file.close()

        shutil.copytree(os.path.join(config.get_templates_path(), template), location)

        for filename, changelist in dict(template_config["files"]).items():
            path = os.path.join(location, filename)
            if not os.path.exists(path):
                print(f"- File {filename} is defined in template config, but file itself does not exist")
                continue

            file = open(path, "r")
            file_data = file.read()

            for var_name, value in dict(changelist).items():
                file_data = file_data.replace(
                    var_name,
                    template_config["define"][value] if value in template_config["define"] else value
                )

            file.close()
            file = open(path, "w")
            file.write(file_data)
            file.close()

        print(f"Project created at {location}")

    @staticmethod
    def _filter_templates(templates: list[str]):
        return list(filter(
            lambda template: "init-project.json" in os.listdir(os.path.join(config.get_templates_path(), template)),
            templates
        ))


template_builder = TemplateBuilder()
