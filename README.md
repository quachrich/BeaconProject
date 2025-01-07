# EasySelenium
# Table of Contents
1. [Overview](#overview)
2. [Directory Structure](#directory-structure)
3. [Usage](#usage)
4. [Configuration](#configuration)
    1. [Setting up the `.env` file](#setting-up-the-env-file)
    2. [Configuring a virutal environment](#setting-up-a-virtual-environment)
5. [Contributing](#contributing)
6. [Contact](#contact)

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

## Usage
To easily download all repo code onto your local machine use:
```git
git clone https://github.com/JoeyRussoniello/RedTailCodeBase
cd RedTailCodeBase
```
Code will not run out-of-the-box unless the dependencies have all been successfully installed. See [Virutal Environment Setup Instructions](#setting-up-a-virtual-environment) for details


#### **NOTE: All webscrapers were developed on a windows OS, and some have `\\` style paths left in the code. These are being gradually replaced with safer os.path.joins, but at the moment, some webscrapers may not function out-of-box on UNIX systems**

## Configuration

### Setting Up the `.env` File

To configure the project, you need to create a `.env` file in the root directory of the project. This file will store environment-specific variables such as paths and credentials. 

**Important:** Do not commit your `.env` file to the repository. It should be included in your `.gitignore` file to keep sensitive information secure.

#### Example `.env` File

Here is an example of what your `.env` file should look like:

```properties
CHROMEDRIVER_PATH=C:\path\to\your\chromedriver
```
With an updating path to your chromedriver instead of the placeholder variable. \
*Note that including chromedriver.exe at the end of the CHROMEDRIVER_PATH variable is not neccesary*

#### Ignoring `.env` with git
Make sure your `.env` file is listed in a `.gitignore` file to prevent it from being committed to the repository. Your `.gitignore` file should include
```properties
.env
.gitignore
.venv/
```
As well as any large output csv files to avoid overpacking the repository.

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

## Contributing
Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## Contact
For any questions or inquiries, please contact the project maintainer at [jrussoniello@highwaywest.com](mailto:jrussoniello@highwaywest.com).
