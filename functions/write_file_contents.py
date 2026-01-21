import os

from google.genai import types

schema_write_file_content = types.FunctionDeclaration(
    name="write_file_content",
    description="Opens or creates the file at a specified file_path relative to the working directory and writes content to it",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File Path to the file that you want to retrieve content from",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content (text) that you want to write to the file located at file_path",
            )
        },
        required=["file_path", "content"],
    ),
)

def write_file(working_directory, file_path, content):

    print("Running write_file")
    try:
        current_step = "starting"

        # Get the absolute path of the working directory /home/username/project/..
        working_dir_abs = os.path.abspath(working_directory)

        # Get the absolute path of the target file_path
        target_file_path = os.path.normpath(os.path.join(working_dir_abs, file_path))

        # Check if the file_path is in the working_directory:
        if not os.path.commonpath([working_dir_abs, target_file_path]) == working_dir_abs:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        
        # Check if the file_path is a directory, we can't write to a directory:
        if os.path.isdir(target_file_path):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        
        current_step = "make directory"
        
        #Create any necessary subdirectories in the working directory needed
        os.makedirs(os.path.dirname(target_file_path), mode=0o777, exist_ok=True)

        current_step = "open file for writing"

        # Open the file for writing
        file_object = open(target_file_path, 'w')

        current_step = "write file"

        # Write the contents to the file
        file_object.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    
    except FileNotFoundError as e:
        return f'Error: Cannot write to "{file_path}", not found.  Current step: {current_step}. Exception: {e}'
    
    except FileExistsError as e:
        return f'Error: Cannot write to "{file_path}", it already exists. Current step: {current_step}. Exception: {e}'
    
    except Exception as e:
        return f'Error: Cannot write to "{file_path}", Current step: {current_step}. Exception: {e}'