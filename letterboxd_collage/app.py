from io import BytesIO

import httpx
from fastapi.responses import StreamingResponse
from fastapi import FastAPI, Response
from .letterboxd_scraping import fetch_data, create_movie_grid
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
async def fetch_letterboxd_data(username: str):
    data = await fetch_data(username)
    grid = create_movie_grid(data, 4, 3)

    img_io = BytesIO()
    grid.save(img_io, 'JPEG')
    img_io.seek(0)

    return StreamingResponse(img_io, media_type="image/jpeg")


@app.get("/proxy-image/{url:path}")
async def proxy_image(url: str):
    if not url.startswith('https://'):
        url = f"https://{url}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return Response(response.content, media_type=response.headers["Content-Type"])