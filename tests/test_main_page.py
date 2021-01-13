import allure
import pytest

from pages.main_page import MainPage
from pages import links
from pages.results_page import ResultsPage


@pytest.fixture()
def page(browser):
    page = MainPage(browser, links.MAIN_PAGE)
    with allure.step(f'Открываем {links.MAIN_PAGE}'):
        page.open()
    return page


@allure.title('Пользователь может осуществить поиск')
@allure.severity(allure.severity_level.NORMAL)
def test_guest_can_go_to_checkout(browser, page):
    with allure.step('Ввод запроса и нажатие кнопки "Поиск в Google"'):
        page.enter_search_query("МТС")
        page.click_search_button()
    with allure.step('Проверка, что первый результат соответствует ожиданиям'):
        results_page = ResultsPage(browser, links.MAIN_PAGE)
        results_page.should_has_result_with_correct_title(0, "МТС - связь и экосистема цифровых сервисов")


@allure.title('Пользователь может осуществить поиск (failed)')
@allure.severity(allure.severity_level.NORMAL)
def test_guest_can_go_to_checkout_failed(browser, page):
    with allure.step('Ввод запроса и нажатие кнопки "Поиск в Google"'):
        page.enter_search_query("МТС")
        page.click_search_button()
    with allure.step('Проверка, что первый результат соответствует ожиданиям'):
        results_page = ResultsPage(browser, links.MAIN_PAGE)
        results_page.should_has_result_with_correct_title(0, "МТС - связь и экосистема цифровых сервисов failed")
