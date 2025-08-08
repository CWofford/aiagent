from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python import schema_run_python_file
from functions.write_file import schema_write_file


print(schema_get_file_content({'file_path': 'main.py'}))
print(schema_write_file({'file_path': 'main.txt', 'content': 'hello'}))
print(schema_run_python_file({'file_path': 'main.py'}))
print(schema_get_files_info({'directory': 'pkg'}))