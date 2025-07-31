import os
from config import MAX_CHARS

def get_files_content(working_directory, file_path):
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