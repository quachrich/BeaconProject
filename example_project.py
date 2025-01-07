from update_drivers import update_driver
from improved_webdriver import WebDriver

#update_driver('win64')

with WebDriver(headless = False,memory_structure = []) as driver:
    driver.get('https://www.roblox.com/charts#/?device=computer&country=all')
    divs = driver.find_elements_by_css('div.game-card-name.game-name-title',10)
    print(list(filter(lambda x:x != "",[div.text for div in divs])))