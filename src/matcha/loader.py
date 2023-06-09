import yaml
"""
Simple module to load a yaml config file.
"""

def validate_config(config):
    trigger_timestamp = config['dca_parameters']['trigger_timestamp']
    isdata = config['dca_parameters']['isdata']
    if trigger_timestamp is None and isdata == True:
        raise ValueError('trigger_timestamp must be specified when running on data')
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
