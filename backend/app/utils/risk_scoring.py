def calculate_osint_risk_score(source: str, raw_data: dict):
    """
    Calculate a normalized risk score (1–10) and category from OSINT data.
    - Applies source weighting and consistent scoring logic.
    """

    print("source", source)
    print("raw_data", raw_data)

    if not raw_data:
        return 1, "Safe"

    # Source reliability weight mapping (0.0–1.0 scale)
    source_weight = {
        "GreyNoise": 0.9,
        "OTX AlienVault": 0.9,
        "VirusTotal": 0.8,
        "AbuseIPDB": 0.8,
        "IntelX": 0.5,
    }

    base_score = 1.0  # Default lowest risk

    # OTX scoring from internal risk_score already normalized
    if source == "OTX AlienVault":
        raw = raw_data.get("risk_score", 1)
        base_score = raw if raw < 10 else raw / 10

    # GreyNoise uses classification
    elif source == "GreyNoise":
        base_score = {"benign": 2, "suspicious": 5, "malicious": 9}.get(
            raw_data.get("classification", "").lower(), 1
        )

    # VirusTotal using malicious votes ratio
    elif source == "VirusTotal":
        malicious = raw_data.get("malicious_votes", 0)
        total = raw_data.get("total_scans", 1)
        ratio = malicious / total if total else 0

        if malicious > 10:
            base_score = 9
        elif ratio > 0.5:
            base_score = 7
        elif ratio > 0.2:
            base_score = 5
        elif ratio > 0.05:
            base_score = 3
        else:
            base_score = 1

    # IntelX based on sensitive data leaks
    elif source == "IntelX":
        base_score = 6 if raw_data.get("sensitive_data_count", 0) > 0 else 1

    # AbuseIPDB based on abuse confidence (0–100)
    elif source == "AbuseIPDB":
        abuse_score = raw_data.get("abuse_confidence_score", 0)
        base_score = round((abuse_score / 100) * 10, 1)

    # Apply credibility-based weight
    weight = source_weight.get(source, 1.0)
    weighted_score = round(min(base_score * weight, 10), 1)

    # Categorize risk levels
    risk_levels = [
        (8, "Critical"),
        (6, "High"),
        (4, "Moderate"),
        (2, "Low"),
    ]
    risk_category = "Safe"
    for threshold, level in risk_levels:
        if weighted_score >= threshold:
            risk_category = level
            break

    return weighted_score, risk_category


def calculate_darkweb_risk_score(source: str, keyword_occurrences: int):
    """
    Calculate risk score (1-10) based on:
    - Frequency of keyword mentions in dark web results.
    - Reputation of dark web sources.
    """

    # Source credibility weight mapping (some onion search engines are more reliable than others)
    source_weight = {
        "Ahmia": 0.8,
        "Tor66": 0.7,
        "OnionSearch": 0.6,
        "IntelX": 0.5,  # IntelX aggregates many sources but includes non-dark-web data
    }

    # Default risk score
    base_score = 1  # Safe if keyword is not found

    # Adjust based on keyword occurrences
    base_score = {
        # base_score: keyword_occurrences
        0: 1,
        1: 4,
        2: 4,
        3: 7,
        4: 7,
        5: 7,
        6: 7,
    }.get(keyword_occurrences, 9)

    # Apply source weight factor
    weighted_score = int(base_score * source_weight.get(source, 1))

    # Assign risk level
    risk_levels = [
        (9, "Critical"),
        (7, "High"),
        (5, "Moderate"),
        (3, "Low"),
    ]

    risk_level = "Safe"
    for threshold, level in risk_levels:
        if weighted_score >= threshold:
            risk_level = level
            break

    return weighted_score, risk_level
