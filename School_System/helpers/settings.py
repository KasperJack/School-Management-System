from School_System.conf import SETTINGS
import json
import os




def remember_mail():

    if os.path.exists(SETTINGS):
        try:
            with open(SETTINGS, "r") as f:
                settings = json.load(f)

            if settings.get('remember', False):
                return settings.get('email', None)

        except (FileNotFoundError, json.JSONDecodeError):
            pass

    return None




def set_remember_true():

    if os.path.exists(SETTINGS):
        try:
            with open(SETTINGS, "r") as f:
                settings = json.load(f)

            settings['remember'] = True

            with open(SETTINGS, "w") as f: #save the new setting.
                json.dump(settings, f, indent=4) #use indent for readability.

        except (FileNotFoundError, json.JSONDecodeError, KeyError, IOError) as e:
            print(f"Error setting 'remember' to True: {e}")
            # Handle errors (e.g., log them)




def set_remember_false():
    """
    Sets the 'remember' setting to False in the settings file.
    """
    if os.path.exists(SETTINGS):
        try:
            with open(SETTINGS, "r") as f:
                settings = json.load(f)

            settings['remember'] = False  # Set 'remember' to False

            with open(SETTINGS, "w") as f: #save the new setting.
                json.dump(settings, f, indent=4) #use indent for readability.

        except (FileNotFoundError, json.JSONDecodeError, KeyError, IOError) as e:
            print(f"Error setting 'remember' to False: {e}")
            # Handle errors (e.g., log them)






def add_email(email):

    if os.path.exists(SETTINGS):
        try:
            with open(SETTINGS, "r") as f:
                settings = json.load(f)

            settings['email'] = email  # Insert or update the 'email'

            with open(SETTINGS, "w") as f:
                json.dump(settings, f, indent=4)

        except (FileNotFoundError, json.JSONDecodeError, IOError) as e:
            print(f"Error inserting email: {e}")
            # Handle errors (e.g., log them)
    else:
        #if the file does not exist, create it with the email.
        try:
            settings = {'email':email}
            with open(SETTINGS, "w") as f:
                json.dump(settings, f, indent=4)
        except IOError as e:
            print(f"Error creating settings file: {e}")
