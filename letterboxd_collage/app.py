from fastapi import FastAPI
from .letterboxd_scraping import fetch_data
from .webdriver_pool import WebDriverPool


app = FastAPI()

@app.get("/")
def read_root():
    return {"Health": "OK"}


@app.get("/collage/{username}")
def fetch_letterboxd_data(username: str):
    return fetch_data(username)