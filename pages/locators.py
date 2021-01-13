from selenium.webdriver.common.by import By


class MainPageLocators:
    SEARCH_FIELD = (By.NAME, 'q')
    SEARCH_BUTTON = (By.NAME, 'btnK')


class ResultPageLocators:
    RESULTS = (By.CSS_SELECTOR, '#res .g')
