import os
import vt

import requests
from greynoise import GreyNoise
from OTXv2 import OTXv2, IndicatorTypes

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

OTX_API_KEY = os.getenv("OTX_API_KEY")
otx_client = OTXv2(OTX_API_KEY)


# Fetch Data Using SDKs & APIs
def fetch_greynoise(ip):
    """Fetch OSINT threat intelligence from GreyNoise Community API (Free version)."""
    print(f"Fetching GreyNoise Community data for {ip}...")
    try:
        url = f"https://api.greynoise.io/v3/community/{ip}"
        headers = {"Accept": "application/json"}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            print(f"GreyNoise response: {response.json()}")  # DEBUG LOG
            return response.json()
        print(f"GreyNoise Error: {response.status_code} - {response.text}")
        return None
    except Exception as e:
        print(f"GreyNoise Error: {e}")
        return None


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
    """Fetch OSINT threat intelligence from OTX AlienVault"""
    print(f"🔍 Fetching OTX AlienVault data for {query} ({query_type})...")

    try:
        indicator_type = {
            "ip": IndicatorTypes.IPv4,
            "domain": IndicatorTypes.DOMAIN,
            "url": IndicatorTypes.URL,
            "hash": IndicatorTypes.FILE_HASH_MD5,  # Default to MD5, adjust below
        }.get(query_type.lower(), IndicatorTypes.HOSTNAME)

        if query_type == "hash":
            if len(query) == 64:
                indicator_type = IndicatorTypes.FILE_HASH_SHA256
            elif len(query) == 40:
                indicator_type = IndicatorTypes.FILE_HASH_SHA1

        response = otx_client.get_indicator_details_by_section(indicator_type, query, "general")

        if not response:
            return None

        parsed_data = {
            "indicator": query,
            "type": query_type,
            "pulses": response.get("pulse_info", {}).get("pulses", []),
            "related_indicators": response.get("related", {}).get("indicators", []),
            "first_seen": response.get("first_seen"),
            "last_seen": response.get("last_seen"),
            "threat_tags": response.get("tags", []),
        }

        if query_type == "url" or query_type == "hash":
            analysis = otx_client.get_indicator_details_full(indicator_type, query)
            parsed_data["analysis"] = analysis.get("analysis", {})

        print(f"OTX AlienVault response: {parsed_data}")  # DEBUG LOG
        return parsed_data

    except Exception as e:
        print(f"OTX AlienVault Error: {e}")
        return None


def fetch_abuseipdb(ip):
    """Fetch OSINT threat intelligence from AbuseIPDB."""
    print(f"Fetching AbuseIPDB data for {ip}...")
    url = f"https://api.abuseipdb.com/api/v2/check?ipAddress={ip}"
    headers = {"Key": API_KEYS["AbuseIPDB"], "Accept": "application/json"}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json().get("data", {})
        parsed_data = {
            "ip": data.get("ipAddress"),
            "abuse_confidence_score": data.get("abuseConfidenceScore"),
            "country": data.get("countryCode"),
            "isp": data.get("isp"),
            "domain": data.get("domain"),
            "is_tor": data.get("isTor"),
            "total_reports": data.get("totalReports"),
            "num_users_reported": data.get("numDistinctUsers"),
            "last_reported": data.get("lastReportedAt"),
        }
        print(f"AbuseIPDB response: {parsed_data}")  # DEBUG LOG
        return parsed_data
    print(f"AbuseIPDB Error: {response.status_code} - {response.text}")
    return None


def fetch_intelx(query, query_type):
    """Fetches data from IntelX (Dark Web & Public Leak Intelligence)"""
    url = f"https://free.intelx.io/intelligent/search"
    headers = {"x-key": API_KEYS["IntelX"]}
    data = {"term": query, "maxresults": 10, "target": query_type}
    response = requests.post(url, json=data, headers=headers)
    return response.json() if response.status_code == 200 else None
