import os
import sys 
from dotenv import load_dotenv
from google import genai
from google.genai import types
from config import system_prompt
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python import schema_run_python_file
from functions.write_file import schema_write_file

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
    available_functions = types.Tool(
        function_declarations=[schema_get_files_info, schema_get_file_content,
            schema_run_python_file, schema_write_file,
                ]
            )
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt)
    )
    
    prompt_text = messages[0].parts[0].text
    if prompt_text.endswith("--verbose"):
        print(f"User prompt: {prompt_text}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    elif response.function_calls is not None:
        function_call_part = response.function_calls[0] if response.function_calls else None
        if function_call_part:
            print(f"Calling function: {function_call_part.name}({function_call_part.args})")
            print(response.text)
        else:
            print("Function call information is missing in the response.")
            print(response.text)
    else:
        print("Response:")
        print(response.text)

if __name__ == "__main__":
    main()