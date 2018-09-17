from selenium import webdriver                          # Allows access/navigation to websites that use JavaScript links
from selenium.webdriver.support.ui import Select        # Easy way to select options from menus on a website
from bs4 import BeautifulSoup                           # Allows data to be extracted from websites
from scrape import web_navigation

def get_rating(name):
    rate_my_professors_url = 'www.ratemyprofessors.com'
    driver = web_navigation.open_web_driver()

