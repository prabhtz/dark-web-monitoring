from fastapi import APIRouter, Query
from app.services.osint import fetch_greynoise, fetch_virustotal, fetch_otx, fetch_abuseipdb, fetch_intelx
from app.utils.formatting import normalize_osint_data

router = APIRouter()


@router.get("/osint")
def get_osint_data(
    ip: str = Query(None, description="IP address to check"),
    url: str = Query(None, description="URL to scan"),
    actor: str = Query(None, description="Threat actor to search"),
    adversary: str = Query(None, description="Adversary group to search"),
    hash: str = Query(None, description="File hash (MD5, SHA1, SHA256)"),
    email: str = Query(None, description="Email address to check"),
    crypto: str = Query(None, description="Cryptocurrency address to check"),
    phone: str = Query(None, description="Phone number to check"),
    breach: str = Query(None, description="Breach event to check"),
):
    """Fetch threat intelligence from multiple OSINT sources using SDKs where available."""

    queries = {
        "IP": ip,
        "URL": url,
        "Threat Actor": actor,
        "Adversary": adversary,
        "File Hash": hash,
        "Email": email,
        "Crypto Address": crypto,
        "Phone Number": phone,
        "Breach Event": breach,
    }

    results = []

    if ip:
        results.extend(
            [
                normalize_osint_data("GreyNoise", fetch_greynoise(ip), "IP"),
                normalize_osint_data("AbuseIPDB", fetch_abuseipdb(ip), "IP"),
                normalize_osint_data("OTX AlienVault", fetch_otx(ip, "ip"), "IP"),
            ]
        )

    if url:
        results.append(normalize_osint_data("VirusTotal", fetch_virustotal(url, "url"), "URL"))

    if actor:
        results.append(normalize_osint_data("OTX AlienVault", fetch_otx(actor, "actor"), "Threat Actor"))

    if adversary:
        results.append(normalize_osint_data("OTX AlienVault", fetch_otx(adversary, "adversary"), "Adversary"))

    if hash:
        results.append(normalize_osint_data("VirusTotal", fetch_virustotal(hash, "hash"), "File Hash"))

    if email:
        results.extend(
            [
                normalize_osint_data("OTX AlienVault", fetch_otx(email, "email"), "Email"),
                normalize_osint_data("IntelX", fetch_intelx(email, "email"), "Email"),
            ]
        )

    if crypto:
        results.append(normalize_osint_data("OTX AlienVault", fetch_otx(crypto, "crypto"), "Crypto Address"))

    if phone:
        results.append(normalize_osint_data("IntelX", fetch_intelx(phone, "phone"), "Phone Number"))

    if breach:
        results.append(normalize_osint_data("OTX AlienVault", fetch_otx(breach, "breach"), "Breach Event"))

    return {"query": queries, "results": [r for r in results if r]}
