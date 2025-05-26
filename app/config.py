import yaml
from typing import Dict, Any

def load_config() -> Dict[str, Any]:
    """Load configuration from config.yaml"""
    with open("config.yaml", "r") as config_file:
        return yaml.safe_load(config_file)

# Global config instance
CONFIG = load_config() 