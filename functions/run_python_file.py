import os
import subprocess

def run_python_file(working_directory, file_path, args=[]):
    get_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not get_path.startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(get_path):
         return f'Error: File "{file_path}" not found.'
    if not get_path.endswith(".py"):  
        return f'Error: "{file_path}" is not a Python file.'
    try:    
        processes = subprocess.run(
            ["python3", get_path, *args],
            capture_output=True, 
            text=True,             
            timeout=30,
            cwd=working_directory
         )
        stdout_data = processes.stdout
        stderr_data = processes.stderr
        exit_code = processes.returncode
        if not stdout_data and not stderr_data:
            return "No output produced"

        result = f"STDOUT:\n{stdout_data}\nSTDERR:\n{stderr_data}"
        if exit_code != 0:
            result += f"\nProcess exited with code {exit_code}"
        return result.strip()
    except Exception as e:
        return f"Error: executing Python file: {e}"    

    


   
 

      
