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

    if not re.match(r'^[A-Za-z\s]+$', stripped_string):
        return False

    #if re.search(r'\d', stripped_string):
        #return False

    words = stripped_string.split()
    if len(words) > 3:
        return False

    capitalized_words = [word[0].upper() + word[1:].lower() for word in words]
    formatted_name = " ".join(capitalized_words)

    if length is not None and len(formatted_name) > length:
        return False

    return formatted_name







def format_name_complex(input_string, length=None):
    """
    Formats a complex name string: strips whitespace, capitalizes words,
    joins the last two words if there are at least three, returns False if more than 3 words.
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

    if not re.match(r'^[A-Za-z\s]+$', stripped_string):
        return False

    words = stripped_string.split()

    if len(words) > 3:
        return False

    if len(words) >= 3:
        # Join the last two words with the second word capitalized.
        last_two = words[-2][0].upper() + words[-2][1:].lower() + words[-1][0].upper() + words[-1][1:].lower()
        formatted_words = [word[0].upper() + word[1:].lower() for word in words[:-2]] + [last_two]

    else:
        # Standard capitalization if there are fewer than 3 words.
        formatted_words = [word[0].upper() + word[1:].lower() for word in words]

    formatted_name = " ".join(formatted_words)

    if length is not None and len(formatted_name) > length:
        return False

    return formatted_name

