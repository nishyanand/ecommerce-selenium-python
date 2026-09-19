"""
test_data_reader.py
Utility module to load test data from test_data/test_data.json.
"""

import json
from pathlib import Path

TEST_DATA_FILE_PATH = Path(__file__).resolve().parent.parent / "test_data" / "test_data.json"

def load_test_data(section=None):
    """
    Loads test data from test_data/test_data.json.
    
    Args:
        section (str, optional): Key for specific data group (e.g., 'valid_user', 'product').
                                 If None, returns the entire JSON dictionary.
                                 
    Returns:
        dict: Parsed test data dictionary.
    """
    if not TEST_DATA_FILE_PATH.exists():
        raise FileNotFoundError(f"Test data file not found at: {TEST_DATA_FILE_PATH}")
        
    with open(TEST_DATA_FILE_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    if section:
        if section not in data:
            raise KeyError(f"Section '{section}' not found in test data file {TEST_DATA_FILE_PATH}")
        return data[section]
        
    return data
