import os
import sys 
from dotenv import load_dotenv
from google import genai
from google.genai import types

def main():
    load_dotenv()
    args = sys.argv[1:]   
    if not args:
        sys.exit(1)

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key) 

    user_prompt = " ".join(args)

    messages = [
            types.Content(role="user", parts=[types.Part(text=user_prompt)]),
        ]
    generate_content(client, messages)


def generate_content(client, messages):
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
    )
    prompt_text = messages[0].parts[0].text
    if prompt_text.endswith("--verbose"):
        print(f"User prompt: {prompt_text}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    else:    
        print("Response:")
        print(response.text)

if __name__ == "__main__":
    main()
