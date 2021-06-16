"""
Python module for handling string parsed data tables.

Classes:

    TableParser

Functions:

    parse_to_dict(keys, values) -> dict

"""
from main.pivotal.utils.api_constants import INT_KEY_LIST


class TableParser:
    """
    Table parser for string based data tables.
    """
    @staticmethod
    def parse_to_dict(keys, values):
        """
        parses the keys and values of a table to a dict.
        Args:
            keys(list): list of keys
            values(list): list of values

        Returns:
            dict: dictionary containing keys:values
        """
        body_dict = {}
        for key, value in zip(keys, values):
            if key in INT_KEY_LIST:
                value = int(value)
            body_dict.update({key: value})
        return body_dict
