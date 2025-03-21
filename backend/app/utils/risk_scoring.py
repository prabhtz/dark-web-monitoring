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
