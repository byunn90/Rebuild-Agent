import os
from google.genai import types
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)
def get_files_info(working_directory, directory="."):
    results = []
    get_path = os.path.abspath(os.path.join(working_directory, directory))

    if not get_path.startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(get_path):
        return f'Error: "{directory}" is not a directory'

    for item in os.listdir(get_path):
        full_path = os.path.join(get_path, item)
        file_size = os.path.getsize(full_path)
        is_dir = os.path.isdir(full_path)
        results.append(f"- {item}: file_size={file_size} bytes, is_dir={is_dir}")

    return "\n".join(results)

