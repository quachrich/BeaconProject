from update_drivers import update_driver
from improved_webdriver import WebDriver

#Automatically download and update the chromedriver based on the full path in .env
update_driver('win64')

#Leverage EasySelenium to manage webdriver using the context manager
with WebDriver(headless = False,memory_structure = []) as driver:
    #Use similar syntax to selenium WebDriver to get a page URL
    driver.get('https://www.roblox.com/charts#/?device=computer&country=all')
    
    #Attempt to find elements by css, waiting for 10 seconds before returning None (coerced error)
    divs = driver.find_elements_by_css('div.game-card-name.game-name-title',wait = 10,errors = 'coerce')
    
    #Print top trending names of games in Roblox
    print(list(filter(lambda x:x != "",[div.text for div in divs])))