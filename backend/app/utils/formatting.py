import re

from datetime import datetime
from app.utils.risk_scoring import (
    calculate_osint_risk_score,
    calculate_darkweb_risk_score,
)


from datetime import datetime


def normalize_osint_data(source, raw_data, query_type):
    """Convert OSINT API response to a structured format with risk scoring."""

    if not raw_data:
        return None

    risk_score, risk_category = calculate_osint_risk_score(source, raw_data)

    normalized_data = {
        "source": source,
        "type": query_type,
        "risk_score": risk_score,
        "risk_category": risk_category,
        "data": {},
    }

    # Handle GreyNoise Response (Community API)
    if source == "GreyNoise":
        normalized_data["data"] = {
            "classification": raw_data.get("classification", "unknown"),
            "ip": raw_data.get("ip"),
            "noise": raw_data.get("noise", False),
            "riot": raw_data.get("riot", False),
            "bot": raw_data.get("bot", False),
            "last_seen": raw_data.get("last_seen"),
            "first_seen": raw_data.get("first_seen"),
        }

    # Handle AbuseIPDB Response
    elif source == "AbuseIPDB":
        normalized_data["data"] = {
            "ip": raw_data.get("ip"),
            "abuse_confidence_score": raw_data.get("abuse_confidence_score"),
            "country": raw_data.get("country"),
            "isp": raw_data.get("isp"),
            "domain": raw_data.get("domain"),
            "is_tor": raw_data.get("is_tor"),
            "total_reports": raw_data.get("total_reports"),
            "num_users_reported": raw_data.get("num_users_reported"),
            "last_reported": raw_data.get("last_reported"),
        }

    # Handle OTX AlienVault Response
    elif source == "OTX AlienVault":
        normalized_data["data"] = {
            "indicator": raw_data.get("indicator"),
            "type": raw_data.get("type"),
            "pulses": raw_data.get("pulses"),
            "related_indicators": raw_data.get("related_indicators"),
            "first_seen": raw_data.get("first_seen"),
            "last_seen": raw_data.get("last_seen"),
            "threat_tags": raw_data.get("threat_tags"),
            "analysis": raw_data.get("analysis"),
        }

    # Handle VirusTotal Response
    elif source == "VirusTotal":
        normalized_data["data"] = {
            "malicious_votes": raw_data.get("malicious_votes", 0),
            "suspicious_votes": raw_data.get("suspicious_votes", 0),
            "undetected": raw_data.get("undetected", 0),
            "harmless": raw_data.get("harmless", 0),
            "total_scans": raw_data.get("total_scans", 0),
            "vendor_detections": raw_data.get("vendor_detections", {}),
            "last_analysis_time": raw_data.get("last_analysis_time"),
        }

    return normalized_data


def normalize_darkweb_data(source, raw_data, query_type):
    """Convert Dark Web API response to a structured format with risk scoring."""
    if not raw_data:
        return None

    risk_score, risk_category = calculate_darkweb_risk_score(source, raw_data)

    formatted_results = []
    for record in raw_data:
        formatted_results.append(
            {
                "title": record.get("title", "Unknown"),
                "date": datetime.utcnow().isoformat(),
                "preview": record.get("preview", "No preview available"),
                "onion_links": record.get("onion_links", []),
                "intelx_link": (
                    record.get("intelx_link") if source == "IntelX" else None
                ),
                "description": record.get("description", "No details available"),
                "tags": record.get("tags", []),
                "first_seen": record.get("first_seen"),
                "last_seen": record.get("last_seen"),
                "leaked_data": record.get("leak_data", []),
                "related_actors": record.get("actors", []),
                "last_analysis_date": (
                    datetime.utcfromtimestamp(record.get("timestamp", 0)).strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )
                    if record.get("timestamp")
                    else None
                ),
            }
        )

    return {
        "source": source,
        "type": query_type,
        "risk_score": risk_score,
        "risk_category": risk_category,
        "data": formatted_results,
    }


def normalize_abuseipdb_blacklist(raw_list):
    """Normalize AbuseIPDB Blacklist response to consistent format with scoring."""
    results = []

    for item in raw_list:
        ip = item.get("ipAddress")
        abuse_score = item.get("abuseConfidenceScore", 0)

        raw_data = {"abuse_confidence_score": abuse_score}
        risk_score, risk_category = calculate_osint_risk_score("AbuseIPDB", raw_data)

        results.append(
            {
                "source": "AbuseIPDB",
                "ip": ip,
                "risk_score": risk_score,
                "risk_category": risk_category,
                "data": {
                    "abuse_confidence_score": abuse_score,
                    "last_reported": item.get("lastReportedAt"),
                },
            }
        )

    return results


def clean_text(text: str) -> str:
    """
    Cleans and normalizes text by removing excess whitespace, control characters,
    and unwanted symbols. Keeps the text ASCII-compatible and printable.
    """
    if not text:
        return ""

    # Remove non-printable characters and excessive whitespace
    cleaned = re.sub(r"[^\x20-\x7E]+", " ", text)  # Keep ASCII printable characters
    cleaned = re.sub(r"\s+", " ", cleaned)  # Collapse all whitespace
    return cleaned.strip()
