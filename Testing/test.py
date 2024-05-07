import os

# Get the path of the current file
current_file_path = __file__

# Get the directory of the current file
current_directory = os.path.dirname(current_file_path)
upper_directory = os.path.dirname(current_directory)
print("Current file path:", current_file_path)
print("Directory of the current file:", current_directory)
print("Directory of the current file:", upper_directory)
current_directory_escaped = current_directory.replace('\\', '\\\\')
print(current_directory_escaped)