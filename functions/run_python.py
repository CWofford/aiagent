import subprocess
import os
from google.genai import types


def run_python_file(working_directory, file_path, args=[]):
    try:
        abspath = os.path.abspath(os.path.join(working_directory, file_path))
        workdir_abspath = os.path.abspath(working_directory)

        if not abspath.startswith(workdir_abspath) or os.path.isdir(abspath):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
       
        if not (os.path.exists(abspath)):
           return f'Error: File "{file_path}" not found.'
        
        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file.'
        
        products = []

        try:
            result = subprocess.run(["python", file_path, *args], cwd = workdir_abspath, capture_output = True,
                         check=True, timeout = 30, text = True) 
            products.append("Process exited with code {e.returncode} ") 
            if result.stdout and result.stderr == None:
               products.append("No output produced")
            else:
                products.append(f"STDOUT: {result.stdout}")
            
        except subprocess.CalledProcessError as e:
            products.append(f"Process exited with code {e.returncode} ")
            products.append(f"STDERR: {e.stderr}")

        return '\n'.join(products)

    except Exception as e:
        return f"Error: executing Python file: {e}"
    
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Run an inputted python, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
           "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file in the current directory",
            ),
            "args": types.Schema (
                type=types.Type.ARRAY,
                description="List of command line arguments to be passed when the python file is run", 
                items = types.Schema (
                    type=types.Type.STRING,
                    description="List of command line arguments to be passed when the python file is run",
                ),
            ),
           
        },
    ),
)

