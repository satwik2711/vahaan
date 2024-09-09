import time
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select 


# class VahanDashboardAutomator:
#     def __init__(self):
#         self.driver = None
#         self.base_url = "https://vahan.parivahan.gov.in/vahan4dashboard/vahan/view/reportview.xhtml"

#     def initialize_driver(self):
#         try:
#             # Specifying a ChromeDriver version manually
#             service = Service(ChromeDriverManager().install())
#             self.driver = webdriver.Chrome(service=service)
#             print("Driver initialized successfully.")
#         except Exception as e:
#             print(f"Error initializing driver: {e}")
#             return None


#     def start(self):
        
#         # if self.driver is None:
#         #     self.driver = self.initialize_driver()
#         # if self.driver is None:
#         #     print("Driver not initialized.")
#         #     return
#         self.driver = self.initialize_driver()
#         print("Starting browser and navigating to the Vahan dashboard.")
#         self.driver.get(self.base_url)
#         self.wait_for_page_load()


from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


class VahanDashboardAutomator:
    def __init__(self):
        self.driver = None
        self.base_url = "https://vahan.parivahan.gov.in/vahan4dashboard/vahan/view/reportview.xhtml"

    def initialize_driver(self):
        try:
            # Specifying a ChromeDriver version manually
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service)
            print("Driver initialized successfully.")
        except Exception as e:
            print(f"Error initializing driver: {e}")
            self.driver = None

    def wait_for_page_load(self):
        # Implement the logic to wait for the page to load
        pass

    def start(self):
        self.initialize_driver()
        if self.driver is None:
            print("Driver not initialized.")
            return
        print("Starting browser and navigating to the Vahan dashboard.")
        self.driver.get(self.base_url)
        self.wait_for_page_load()


    def select_custom_dropdown_value(self, dropdown_id, value):
        try:
            # Click to open the dropdown
            dropdown = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, dropdown_id))
            )
            dropdown.click()

            # Wait for the options to become visible and click the desired option
            option = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, f"//li[text()='{value}']"))
            )
            option.click()

            print(f"Selected {value} from custom dropdown {dropdown_id}.")
        except (NoSuchElementException, TimeoutException) as e:
            print(f"Error selecting dropdown value: {e}")



    def click_refresh_button(self, refresh_button_id):
        try:
            refresh_button = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, refresh_button_id))
            )
            refresh_button.click()
            print(f"Clicked refresh button with id '{refresh_button_id}'.")
        except NoSuchElementException:
            print(f"Refresh button with id '{refresh_button_id}' not found.")
        except TimeoutException:
            print(f"Refresh button with id '{refresh_button_id}' timed out.")

    def select_vehicle_category(self):
        try:
            # Click the button to open the vehicle category section
            open_button = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//a[@title='Collapse']"))
            )
            open_button.click()
            print("Opened vehicle category section.")
            
            # Select the 'Light Goods Vehicle' category checkbox
            checkbox = self.driver.find_element(By.ID, "VhcatgLbl")
            checkbox.click()
            print("Selected 'Light Goods Vehicle' checkbox.")
        except NoSuchElementException:
            print("Vehicle category checkbox not found.")
        except TimeoutException:
            print("Timeout while opening vehicle category or selecting checkbox.")

    def select_fuel_type(self, fuel_type):
        try:
            fuel_checkbox = self.driver.find_element(By.XPATH, f"//label[text()='{fuel_type}']/input[@type='checkbox']")
            if not fuel_checkbox.is_selected():
                fuel_checkbox.click()
            print(f"Selected fuel type: {fuel_type}")
        except NoSuchElementException:
            print(f"Fuel type checkbox for {fuel_type} not found.")
        except TimeoutException:
            print(f"Timeout while selecting fuel type: {fuel_type}")

    def deselect_all_fuel_types(self):
        try:
            fuel_checkboxes = self.driver.find_elements(By.XPATH, "//label[@id='fuelLbl']/input[@type='checkbox']")
            for checkbox in fuel_checkboxes:
                if checkbox.is_selected():
                    checkbox.click()
            print("Deselected all fuel types.")
        except NoSuchElementException:
            print("Fuel checkboxes not found.")
        except TimeoutException:
            print("Timeout while deselecting fuel checkboxes.")

    def download_excel(self):
        try:
            download_button = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "vchgroupTable:xls"))
            )
            download_button.click()
            print("Excel file download initiated.")
        except NoSuchElementException:
            print("Download button not found.")
        except TimeoutException:
            print("Timeout while clicking download button.")

    def wait_for_page_load(self, timeout=10):
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda d: d.execute_script('return document.readyState') == 'complete'
            )
            print("Page loaded successfully.")
        except TimeoutException:
            print("Page load timed out.")

    def close(self):
        print("Closing browser.")
        self.driver.quit()

# Example of how to use the class
if __name__ == "__main__":
    automator = VahanDashboardAutomator()
    automator.start()
    if automator.driver:
        print("auto")
        # automator.select_dropdown_value("state_dropdown_id", "Uttar Pradesh")  # Replace with correct dropdown ID
    # Select values for State and RTO
    automator.select_custom_dropdown_value("selectedState", "Uttar Pradesh")

    # Select "Agra RTO" from the RTO dropdown
    automator.select_custom_dropdown_value("selectedRto", "Agra RTO - UP80( 23-NOV-2017 )")
  # Replace with correct RTO name
    
    # Set X and Y axis values
    automator.select_custom_dropdown_value("xaxisVar", "Fuel")
    automator.select_custom_dropdown_value("yaxisVar", "Maker")
    
    # Click first refresh button
    automator.click_refresh_button("j_idt73")
    
    # Select vehicle category and fuel types
    automator.select_vehicle_category()
    
    # For CNG
    automator.select_fuel_type("CNG")
    automator.click_refresh_button("j_idt78")
    automator.download_excel()
    
    # For Petrol
    automator.select_fuel_type("Petrol")
    automator.click_refresh_button("j_idt78")
    automator.download_excel()
    
    # For None (deselect all)
    automator.deselect_all_fuel_types()
    automator.click_refresh_button("j_idt78")
    automator.download_excel()
    
    
#     requests
# selenium
# webdriver-manager
    
    # Close the browser
    automator.close()
