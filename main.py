import os
import sys
import time
import random
import traceback
from google.genai import types, errors as genai_errors
from google import genai
from dotenv import load_dotenv

# Tool schemas + your dispatcher
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file
from functions.call_function import call_function


MAX_ITERS = 20

def call_model_with_retry(client, *, model, contents, config, tries=3):
    """Retry generate_content on 429 (rate/quota) with small backoff."""
    delay = 1.0
    for attempt in range(1, tries + 1):
        try:
            return client.models.generate_content(
                model=model, contents=contents, config=config
            )
        except genai_errors.ClientError as e:
            if getattr(e, "status_code", None) == 429:
                # gentle, bounded backoff with a touch of jitter
                sleep_for = delay + random.uniform(0.1, 0.3)
                print(f"[retry {attempt}] 429 RESOURCE_EXHAUSTED; waiting {sleep_for:.1f}s")
                time.sleep(sleep_for)
                delay = min(delay * 2, 4.0)
                continue
            raise


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

        When the user asks about how code works or mentions 'calculator', ALWAYS:
        1) Call get_files_info first to see available files (working dir is ./calculator).
        2) Then call get_file_content on likely targets (e.g., main.py, calculator.py).
        3) Only after inspecting files, explain the answer in normal text.

        Rules:
        - Prefer tool calls over clarifying questions.
        - All paths are relative; DO NOT include working_directory (it is injected automatically).
        - When you are done, return a normal text response (no more tool calls).
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

    if is_verbose:
        print(f"User prompt: {prompt_control}")

    try:
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


            time.sleep(0.3)

        else:
            print(f"Maximum iterations ({MAX_ITERS}) reached without a final text response.")

    except Exception:
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
