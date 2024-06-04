import os

from bs4 import BeautifulSoup
from selenium.webdriver import ChromeOptions
from seleniumrequests import Remote


SELENIUM_OPTIONS = {
    'REMOTE_SELENIUM_ADDRESS': os.getenv('REMOTE_SELENIUM_ADDRESS', 'http://34.232.72.59:4444/wd/hub'),
    'SELENIUM_REQUESTS_PROXY_HOST': os.getenv('SELENIUM_REQUESTS_PROXY_HOST', '192.168.101.2')
}


def fetch_data(username: str):
    options = ChromeOptions()
    driver = Remote(
        command_executor=SELENIUM_OPTIONS['REMOTE_SELENIUM_ADDRESS'],
        options=options,
        proxy_host=SELENIUM_OPTIONS['SELENIUM_REQUESTS_PROXY_HOST']
    )

    #url para enviar um request get para receber uma pagina html com o src da img https://letterboxd.com/ajax/poster/film/waves-2019/std/35x52/?k=09602ad1

    try:
        driver.get(f'https://letterboxd.com/{username}/films/diary/')

        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        diary_table = soup.find('table', {'id': 'diary-table'})
        tbody = diary_table.find('tbody')
        rows = tbody.find_all('tr')
        movies = []
        for row in rows[1:10]:
            film_details_element = row.find(class_='td-film-details')
            rating_element = row.find(class_='td-rating rating-green')
            film_elements = film_details_element.find(
                attrs={'data-film-id': True})
            film_id = film_elements.get('data-film-id')
            film_slug = film_elements.get('data-film-slug')
            film_name = film_details_element.find('a').get_text(strip=True)
            film_rating = rating_element.get_text(strip=True) if rating_element is not None else ''
            film_poster_request_url = f'https://letterboxd.com/ajax/poster/film/{film_slug}/std/1000x1500/'

            driver.get(film_poster_request_url)
            film_poster_html = driver.page_source

            film_poster_soup = BeautifulSoup(film_poster_html, 'html.parser')
            film_poster_img = film_poster_soup.find(class_='image')
            film_poster_img_link = film_poster_img.get('src')
            film_data = {
                'id': film_id,
                'slug': film_slug,
                'name': film_name,
                'rating': film_rating,
                'link-poster': film_poster_img_link,
            }
            movies.append(film_data)
    finally:
        driver.quit()

    return movies
