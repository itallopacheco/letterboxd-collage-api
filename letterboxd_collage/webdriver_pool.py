from selenium.webdriver import ChromeOptions
from seleniumrequests import Remote
from queue import Queue

SELENIUM_OPTIONS = {
    'REMOTE_SELENIUM_ADDRESS': 'http://localhost:4444/wd/hub',
    'SELENIUM_REQUESTS_PROXY_HOST': '192.168.101.2'
}


class WebDriverPool:
    def __init__(self, size: int):
        self._avaliable = Queue(maxsize=size)
        self._in_use = Queue(maxsize=size)
        for _ in range(size):
            driver = self._create_new_driver()
            self._avaliable.put(driver)

    def _create_new_driver(self):
        options = ChromeOptions()
        driver = Remote(
            command_executor=SELENIUM_OPTIONS['REMOTE_SELENIUM_ADDRESS'],
            options=options,
            proxy_host=SELENIUM_OPTIONS['SELENIUM_REQUESTS_PROXY_HOST']
        )
        return driver

    def get_driver(self):
        driver = self._avaliable.get()
        self._in_use.put(driver)
        return driver

    def return_driver(self, driver):
        self._in_use.get(driver)
        self._avaliable.put(driver)