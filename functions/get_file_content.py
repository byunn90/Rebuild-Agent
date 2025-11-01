import os
from functions.config import MAX_CHARS

def get_file_content(working_directory, file_path):
    get_path = os.path.abspath(os.path.join(working_directory, file_path))
    file_content_string = os.listdir(get_path)
    
    if not get_path.startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(get_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    # Question 
    #  Read the file and return its contents as a string.
    #  I'll list some useful standard library functions in the tips section below.
    #  If the file is longer than 10000 characters, truncate it to 10000 characters and append this message to the end [...File "{file_path}" truncated at 10000 characters].
    #  Instead of hard-coding the 10000 character limit, I stored it in a config.py file.
    #  Use to get the contents os.listdir(): List the contents of a directory
    try:
        with open(get_path, "r", encoding="utf-8") as f:
            file_content_string = f.read(MAX_CHARS)
            extra = f.read(1)  # check if there’s more content
        if extra:
            file_content_string += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
        return file_content_string
    except Exception as e:
        return f"Error: {e}"



    # code that might raise an error
    except Exception as e:
    # code to handle the error


    
