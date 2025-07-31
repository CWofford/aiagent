import os
def get_files_info(working_directory, directory="."):
    try:
        path = os.path.join(working_directory, directory)
        abspath = os.path.abspath(path)
        workdir_abspath = os.path.abspath(working_directory)

        if not abspath.startswith(workdir_abspath):
            return(f'Error: Cannot list "{directory}" as it is outside the permitted working directory')
        if not (os.path.isdir(path)):
            return(f'Error: "{directory}" is not a directory')
        
        result = []

        if directory==".":
            result.append(f"Result for current directory:")
        else:
            result.append(f"Result for {directory}:") 

        for files in os.listdir(path):
            dir_path = os.path.join(path,files)
            result .append(f" - {files}: file_size={os.path.getsize(dir_path)} bytes, is_dir={os.path.isdir(dir_path)}")

        return '\n'.join(result) 
    
    except Exception as e:
        return (f"Error: {e}") 