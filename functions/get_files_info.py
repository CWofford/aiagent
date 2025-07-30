import os
def get_files_info(working_directory, directory="."):
    path = os.path.join(working_directory, directory)
    abspath = os.path.abspath(working_directory)
    if path != abspath:
        print(f'Error: Cannot list "{directory}" as it is outside the permitted working directory')
    if not (os.path.isdir(directory)):
        print(f'Error: "{directory}" is not a directory')
    print(os.listdir(directory))
    print(f"{os.listdir(directory)}: file_size={os.path.getsize(directory)}, is_dir={os.path.isdir(directory)}")