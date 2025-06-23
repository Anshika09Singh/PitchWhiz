import os
import re
import json
import google.generativeai as genai
from dotenv import load_dotenv


load_dotenv()


genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


model = genai.GenerativeModel("gemini-1.5-flash")

def classify_startup(email_body):
    prompt = f"""
Extract the following details from this startup pitch email and return only a valid JSON object:
- name
- sector
- stage
- pitch_deck_url

Email:
\"\"\"{email_body}\"\"\"

Only return valid JSON. Do NOT include explanations, comments, or markdown formatting like ```json.
"""

    response = model.generate_content(prompt)
    text = response.text.strip()

    
    clean_text = re.sub(r"^```json\s*|\s*```$", "", text, flags=re.MULTILINE).strip()

    # Check it's a valid JSON string
    if clean_text.startswith("{") and clean_text.endswith("}"):
        return clean_text
    else:
        raise ValueError("Gemini response is not valid JSON:\n" + text)
