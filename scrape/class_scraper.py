from selenium.webdriver.support.ui import Select        # Easy way to select options from menus on a website
from bs4 import BeautifulSoup                           # Allows data to be extracted from websites
from scrape import web_navigation                       # Provides user-defined functions to navigate the selenium webdriver
from scrape.parse_exceptions import InvalidCourse       # Exceptions while parsing
from scrape.parse_exceptions import InvalidDepartment   # Exceptions while parsing
from scrape.class_parser import scrape_classes          # Functions to scrape classes from UCI departments


def get_classes(path_to_arguments=''):
    """
    A function that web-scrapes using BeautifulSoup and Selenium to collect data on specified classes. This function is passed a *.txt file
    containing the classes to scrape for.

    :param path_to_arguments: A string that is the path to the *.txt file containing information on which classes to scrape for.
    :return: A list of departments (each department contains several courses and each course contains several classes)
    """

    # Class Search URL
    class_search_url = "https://www.reg.uci.edu/perl/WebSoc/"

    driver = web_navigation.open_web_driver()             # Create an instance of a Chrome WebDriver
    driver.get(class_search_url)                          # Open the class schedule

    # Scrape the term name
    select = Select(driver.find_element_by_name("YearTerm"))
    term = " ".join(select.first_selected_option.text.split())

    # Scrape the Department options into a dictionary for later use (validation)
    select = web_navigation.select_department_menu(driver)
    department_options = {}
    options = select.options
    for option in options:
        department_line = option.text.split('.')
        department_name = department_line[len(department_line) - 1].rstrip().lstrip()
        department_code = department_line[0].rstrip().lstrip()
        if department_name != "Include All Departments":        # Don't add the first line to the dictionary (it's useless)
            department_options[department_code] = department_name
    select = None

    departments = None      # List of departments to loop through
    courses = []            # List of courses per department

    try:
        input_file = open(path_to_arguments, 'r')
        input_arguments = []
        for line in input_file.readlines():
            input_arguments.append(line)
        departments = str(input_arguments[0]).strip('\n')                 # List of departments will always be the first line in the *.txt file
        departments = departments.split(",")
        for i in range(1, len(input_arguments)):                          # Each line following contains courses per department
            courses.append(input_arguments[i].strip('\n'))

    except FileNotFoundError:
        departments = input("Enter in the department names (in the form of \"DPT1,DPT2,etc.\" *no spaces*):\n")
        departments = departments.split(",")
        for each_department in departments:
            courses_input = input(
                "Enter in the course names for " + each_department + " (in the form of \"C1,C2,etc.\", e.g. If DEPT is I&C SCI then enter in \"6B, 31\" *spaces*):\n")
            courses.append(courses_input)

    # Change option to only include courses if there is some space
    capacity_menu = driver.find_element_by_name("FullCourses")
    select = Select(capacity_menu)
    select.select_by_value("SkipFullWaitlist")        # Select option to show classes that are full if there is room on the wait list
    #select.select_by_value("FullOnly")
    select = None

    # good_html = css_soup_for_a_department.prettify()
    # print(good_html)

    all_courses = []                    # Keep track of all courses while web-scraping the data
    i = 0                               # Keep track of which courses are with which department

    for department in departments:
        try:
            if department in department_options:                                        # Validation of user-input (file or manually entered)
                select = web_navigation.select_department_menu(driver)
                select.select_by_value(department)
                course_number_box = driver.find_element_by_css_selector("input[name=CourseNum]")
                course_number_box.clear()                                               # Make sure that the text box is clear before entering new courses
                course_number_box.send_keys(courses[i])
                web_navigation.display_web_results(driver)
                bad_html = driver.page_source
                css_soup_for_a_department = BeautifulSoup(bad_html, 'html.parser')
                all_courses.append(scrape_classes(css_soup_for_a_department))           # Call the "scrape_classes" function to scrape data on the classes then append it to the "master list"
                driver.back()
                i += 1                                                                  # Make sure that the correct course is with the correct department
            else:
                raise InvalidDepartment                                                 # Raise an exception to let user know what went wrong if department does not exist (thanks to dictionary)
        except InvalidDepartment:
            print(
                "Invalid department entered: \"" + department + "\", program terminating, refer to the \"departments.txt\" and enter in the correct department code.")
            break
        except InvalidCourse:
            print(
                "Invalid course number entered or is full/unavailable for the \"" + department + "\" department, program terminating, refer to the UCI website and search for the correct course numbers and availability.")
            break

    driver.close()
    return all_courses
