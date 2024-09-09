from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time




"""

TODO:
    
    implement  logic by changing the string j_idt38_33 suffix 33 ->uttar pradesh 
    
    implement  logic by changing the string selectedRto_1 , get the RTO count from XPATH //*[@id="j_idt38_label"]  
    get the text Chandigarh(1)  get the number and loop it that many time O(n^2) selectedRto_1 
        
    implement checkbox logic by inspect element of the checkbox rightclick copy xpath paste the xpath 
    
    impement file_name save thing 
    
    lower the sleep time by experimenting 2 sec - 5 sec
    
    complete
    
    you can do this broski , Bring $$$$
    
      

"""

def automate_vahan_dashboard():
    # Initialize the WebDriver
    driver = webdriver.Chrome()

    try:
        # Open the URL
        driver.get("https://vahan.parivahan.gov.in/vahan4dashboard/vahan/view/reportview.xhtml")

        # Wait for the page to load and interact with elements
        wait = WebDriverWait(driver, 15)


        """
        implement  logic by changing the string j_idt38_33 suffix 33 ->uttar pradesh 
        """

        label1 = wait.until(EC.element_to_be_clickable((By.ID, "j_idt38_label")))
        driver.execute_script("arguments[0].click();", label1)
        time.sleep(2)
        option1 = wait.until(EC.element_to_be_clickable((By.ID, "j_idt38_33")))
        driver.execute_script("arguments[0].click();", option1)
        # driver.execute_script("arguments[0].click();", option1)
        # time.sleep(5)
        print("state")
        
        
        """
        implement  logic by changing the string selectedRto_1 , get the RTO count from XPATH //*[@id="j_idt38_label"]  
        get the text Chandigarh(1)  get the number and loop it that many time O(n^2) selectedRto_1 
        """
        
        # Select the second dropdown option
        label2 = wait.until(EC.element_to_be_clickable((By.ID, "selectedRto_label")))
        driver.execute_script("arguments[0].click();", label2)
        time.sleep(2)
        option2 = wait.until(EC.element_to_be_clickable((By.ID, "selectedRto_1")))
        driver.execute_script("arguments[0].click();", option2)
        time.sleep(5)
        print("rto.")
        # Select the third dropdown option
        label3 = wait.until(EC.element_to_be_clickable((By.ID, "xaxisVar_label")))
        driver.execute_script("arguments[0].click();", label3)
        time.sleep(2)
        option3 = wait.until(EC.element_to_be_clickable((By.ID, "xaxisVar_2")))
        driver.execute_script("arguments[0].click();", option3)
        time.sleep(5)
        print("xaxis.")
        # Select the fourth dropdown option
        label4 = wait.until(EC.element_to_be_clickable((By.ID, "yaxisVar_label")))
        driver.execute_script("arguments[0].click();", label4)
        time.sleep(2)
        option4 = wait.until(EC.element_to_be_clickable((By.ID, "yaxisVar_4")))
        driver.execute_script("arguments[0].click();", option4)
        time.sleep(5)
        print("yaxis.")
        
        refresh_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Refresh']")))
        driver.execute_script("arguments[0].click();", refresh_button)
        time.sleep(10)

        # Click the span with the class 'ui-icon ui-icon-arrow-4-diag'
        span_icon = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "span.ui-icon.ui-icon-arrow-4-diag")))
        driver.execute_script("arguments[0].click();", span_icon)
        time.sleep(2)
        # Click the fifth span with the class 'ui-chkbox-icon ui-icon ui-icon-blank ui-c'
        spans = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "span.ui-chkbox-icon.ui-icon.ui-icon-blank.ui-c")))
        driver.execute_script("arguments[0].click();", spans[4])
        time.sleep(2)
        # Check the checkbox with the ID 'norms:0'
        
        """
        implement checkbox logic by inspect element of the checkbox rightclick copy xpath paste the xpath 
        """
        
        
        
        checkbox = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="VhCatg"]/tbody/tr[4]/td/div/div[2]')))
        print("done")
        driver.execute_script("arguments[0].click();", checkbox)
        time.sleep(2)
        print("done")
        refresh_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Refresh']")))
        
        print(refresh_button.text)
        driver.execute_script("arguments[0].click();", refresh_button)
        time.sleep(5)
        
        download = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/form/div[2]/div/div/div[3]/div/div[2]/div/div/div[1]/div[1]/a'))) 
        driver.execute_script("arguments[0].click();", download)
        time.sleep(5)
        
        print("Automation completed successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")

        # Close the browser
        driver.quit()

if __name__ == "__main__":
    automate_vahan_dashboard()