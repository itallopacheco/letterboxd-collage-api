from io import BytesIO

import time
from concurrent.futures import ThreadPoolExecutor

import httpx
import requests
from PIL import Image, ImageDraw, ImageFont
from bs4 import BeautifulSoup


def format_rating(rating: str):
    scoreToTextMap = {
        "0.5": "½",
        "1.0": "★",
        "1.5": "★½",
        "2.0": "★★",
        "2.5": "★★½",
        "3.0": "★★★",
        "3.5": "★★★½",
        "4.0": "★★★★",
        "4.5": "★★★★½",
        "5.0": "★★★★★",
    }
    return scoreToTextMap.get(rating, rating)


async def fetch_data(username: str):
    url = f"https://letterboxd.com/{username}/rss/"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "xml")
        items = soup.find_all("item")
        movies = []
        for item in items:
            if item.find("tmdb:movieId") is not None:
                movie = {
                    "title": item.find("letterboxd:filmTitle").text,
                    "rating": format_rating(item.find("letterboxd:memberRating").text),
                    "rewatch": item.find("letterboxd:rewatch").text,
                    "poster_medium": BeautifulSoup(item.find("description").text).find("img")["src"].replace(
                        '-0-600-0-900-crop', '-0-230-0-345-crop'),
                    "poster_large": BeautifulSoup(item.find("description").text).find("img")["src"].replace(
                        '-0-600-0-900-crop', '-0-1000-0-1500-crop'),
                }
                movies.append(movie)
        return movies
    else:
        return None


def create_movie_image(movie_data):
    response = requests.get(movie_data["poster_large"])
    img = Image.open(BytesIO(response.content))

    img = img.resize((230, 345))

    draw = ImageDraw.Draw(img)

    font = ImageFont.truetype("fonts/NotoSans-Bold.ttf", 15)
    font_star = ImageFont.truetype("fonts/NotoSans-Symble.ttf", 20)

    y_text = img.height - 60
    y_stars = img.height - 40

    draw.text((10, y_text), f"{movie_data['title']}", font=font, fill="white")
    draw.text((10, y_stars), f"{movie_data['rating']}", font=font_star, fill="green")

    return img


def create_movie_grid(fetch_data, n, m):
    poster_width = 230
    poster_height = 345

    grid = Image.new('RGB', (n * poster_width, m * poster_height))

    with ThreadPoolExecutor() as executor:
        posters = list(executor.map(create_movie_image, fetch_data))

    for i, poster in enumerate(posters):
        x = (i % n) * poster_width
        y = (i // n) * poster_height

        grid.paste(poster, (x, y))

        if i >= n * m - 1:
            break
    return grid
