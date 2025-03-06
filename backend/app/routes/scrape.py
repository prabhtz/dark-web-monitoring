from fastapi import APIRouter, Query
from typing import List
from app.services.scraper import fetch_page
from app.services.extractor import extract_data
from app.config import SCRAPABLE_SITES

router = APIRouter()


# === 🛠 Scrape and Search for Keywords & Threat Actors ===
def scrape_and_search(name, url, keywords, actors):
    soup = fetch_page(url)
    if soup:
        extracted_data = {
            "site": name,
            "url": url,
            "extracted_data": extract_data(name, soup),
            "threats_detected": [],
            "threat_actors_detected": [],
        }

        # Search for Threat Keywords
        extracted_data["threats_detected"] = [
            item
            for item in extracted_data["extracted_data"]
            if any(keyword.lower() in item["value"].lower() for keyword in keywords)
        ]

        # Search for Threat Actors
        extracted_data["threat_actors_detected"] = [
            item["value"]
            for item in extracted_data["extracted_data"]
            if item["type"] == "threat_actor" and item["value"] in actors
        ]

        return extracted_data
    return {"site": name, "url": url, "error": "Failed to fetch"}


# === 🛠 API Endpoint for Scraping ===
@router.get("/scrape-all/")
def scrape_all_sites(
    keywords: List[str] = Query([], description="Keywords to search for threats"),
    actors: List[str] = Query([], description="Threat actors to monitor"),
):
    results = []
    for name, url in SCRAPABLE_SITES.items():
        results.append(scrape_and_search(name, url, keywords, actors))
    return results
