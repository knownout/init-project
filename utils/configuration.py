import json
import os

CONFIG_FILE_PATH = os.path.join(os.getcwd(), "config.json")
DEFAULT_CONFIGURATION = {
    "templates": os.path.join(os.getcwd(), "templates"),
    "default-author": "Alexandr <re-knownout> knownout@hotmail.com",
    "author": "Alexandr <re-knownout> knownout@hotmail.com",
    "projects-location": os.path.join(os.getcwd(), "projects")
}


class Configuration:
    _config = DEFAULT_CONFIGURATION

    def __init__(self):
        if os.path.exists(CONFIG_FILE_PATH):
            file = open(CONFIG_FILE_PATH, "r+")
            try:
                self._config = json.loads(file.read())

            except json.decoder.JSONDecodeError:
                print("- Invalid config file found, default configuration loaded")
                self._config = DEFAULT_CONFIGURATION

            file.close()

        else:
            file = open(CONFIG_FILE_PATH, "w+")
            file.write(json.dumps(DEFAULT_CONFIGURATION, indent=4, sort_keys=True))
            print(f"+ Created configuration file from default configuration at {CONFIG_FILE_PATH}")

            file.close()

    def get_templates_path(self):
        if "templates" in self._config:
            return self._config["templates"]
        else:
            return DEFAULT_CONFIGURATION["templates"]

    def get_property(self, prop: str):
        if prop in self._config:
            return self._config[prop]
        elif prop in DEFAULT_CONFIGURATION:
            return DEFAULT_CONFIGURATION[prop]

        return None
