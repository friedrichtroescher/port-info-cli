import os
import json


def get_config_dir():
    """Get the platform-specific configuration directory."""
    if os.name == "nt":
        config_dir = os.path.join(os.environ.get("APPDATA", ""), "port-cli")
    else:
        config_dir = os.path.join(os.path.expanduser("~"), ".config", "port-cli")

    if not os.path.exists(config_dir):
        os.makedirs(config_dir)

    return config_dir


def load_port_data(json_file_path):
    """Load port data from the bundled JSON file."""
    try:
        with open(json_file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading port data: {e}")
        return {}


def load_original_data(config_dir):
    """Load the original port data from the config JSON file."""
    path = os.path.join(config_dir, "original_data.json")
    try:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}
    except Exception as e:
        print(f"Error loading original data: {e}")
        return {}


def save_original_data(data, config_dir):
    """Save the original port data to the config JSON file."""
    path = os.path.join(config_dir, "original_data.json")
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return path
    except Exception as e:
        print(f"Error saving original data: {e}")
        return None


def load_custom_data(config_dir):
    """Load custom port descriptions from the config JSON file."""
    path = os.path.join(config_dir, "custom_descriptions.json")
    try:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}
    except Exception as e:
        print(f"Error loading custom data: {e}")
        return {}


def save_custom_data(data, config_dir):
    """Save custom port descriptions to the config JSON file."""
    path = os.path.join(config_dir, "custom_descriptions.json")
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"Error saving custom data: {e}")
        return False


def find_port_key(port_str, data):
    """Find the matching key for a port number, handling ranges like '6660-6669'.

    Args:
        port_str: The port number as a string.
        data: The port data dictionary.

    Returns:
        The matching key string, or None if not found.
    """
    if port_str in data:
        return port_str

    try:
        port_num = int(port_str)
    except ValueError:
        return None

    for key in data:
        if "-" in key:
            try:
                start, end = key.split("-")
                if int(start) <= port_num <= int(end):
                    return key
            except ValueError:
                continue

    return None
