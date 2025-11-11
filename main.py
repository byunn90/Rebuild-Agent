import os
import sys
from google.genai import types
from google import genai
from dotenv import load_dotenv

from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file
from functions.call_function import call_function


MAX_ITERS = 20

def main():
    if len(sys.argv) < 2:
        print("Error has occured")
        sys.exit(1)

    prompt_control = sys.argv[1]
    is_verbose = "--verbose" in sys.argv

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Missing GEMINI_API_KEY")
        sys.exit(1)

    client = genai.Client(api_key=api_key)

    system_prompt = """
    You are a helpful AI coding agent.

    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:
    - List files and directories
    - Read file contents
    - Execute Python files with optional arguments
    - Write or overwrite files

    Prefer returning a function call with the correct name and arguments over natural-language answers whenever a request maps to one of the operations.
    All paths must be relative to the working directory. Do not include a working_directory argument; it is injected automatically.

    When you are done, return a normal text response (no further tool calls).
    """


    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_run_python_file,
            schema_write_file,
        ]
    )


    messages = [
        types.Content(
            role="user",
            parts=[types.Part.from_text(text=prompt_control)],
        )
    ]

    config = types.GenerateContentConfig(
        tools=[available_functions],
        system_instruction=system_prompt,
    )

    if is_verbose:
        print(f"User prompt: {prompt_control}")


    for i in range(MAX_ITERS):
        if is_verbose:
            print(f"\n=== ITERATION {i+1} ===")

        response = client.models.generate_content(
            model="gemini-2.0-flash-001",
            contents=messages,
            config=config,
        )

        if getattr(response, "text", None):
            print("Final response:\n" + response.text)
            break


        candidates = getattr(response, "candidates", []) or []
        if is_verbose:
            print(f"Candidates: {len(candidates)}")

        for cand in candidates:

            messages.append(cand.content)


            for part in cand.content.parts:
                fc = getattr(part, "function_call", None)
                if not fc:
                    continue


                args = dict(fc.args or {})
                args["working_directory"] = "calculator"
                fc.args = args

                if is_verbose:
                    print(f" - Calling function: {fc.name}({list(args.keys())})")


                result = call_function(fc, verbose=is_verbose)

                messages.append(
                    types.Content(
                        role="user",
                        parts=[
                            types.Part.from_function_response(
                                name=fc.name,
                                response=result if isinstance(result, dict) else {"result": result},
                            )
                        ],
                    )
                )
    else:
        print(f"Maximum iterations ({MAX_ITERS}) reached without a final text response.")


if __name__ == "__main__":
    main()
