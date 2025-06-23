import requests, os
from dotenv import load_dotenv
load_dotenv()

def store_data(data):
    API_KEY = os.getenv("AIRTABLE_API_KEY")
    BASE_ID = os.getenv("AIRTABLE_BASE_ID")
    TABLE = os.getenv("AIRTABLE_TABLE_NAME")
    
    url = f"https://api.airtable.com/v0/{BASE_ID}/{TABLE}"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "fields": {
            "Name": data.get("name", "N/A"),
            "Sector": data.get("sector", "N/A"),
            "Stage": data.get("stage", "N/A"),
            "Pitch Deck": data.get("pitch_deck_url", "N/A")
        }
    }

    return requests.post(url, headers=headers, json=payload)
