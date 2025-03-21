import os
import vt

import requests
from greynoise import GreyNoise
from OTXv2 import OTXv2
from dotenv import load_dotenv

load_dotenv()  # Load API keys

# Load API Keys
API_KEYS = {
    "GreyNoise": os.getenv("GREYNOISE_API_KEY"),
    "VirusTotal": os.getenv("VIRUSTOTAL_API_KEY"),
    "OTX AlienVault": os.getenv("OTX_API_KEY"),
    "AbuseIPDB": os.getenv("ABUSEIPDB_API_KEY"),
    "IntelX": os.getenv("INTELX_API_KEY"),
}

# Initialize API Clients
gn_client = GreyNoise(api_key=API_KEYS["GreyNoise"])
vt_client = vt.Client(API_KEYS["VirusTotal"])
otx_client = OTXv2(API_KEYS["OTX AlienVault"])


# Fetch Data Using SDKs & APIs
def fetch_greynoise(ip):
    try:
        return gn_client.ip(ip)
    except Exception as e:
        return {"error": str(e)}


def fetch_virustotal(query, query_type):
    try:
        if query_type == "url":
            query_id = vt.url_id(query)
            return vt_client.get_object(f"/urls/{query_id}")
        elif query_type == "hash":
            return vt_client.get_object(f"/files/{query}")
        return None
    except Exception as e:
        return {"error": str(e)}


def fetch_otx(query, query_type):
    try:
        if query_type in ["ip", "url", "email", "crypto", "phone"]:
            return otx_client.get_indicator_details_by_section(query_type.capitalize(), query, "general")
        elif query_type in ["actor", "adversary", "breach"]:
            return otx_client.search(query)
    except Exception as e:
        return {"error": str(e)}


def fetch_abuseipdb(ip):
    url = f"https://api.abuseipdb.com/api/v2/check?ipAddress={ip}"
    headers = {"Key": API_KEYS["AbuseIPDB"], "Accept": "application/json"}
    response = requests.get(url, headers=headers)
    return response.json() if response.status_code == 200 else None


def fetch_intelx(query, query_type):
    """Fetches data from IntelX (Dark Web & Public Leak Intelligence)"""
    url = f"https://free.intelx.io/intelligent/search"
    headers = {"x-key": API_KEYS["IntelX"]}
    data = {"term": query, "maxresults": 10, "target": query_type}
    response = requests.post(url, json=data, headers=headers)
    return response.json() if response.status_code == 200 else None
