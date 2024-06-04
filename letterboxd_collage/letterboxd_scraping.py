from time import sleep

from bs4 import BeautifulSoup
from selenium.webdriver import ChromeOptions
from seleniumrequests import Remote




def fetch_data(username: str, driver: Remote):
    options = ChromeOptions()
    driver.get(f'https://letterboxd.com/{username}/films/diary/')

    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    diary_table = soup.find('table', {'id': 'diary-table'})
    tbody = diary_table.find('tbody')
    rows = tbody.find_all('tr')
    movies = []
    for row in rows:
        film_details_element = row.find(class_='td-film-details')
        rating_element = row.find(class_='td-rating rating-green')
        film_elements = film_details_element.find(
            attrs={'data-film-id': True})
        film_data = {
            'id': film_elements.get('data-film-id'),
            'slug': film_elements.get('data-film-slug'),
            'name': film_details_element.find('a').get_text(strip=True),
            'rating': rating_element.get_text(strip=True) if rating_element is not None else '',
            'link-poster': f'https://letterboxd.com/ajax/poster/film/{film_elements.get("data-film-slug")}/hero/150x225/',
        }
        movies.append(film_data)

    return movies
