def calculate_risk_score(source, raw_data):
    """Standardize risk scores (1-10) from different OSINT APIs."""

    if not raw_data:
        return 1, "Safe"

    score_mapping = {
        "GreyNoise": {"benign": 2, "suspicious": 5, "malicious": 8},
        "OTX AlienVault": {"APT": 7, "botnet": 8, "adversary": 6},
        "VirusTotal": lambda votes: 9 if votes > 5 else 6 if votes > 1 else 3,
    }

    if source in score_mapping:
        if isinstance(score_mapping[source], dict):
            return score_mapping[source].get(raw_data.get("classification"), 1), "Medium"
        return score_mapping[source](raw_data.get("malicious_votes", 0)), "Critical"

    if source == "AbuseIPDB":
        abuse_score = raw_data.get("data", {}).get("abuseConfidenceScore", 0) // 10
        return abuse_score, "High" if abuse_score > 5 else "Medium"

    return 1, "Safe"


def calculate_darkweb_risk_score(source, raw_data):
    """Standardize risk scores (1-10) from Dark Web APIs."""

    if not raw_data:
        return 1, "Safe"

    darkweb_score_mapping = {
        "IntelX": lambda data: (
            9 if len(data.get("leaked_data", [])) > 5 else 6 if len(data.get("leaked_data", [])) > 1 else 3
        ),
        "DarkSearch": lambda data: (
            8 if "ransomware" in data.get("tags", []) else 6 if "malware" in data.get("tags", []) else 4
        ),
        "OnionSearch": lambda data: (
            7 if len(data.get("onion_urls", [])) > 3 else 5 if len(data.get("onion_urls", [])) > 1 else 2
        ),
        "Ahmia": lambda data: 6 if "hacking" in data.get("tags", []) else 3,
        "OnionLand": lambda data: 8 if "stolen credentials" in data.get("description", "").lower() else 4,
        "Phobos": lambda data: 9 if "cybercrime" in data.get("tags", []) else 5,
    }

    if source in darkweb_score_mapping:
        score = darkweb_score_mapping[source](raw_data)
        return score, "Critical" if score >= 8 else "Medium" if score >= 5 else "Low"

    return 1, "Safe"
