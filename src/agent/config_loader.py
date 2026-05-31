import yaml
from pathlib import Path

PROMPTS_PATH = Path(__file__).parent.parent.parent / "config" / "prompts.yaml"

def get_node_config(node_name: str, version=None):

    with open(PROMPTS_PATH, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    node_data = config[node_name]

    # Get a specific versions config (defaults to "current_version" in file)
    active_version = version if version else node_data["current_version"]
    versioned_data = node_data["versions"][active_version]

    # Extract config based on version
    model_name = versioned_data["model"]
    prompt = versioned_data["prompt"]
    temperature = versioned_data.get("temperature", 1.0) # matches langchain default
    
    return model_name, prompt, temperature