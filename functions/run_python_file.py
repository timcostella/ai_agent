import os, subprocess

from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs the python file specified by file_path with the optional arguments specified by args",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File Path to the python file that you want run ",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                    description="Optional argument to pass to the python file you want to run",
                ),
                description="Optional list of arguments to pass to the python file",
            ),
        },
        required=["file_path"],
    ),
)

def run_python_file(working_directory, file_path, args=None):

    # Get the absolute path of the working directory /home/username/project/..
    working_dir_abs = os.path.abspath(working_directory)

    # Get the absolute path of the target file_path
    target_file_path = os.path.normpath(os.path.join(working_dir_abs, file_path))

    # Check if the file_path is in the working_directory:
    if not os.path.commonpath([working_dir_abs, target_file_path]) == working_dir_abs:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        
    if not os.path.isfile(target_file_path):
        return f'Error: "{file_path}" does not exist or is not a regular file'
        
    if not target_file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file'
    
    command = ["python", target_file_path]

    if args:
        command.extend(args)

    try:
    
        completed_process_obj = subprocess.run(command, capture_output=True, text=True, timeout=30)

        if completed_process_obj.returncode != 0:
            return f'Process exited with code {completed_process_obj.returncode}'
        
        if not completed_process_obj.stderr and not completed_process_obj.stdout:
            return f'No output produced'
        else:
            output = f"STDOUT: {completed_process_obj.stdout} STDERR: {completed_process_obj.stderr}"
            return output
    
    except Exception as e:
        return (f"Error: executing Python file: {e}")