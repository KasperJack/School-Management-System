import os
# Define the absolute path to the 'io' directory
ICONS = os.path.join(os.path.dirname(__file__), "TableIcons")



view_button_style_sheet = """
/* Base Style for All Buttons */
QPushButton {
    background-color: #ffffff; /* White background */
    color: #000000; /* Black text */
    border: 1px solid #cccccc; /* Light gray border */
    border-radius: 3px; /* Subtle rounded corners */
    padding: 4px 8px; /* Reduced padding for smaller size */
    font-family: "Segoe UI"; /* Windows system font */
    font-size: 10px; /* Smaller font size */
    min-width: 40px; /* Smaller minimum width */
    min-height: 20px; /* Smaller minimum height */
}

/* Hover State */
QPushButton:hover {
    background-color: #f0f0f0; /* Light gray on hover */
    border: 1px solid #999999; /* Darker gray border on hover */
}

/* Pressed State */
QPushButton:pressed {
    background-color: #e0e0e0; /* Slightly darker gray when pressed */
    border: 1px solid #777777; /* Darker gray border when pressed */
}

/* Disabled State */
QPushButton:disabled {
    background-color: #f8f8f8; /* Very light gray background */
    color: #a0a0a0; /* Gray text for disabled state */
    border: 1px solid #dddddd; /* Light gray border for disabled state */
}
"""





delete_button_style_sheet = """
/* Base Style for All Buttons */
QPushButton {
    background-color: #f0f0f0; /* Light gray background */
    color: #000000; /* Black text */
    border: 1px solid #cccccc; /* Light gray border */
    border-radius: 3px; /* Subtle rounded corners */
    padding: 4px 8px; /* Reduced padding for smaller size */
    font-family: "Segoe UI"; /* Windows system font */
    font-size: 10px; /* Smaller font size */
    min-width: 40px; /* Smaller minimum width */
    min-height: 20px; /* Smaller minimum height */
}

/* Hover State */
QPushButton:hover {
    background-color: #e6e6e6; /* Slightly darker gray on hover */
    border: 1px solid #999999; /* Darker border on hover */
}

/* Pressed State */
QPushButton:pressed {
    background-color: #d9d9d9; /* Even darker gray when pressed */
    border: 1px solid #666666; /* Darker border when pressed */
}

/* Disabled State */
QPushButton:disabled {
    background-color: #f0f0f0; /* Light gray background */
    color: #a0a0a0; /* Gray text for disabled state */
    border: 1px solid #cccccc; /* Light gray border */
}
"""






edit_button_style_sheet = """
/* Base Style for All Buttons */
QPushButton {
    background-color: #0078d7; /* Blue background for Edit */
    color: white; /* White text */
    border: 1px solid #005a9e; /* Darker blue border */
    border-radius: 3px; /* Subtle rounded corners */
    padding: 4px 8px; /* Reduced padding for smaller size */
    font-family: "Segoe UI"; /* Windows system font */
    font-size: 10px; /* Smaller font size */
    min-width: 40px; /* Smaller minimum width */
    min-height: 20px; /* Smaller minimum height */
}

/* Hover State */
QPushButton:hover {
    background-color: #005a9e; /* Darker blue on hover */
    border: 1px solid #004578; /* Even darker blue border on hover */
}

/* Pressed State */
QPushButton:pressed {
    background-color: #004578; /* Even darker blue when pressed */
    border: 1px solid #003366; /* Darkest blue border when pressed */
}

/* Disabled State */
QPushButton:disabled {
    background-color: #e0e0e0; /* Light gray background */
    color: #a0a0a0; /* Gray text for disabled state */
    border: 1px solid #cccccc; /* Light gray border */
}
"""
















edit_s_button_style_sheet = """
/* Base Style for All Buttons */
QPushButton {
    background-color: #0078d7; /* Blue background for Edit */
    color: white; /* White text */
    border: 1px solid #005a9e; /* Darker blue border */
    border-radius: 3px; /* Subtle rounded corners */
    padding: 4px 8px; /* Reduced padding for smaller size */
    font-family: "Segoe UI"; /* Windows system font */
    font-size: 12px; /* Smaller font size */
    min-width: 20px; /* Smaller minimum width */
    min-height: 10px; /* Smaller minimum height */
}

/* Hover State */
QPushButton:hover {
    background-color: #005a9e; /* Darker blue on hover */
    border: 1px solid #004578; /* Even darker blue border on hover */
}

/* Pressed State */
QPushButton:pressed {
    background-color: #004578; /* Even darker blue when pressed */
    border: 1px solid #003366; /* Darkest blue border when pressed */
}

/* Disabled State */
QPushButton:disabled {
    background-color: #e0e0e0; /* Light gray background */
    color: #a0a0a0; /* Gray text for disabled state */
    border: 1px solid #cccccc; /* Light gray border */
}
"""


delete_s_button_style_sheet = """ /* Base Style for All Buttons */
QPushButton {
    background-color: #D83B01; /* Orange-red background for Remove */
    color: white; /* White text */
    border: 1px solid #A82A00; /* Darker red border */
    border-radius: 3px; /* Subtle rounded corners */
    padding: 4px 8px; /* Reduced padding for smaller size */
    font-family: "Segoe UI"; /* Windows system font */
    font-size: 12px; /* Smaller font size */
    min-width: 20px; /* Smaller minimum width */
    min-height: 10px; /* Smaller minimum height */
}

/* Hover State */
QPushButton:hover {
    background-color: #A82A00; /* Darker red on hover */
    border: 1px solid #861F00; /* Even darker red border on hover */
}

/* Pressed State */
QPushButton:pressed {
    background-color: #861F00; /* Darkest red when pressed */
    border: 1px solid #6B1600; /* Strong border for pressed state */
}

/* Disabled State */
QPushButton:disabled {
    background-color: #F4F4F4; /* Very light gray background */
    color: #B4B4B4; /* Muted text color */
    border: 1px solid #E0E0E0; /* Soft gray border */
}

"""