from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import os
import re

# Set the download directory
download_dir = '/home/siddhant/Documents/satwik-work/vahaan-downloads'

# Ensure the download directory exists
if not os.path.exists(download_dir):
    os.makedirs(download_dir)

# Configure Chrome options to set the download directory
chrome_options = Options()
chrome_prefs = {
    "download.default_directory": download_dir,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True,
    "plugins.always_open_pdf_externally": True
}
chrome_options.add_experimental_option('prefs', chrome_prefs)
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
# Optionally, run Chrome in headless mode
# chrome_options.add_argument('--headless')

# Initialize the driver
driver = webdriver.Chrome(options=chrome_options)

try:
    # Open the website
    url = 'https://vahan.parivahan.gov.in/vahan4dashboard/vahan/view/reportview.xhtml'  # Adjust URL if necessary
    driver.get(url)

    wait = WebDriverWait(driver, 20)

    # Function to select an option from a custom dropdown
    def select_custom_dropdown_option(dropdown_id, option_text):
        try:
            # Click on the dropdown to open it
            dropdown = wait.until(EC.element_to_be_clickable((By.ID, dropdown_id)))
            dropdown.click()

            # Wait for the panel to be visible
            panel_id = dropdown.get_attribute('aria-owns')
            panel = wait.until(EC.visibility_of_element_located((By.ID, panel_id)))

            # Find the option in the panel
            options = panel.find_elements(By.TAG_NAME, 'li')
            for option in options:
                if option.text.strip() == option_text:
                    option.click()
                    break
            else:
                print(f"Option '{option_text}' not found in dropdown '{dropdown_id}'")
                return False

            # Wait for the dropdown panel to close
            wait.until(EC.invisibility_of_element_located((By.ID, panel_id)))

            # Click outside to ensure dropdown is closed
            body = driver.find_element(By.TAG_NAME, 'body')
            body.click()

            # Alternatively, send ESCAPE key to close any open dropdowns
            # body.send_keys(Keys.ESCAPE)

            # Small pause to ensure the dropdown is closed
            time.sleep(1)

            return True
        except Exception as e:
            print(f"Error selecting option '{option_text}' in dropdown '{dropdown_id}': {e}")
            return False

    # Function to get all options from a custom dropdown
    def get_custom_dropdown_options(dropdown_id):
        try:
            # Click on the dropdown to open it
            dropdown = wait.until(EC.element_to_be_clickable((By.ID, dropdown_id)))
            dropdown.click()

            # Wait for the panel to be visible
            panel_id = dropdown.get_attribute('aria-owns')
            panel = wait.until(EC.visibility_of_element_located((By.ID, panel_id)))

            # Get all the options
            options = panel.find_elements(By.TAG_NAME, 'li')
            option_texts = [opt.text.strip() for opt in options]

            # Close the dropdown by clicking outside
            body = driver.find_element(By.TAG_NAME, 'body')
            body.click()

            # Wait for the dropdown to close
            wait.until(EC.invisibility_of_element_located((By.ID, panel_id)))

            return option_texts
        except Exception as e:
            print(f"Error getting options from dropdown '{dropdown_id}': {e}")
            return []

    # Function to select a checkbox by label text
    def select_checkbox_by_label(label_text, select=True):
        try:
            # Use XPath to find the label that contains the text
            label_xpath = f"//label[contains(text(), '{label_text}')]"
            label_element = driver.find_element(By.XPATH, label_xpath)
            
            # Now, navigate up to the containing td, then down to the checkbox div
            checkbox_div = label_element.find_element(By.XPATH, ".//preceding::td[1]//div[contains(@class, 'ui-chkbox-box')]")
            
            # Scroll the checkbox into view
            driver.execute_script("arguments[0].scrollIntoView(true);", checkbox_div)
            time.sleep(1)
            
            # Check if the checkbox is already selected
            is_selected = 'ui-state-active' in checkbox_div.get_attribute('class')
            if is_selected != select:
                checkbox_div.click()
            return True
        except Exception as e:
            print(f"Error interacting with checkbox for label '{label_text}': {e}")
            return False



    # Step 1: Select 'Fuel' from X-Axis and 'Maker' from Y-Axis (only once)
    if not select_custom_dropdown_option('xaxisVar', 'Fuel'):
        print("Error selecting 'Fuel' for X-Axis.")
    else:
        print("Selected 'Fuel' for X-Axis.")

    if not select_custom_dropdown_option('yaxisVar', 'Maker'):
        print("Error selecting 'Maker' for Y-Axis.")
    else:
        print("Selected 'Maker' for Y-Axis.")

    # Hit refresh button (j_idt62) to apply X-Axis and Y-Axis selections
    try:
        refresh_button = wait.until(EC.element_to_be_clickable((By.ID, 'j_idt62')))
        refresh_button.click()
        print("Clicked refresh button to apply X-Axis and Y-Axis selections.")
    except Exception as e:
        print(f"Error clicking refresh button: {e}")

    # Wait for the page to update
    time.sleep(5)

    # Get list of states
    state_options = get_custom_dropdown_options('j_idt31')

    # Skip the first option if it's 'All Vahan4 Running States'
    start_state_index = 1 if 'All Vahan4' in state_options[0] else 0

    # Iterate over all states
    for state_index in range(start_state_index, len(state_options)):
        state_name = state_options[state_index]

        # Select the state
        if not select_custom_dropdown_option('j_idt31', state_name):
            print(f"Skipping state '{state_name}' due to selection error.")
            continue
        print(f"Processing state: {state_name}")

        # Wait for RTO options to load
        time.sleep(2)

        # Get list of RTOs
        rto_options = get_custom_dropdown_options('selectedRto')

        if not rto_options:
            print(f"No RTO options found for state '{state_name}'.")
            continue

        # Skip the first option if it's 'All Vahan4 Running Office'
        start_rto_index = 1 if 'All Vahan4' in rto_options[0] else 0

        # Iterate over all RTOs
        for rto_index in range(start_rto_index, len(rto_options)):
            rto_name = rto_options[rto_index]

            # Select the RTO
            if not select_custom_dropdown_option('selectedRto', rto_name):
                print(f"  Skipping RTO '{rto_name}' due to selection error.")
                continue
            print(f"  Processing RTO: {rto_name}")

            # Wait for any dynamic content to load
            time.sleep(2)

            # Click outside to ensure any dropdowns are closed
            body = driver.find_element(By.TAG_NAME, 'body')
            body.click()
            time.sleep(1)

            # Step 4: Hit refresh button (j_idt62) to refresh data for the selected RTO
            try:
                refresh_button = wait.until(EC.element_to_be_clickable((By.ID, 'j_idt62')))
                refresh_button.click()
            except Exception as e:
                print(f"  Error clicking refresh button: {e}")
                continue

            # Wait for the page to update
            time.sleep(5)

            # Rest of your code remains the same...

            # Step 5: Click and open the 'filterLayout-toggler'
            # Click the expand icon to open the filter panel
            try:
                filter_expand_icon = wait.until(EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, 'a.ui-layout-unit-expand-icon.ui-state-default.ui-corner-all'))
                )
                filter_expand_icon.click()
                time.sleep(2)
            except Exception as e:
                print(f"  Error clicking filter expand icon: {e}")
                continue

            # Step 6: Select checkboxes for 'Light Goods Vehicle' and 'Light Motor Vehicle'
            vhclass_labels = ['LIGHT GOODS VEHICLE', 'LIGHT MOTOR VEHICLE']
            vhclass_found = False
            for label in vhclass_labels:
                if select_checkbox_by_label(label):
                    vhclass_found = True

            if not vhclass_found:
                print(f"    No matching Vehicle Class checkboxes found in '{rto_name}'; skipping this RTO.")
                # Close the filter panel
                try:
                    filter_collapse_icon = wait.until(EC.element_to_be_clickable(
                        (By.CSS_SELECTOR, 'a.ui-layout-unit-header-icon.ui-state-default.ui-corner-all[title="Collapse"]'))
                    )
                    filter_collapse_icon.click()
                    time.sleep(2)
                except Exception as e:
                    print(f"  Error clicking filter collapse icon: {e}")
                continue  # Skip to the next RTO

            # Proceed with selecting 'CNG ONLY' and 'PETROL' fuels
            fuel_labels = ['CNG ONLY', 'PETROL']
            for fuel_label in fuel_labels + [None]:  # The None case is when both fuels are deselected
                if fuel_label is not None:
                    # Deselect all fuels first
                    select_checkbox_by_label('CNG ONLY', select=False)
                    select_checkbox_by_label('PETROL', select=False)
                    if select_checkbox_by_label(fuel_label):
                        print(f"    Selected fuel: {fuel_label}")
                    else:
                        print(f"    Fuel '{fuel_label}' not found; skipping.")
                        continue
                else:
                    # Deselect both fuels for 'all fuels' case
                    select_checkbox_by_label('CNG ONLY', select=False)
                    select_checkbox_by_label('PETROL', select=False)
                    print("    Selected all fuels (no specific fuel selected).")

                # Hit the secondary refresh button (j_idt67)
                try:
                    secondary_refresh_button = wait.until(EC.element_to_be_clickable((By.ID, 'j_idt67')))
                    secondary_refresh_button.click()
                except Exception as e:
                    print(f"    Error clicking secondary refresh button: {e}")
                    continue

                # Wait for the page to update
                time.sleep(5)

                # Download the report
                try:
                    download_link = wait.until(EC.element_to_be_clickable((By.ID, 'groupingTable:xls')))
                    download_link.click()
                    if fuel_label:
                        print(f"    Downloaded report for {fuel_label}")
                    else:
                        print(f"    Downloaded report for all fuels")
                except Exception as e:
                    if fuel_label:
                        print(f"    Download link not found for {fuel_label}: {e}")
                    else:
                        print(f"    Download link not found for all fuels: {e}")

                # Wait for the download to complete
                time.sleep(5)

            # Close the filter panel
            try:
                filter_collapse_icon = wait.until(EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, 'a.ui-layout-unit-header-icon.ui-state-default.ui-corner-all[title="Collapse"]'))
                )
                filter_collapse_icon.click()
                time.sleep(2)
            except Exception as e:
                print(f"  Error clicking filter collapse icon: {e}")

        # Wait before processing the next state
        time.sleep(2)

finally:
    # Close the driver
    driver.quit()
