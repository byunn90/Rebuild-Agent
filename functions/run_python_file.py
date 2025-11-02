import os


def run_python_file(working_directory, file_path, args=[]):
    get_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not get_path.startswith(os.path.abspath(working_directory)):
         return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not get_path.os.path.exists(file_path):
        return print(f"Error: {file_path}") 