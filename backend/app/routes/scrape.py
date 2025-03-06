from fastapi import APIRouter
from app.services.scraper import scrape_sites

router = APIRouter()


@router.get("/scrape-all")
def scrape_all():
    """
    Scrape top threat intelligence sources from Surface & Dark Web.
    Returns a list of valid threat-related URLs.
    """
    scraped_results = scrape_sites()
    return {"scraped_data": scraped_results, "total_links_found": len(scraped_results)}
