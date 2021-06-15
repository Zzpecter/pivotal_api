"""
Python module for handling everything related to regular expressions.

Classes:

    StringUtils

Functions:

    replace_string(pattern, base_string, replace_string) -> string

"""
import re


class StringUtils:
    """
    Regular expression handler is a static class for manipulating strings
    based on RE's
    """

    @staticmethod
    def replace_string(base_string, replace_string, pattern=r"<(\w+)>"):
        """
        Function that receives a base string, some other string to
        replace parts of the base string and a regular expression
        to validate when the replace string should be applied.
        Args:
            base_string(str): the original string sent to the function
            replace_string(str): the string which should be inserted if the
            replacement pattern is found
            pattern(str): the pattern that is going to be replaced from the
            string.
        Returns:
            string: the base string updated.

        """
        return re.sub(pattern, replace_string, base_string)
