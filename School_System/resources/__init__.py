import os
# Define the absolute path to the 'io' directory
ICONS = os.path.join(os.path.dirname(__file__), "TableIcons")



view_button_style_sheet = """ /* Base Style for All Buttons */
QPushButton {
    background-color: #f0f0f0; /* Light gray background */
    color: #000000; /* Black text */
    border: 1px solid #cccccc; /* Light gray border */
    border-radius: 4px; /* Rounded corners */
    padding: 6px 12px; /* Padding inside the button */
    font-family: "Segoe UI"; /* Windows system font */
    font-size: 12px; /* Small font size */
    min-width: 60px; /* Minimum width for consistency */
    min-height: 24px; /* Minimum height for consistency */
}

/* Hover State */
QPushButton:hover {
    background-color: #e0e0e0; /* Slightly darker gray on hover */
    border: 1px solid #999999; /* Darker border on hover */
}

/* Pressed State */
QPushButton:pressed {
    background-color: #d0d0d0; /* Even darker gray when pressed */
    border: 1px solid #777777; /* Darker border when pressed */
}


/* View Button Specific Style */
QPushButton {
    background-color: #107c10; /* Green background for View */
    color: white; /* White text for View */
    border: 1px solid #0a4f0a; /* Darker green border */
}

QPushButton:hover {
    background-color: #0a4f0a; /* Darker green on hover */
    border: 1px solid #063806; /* Even darker green border on hover */
}

QPushButton:pressed {
    background-color: #063806; /* Even darker green when pressed */
    border: 1px solid #042504; /* Darkest green border when pressed */
}"""


delete_button_style_sheet = """ /* Base Style for All Buttons */
QPushButton {
    background-color: #f0f0f0; /* Light gray background */
    color: #000000; /* Black text */
    border: 1px solid #cccccc; /* Light gray border */
    border-radius: 4px; /* Rounded corners */
    padding: 6px 12px; /* Padding inside the button */
    font-family: "Segoe UI"; /* Windows system font */
    font-size: 12px; /* Small font size */
    min-width: 60px; /* Minimum width for consistency */
    min-height: 24px; /* Minimum height for consistency */
}

/* Hover State */
QPushButton:hover {
    background-color: #e0e0e0; /* Slightly darker gray on hover */
    border: 1px solid #999999; /* Darker border on hover */
}

/* Pressed State */
QPushButton:pressed {
    background-color: #d0d0d0; /* Even darker gray when pressed */
    border: 1px solid #777777; /* Darker border when pressed */
}


/* Delete Button Specific Style */
QPushButton {
    background-color: #d83b01; /* Red background for Delete */
    color: white; /* White text for Delete */
    border: 1px solid #a52a00; /* Darker red border */
}

QPushButton:hover {
    background-color: #a52a00; /* Darker red on hover */
    border: 1px solid #7f1d00; /* Even darker red border on hover */
}

QPushButton:pressed {
    background-color: #7f1d00; /* Even darker red when pressed */
    border: 1px solid #5a1400; /* Darkest red border when pressed */
}  """




edit_button_style_sheet = """ /* Base Style for All Buttons */
QPushButton {
    background-color: #f0f0f0; /* Light gray background */
    color: #000000; /* Black text */
    border: 1px solid #cccccc; /* Light gray border */
    border-radius: 4px; /* Rounded corners */
    padding: 6px 12px; /* Padding inside the button */
    font-family: "Segoe UI"; /* Windows system font */
    font-size: 12px; /* Small font size */
    min-width: 60px; /* Minimum width for consistency */
    min-height: 24px; /* Minimum height for consistency */
}

/* Hover State */
QPushButton:hover {
    background-color: #e0e0e0; /* Slightly darker gray on hover */
    border: 1px solid #999999; /* Darker border on hover */
}

/* Pressed State */
QPushButton:pressed {
    background-color: #d0d0d0; /* Even darker gray when pressed */
    border: 1px solid #777777; /* Darker border when pressed */
}

/* Edit Button Specific Style */
QPushButton {
    background-color: #0078d7; /* Blue background for Edit */
    color: white; /* White text for Edit */
    border: 1px solid #005a9e; /* Darker blue border */
}

QPushButton:hover {
    background-color: #005a9e; /* Darker blue on hover */
    border: 1px solid #004578; /* Even darker blue border on hover */
}

QPushButton:pressed {
    background-color: #004578; /* Even darker blue when pressed */
    border: 1px solid #003366; /* Darkest blue border when pressed */
}

 """
