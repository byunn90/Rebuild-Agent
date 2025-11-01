import os
from google import genai
from dotenv import load_dotenv



def get_files_info(working_directory, directory="."):
    results = []
    # Get Path
    get_path = os.path.abspath(os.path.join(working_directory, directory))
    if not get_path.startswith(os.path.abspath(working_directory)):
         return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(get_path):
        return f'Error: "{directory}" is not a directory'
    # Get content 
    get_contents = os.listdir(get_path)    
    for item in get_contents:
        full_path = os.path.join(get_path, item)
        file_size = os.path.getsize(full_path)
        is_dir = os.path.isdir(full_path)
        line = f"- {item}: file_size={file_size} bytes, is_dir={is_dir}"
        results.append(line)
    return "\n".join(results)

get_files_info("calculator", ".")




    

get_files_info("calculator", ".")

