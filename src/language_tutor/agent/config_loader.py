import yaml
from pathlib import Path

PROMPTS_PATH = Path(__file__).parent.parent.parent.parent / "config" / "prompts.yaml"


def get_node_config(node_name: str, version: str = None):
    """
    Returns a tuple of (model_name, prompt, temperature) based on your settings.

    Takes node_name and an optional version. If version not included, the
    default version for the node will be used.

    Args:
        node_name: The name of the node found in 'config/prompts.yaml'
            i.e 'japanese_tutor'.
        version: A string of the version number in the format i.e. "v0.1.0".
            If not provided the default for the node will be used.

    Returns:
        A tuple of (model_name, prompt, temperature)
    """

    with open(PROMPTS_PATH, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    node_data = config[node_name]

    # Get a specific versions config (defaults to "current_version" in file)
    active_version = version if version else node_data["current_version"]
    versioned_data = node_data["versions"][active_version]

    # Extract config based on version
    model_name = versioned_data["model"]
    prompt = versioned_data["prompt"]
    temperature = versioned_data.get("temperature", 1.0)  # matches langchain default

    return model_name, prompt, temperature
