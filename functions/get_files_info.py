import os
from google import genai
from dotenv import load_dotenv



def get_files_info(working_directory, directory="."):
    finding_directory = os.path.abspath(os.path.join(working_directory, directory))
    get_contents_of_path = os.listdir(finding_directory)
    new_array = []
    # What we need now 
    # - README.md: file_size=1032 bytes, is_dir=False
    # - src: file_size=128 bytes, is_dir=True
    # - package.json: file_size=1234 bytes, is_dir=False
    if not finding_directory.startswith(working_directory): 
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(directory):
        return f'Error: "{directory}" is not a directory'
    for i in get_contents_of_path:
        print(i)
        new_array.append(i)
    return print(new_array)    

    

get_files_info("calculator", ".")

