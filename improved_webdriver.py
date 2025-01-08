#Webscraper selenium Imports
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import logging, os #Standard system imports
from dotenv import load_dotenv
from bs4 import BeautifulSoup #To pass a selenium object to bs4 in .get_soup()

load_dotenv()
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log', mode='a'),
        logging.StreamHandler()
    ]
)

CHROMEDRIVER_DIRECTORY = os.getenv("CHROMEDRIVER_PATH",default = None)
if CHROMEDRIVER_DIRECTORY is None:
    CHROMEDRIVER_DIRECTORY = os.path.dirname(__file__)
    logging.warning(
        "No CHROMEDRIVER_PATH established in .env, instead using relative file directory. For absolute path references, ensure you \
        have created a .env file with the abspath of your directory in a CHROMEDRIVER_PATH variable"
    )
CHROMEDRIVER_PATH = os.path.join(CHROMEDRIVER_DIRECTORY,"chromedriver.exe")


class WebDriver:
    """
    A helpful object to reduce tedious syntax in selenium programming
    
    Notably, allows for a wait parameter to be passed to the find_element_by_id and find_element_by_class methods
    
    Self.memory defaults to a list, but can be specified as a different data structure
    
    <headless>: boolean to determine whether to opened page will be visible
    <memory_structure>: a data structure to hold values for later use
    """
    def __init__(self, headless=False, memory_structure=[]):
        """
        Initialize the WebDriver instance.

        :param headless: Boolean to determine whether the opened page will be visible.
        :param memory_structure: A data structure to hold values for later use.
        """
        service =  Service(executable_path=CHROMEDRIVER_PATH)
        if not headless:
            self.driver = webdriver.Chrome(service=service)
        else:
            options = Options()
            options.add_argument("--window-size=1920,1080")
            options.add_argument("--headless=new")
            options.add_argument("--disable-gpu")
            options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")
            self.driver = webdriver.Chrome(service=service,options= options)
        self.memory = memory_structure
        logging.info("Webdriver opened")
    
    #Allows for the use of the 'with' statement
    def __enter__(self):
        """
        Allows for the use of the 'with' statement.
        """
        return self
    def __exit__(self,exception_type, exception_value, traceback):
        """
        Ensures the WebDriver is closed when exiting the 'with' statement.

        :param exception_type: Type of the exception.
        :param exception_value: Value of the exception.
        :param traceback: Traceback of the exception.
        """
        self.close()
        if exception_type is not None:
            logging.error("\nExecution type:", exception_type)
            logging.error("\nExecution value:", exception_value)
            logging.error("\nTraceback:", traceback)
        return True
    
    def set_timeout_limit(self,seconds):
        """
        Set the page load timeout limit.

        :param seconds: Number of seconds to wait before timing out.
        """
        self.driver.set_page_load_timeout(seconds)
    
    def get(self,url):
        """
        Navigate to a specified URL.

        :param url: The URL to navigate to.
        """
        self.driver.get(url)
    
    def get_current_link(self):
        """
        Get the current URL of the WebDriver.

        :return: The current URL.
        """
        return self.driver.current_url
    
    def find_element_by_id(self, id, wait=None, errors='raise'):
        """
        Find an element by its ID.

        :param id: The ID of the element.
        :param wait: Time to wait for the element to be present.
        :param errors: Error handling strategy ('raise' or 'coerce').
        :return: The found element.
        """
        if errors == 'coerce':
            try:
                if wait:
                    WebDriverWait(self.driver, wait).until(EC.presence_of_element_located((By.ID, id)))
                return self.driver.find_element(By.ID, id)
            except Exception as e:
                print(f"Error finding element by ID: {e}")
        else:
            if wait:
                WebDriverWait(self.driver, wait).until(EC.presence_of_element_located((By.ID, id)))
            return self.driver.find_element(By.ID, id)

    def find_elements_by_id(self, id, wait=None, errors='raise'):
        """
        Find multiple elements by their ID.

        :param id: The ID of the elements.
        :param wait: Time to wait for the elements to be present.
        :param errors: Error handling strategy ('raise' or 'coerce').
        :return: A list of found elements.
        """
        if errors == 'coerce':
            try:
                if wait:
                    WebDriverWait(self.driver, wait).until(EC.presence_of_element_located((By.ID, id)))
                return self.driver.find_elements(By.ID, id)
            except Exception as e:
                print(f"Error finding elements by ID: {e}")
        else:
            if wait:
                WebDriverWait(self.driver, wait).until(EC.presence_of_element_located((By.ID, id)))
            return self.driver.find_elements(By.ID, id)

    def find_element_by_css(self, css_tag, wait=False, errors='raise'):
        """
        Find an element by its CSS selector.

        :param css_tag: The CSS selector of the element.
        :param wait: Time to wait for the element to be present.
        :param errors: Error handling strategy ('raise' or 'coerce').
        :return: The found element.
        """
        if errors == 'coerce':
            try:
                if wait:
                    WebDriverWait(self.driver, wait).until(EC.presence_of_element_located((By.CSS_SELECTOR, css_tag)))
                return self.driver.find_element(By.CSS_SELECTOR, css_tag)
            except Exception as e:
                print(f"Error finding element by CSS: {e}")
        else:
            if wait:
                WebDriverWait(self.driver, wait).until(EC.presence_of_element_located((By.CSS_SELECTOR, css_tag)))
            return self.driver.find_element(By.CSS_SELECTOR, css_tag)

    def find_elements_by_css(self, css_tag, wait=None, errors='raise'):
        """
        Find multiple elements by their CSS selector.

        :param css_tag: The CSS selector of the elements.
        :param wait: Time to wait for the elements to be present.
        :param errors: Error handling strategy ('raise' or 'coerce').
        :return: A list of found elements.
        """
        if errors == 'coerce':
            try:
                if wait:
                    WebDriverWait(self.driver, wait).until(EC.presence_of_element_located((By.CSS_SELECTOR, css_tag)))
                return self.driver.find_elements(By.CSS_SELECTOR, css_tag)
            except Exception as e:
                print(f"Error finding elements by CSS: {e}")
        else:
            if wait:
                WebDriverWait(self.driver, wait).until(EC.presence_of_element_located((By.CSS_SELECTOR, css_tag)))
            return self.driver.find_elements(By.CSS_SELECTOR, css_tag)

    def find_element_by_class(self, class_name, wait=None, errors='raise'):
        """
        Find an element by its class name.

        :param class_name: The class name of the element.
        :param wait: Time to wait for the element to be present.
        :param errors: Error handling strategy ('raise' or 'coerce').
        :return: The found element.
        """
        if errors == 'coerce':
            try:
                if wait:
                    WebDriverWait(self.driver, wait).until(EC.presence_of_element_located((By.CLASS_NAME, class_name)))
                return self.driver.find_element(By.CLASS_NAME, class_name)
            except Exception as e:
                print(f"Error finding element by class: {e}")
        else:
            if wait:
                WebDriverWait(self.driver, wait).until(EC.presence_of_element_located((By.CLASS_NAME, class_name)))
            return self.driver.find_element(By.CLASS_NAME, class_name)

    def find_elements_by_class(self, class_name, wait=None, errors='raise'):
        """
        Find multiple elements by their class name.

        :param class_name: The class name of the elements.
        :param wait: Time to wait for the elements to be present.
        :param errors: Error handling strategy ('raise' or 'coerce').
        :return: A list of found elements.
        """
        if errors == 'coerce':
            try:
                if wait:
                    WebDriverWait(self.driver, wait).until(EC.presence_of_element_located((By.CLASS_NAME, class_name)))
                return self.driver.find_elements(By.CLASS_NAME, class_name)
            except Exception as e:
                print(f"Error finding elements by class: {e}")
        else:
            if wait:
                WebDriverWait(self.driver, wait).until(EC.presence_of_element_located((By.CLASS_NAME, class_name)))
            return self.driver.find_elements(By.CLASS_NAME, class_name)
    
    def hold_values(self,values):
        """
        Hold values in the memory structure.

        :param values: Values to hold.
        """
        self.memory.append(values)
    
    def get_memory(self):
        """
        Get the values stored in the memory structure.

        :return: The memory structure.
        """
        return self.memory

    def get_page_source(self):
        """
        Get the page source of the current page.

        :return: The page source.
        """
        return self.driver.page_source

    def get_soup(self):
        """
        Get a BeautifulSoup object of the current page source.

        :return: A BeautifulSoup object.
        """
        html_content = self.get_page_source()
        return BeautifulSoup(html_content, 'html.parser')

    def close(self):
        """
        Close the WebDriver.
        """
        self.driver.quit()
        logging.info("WebDriver Closed")