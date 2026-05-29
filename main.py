import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys,argparse

def main():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose",action="store_true",help="Enable verbose output")
    args = parser.parse_args()
    prompt = args.user_prompt
    print(prompt)

    load_dotenv()
    api_key= os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY environment variable not set")

    client = genai.Client(api_key=api_key)
    
    #if len(sys.argv)<2:
    #    print("I need a prompt!")
    #    sys.exit(1)
    #prompt = sys.argv[1]

    try:
        #prompt = """Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."""
        #print(prompt)

        messages: list[types.Content] = [
            types.Content(role="user", parts=[types.Part(text=args.user_prompt)])
            ]



        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=messages,
        )

        print("Response:")
        print(response.text)
        
        if response is None or response.usage_metadata is None:
            print("response is malformed")
            return
        if args.verbose:
            print(f"User prompt:{prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    except Exception as e:
        print("Prompt tokens: 0")
        print("Response tokens: 0")
        print(f"Error: {e}")

if __name__=="__main__":
    main()
