from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import osint


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

app.include_router(osint.router, prefix="/api")


@app.get("/")
def read_root():
    return {"message": "CORS is working!"}
