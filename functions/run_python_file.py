import os


def run_python_file(working_directory, file_path, args=[]):
    get_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not get_path.startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(get_path): 
        return print(f"Error: {file_path}") 
    if not get_path.endswith(".py"):  
        return f'Error: "{file_path}" is not a Python file.'
    x = subprocess.run(
        args,
        stdin=None, 
        input=None, 
        stdout=None,
        timeout=30
    )       
    return x    
