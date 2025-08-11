import os
import sys 
from dotenv import load_dotenv
from google import genai
from google.genai import types
from config import system_prompt
from functions.get_files_info import schema_get_files_info, get_files_info
from functions.get_file_content import schema_get_file_content, get_file_content
from functions.run_python import schema_run_python_file, run_python_file
from functions.write_file import schema_write_file, write_file

def main():
    load_dotenv()
    args = sys.argv[1:]   
    if not args:
        sys.exit(1)

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key) 
    isVerbose = False
    if args and args[-1] == "--verbose":
        isVerbose = True
        args = args[:-1]  

    user_prompt = " ".join(args)
    if isVerbose:
        print(f"User prompt: {user_prompt}\n")

    messages = [
            types.Content(role="user", parts=[types.Part(text=user_prompt)]),
        ]
    generate_content(client, messages, isVerbose)


def generate_content(client, messages, verbose):
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

    if verbose:
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)

    if not response.function_calls:
        return response.text
    
    function_responses = []
    for function_call_part in response.function_calls:
        function_call_result = call_function(function_call_part, verbose)
        if (
            not function_call_result.parts
            or not function_call_result.parts[0].function_response
        ):
            raise Exception("empty function call result")
        if verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")
        function_responses.append(function_call_result.parts[0])

    if not function_responses:
        raise Exception("no function responses generated, exiting.")


def call_function(function_call_part, verbose=False):
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    
    else:
        print(f" - Calling function: {function_call_part.name}")
    available_functions = {"get_files_info":get_files_info, "get_file_content" :get_file_content,
            "run_python_file":run_python_file, "write_file" :write_file,
    }
    
    args = {**function_call_part.args, "working_directory": "./calculator"}
    
    if available_functions.get(function_call_part.name) == None:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"error": f"Unknown function: {function_call_part.name}"},
                )
            ],
        )
    
    else: 
        called_fn = available_functions[function_call_part.name] 
        res = called_fn(**args)
        print(res)
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"result": res},
                )
            ],
        )

if __name__ == "__main__":
    main()