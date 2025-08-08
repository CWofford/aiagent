import os 
from google.genai import types

def write_file(working_directory, file_path, content):
    try:
        path = os.path.join(working_directory, file_path)
        abspath = os.path.abspath(path)
        workdir_abspath = os.path.abspath(working_directory)

        if not abspath.startswith(workdir_abspath) or os.path.isdir(abspath):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        if not (os.path.exists(abspath)):
            os.makedirs(os.path.dirname(abspath), exist_ok=True)
        with open(abspath, "w") as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
         
    except Exception as e:
        return f"Error: {e}"

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes or overwrites a file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file in the current directory",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="New text content to add or modify the selected file with",
            ),
        },
    ),
)

