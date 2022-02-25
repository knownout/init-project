import json
import os

# Path to script confguration file
CONFIG_FILE_PATH = os.path.join(os.getcwd(), "config.json")

# Default script configuration
DEFAULT_CONFIGURATION = {
    "templates": os.path.join(os.getcwd(), "templates"),
    "default-author": "Alexandr <re-knownout> knownout@hotmail.com",
    "author": "Alexandr <re-knownout> knownout@hotmail.com",
    "projects-location": os.path.join(os.getcwd(), "projects")
}


class Configuration:
    """
    Class for working with script configuration file
    """

    _config = DEFAULT_CONFIGURATION

    def __init__(self):
        # Check if config file exist
        if os.path.exists(CONFIG_FILE_PATH):
            file = open(CONFIG_FILE_PATH, "r+")

            # Try to parse config file as json
            try:
                self._config = json.loads(file.read())

            except json.decoder.JSONDecodeError:
                print("- Invalid config file found, default configuration loaded")

                # If file is invalid, use default configuration
                self._config = DEFAULT_CONFIGURATION

            file.close()

        else:
            # Create configuration file from default config (if not exist)
            file = open(CONFIG_FILE_PATH, "w+")
            file.write(json.dumps(DEFAULT_CONFIGURATION, indent=4, sort_keys=True))

            print(f"+ Created configuration file from default configuration at {CONFIG_FILE_PATH}")
            file.close()

    def get_templates_path(self):
        """
        Get path to templates folder
        :return: path to templates folder
        """
        if "templates" in self._config:
            return self._config["templates"]
        else:
            return DEFAULT_CONFIGURATION["templates"]

    def get_property(self, prop: str):
        """
        Get configuration property by name from script config
        :param prop: property name
        :return: property value
        """
        if prop in self._config:
            return self._config[prop]
        elif prop in DEFAULT_CONFIGURATION:
            return DEFAULT_CONFIGURATION[prop]

        return None
