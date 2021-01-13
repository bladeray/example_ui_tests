import pytest
import allure
from selenium import webdriver
import datetime
import pip
import platform
import xdist
import selenium
import os


def pytest_addoption(parser):
    parser.addoption('--browser', action='store', default='chrome', help='Available: chrome, firefox, opera')
    parser.addoption('--executor', action='store', default='local', help='Choose execute: local, selenoid')
    parser.addoption('--vnc', action='store', default='disable', help='enableVNC: enable, disable')
    parser.addoption('--video', action='store', default='disable', help='Saving Video: enable, disable')


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
    return rep


@pytest.fixture(scope='function')
def browser(request):
    with allure.step('Запускаем браузер'):
        if request.config.getoption('--executor') == 'selenoid':

            capabilities = {
                "browserName": request.config.getoption('--browser'),
                "enableVNC": False if request.config.getoption('--vnc') == 'disable' else True,
                "enableVideo": False if request.config.getoption('--video') == 'disable' else True,
                "env": ["TZ=Europe/Moscow"]
            }

            browser = webdriver.Remote(command_executor="http://localhost:4444/wd/hub",
                                       desired_capabilities=capabilities)

        elif request.config.getoption('--executor') == 'local':
            if request.config.getoption('--browser') == 'chrome':
                browser = webdriver.Chrome()

            elif request.config.getoption('--browser') == 'firefox':
                browser = webdriver.Firefox()

            elif request.config.getoption('--browser') == 'opera':
                browser = webdriver.Opera()
    browser.set_window_position(0, 0)
    browser.set_window_size(1920, 1080)
    browser.implicitly_wait(10)
    yield browser

    if request.config.getoption('--alluredir') == 'allure_results':
        env_file = open('./allure_results/environment.properties', 'w+')
        env_file.write(f'OS.version={platform.platform()}'
                       f'\nPython.version={platform.python_version()}'
                       f'\nPytest.version={pytest.__version__}'
                       f'\nSelenium.version={selenium.__version__}'
                       f'\nPip.version={pip.__version__}'
                       f'\nXdist.version={xdist.__version__}'
                       f'\nExecutor.type={request.config.getoption("--executor")}'
                       f'\nBrowser={request.config.getoption("--browser")}')
        env_file.close()

    if request.node.rep_call.failed:
        try:
            browser.execute_script("document.body.bgColor = 'white';")
            date = str(datetime.datetime.now().strftime("%d-%m-%Y_%H%M%S"))
            browser.save_screenshot(f'./screenshots/{date}_{request.function.__name__}.png')
            allure.attach(browser.get_screenshot_as_png(),
                          name=request.function.__name__,
                          attachment_type=allure.attachment_type.PNG)
        finally:
            pass

    with allure.step('Закрываем браузер'):
        browser.quit()
