def calculate_osint_risk_score(source: str, raw_data: dict):
    """
    Calculate a risk score (1-100) based on OSINT data.
    - Uses risk levels from OTX, VirusTotal, IntelX, and other sources.
    """

    print("source", source)
    print("raw_data", raw_data)

    if not raw_data:
        return 1, "Safe"

    # Source reliability weight mapping
    source_weight = {
        "GreyNoise": 0.9,
        "OTX AlienVault": 0.9,  # More weight since OTX has a stronger scoring model
        "VirusTotal": 0.8,
        "AbuseIPDB": 0.8,
        "IntelX": 0.5,  # Lower weight due to large aggregated data
    }

    # Risk mapping by classification type
    score_mapping = {
        "GreyNoise": {"benign": 2, "suspicious": 5, "malicious": 9},
        "OTX AlienVault": lambda data: data.get("risk_score", 1),  # Uses OTX's calculated risk
        "VirusTotal": lambda votes: 90 if votes > 10 else 75 if votes > 5 else 50 if votes > 1 else 10,
    }

    base_score = 1  # Default safe score

    # OTX AlienVault Scoring
    if source == "OTX AlienVault":
        base_score = score_mapping[source](raw_data)  # Uses new OTX scoring

    # GreyNoise Risk Classification
    elif source == "GreyNoise":
        base_score = score_mapping[source].get(raw_data.get("classification"), 1)

    # VirusTotal Reputation Score
    elif source == "VirusTotal":
        base_score = score_mapping[source](raw_data.get("malicious_votes", 0))

    # IntelX Risk Factor
    elif source == "IntelX":
        sensitive_data_found = raw_data.get("sensitive_data_count", 0) > 0
        base_score = 60 if sensitive_data_found else 10

    # AbuseIPDB Confidence Score
    elif source == "AbuseIPDB":
        abuse_score = raw_data.get("abuse_confidence_score", 0)
        normalized_score = (abuse_score / 100) * 10  # Normalize to range 1-10
        base_score = min(10, max(1, normalized_score))  # Ensure score is within 1-10

    # Apply weighting factor based on source credibility
    weighted_score = int(base_score * source_weight.get(source, 1))

    # Risk Categorization
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

    return min(weighted_score, 100), risk_category


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
