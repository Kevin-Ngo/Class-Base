from selenium import webdriver                          # Allows access/navigation to websites that use JavaScript links
from selenium.webdriver.support.ui import Select        # Easy way to select options from menus on a website
import os                                               # Provides a way to use operating system dependent functions
import platform as plat                                 # A way to grab information about the system
from os import chmod                                    # Change file permissions the first time


def open_web_driver():
    """
    A function that checks the system for which OS it is being run from, then chooses the correct selenium driver to open.

    :return: None
    """

    # Configure which system (Windows or Mac) then choose the correct driver
    driver_path = os.getcwd()    # Get root directory (location of the web_drivers)
    op_system = plat.platform()  # Get the type of system
    if "Windows" in op_system:
        driver_path += "\web_drivers\chromedriver.exe"
    else:
        driver_path += "/web_drivers/chromedriver"
        os.chmod(driver_path, 509)
    print(driver_path)
    return webdriver.Chrome(driver_path)  # Create an instance of a Chrome WebDriver


def select_department_menu(driver):
    """
    A function to return a Select object that has the Dept. drop down menu selected.

    :return: A Select object that has selected the drop down menu for departments.
    """

    department_menu = driver.find_element_by_name("Dept")
    return Select(department_menu)


def display_web_results(driver):
    """
    Use Selenium to click the button "Display Web Results" to .... display classes ...

    :return: Nothing
    """

    driver.find_element_by_css_selector("input[value='Display Web Results']").click()
