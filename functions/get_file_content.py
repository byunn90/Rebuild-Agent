import os
from functions.config import MAX_CHARS  # MAX_CHARS = 10000 in functions/config.py

def get_file_content(working_directory, file_path):
    get_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not get_path.startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(get_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    try:
        with open(get_path, "r", encoding="utf-8", errors="replace") as f:
            s = f.read(MAX_CHARS)
            extra = f.read(1)
            if extra:
                s += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
        return s
    except Exception as e:
        return f"Error: {e}"




    
