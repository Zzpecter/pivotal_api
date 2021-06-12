"""
Python helper module for reading the contents of different file formats.


Functions:

    read_json(file) -> dict
    read_yaml(file) -> dict

Misc variables:

    file
"""
import json
import yaml


def read_json(file):
    """
    Helper function for reading JSON files

    Parameters
    ----------
        file : str
            Path to the file to be read

    Returns
    ----------
        data : dict
            Dict-parsed data of the JSON file read
    """
    with open(file) as file_stream:
        data = json.load(file_stream)
    return data


def read_yaml(file):
    """
    Helper function for reading YAML files

    Parameters
    ----------
        file : str
            Path to the file to be read

    Returns
    ----------
        data : dict
            Dict-parsed data of the YAML file read
    """
    with open(file, 'r') as file_stream:
        data = yaml.safe_load(file_stream.read())
    return data
