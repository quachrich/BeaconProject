from Easy_Selenium import WebDriver, update_driver
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
import time
import os

# Automatically download and update the chromedriver based on the full path in .env
update_driver('mac-x64')

max_pages = 10 
current_page = 0
orginal_data = []

CHROMEDRIVER_PATH = os.getenv('CHROMEDRIVER_PATH', '/Users/richardquach/projects/webscraper/chromedriver')

with WebDriver(headless=False, memory_structure=[]) as driver:
    driver.get('https://beaconbio.org/en/')
    
    while current_page < max_pages:
        try:
            divs = driver.find_elements_by_css('div.MuiBox-root.mui-1ntp5xn > a', wait=25, errors='coerce')
        
            if not divs:
                print("No elements found on this page.")
                break
            for div in divs:
                try:
                    # Checkers
                    print(div.text)
                    orginal_data.append(div.text)
                except StaleElementReferenceException:
                    print("Element became stale, skipping...")
                    continue
            #Test
            current_page += 1
            #print(divs)
            #print(dates)
            print(f"Processed page {current_page}")

            try:
                # ID where button is to click
                next_button = driver.find_element_by_css('button[aria-label="Go to next page"]', wait=25, errors='coerce')
                
                # Additional Wait Time
                time.sleep(5)
                
                # How to click button
                if next_button and next_button.is_enabled():
                    next_button.click()
                else:
                    print("Next page button is not clickable.")
                    break

            except (NoSuchElementException, StaleElementReferenceException) as nav_error:
                print(f"Error navigating to next page: {nav_error}")
                break

            # Wait time
            time.sleep(5)

        except Exception as e:
            print(f"Unexpected error on page {current_page}: {e}")
            break

clean_list = list(filter(str.strip, orginal_data))
print(clean_list)
