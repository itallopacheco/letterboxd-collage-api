import os.path

from fastapi import FastAPI, Request, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .letterboxd_scraping import fetch_data, create_movie_grid

app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/collage")
async def fetch_letterboxd_data(username: str = Form(...)):
    data = await fetch_data(username)
    if data is not None:
        grid = create_movie_grid(data, 4, 3)

        filename = f"{username}_collage.jpg"
        filepath = os.path.join("static", filename)
        grid.save(filepath)

        url = f"/static/{filename}"
    else:
        return HTMLResponse("<h1>Invalid username</h1>")
    return HTMLResponse(f'<img src="{url}" alt="Result">')