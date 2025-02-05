# EasySelenium
# Table of Contents
1. [Overview](#overview)
2. [Directory Structure](#directory-structure)
3. [Configuration](#configuration)
    1. [Setting up the `.env` file](#setting-up-the-env-file)
    2. [Configuring a virutal environment](#setting-up-a-virtual-environment)
4. [Usage](#usage)
    1. [Web Driver Class](#webdriver-class-usage)
    2. [Automatically Updating Chromedriver](#updating-chromedriver)
5. [Contributing](#contributing)

## Overview
The EasySelenium project is designed to make the `Selenium` module a little bit easier to use. It supports automatic chromedriver updates, and shorter syntax for finding_elements. 

## Directory Structure

```
redtail/
├──improved_webdriver.py
├──update_drivers.py
├──example_project.py
├── README.md
├── chromedriver.exe
└── requirements.txt
```

### Modules
- `improved_webdriver.py`: Contains the `WebDriver` class, which simplifies the use of Selenium WebDriver for web scraping. It includes methods for navigating web pages, finding elements with built-in EC delays, and passing Selenium content to BeautifulSoup.
- `update_drivers.py`: Contains the `update_chromedriver` functions, which sends an HTML request, downloading the most recent version of *chromedriver.exe* in place, overwriting the existing chromedriver with the most recent version

## Configuration
To easily download all repo code onto your local machine use:
```git
git clone https://github.com/JoeyRussoniello/EasySelenium
cd EasySelenium
```
Code will not run out-of-the-box unless the dependencies have all been successfully installed. See [Virutal Environment Setup Instructions](#setting-up-a-virtual-environment) for details

### Setting Up the `.env` File

To configure the project, it is recommended to set up a  `.env` file in the root directory of the project. This file will store environment-specific variables such as paths and credentials, when not given the `CHROMEDRIVER_PATH` will default to your current working directory.

#### Example `.env` File

Here is an example of what your `.env` file should look like:

```properties
CHROMEDRIVER_PATH=C:\path\to\your\chromedriver
```
With an updating path to your chromedriver instead of the placeholder variable. \
*Note that including chromedriver.exe at the end of the CHROMEDRIVER_PATH variable is not neccesary*

### Setting Up a Virtual Environment
It is recommended to use a virtual environment to manage dependencies. Follow these steps to create and activate a virtual environment

1. Create a Virtual Environment
```bash 
python -m venv .venv
```
**Note: Ensure you include the .venv at the end of the installation path** \ 
2. Activate the Virtual Environment
- On Windows:
```bash
.\.venv\Scripts\activate
```
- On macOS and Linux:
```bash
source .venv/bin/activate
```
3. Install Dependencies
With the virtual environment activated, install the required dependencies using the `requirements.txt` file
```bash
pip install -r requirements.txt
```
# Usage

## WebDriver Class Usage

The `WebDriver` class is designed to simplify Selenium programming by reducing tedious syntax. Below are the usage instructions and examples.

### Initialization

```python
from improved_webdriver import WebDriver

# Initialize WebDriver with default settings
driver = WebDriver()

# Initialize WebDriver in headless mode
driver = WebDriver(headless=True)

# Initialize WebDriver with a custom memory structure
driver = WebDriver(memory_structure={})

#Initialize WebDriver, if unsuccesful try updating the chromedriver for windows and initialize again
driver = WebDriver(headless = True, platform = 'win64')
```

#### Parameters

- `headless`: A boolean to determine whether the opened page will be visible. If `True`, the browser will run in headless mode (no GUI). Defaults to `False`.
- `memory_structure`: A data structure to hold values for later use. Defaults to an empty list.
- `platform`: In case of initialization failure, attempt to update `chromedriver.exe` by calling `update_drivers.update_chromedriver(platform)`. Defaults to 'win64' The available platforms are:
    - `linux64`
    - `mac-arm64`
    - `mac-x64`
    - `win32`
    - `win64`

### Methods

#### `find_element_by_id`

```python
element = driver.find_element_by_id('element_id', wait=10, errors='raise')
```

- `id`: The ID of the element to find.
- `wait`: Time in seconds to wait for the element to be present. Defaults to `None`.
- `errors`: Error handling strategy. If `'raise'`, an exception will be raised on error. If `'coerce'`, the error will be printed and the program will continue.

#### `find_elements_by_id`

```python
elements = driver.find_elements_by_id('element_id', wait=10, errors='raise')
```

- `id`: The ID of the elements to find.
- `wait`: Time in seconds to wait for the elements to be present. Defaults to `None`.
- `errors`: Error handling strategy. If `'raise'`, an exception will be raised on error. If `'coerce'`, the error will be printed and the program will continue.


EasySelenium can also be used to search by *class, css selector, and by xpath* with similar syntax, using:
- `find_element_by_class` and `find_elements_by_class` to search by class
- `find_element_by_css` and `find_elements_by_css`to search by css selector
- `find_element_by_xpath` and `find_elements_by_xpath` to search by xpath

### `get_soup`
```
#Returns a BeautifulSoup html parser of the JS-rendered page. 
soup = driver.get_soup()
```
### Example Usage

```python
from improved_webdriver import WebDriver

with WebDriver(headless=True) as driver:
    driver.get('https://example.com')
    #This may not exist on the website, so in that case we'll just log that it wasn't found instead of halting the program
    element = driver.find_element_by_id('example_id', wait=10, errors='raise')
    print(element.text if element else "Element not found")
    #This is essential for the program to run, raise an error if not found
    elements = driver.find_elements_by_class('example_class', wait=10, errors='coerce')
    for elem in elements:
        print(elem.text)
    #Create a BeautifulSoup parser of the driver (post JS-rendering)
    soup = driver.get_soup()
```
## Updating Chromedriver

The `update_drivers.update_driver` function allows you to download and update the chromedriver for different platforms.

### Platforms

The available platforms are:
- `linux64`
- `mac-arm64`
- `mac-x64`
- `win32`
- `win64`

### Example Usage

```python
from update_drivers import update_driver

# Update chromedriver for Windows 64-bit
update_driver('win64')

# Update chromedriver for macOS ARM64
update_driver('mac-arm64')
```

This will download the most recent chromedriver for the specified platform and place it in the directory specified by the `CHROMEDRIVER_PATH` environment variable. If `CHROMEDRIVER_PATH` is not set, it will use the directory of the script.

## Contributing
Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.
