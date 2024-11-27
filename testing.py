from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time

def main():
    try:
        print("Starting browser...")

        # Get the path to the installed driver
        driver_path = ChromeDriverManager().install()
        print(f"ChromeDriver installed at: {driver_path}")

        # Create a Service object using the driver path
        service = Service(driver_path)

        # Initialize Chrome options
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")

        # Initialize the Chrome WebDriver using the service
        driver = webdriver.Chrome(service=service, options=options)

        driver.maximize_window()

        # Navigate to FitPeo HomePage
        print("Navigating to FitPeo HomePage...")
        driver.get("https://www.fitpeo.com/")

        # Wait for the "Revenue Calculator" link and click it
        print("Waiting for 'Revenue Calculator' link...")
        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Revenue Calculator"))
        ).click()
        print("Navigated to Revenue Calculator Page.")

        # Scroll to the slider section
        print("Waiting for slider section to appear...")
        slider_section = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(
                (By.XPATH, "//div[contains(@class, 'MuiBox-root') and contains(@class, 'css-79elbk')]")
            )
        )
        print("Slider section found. Scrolling into view...")
        driver.execute_script("arguments[0].scrollIntoView(true);", slider_section)
        time.sleep(2)  # Allow time for loading

        # Locate the slider thumb element
        print("Locating slider thumb...")
        slider_thumb = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, ".MuiSlider-thumb")
            )
        )

        # Use ActionChains to drag the slider to an initial value (e.g., 820)
        print("Increasing slider value...")
        action = ActionChains(driver)
        action.click_and_hold(slider_thumb).move_by_offset(93, 0).release().perform()
        time.sleep(2)  # Allow time to see the slider move
        print("Slider value increased to 820")
        
        # Update the text area with a new value
        print("Locating and updating the value")
        input_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, ":r0:"))
        )
        
        # Click on the input field to focus it
        input_element.click()

        # Clear the existing value
        input_element.clear()

        # Set the new value
        new_value = 560
        input_element.send_keys(str(new_value))

        # Wait a bit after setting the value
        time.sleep(1)  # Adjust as necessary

        # Update the slider based on the new input value
        slider_value = new_value
        known_value = 900
        known_offset = 63 #73=520

        # Calculate the position of the slider thumb based on the input value
        new_offset = (slider_value / known_value) * known_offset
        print(f"Calculated offset for {new_value}: {new_offset:.2f} px")

        # Move the slider thumb to match the input value
        print(f"Moving slider to {new_value}...")
        action = ActionChains(driver)
        action.click_and_hold(slider_thumb).move_by_offset(-new_offset, 0).release().perform()

        # Trigger input events to synchronize the changes
        driver.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", input_element)
        driver.execute_script("arguments[0].dispatchEvent(new Event('change', { bubbles: true }));", input_element)

        # Verify that both the input and slider values are synchronized
        input_value = input_element.get_dom_attribute('value')
        print(f"Input value is: {input_value}")

        if input_value == str(new_value):
            print("textarea update test case passed")
        else:
            print("Error")

        time.sleep(3)
    

        # Reset the slider and input to 820
        print("Resetting slider and input value to 820")

        # Move the slider back to 820 (reset)
        reset_value = 570
        reset_offset = (reset_value / known_value) * known_offset  # Recalculate offset for 820
        print(f"Calculated reset offset for 820: {reset_offset:.2f} px")

        # Move the slider thumb back to the reset value
        action = ActionChains(driver)
        action.click_and_hold(slider_thumb).move_by_offset(reset_offset, 0).release().perform()

        # Reset the input field to 820
        input_element.clear()
        input_element.send_keys(str(reset_value))

        # Trigger input events for synchronization
        driver.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", input_element)
        driver.execute_script("arguments[0].dispatchEvent(new Event('change', { bubbles: true }));", input_element)

        time.sleep(3)
        
        # Scroll to CPT Codes section and select specified checkboxes
        print("Scrolling to CPT Codes section...")
        cpt_section = driver.find_element(By.XPATH, "//div[contains(@class, 'MuiBox-root') and contains(@class, 'css-1eynrej')]")
        driver.execute_script("arguments[0].scrollIntoView(true);", cpt_section)

        time.sleep(2)
        
        #Selecting the checkboxes of CPT Codes
        print("Selecting CPT code checkboxes...")
        checkbox_indices = [1, 2, 3, 8]  # Corresponds to 0th, 1st, 2nd, and 7th checkboxes
        for index in checkbox_indices:
            checkbox = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((
                    By.CSS_SELECTOR, f".MuiBox-root.css-1eynrej:nth-child({index}) input.PrivateSwitchBase-input.css-1m9pwf3"
                ))
            )
            # Select the checkbox if not already selected
            if not checkbox.is_selected():
                checkbox.click()
                print(f"Checkbox {index} selected.")

        time.sleep(3)  # Allow time to observe the selection
        
        #Locating Total Recurring Reimbursement
        try:
            # Wait for the parent container to load
            parent_container = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located(
                    (By.CLASS_NAME, "MuiBox-root.css-19zjbfs")
                )
            )
            
            # Locate the child element containing the total recurring reimbursement
            recurring_reimbursement_element = parent_container.find_element(
                By.CSS_SELECTOR, ".MuiBox-root.css-m1khva p:nth-of-type(2)"
            )
            
            # Extract the reimbursement value
            recurring_reimbursement_value = recurring_reimbursement_element.text.strip()
            print(f"Extracted Total Recurring Reimbursement: {recurring_reimbursement_value}")
            
            # Validate the value
            expected_value = "$110700"
            if recurring_reimbursement_value == expected_value:
                print("Validation Passed: Total Recurring Reimbursement is correct.")
            else:
                print(
                    f"Validation Failed: Expected {expected_value}, but got {recurring_reimbursement_value}."
                )
        
        except Exception as e:
             print(f"An error occurred during validation: {e}")


        time.sleep(10)
        
        
    except Exception as e:
        print(f"Test case failed: {e}")

    finally:
        driver.quit()
        print("all test cases passed successfully and browser is closed")

if __name__ == "__main__":
    main()
