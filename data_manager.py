import os
import sys
from utils import (
    get_config_dir,
    load_port_data,
    save_original_data,
    load_original_data,
    load_custom_data,
    save_custom_data,
    find_port_key,
)


class DataManager:
    def __init__(self, json_file_path):
        self.config_dir = get_config_dir()
        self.json_file_path = json_file_path
        self.original_data = {}
        self.custom_data = {}
        self.initialize_data()

    def initialize_data(self):
        """Initialize data by loading from config or importing from bundled JSON."""
        self.original_data = load_original_data(self.config_dir)

        if not self.original_data:
            self.original_data = load_port_data(self.json_file_path)
            if self.original_data:
                save_original_data(self.original_data, self.config_dir)
            else:
                print("Error: Could not load port data.")
                sys.exit(1)

        self.custom_data = load_custom_data(self.config_dir)

    def get_info(self, port):
        """Get info for a given port number.

        Args:
            port (str): The port number.

        Returns:
            dict or None: {"protocol", "service", "description"} or None.
        """
        if not port.isdigit():
            return None

        port_num = int(port)
        if port_num < 0 or port_num > 65535:
            return None

        # Check custom data first
        custom_key = find_port_key(port, self.custom_data)
        if custom_key:
            return self.custom_data[custom_key]

        # Then original data
        orig_key = find_port_key(port, self.original_data)
        if orig_key:
            return self.original_data[orig_key]

        return None

    def set_custom_description(self, port, description):
        """Set a custom description for a port.

        Args:
            port (str): The port number.
            description (str): The new description.

        Returns:
            bool: True if successful.
        """
        if not port.isdigit():
            return False

        key = find_port_key(port, self.original_data)
        if not key:
            return False

        if key not in self.custom_data:
            self.custom_data[key] = dict(self.original_data[key])
        self.custom_data[key]["description"] = description
        return save_custom_data(self.custom_data, self.config_dir)

    def reset_custom_description(self, port):
        """Reset the custom description for a port.

        Returns:
            bool: True if successful.
        """
        if not port.isdigit():
            return False

        key = find_port_key(port, self.custom_data)
        if not key:
            return False

        del self.custom_data[key]
        return save_custom_data(self.custom_data, self.config_dir)

    def reset_all_custom_descriptions(self):
        """Reset all custom descriptions."""
        self.custom_data = {}
        return save_custom_data(self.custom_data, self.config_dir)

    def has_custom_description(self, port):
        """Check if a custom description exists for a port."""
        return find_port_key(port, self.custom_data) is not None

    def get_all_ports(self):
        """Get all port keys."""
        return sorted(self.original_data.keys(), key=lambda k: int(k.split("-")[0]))
