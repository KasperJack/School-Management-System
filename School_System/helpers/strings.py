

import re

def format_name(input_string, length=None):
    """
    Formats a name string: strips whitespace, capitalizes each word,
    checks for numbers, and validates length.

    Args:
        input_string (str): The name string to format.
        length (int, optional): The desired length of the name.

    Returns:
        str: The formatted name string, or False if validation fails.
    """
    if not isinstance(input_string, str):
        return False

    stripped_string = input_string.strip()

    if not stripped_string:
        return False

    if re.search(r'\d', stripped_string):  # Check for numbers
        return False

    words = stripped_string.split()
    capitalized_words = [word[0].upper() + word[1:].lower() for word in words]
    formatted_name = " ".join(capitalized_words)

    if length is not None and len(formatted_name) != length:
        return False

    return formatted_name
