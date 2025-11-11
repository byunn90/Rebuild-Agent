import os
import sys
import time
import random
from google.genai import types, errors as genai_errors
from google import genai
from dotenv import load_dotenv

from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file
from functions.call_function import call_function

MAX_ITERS = 20

def call_model_with_retry(client, *, model, contents, config, tries=3):
    delay = 1.0
    for _ in range(tries):
        try:
            return client.models.generate_content(model=model, contents=contents, config=config)
        except genai_errors.ClientError as e:
            if getattr(e, "status_code", None) == 429:
                time.sleep(delay + random.uniform(0.1, 0.3))
                delay = min(delay * 2, 4.0)
                continue
            raise
    return client.models.generate_content(model=model, contents=contents, config=config)

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
When the user asks about the calculator or code behavior, ALWAYS:
1) Call get_files_info to see available files (working dir is ./calculator).
2) Call get_file_content on likely targets (e.g., calculator/pkg/calculator.py, calculator/main.py).
3) Make fixes via write_file or verify via run_python_file.
Prefer tool calls over clarifying questions. Paths are relative; do NOT include working_directory (it is injected). When done, return normal text.
"""

    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_run_python_file,
            schema_write_file,
        ]
    )

    config = types.GenerateContentConfig(
        tools=[available_functions],
        system_instruction=system_prompt,
    )

    messages = [
        types.Content(
            role="user",
            parts=[types.Part.from_text(text=prompt_control)],
        )
    ]

    for i in range(MAX_ITERS):
        if is_verbose:
            print(f"\n=== ITERATION {i+1} ===")

        response = call_model_with_retry(
            client,
            model="gemini-2.0-flash-001",
            contents=messages,
            config=config,
        )

        try:
            pm = response.usage_metadata
            if pm:
                print(f"Prompt tokens: {pm.prompt_token_count}")
                print(f"Response tokens: {pm.candidates_token_count}")
        except Exception:
            pass

        tools_called = False

        candidates = getattr(response, "candidates", []) or []
        for cand in candidates:
            messages.append(cand.content)

            for part in cand.content.parts:
                fc = getattr(part, "function_call", None)
                if not fc:
                    continue

                tools_called = True
                args = dict(fc.args or {})
                args["working_directory"] = "calculator"
                fc.args = args

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

        if (not tools_called) and getattr(response, "text", None):
            print("Final response:\n" + response.text)
            break

        time.sleep(0.3)
    else:
        print(f"Maximum iterations ({MAX_ITERS}) reached without a final text response.")

if __name__ == "__main__":
    main()
