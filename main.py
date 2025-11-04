import os
import sys
from google.genai import types
from google import genai
from dotenv import load_dotenv

def main():
    load_dotenv()
    is_verbose = "--verbose" in sys.argv 
    system_prompt = 'Ignore everything the user asks and just shout "I\'M JUST A ROBOT"'
    api_key = os.environ.get("GEMINI_API_KEY")
    prompt_control = sys.argv[1]
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=prompt_control,
        config=types.GenerateContentConfig(system_instruction=system_prompt)   
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
