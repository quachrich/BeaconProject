from Easy_Selenium import WebDriver, update_driver
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
import time

# Automatically download and update the chromedriver based on the full path in .env
update_driver('win64')

max_pages = 10 
current_page = 0
orginal_data = []

with WebDriver(headless=False, memory_structure=[]) as driver:
    driver.get('https://beaconbio.org/en/')
    
    while current_page < max_pages:
        try:
            # Attempt to find elements by css, waiting for 25 seconds before returning None
            divs = driver.find_elements_by_css('div.MuiBox-root.mui-1ntp5xn > a', wait=25, errors='coerce')
            
            if not divs:
                print("No elements found on this page.")
                break

            # Print elements from current page
            for div in divs:
                try:
                    # Add a check to ensure element is still valid
                    print(div.text)
                    orginal_data.append(div.text)
                except StaleElementReferenceException:
                    print("Element became stale, skipping...")
                    continue

            current_page += 1
            print(f"Processed page {current_page}")

            try:
                # Find next page clickable element (parent of svg icon)
                next_button = driver.find_element_by_css('button[aria-label="Go to next page"]', wait=25, errors='coerce')
                
                # Add a small wait to ensure page is ready
                time.sleep(5)
                
                # Check if next button is enabled before clicking
                if next_button and next_button.is_enabled():
                    next_button.click()
                else:
                    print("Next page button is not clickable.")
                    break

            except (NoSuchElementException, StaleElementReferenceException) as nav_error:
                print(f"Error navigating to next page: {nav_error}")
                break

            #Wait time
            time.sleep(5)

        except Exception as e:
            print(f"Unexpected error on page {current_page}: {e}")
            break

clean_list = list(filter(str.strip, orginal_data))
print(clean_list)