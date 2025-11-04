import os
import sys
from google.genai import types
from google import genai
from dotenv import load_dotenv
from functions.get_files_info import schema_get_files_info
def main():
    load_dotenv()
    is_verbose = "--verbose" in sys.argv 
    system_prompt = """
    You are a helpful AI coding agent.

    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

    - List files and directories

    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """
    available_functions = types.Tool(function_declarations=[schema_get_files_info])
    api_key = os.environ.get("GEMINI_API_KEY")
    prompt_control = sys.argv[1]
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=prompt_control,
        config=types.GenerateContentConfig(
        tools=[available_functions],
        system_instruction=system_prompt
    ),
)
    if len(sys.argv) < 2:
        print("Error has occured")
        sys.exit(1)    
    if "--verbose" in sys.argv:    
        print(f"User prompt: {prompt_control}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
        print(response.text)
    print("Error No --verbose")
    print(response.text)

    
if __name__ == "__main__":
    main()
