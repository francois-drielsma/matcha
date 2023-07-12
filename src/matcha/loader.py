import os
import yaml
"""
Module to load and validate the yaml config file.
"""

def validate_config(config):

    trigger_timestamp = config['dca_parameters']['trigger_timestamp']
    isdata = config['dca_parameters']['isdata']
    if trigger_timestamp is None and isdata == True:
        raise ValueError('trigger_timestamp must be specified when isdata = True')

    file_save_config = config['file_save_config']
    save_file_path = file_save_config['save_file_path']
    if not os.path.exists(save_file_path):
        raise ValueError('save_file_path {:s} does not exist'.format(save_file_path))

    return True

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

    validate_config(config)
    print('*******Running with config********\n', yaml.dump(config))
    print('**********************************')

    return config
