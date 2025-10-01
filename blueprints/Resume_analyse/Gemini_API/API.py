import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

def ChatBot(message, budget=200):
    # Load environment variables
    load_dotenv()

    # Fetching the api key from .env file
    api_key = os.getenv("GOOGLE_API_KEY")

    if not api_key:
        return "API key is not found."

    print("API is loaded successfully:**********",api_key[:6])

    client = genai.Client(
        api_key = api_key,
        )

    
    def generate():
        model = "gemini-2.5-flash"
        contents = [
            types.Content(
                role = "user",
                parts = [types.Part(text=message)]
            ),
        ]
        
        generate_content_config = types.GenerateContentConfig(
            thinking_config=types.ThinkingConfig(thinking_budget = budget),
        )

        response_text = ""
        for chunk in client.models.generate_content_stream(
            model = model,
            contents = contents,
            config = generate_content_config,
        ):
            if hasattr(chunk, "text") and chunk.text:
                response_text += chunk.text
        return response_text
    response = generate()
    return response