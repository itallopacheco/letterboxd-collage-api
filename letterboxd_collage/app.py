from fastapi import FastAPI
from .letterboxd_scraping import fetch_data
from .webdriver_pool import WebDriverPool


app = FastAPI()
driver_pool = WebDriverPool(1)

@app.get("/")
def read_root():
    return {"Health": "OK"}


@app.get("/collage/{username}")
def fetch_letterboxd_data(username: str):
    driver = driver_pool.get_driver()
    try:
        return fetch_data(username, driver)
    finally:
        driver_pool.return_driver(driver)
