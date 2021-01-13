from .base_page import BasePage
from .locators import MainPageLocators


class MainPage(BasePage):
    def is_main_page(self):
        current_url = self.browser.current_url
        return current_url == 'https://www.google.com/'

    def enter_search_query(self, query):
        self.browser.find_element(*MainPageLocators.SEARCH_FIELD).send_keys(query)

    def click_search_button(self):
        self.browser.find_element(*MainPageLocators.SEARCH_BUTTON).click()
