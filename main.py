import os
import sys
from google.genai import types
from google import genai
from dotenv import load_dotenv
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file
def main():


    if len(sys.argv) < 2:
        print("Error has occured")
        sys.exit(1)
    prompt_control = sys.argv[1]        
    load_dotenv()
    is_verbose = "--verbose" in sys.argv 
    system_prompt = """
        You are a helpful AI coding agent.

        When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

        - List files and directories
        - Read file contents
        - Execute Python files with optional arguments
        - Write or overwrite files

        Prefer returning a function call with the correct name and arguments over natural-language answers whenever a request maps to one of the operations. All paths must be relative to the working directory. Do not include a working_directory argument; it is injected automatically.
        """

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
        
    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_run_python_file,
            schema_write_file,
        ]
    )
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=prompt_control,
        config=types.GenerateContentConfig(
        tools=[available_functions],
        system_instruction=system_prompt
    ),
)

    if is_verbose:
         print(f"User prompt: {prompt_control}")
    try:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    except Exception:
        pass
    if getattr(response, "function_calls", None):
        for function_call_part in response.function_calls:
             print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
            print(response.text)


    
if __name__ == "__main__":
    main()
