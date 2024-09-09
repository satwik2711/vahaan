from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementNotInteractableException


class VahanDashboardAutomator:
    def __init__(self):
        self.driver = None
        self.base_url = "https://vahan.parivahan.gov.in/vahan4dashboard/vahan/view/reportview.xhtml"

    def initialize_driver(self):
        try:
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service)
            print("Driver initialized successfully.")
        except Exception as e:
            print(f"Error initializing driver: {e}")
            self.driver = None

    def start(self):
        self.initialize_driver()
        if self.driver is None:
            print("Driver not initialized.")
            return
        print("Starting browser and navigating to the Vahan dashboard.")
        self.driver.get(self.base_url)
        self.wait_for_page_load()

    def wait_for_page_load(self, timeout=10):
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda d: d.execute_script('return document.readyState') == 'complete'
            )
            print("Page loaded successfully.")
        except TimeoutException:
            print("Page load timed out.")

    def select_custom_dropdown_value(self, dropdown_id, value):
        try:
            dropdown = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, dropdown_id))
            )
            dropdown.click()
            option = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, f"//li[contains(text(), '{value}')]"))
            )
            option.click()
            print(f"Selected {value} from dropdown {dropdown_id}.")
        except (NoSuchElementException, TimeoutException, ElementNotInteractableException) as e:
            print(f"Error selecting dropdown value: {e}")

    def click_refresh_button(self, refresh_button_id):
        try:
            refresh_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, refresh_button_id))
            )
            refresh_button.click()
            print(f"Clicked refresh button with id '{refresh_button_id}'.")
        except NoSuchElementException:
            print(f"Refresh button with id '{refresh_button_id}' not found.")
        except TimeoutException:
            print(f"Refresh button with id '{refresh_button_id}' timed out.")

    def close(self):
        print("Closing browser.")
        self.driver.quit()


if __name__ == "__main__":
    automator = VahanDashboardAutomator()
    automator.start()

    automator.select_custom_dropdown_value("j_idt38", "Uttar Pradesh")
    automator.select_custom_dropdown_value("selectedRto", "Agra RTO")
    automator.select_custom_dropdown_value("xaxisVar", "Fuel")
    automator.select_custom_dropdown_value("yaxisVar", "Maker")
    automator.click_refresh_button("j_idt73")
    input("Press Enter to close the browser...")
