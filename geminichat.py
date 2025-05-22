import google.generativeai as genai
from dotenv import load_dotenv
import os
import time

# Load the .env file to access the environment variables
load_dotenv()

# Access the Gemini API key securely from the .env file
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# Configure the Gemini API with the loaded API key
genai.configure(api_key=GEMINI_API_KEY)

# Function to interact with the Gemini model
def ask_gemini(message):
    try:
        # Use the Gemini 1.5 Flash model for generating chat responses
        model = genai.GenerativeModel(model_name="gemini-1.5-flash")
        chat = model.start_chat(history=[])
        response = chat.send_message(message)

        return response.text.strip()
    
    except Exception as e:
        # If there's a quota error, wait and retry
        if "quota" in str(e).lower():
            print("Quota exceeded. Retrying after waiting...")
            time.sleep(10)  # Reduce wait time to 10 seconds
            return ask_gemini(message)  # Retry the request recursively
        else:
            print(f"Error communicating with Gemini: {str(e)}")
            return f"Error communicating with Gemini: {str(e)}"
