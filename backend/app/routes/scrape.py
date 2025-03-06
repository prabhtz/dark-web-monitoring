from fastapi import APIRouter, Query
from typing import List, Optional
from app.services.scraper import scrape_sites

router = APIRouter()


@router.get("/scrape")
def scrape(keywords: Optional[List[str]] = Query(None)):
    """
    Scrape both main pages and search results from the best threat intelligence sources.
    If no keywords are provided, default ones are used.
    """
    scraped_results = scrape_sites(keywords)
    return {
        "keywords_used": keywords or "Default threat keywords",
        "scraped_data": scraped_results,
        "total_links_found": len(scraped_results),
    }
