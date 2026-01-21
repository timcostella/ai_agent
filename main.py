import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from call_functions import available_functions, call_function


def main():
    load_dotenv()

    # get the API key from the environment variable
    api_key = os.environ.get("GEMINI_API_KEY")

    # if no API key, well we can't do much can we   
    if api_key == None:
        raise RuntimeError("Error: No Gemini API Key Found")
    
    # create a genai client object with the key
    client = genai.Client(api_key=api_key)

    # using argparse we will parse input fed into the script in a user_prompt argument that will be sent to the model
    # additionally we will look for a verbose argument to see how much data to 
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")

    args = parser.parse_args()

    # create a system prompt to keep our AI agent on task
    system_prompt = """
    
    You are a helpful AI coding agent. When a user asks a question or makes a request, make a function call plan. You can perform the following operations:
    - List files and directories
    - Read file contents
    - Execute Python files with optional arguments
    - Write or overwrite files

    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.

    """

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    # set the prefered model version
    model_version="gemini-2.5-flash"

    # send the request, with the system prompt and the user prompt, and the available function calls
    response = client.models.generate_content(
    model=model_version,
    contents=messages,
    config=types.GenerateContentConfig(tools=[available_functions],system_instruction=system_prompt),
    )

    # if no response - then something went wrong obviously
    if response.usage_metadata == None:
        raise RuntimeError("Error: No response metadata found")
    
    # if verbose is specified output more information
    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    if response.function_calls != None:
        if(type(response.function_calls) == list):
            for function_call in response.function_calls:
                print(f"Type: {type(function_call)}")
                print(f"Function call: {function_call}")
                print(f"Calling A Function: {function_call.name} {function_call.args}")
                call_function_result = call_function(function_call)
        else:
            print(f"Calling The Function: {response.function_calls.name} {response.function_calls.args}") 
            call_function_result = call_function(response.function_calls)

            if len(call_function_result.parts) == 0:
                raise Exception("Error: parts empty")
            
            if call_function_result.parts[0].function_response == None:
                raise Exception("Error: no function response recieved")
            
            if call_function_result.parts[0].function_response.response == None:
                raise Exception("Error: no function response recieved")
            
            if args.verbose:
                print(f"-> {call_function_result.parts[0].function_response.response}")
            
    else:
         print(response)
         print(response.text)


if __name__ == "__main__":
    main()
