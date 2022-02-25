import json
import os
import shutil

from utils.configuration import Configuration
from utils.template_config_parser import parse_definitions


class InitProject:
    """
    Class for creating new project from
    specific template
    """

    # List of templates
    templates: list[str]

    # Selected template
    template: str

    config: Configuration

    def __init__(self, config: Configuration):
        self.config = config

        # Create templates folder if not exist
        if not os.path.exists(config.get_templates_path()):
            os.makedirs(config.get_templates_path())
            print(f"- No valid templates found under {config.get_templates_path()}")
            return

        # Get templates from folder
        self.templates = self._filter_templates([
            template for template in os.listdir(config.get_templates_path())
            if os.path.isdir(os.path.join(config.get_templates_path(), template))
        ])

        # Check valid templates count
        if len(self.templates) < 1:
            print(f"- No valid templates found under {config.get_templates_path()}")
            return

        print(f"Found {len(self.templates)} valid templates")

        # Get template name from user
        template = input(f"Select template (default: {self.templates[-1]}): ") or self.templates[-1]

        print(f"+ {template} template selected")

        # Get project location from user
        location = input(
            f"Project location (default: {config.get_property('projects-location')}):\n> ") or os.path.join(
            config.get_property("projects-location"), template
        )

        # Make sure a project with that name does not exist
        if os.path.exists(location):
            print("- Location already exist")
            return

        # Open template config file
        template_config_file = open(os.path.join(config.get_templates_path(), template, "init-project.json"), "r")
        try:
            # Try to parse config fil content as json and get definitions
            template_config = parse_definitions(json.loads(template_config_file.read()), config)

        except json.decoder.JSONDecodeError:
            print(f"- Invalid template configuration file")
            return

        # Close file
        template_config_file.close()

        # Copy template files to defined location
        shutil.copytree(os.path.join(config.get_templates_path(), template), location)

        # Process template config "files" key
        for filename, changelist in dict(template_config["files"]).items():
            # Get absolute file path
            path = os.path.join(location, filename)

            # Check if file exist
            if not os.path.exists(path):
                print(f"- File {filename} is defined in template config, but file itself does not exist")
                continue

            # Read file content
            file = open(path, "r")
            file_data = file.read()
            file.close()

            # Replace variables in file
            for var_name, value in dict(changelist).items():
                file_data = file_data.replace(
                    var_name,
                    template_config["define"][value] if value in template_config["define"] else value
                )

            # Write processed data to file
            file = open(path, "w")
            file.write(file_data)
            file.close()

        print(f"Project created at {location}")

    def _filter_templates(self, templates: list[str]):
        """
        Method for filtering templates list
        :param templates: list of templates (not filtered)
        :return: filtered templates list
        """
        return list(filter(
            lambda template: "init-project.json" in os.listdir(
                os.path.join(self.config.get_templates_path(), template)),
            templates
        ))


if __name__ == "__main__":
    InitProject(Configuration())
