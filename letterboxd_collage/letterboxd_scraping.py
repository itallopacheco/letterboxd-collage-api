import os

from bs4 import BeautifulSoup
from selenium.webdriver import ChromeOptions
from seleniumrequests import Remote


SELENIUM_OPTIONS = {
    'REMOTE_SELENIUM_ADDRESS': os.getenv('REMOTE_SELENIUM_ADDRESS', 'http://localhost:4444/wd/hub'),
    'SELENIUM_REQUESTS_PROXY_HOST': os.getenv('SELENIUM_REQUESTS_PROXY_HOST', '192.168.101.2')
}


def fetch_data(username: str):
    options = ChromeOptions()
    driver = Remote(
        command_executor=SELENIUM_OPTIONS['REMOTE_SELENIUM_ADDRESS'],
        options=options,
        proxy_host=SELENIUM_OPTIONS['SELENIUM_REQUESTS_PROXY_HOST']
    )

    try:
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
    finally:
        driver.quit()

    return movies
