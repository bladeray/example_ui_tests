from .base_page import BasePage
from .locators import ResultPageLocators


class ResultsPage(BasePage):
    def should_has_result_with_correct_title(self, result_number, result_title):
        assert self.browser.find_elements(*ResultPageLocators.RESULTS)[result_number].text.find(result_title) != -1, f"{result_title} is not presented in result number {result_number}"
