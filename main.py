import os
import sys
from google import genai
from dotenv import load_dotenv



def main():
    load_dotenv()
    prompt_control = sys.argv[0]
    api_key = os.environ.get("GEMINI_API_KEY")

    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=prompt_control

        
    )
    print("Prompt tokens:", response.usage_metadata.prompt_token_count)
    print("Response tokens:", response.usage_metadata.candidates_token_count)
    print("Response:")
    print(response.text)

    if len(sys.argv) < 2:
        print("Error has occured")
        sys.exit(1)
    print(prompt_control)    


if __name__ == "__main__":
    main()
