

def format_name(input_string):

    if not isinstance(input_string, str):
        return ""

    stripped_string = input_string.strip()  # Remove leading/trailing whitespace

    if not stripped_string:
        return ""

    return stripped_string[0].upper() + stripped_string[1:]  # Capitalize first letter

