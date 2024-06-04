from fastapi import FastAPI
from .letterboxd_scraping import fetch_data
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"Health": "OK"}


@app.get("/collage/{username}")
def fetch_letterboxd_data(username: str):
    return fetch_data(username)
