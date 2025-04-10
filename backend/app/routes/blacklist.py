from fastapi import APIRouter
from app.utils.formatting import normalize_abuseipdb_blacklist

from app.services.osint import (
    fetch_abuseipdb_blacklist,
)

router = APIRouter()


@router.get("/blacklist")
def get_blacklisted_ips():
    raw_data = fetch_abuseipdb_blacklist()
    normalized = normalize_abuseipdb_blacklist(raw_data)
    return {"results": normalized}
