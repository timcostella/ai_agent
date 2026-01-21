import os
from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Read the contents of a file at a specified file_path relative to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File Path to the file to read content from",
            ),
        },
        required=["file_path"],
    ),
)

# define the maximum amount of characters to read from a file
MAX_FILE_CHARS = 10000

def get_file_content(working_directory, file_path):

    try:
        # Get the absolute path of the working directory /home/username/project/..
        working_dir_abs = os.path.abspath(working_directory)

        # Get the absolute path of the target file_path
        target_file_path = os.path.normpath(os.path.join(working_dir_abs, file_path))

        # Check if the file_path is in the working_directory:
        if not os.path.commonpath([working_dir_abs, target_file_path]) == working_dir_abs:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        
        # Check if the file_path is a file:
        if not os.path.isfile(target_file_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        
        # Read the file:
        file_object = open(target_file_path, "r")
        file_contents = file_object.read(MAX_FILE_CHARS)

        # Check if the entire file was read by reading 1 more char and seeing if has content or not
        # If the file is empty this will return an empty string which will evaluate to False
        if file_object.read(1):
            file_contents += f'[...File "{file_path}" truncated at {MAX_FILE_CHARS} characters]'
        
        return file_contents

    except Exception:
        print ("Error: File path or file not found")

