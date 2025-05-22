# virustotal_scan.py
import requests
import time
import os
from dotenv import load_dotenv

load_dotenv()  # Charge les variables du fichier .env

API_KEY = os.getenv("VIRUSTOTAL_API_KEY")
VT_URL_UPLOAD = "https://www.virustotal.com/api/v3/files"
HEADERS = {"x-apikey": API_KEY}

def scan_file_virustotal(file_stream, filename):
    if not API_KEY:
        return {"error": "API key not found. Check your .env file."}

    files = {"file": (filename, file_stream)}
    response = requests.post(VT_URL_UPLOAD, headers=HEADERS, files=files)

    if response.status_code != 200:
        return {"error": f"Upload failed with status {response.status_code}"}

    file_id = response.json()["data"]["id"]
    analysis_url = f"https://www.virustotal.com/api/v3/analyses/{file_id}"

    for _ in range(30):
        result = requests.get(analysis_url, headers=HEADERS)
        data = result.json()

        status = data["data"]["attributes"]["status"]
        if status == "completed":
            stats = data["data"]["attributes"]["stats"]
            return {
                 "malveillant": stats.get("malicious", 0),
                 "suspect": stats.get("suspicious", 0),
                 "inoffensif": stats.get("harmless", 0),}

        time.sleep(2)

    return {"error": "Timeout waiting for scan result"}
