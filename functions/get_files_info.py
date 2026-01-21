import os
from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)

def get_files_info(working_directory, directory="."):

    # Get the absolute path of the working directory /home/username/project/..
    working_dir_abs = os.path.abspath(working_directory)
    #print(f"Working Directory: {working_dir_abs}")

    # Get the absolute path of the target directory
    target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
    #print(f"Target Directory: {target_dir}")

     # Check if the target directory is a directory
    if not os.path.isdir(target_dir):
        return f'Error: {directory} is not a directory'

    # Check if the target directory is within the working directory 
    if not os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    # Iterate over the contents of the directory
    dir_contents = os.listdir(target_dir)
    
    dir_contents_list = []

    for dir_item in dir_contents:
       # print(f"Directory Item: {dir_item}")
    
        try:
            file_size = os.path.getsize(f"{target_dir}/{dir_item}")
            is_dir = os.path.isdir(f"{target_dir}/{dir_item}")
        except FileNotFoundError:
            # print(f"File {dir_item} not found")
            return f"File {dir_item} not found"
        
        dir_contents_list.append(f"- name: {dir_item}, file_size:{file_size}, is_dir:{is_dir}")

    # print("returning results")
    return "\n".join(dir_contents_list)
        
        