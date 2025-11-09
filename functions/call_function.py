from get_files_info import schema_get_files_info
from get_file_content import schema_get_file_content
from run_python_file import schema_run_python_file
from write_file import schema_write_file


def call_function(function_call_part, verbose=False):

    function_map = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "run_python_file":  run_python_file,
        "write_file": write_file

    }
    if verbose == True:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")   
    
    function_name = function_call_part.name
    #  Dont forget to use types.content
    function_arg = dict(function_call_part.args or {})
    fn = function_map.get(function_name)

    function_arg["working_directory"] = "calculator"

    result = fn(**function_arg)





    

