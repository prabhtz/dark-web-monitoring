from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import osint, darkweb, blacklist

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(osint.router, prefix="/api")
app.include_router(darkweb.router, prefix="/api")
app.include_router(blacklist.router, prefix="/api")


@app.get("/")
def root():
    return {"message": "Threat Intelligence API is running!"}
