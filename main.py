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
    parser.add_argument("user_prompt", type=str, help="User prompt to send to Gemini")
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

    You can use the funtions to retrieve/review the code in question, and make any necessary changes to fix issues with code.

    """

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    # set the prefered model version
    model_version="gemini-2.5-flash"

    function_call_responses = []

    for i in range(0, 20):
        # call the model, handle responses, etc.

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

        # Response candidates are previous responses, add to the message so the ai engine has context on next iteration, or so I think
        if response.candidates:
            for candidate in response.candidates:
                messages.append(candidate.content)

        # If the ai engine calls another function then run it, recieve its results send back to AI agent.  
        # If the ai agent doesn't call another function consider it the final response and exit
        if response.function_calls != None:
            if(type(response.function_calls) == list):

                for function_call in response.function_calls:
                    print(f"Type: {type(function_call)}")
                    print(f"Function call: {function_call}")
                    print(f"Calling A Function: {function_call.name} {function_call.args}")
                    call_function_result = call_function(function_call, args.verbose)
            else:
                print(f"Calling The Function: {response.function_calls.name} {response.function_calls.args}") 
                call_function_result = call_function(response.function_calls)

            if len(call_function_result.parts) == 0:
                raise Exception("Error: parts empty")
            
            if call_function_result.parts[0].function_response == None:
                raise Exception("Error: no function response recieved")
            
            if call_function_result.parts[0].function_response.response == None:
                raise Exception("Error: no function response recieved")
            
            function_call_responses.append(call_function_result.parts[0])

            if args.verbose:
                print(f"-> {call_function_result.parts[0].function_response.response}")
                
        else:
            print(response)
            print(response.text)
            return
        
        # iterate i so we don't loop forever, limits total calls to ai engine
        i += 1

        # append the results of the function call to the messsage for the ai engine to review
        messages.append(types.Content(role="user", parts=function_call_responses))



if __name__ == "__main__":
    main()
