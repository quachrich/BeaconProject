from update_drivers import update_driver
from improved_webdriver import WebDriver

#Automatically download and update the chromedriver based on the full path in .env
update_driver('win64')

#Uses the EasySelenium ability to use webdrivers in a with statement
with WebDriver(headless = False,memory_structure = []) as driver:
    driver.get('https://www.roblox.com/charts#/?device=computer&country=all')
    
    #Utilize Easy Selenium to wait 10 seconds for presence of element, and coerce in case of errors in one line
    divs = driver.find_elements_by_css('div.game-card-name.game-name-title',10,errors = 'coerce')
    
    #Print top trending names of games in Roblox
    print(list(filter(lambda x:x != "",[div.text for div in divs])))