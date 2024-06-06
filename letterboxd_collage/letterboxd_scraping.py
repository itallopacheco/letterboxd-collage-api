import requests
from bs4 import BeautifulSoup


def fetch_data(username: str):
    url = f"https://letterboxd.com/{username}/rss/"
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "xml")
        items = soup.find_all("item")
        for item in items:
            if item.find("tmdb:movieId") is not None:
                yield {
                    "title": item.find("letterboxd:filmTitle").text,
                    "rating": item.find("letterboxd:memberRating").text,
                    "rewatch": item.find("letterboxd:rewatch").text,
                    "poster": BeautifulSoup(item.find("description").text).find("img")["src"],
                }

        return response.text
    else:
        return None
