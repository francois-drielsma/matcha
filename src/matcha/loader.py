import yaml
"""
Simple module to load a yaml config file.
"""

def load_config(file_path):
    """
    Load the yaml configuration file.

    Parameters:
        file_path (str): Path to the yaml configuraiton file.

    Returns:
        dict: Dictionary containing yaml configuration.
    """
    with open(file_path, 'r') as file:
        config = yaml.safe_load(file)
    return config
