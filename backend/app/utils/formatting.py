from datetime import datetime
from app.utils.risk_scoring import calculate_risk_score


def normalize_osint_data(source, raw_data, query_type):
    """Convert OSINT API response to a standard format with risk scoring."""

    if not raw_data:
        return None

    risk_score, risk_category = calculate_risk_score(source, raw_data)

    return {
        "source": source,
        "type": query_type,
        "risk_score": risk_score,
        "risk_category": risk_category,
        "data": {
            "classification": raw_data.get("classification"),
            "first_seen": raw_data.get("first_seen"),
            "last_seen": raw_data.get("last_seen"),
            "tags": raw_data.get("tags", []),
            "malicious_votes": raw_data.get("data", {}).get("malicious_votes", 0),
            "total_reports": raw_data.get("data", {}).get("totalReports"),
            "country": raw_data.get("data", {}).get("countryName"),
            "threat_type": raw_data.get("type"),
            "last_analysis_date": (
                datetime.utcfromtimestamp(
                    raw_data.get("data", {}).get("attributes", {}).get("last_analysis_date", 0)
                ).strftime("%Y-%m-%d %H:%M:%S")
                if raw_data.get("data", {}).get("attributes", {}).get("last_analysis_date")
                else None
            ),
            "additional_info": raw_data.get("description", "No details available."),
        },
    }
