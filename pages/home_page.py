import time
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage


class HomePage(BasePage):
    URL = "https://inerg-test.web.app/"
    STATE_DROPDOWN = (By.TAG_NAME, "select")
    PIE_CHART_TEXTS = (By.CLASS_NAME, "slicetext")
    TOTAL_CASES = (By.XPATH, "//p[1]")
    ACTIVE_CASES = (By.XPATH, "//p[2]")
    RECOVERED_CASES = (By.XPATH, "//p[3]")
    DEATHS = (By.XPATH, "//p[4]")
    LINE_CHART_POINTS = (By.CSS_SELECTOR, "g.scatterlayer g.trace")

    def __init__(self, driver):
        super().__init__(driver)
        driver.get(self.URL)

    def select_state_from_dropdown(self, state):
        self.select_state(self.STATE_DROPDOWN, state)

    def get_pie_chart_values(self):
        values_elements = self.driver.find_elements(*self.PIE_CHART_TEXTS)
        values = list(set([elem.text.strip() for elem in values_elements if elem.text.strip()]))
        return values

    def get_dashboard_numbers(self):
        wait = WebDriverWait(self.driver, 10)

        def get_text(locator):
            try:
                element = wait.until(EC.presence_of_element_located(locator))
                text = element.text.strip()
                numbers = re.findall(r'\d+', text)
                return numbers[0] if numbers else "Not found"
            except:
                return "Not found"

        return {
            "Total Cases": get_text(self.TOTAL_CASES),
            "Active Cases": get_text(self.ACTIVE_CASES),
            "Recovered": get_text(self.RECOVERED_CASES),
            "Deaths": get_text(self.DEATHS),
        }

    def get_line_chart_values(self):
        """ Extract (X, Y) values from the line chart. """
        wait = WebDriverWait(self.driver, 10)
        try:

            chart_container = self.driver.find_element(By.CLASS_NAME, "js-plotly-plot")
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",chart_container)
            time.sleep(2)

            script = """
            let chart = document.querySelector('.js-plotly-plot');
            if (!chart || !Plotly || !chart.data) return [];
            return chart.data.map(trace => ({x: trace.x, y: trace.y}));
            """
            chart_data = self.driver.execute_script(script)

            extracted_points = [(x, y) for trace in chart_data for x, y in zip(trace["x"], trace["y"])]
            for i, (x, y) in enumerate(extracted_points):
                print(f"Point {i + 1}: X = {x}, Y = {y}")

            return extracted_points if extracted_points else "No line chart data found"
        except Exception as e:
            return f"Error extracting line chart values: {str(e)}"
