from selenium.webdriver.support.ui import Select


class BasePage:
    def __init__(self, driver):
        self.driver = driver

    def select_state(self, dropdown_locator, state_name):
        select = Select(self.driver.find_element(*dropdown_locator))
        select.select_by_visible_text(state_name)