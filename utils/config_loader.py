import yaml

def load_config(config_path : str = "config/config.yaml") -> dict:
    with open(config_path, 'r') as file:
        # yaml.safe_load parses the YAML file into nested Python dictionaries.
        config = yaml.safe_load(file)

    return config
    # output will look like this:
    # {'llm': {'groq': {'provider': 'groq', 'model_name': 'openai/gpt-oss-120b'}}}

