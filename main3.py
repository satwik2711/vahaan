from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver import ActionChains
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

    def select_custom_dropdown_value_js(self, dropdown_id, value):
        try:
            # Open the dropdown
            dropdown = WebDriverWait(self.driver, 15).until(
                EC.element_to_be_clickable((By.ID, dropdown_id))
            )
            dropdown.click()

            # Use JavaScript to select the option (this is useful for custom dropdowns)
            option = WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.XPATH, f"//li[contains(text(), '{value}')]"))
            )
            self.driver.execute_script("arguments[0].click();", option)

            print(f"Selected {value} from dropdown {dropdown_id}.")
        except (NoSuchElementException, TimeoutException, ElementNotInteractableException) as e:
            print(f"Error selecting dropdown value: {e}")


    def click_refresh_button(self, refresh_button_id):
        try:
            refresh_button = WebDriverWait(self.driver, 15).until(
                EC.element_to_be_clickable((By.ID, refresh_button_id))
            )
            self.driver.execute_script("arguments[0].click();", refresh_button)
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

    # Select "Uttar Pradesh" from the state dropdown using JavaScript
    automator.select_custom_dropdown_value_js("j_idt38", "Uttar Pradesh")

    # Select "Agra RTO" from the RTO dropdown using JavaScript
    automator.select_custom_dropdown_value_js("selectedRto", "Agra RTO")

    # Select "Fuel" for X-axis
    automator.select_custom_dropdown_value_js("xaxisVar", "Fuel")

    # Select "Maker" for Y-axis
    automator.select_custom_dropdown_value_js("yaxisVar", "Maker")

    # Click the refresh button
    automator.click_refresh_button("j_idt69")
    input("Press Enter to close the browser...")

    # Close the browser
    # automator.close()
