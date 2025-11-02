import os

def write_file(working_directory, file_path, content):
    get_path = os.path.abspath(os.path.join(working_directory, file_path))

    # Security check
    if not get_path.startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    try:
        # Create directories if they don't exist
        os.makedirs(os.path.dirname(get_path), exist_ok=True)

        # Write (overwrite) file content
        with open(get_path, "w", encoding="utf-8") as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f"Error: {e}"



