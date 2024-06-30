import os
import json
from dotenv import load_dotenv
import google.generativeai as genai

# Load API key from .env file
load_dotenv()
api_key = os.getenv('gemini_api')

# Ensure API key is loaded
if not api_key:
    raise ValueError("API key not found. Please set 'gemini_api' in your .env file.")

# Configure the generative AI model
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.0-pro-latest')

def generate_structured_json(prompt):
    input_text = f"""
    {prompt}
    """
    
    response = model.generate_content(input_text)
    text = response.text
    
    def parse_json_garbage(s):
        s = s[next(idx for idx, c in enumerate(s) if c in "{["):]
        try:
            return json.loads(s)
        except json.JSONDecodeError as e:
            try:
                return json.loads(s[:e.pos])
            except json.JSONDecodeError:
                return {"error": "Unable to parse JSON response"}
    
    return parse_json_garbage(text)
