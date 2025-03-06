from fastapi import FastAPI
from app.routes import scrape
from app.config import setup_tor_proxy

# Initialize FastAPI app
app = FastAPI()

# Setup Tor Proxy
# setup_tor_proxy()

# Include routes
app.include_router(scrape.router)


@app.get("/")
def root():
    return {"message": "Dark Web Monitoring API Running"}
