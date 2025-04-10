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
    import vt


from datetime import datetime


def fetch_virustotal(query, query_type):
    try:
        with vt.Client(API_KEYS["VirusTotal"]) as client:
            if query_type == "url":
                query_id = vt.url_id(query)
                obj = client.get_object(f"/urls/{query_id}")
            elif query_type == "hash":
                obj = client.get_object(f"/files/{query}")
            else:
                return None

            # Extract scan results
            response = obj
            stats = response.get("last_analysis_stats", {})
            scans = response.get("last_analysis_results", {})

            print(f"VirusTotal response: {response}")  # DEBUG LOG

            # Basic detection counts
            malicious = stats.get("malicious", 0)
            suspicious = stats.get("suspicious", 0)
            undetected = stats.get("undetected", 0)
            harmless = stats.get("harmless", 0)

            # Pull out key vendors for insights
            vendor_detections = {}
            key_vendors = [
                "Microsoft",
                "Kaspersky",
                "Symantec",
                "ClamAV",
                "BitDefender",
            ]
            for vendor in key_vendors:
                result = scans.get(vendor, {}).get("result")
                if result:
                    vendor_detections[vendor] = result

            # Get last analysis time
            last_analysis_time = response.get("last_analysis_date")
            last_analysis_time = (
                datetime.utcfromtimestamp(last_analysis_time).strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
                if last_analysis_time
                else None
            )

            return {
                "malicious_votes": malicious,
                "suspicious_votes": suspicious,
                "undetected": undetected,
                "harmless": harmless,
                "vendor_detections": vendor_detections,
                "last_analysis_time": last_analysis_time,
                "total_scans": sum(stats.values()),
            }

    except Exception as e:
        return {"error": str(e)}


def calculate_otx_risk_score(pulses, malware_families, analysis):
    """
    Improved Risk Scoring for OTX Data (Normalized to 1–10)
    - Now better supports IP indicators (no 'analysis')
    - Incorporates threat tags within pulses
    """
    score = 0

    # Count pulses and unique threat tags
    pulse_count = len(pulses)
    threat_tags = set()
    pulse_sources = set()

    for pulse in pulses:
        pulse_tags = pulse.get("tags", [])
        author = pulse.get("author", {}).get("username", "")
        pulse_sources.add(author)

        # Collect threat-relevant tags
        for tag in pulse_tags:
            if tag and tag.lower() in {
                "malicious",
                "botnet",
                "portscan",
                "ssh",
                "telnet",
                "honeypot",
                "bruteforce",
            }:
                threat_tags.add(tag.lower())

    # Pulses
    if pulse_count >= 10:
        score += 30
    elif pulse_count >= 5:
        score += 20
    elif pulse_count > 0:
        score += 10

    # Threat tags from pulses
    if len(threat_tags) >= 3:
        score += 30
    elif len(threat_tags) > 0:
        score += 20

    # Unique pulse authors (diverse sources)
    if len(pulse_sources) >= 3:
        score += 10

    # Malware families
    if malware_families:
        score += 20

    # Analysis info for URL/File only
    if "malware" in analysis:
        score += 20
    elif "suspicious" in analysis:
        score += 10

    # Normalize to 1–10 range
    raw_score = min(score, 100)
    normalized_score = max(1, int((raw_score / 100) * 10))

    # Risk Category Mapping
    risk_category = "Safe"
    if normalized_score >= 9:
        risk_category = "Critical"
    elif normalized_score >= 7:
        risk_category = "High"
    elif normalized_score >= 5:
        risk_category = "Moderate"
    elif normalized_score >= 3:
        risk_category = "Low"

    print(f"OTX Risk: {normalized_score} ({risk_category}) from raw {score}")
    return normalized_score, risk_category


def fetch_otx(query, query_type):
    """Fetch OSINT threat intelligence from OTX AlienVault"""
    print(f"Fetching OTX AlienVault data for {query} ({query_type})...")

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

        response = otx_client.get_indicator_details_by_section(
            indicator_type, query, "general"
        )

        if not response:
            return None

        # Extract details
        pulses = response.get("pulse_info", {}).get("pulses", [])
        malware_families = response.get("malware_families", [])
        related_indicators = response.get("related", {}).get("indicators", [])
        first_seen = response.get("first_seen")
        last_seen = response.get("last_seen")
        threat_tags = response.get("tags", [])

        parsed_data = {
            "indicator": query,
            "type": query_type,
            "pulses": pulses,
            "malware_families": malware_families,
            "related_indicators": related_indicators,
            "first_seen": first_seen,
            "last_seen": last_seen,
            "threat_tags": threat_tags,
        }

        analysis = otx_client.get_indicator_details_full(indicator_type, query)
        parsed_data["analysis"] = analysis.get("analysis", {})

        # Calculate Risk Score
        risk_score, risk_category = calculate_otx_risk_score(
            pulses, malware_families, parsed_data.get("analysis", {})
        )

        parsed_data["risk_score"] = risk_score
        parsed_data["risk_category"] = risk_category

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


def fetch_abuseipdb_blacklist(confidence_minimum: int = 90, limit: int = 100):
    """Fetch top blacklisted IPs from AbuseIPDB based on confidence score."""
    url = "https://api.abuseipdb.com/api/v2/blacklist"
    headers = {"Key": API_KEYS["AbuseIPDB"], "Accept": "application/json"}

    params = {"confidenceMinimum": str(confidence_minimum), "limit": str(limit)}

    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        data = response.json().get("data", [])
        return data[:limit]  # restrict list for performance
    except Exception as e:
        print(f"Error fetching blacklist from AbuseIPDB: {e}")
        return []
