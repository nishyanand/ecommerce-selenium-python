"""
config_reader.py
Utility module to read project configuration from config/config.json.
"""

import json
from pathlib import Path

CONFIG_FILE_PATH = Path(__file__).resolve().parent.parent / "config" / "config.json"

def load_config():
    """
    Loads and returns configuration settings from config/config.json.
    Returns:
        dict: Configuration dictionary containing base_url, timeout, browser, etc.
    """
    if not CONFIG_FILE_PATH.exists():
        raise FileNotFoundError(f"Configuration file not found at: {CONFIG_FILE_PATH}")
    
    with open(CONFIG_FILE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def get_base_url():
    """Returns the base application URL from configuration."""
    return load_config().get("base_url", "https://tutorialsninja.com/demo/")

def get_timeout():
    """Returns the explicit timeout duration in seconds."""
    return load_config().get("timeout", 10)

def is_headless():
    """Returns boolean indicating if headless execution is enabled."""
    return load_config().get("headless", True)
