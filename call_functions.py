from google.genai import types
from functions.get_files_info import schema_get_files_info, get_files_info
from functions.get_file_content import schema_get_file_content, get_file_content
from functions.run_python_file import schema_run_python_file, run_python_file
from functions.write_file_contents import schema_write_file_content, write_file

available_functions = types.Tool(
    function_declarations=[schema_get_files_info, schema_write_file_content, schema_get_file_content, schema_run_python_file],
)

def call_function(function_call, verbose=False):
    
    if verbose:
        print(f"Calling function: {function_call.name}({function_call.args})")
    else:
        print(f" - Calling function: {function_call.name}")
    
    function_map = {
    "get_file_content": get_file_content,
    "get_files_info": get_files_info,
    "run_python_file": run_python_file,
    "write_file_content": write_file
    }

    function_name = function_call.name or ""

    if function_name not in function_map:

        return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"Error": f"Unknown function: {function_name}"},
            )
        ],
        )
    args = dict(function_call.args) if function_call.args else {}
    args["working_directory"] = "./calculator"

    # print(f"Args: {args}")
    function_result = function_map[function_name](**args)
    
    print(f"Function Result: {function_result}")

    return types.Content(
    role="tool",
    parts=[
        types.Part.from_function_response(
            name=function_name,
            response={"result": function_result},
        )
    ],
)
