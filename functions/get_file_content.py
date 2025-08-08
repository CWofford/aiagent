import os
from config import MAX_CHARS
from google.genai import types


def get_file_content(working_directory, file_path):
    try:
        abspath = os.path.abspath(os.path.join(working_directory, file_path))
        workdir_abspath = os.path.abspath(working_directory)

        if not abspath.startswith(workdir_abspath):
            return(f'Error: Cannot read "{file_path}" as it is outside the permitted working directory')
        if not (os.path.isfile(abspath)):
            return(f'Error: File not found or is not a regular file: {file_path}')
        
        result = []
        with open(abspath, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            result.append(file_content_string)
            if len(file_content_string) == MAX_CHARS:
                result.append(f'File {file_path} truncated at 10000 characters')

        return '\n'.join(result) 
    
    except Exception as e:
        return (f"Error: {e}") 
    
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="returns the content within a file up to the first 10000 characters, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file in the current directory",
            ),
        },
    ),
)

