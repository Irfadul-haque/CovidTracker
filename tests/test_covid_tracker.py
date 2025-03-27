import pytest
from selenium import webdriver
from pages.home_page import HomePage
import time
from selenium.webdriver.common.by import By


def test_covid_tracker():
    driver = webdriver.Chrome()
    driver.maximize_window()

    home_page = HomePage(driver)
    home_page.select_state_from_dropdown("Kerala")

    time.sleep(3)


    pie_chart_values = home_page.get_pie_chart_values()

    print("Extracted Pie Chart Values:", pie_chart_values)

    assert pie_chart_values, "ZNo pie chart values were extracted!"

    dashboard_numbers = home_page.get_dashboard_numbers()
    print(" Extracted Dashboard Numbers:", dashboard_numbers)

    line_chart_elements = home_page.driver.find_elements(By.CSS_SELECTOR, "g.scatterlayer g.trace")
    print("Found line chart elements:", len(line_chart_elements))



    driver.quit()
