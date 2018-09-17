import re                               # Use Regular Expressions to look for or fix specific string patterns
import department as crs                # A way to organize courses and classes
from scrape import parse_exceptions     # Exceptions when parsing each department for its classes


def scrape_classes(soup_obj):
    """
    Scrape the passed soup object for data contained in html tables.

    :param soup_obj: BeautifulSoup object that has been instantiated using the source html of the url that is to be parsed.
    :return: A list containing all of the courses and their corresponding classes that were scraped.
    :raises course_parse_exceptions.InvalidCourse: An exception that signals no classes were found for this term.
    """

    for divTag in soup_obj.find_all('div', style="color: red; font-weight: bold;"):
        if divTag.text == "\n\tNo courses matched your search criteria for this term.\n\n":
            raise parse_exceptions.InvalidCourse

    type_of_class = section = class_code = units = instructor = days_and_time = place = final = None        # Parameters of a "Class" object
    capacity = enrolled = wait_list = status = None
    courses = []                                                                                            # Courses in the department i.e. ICS 6B or ICS 31
    current_course = None
    counter = 0
    for trTag in soup_obj.find_all('tr', valign='top'):                                                     # On the UCI class search page, records containing class data
        for tdTag in trTag.find_all('td'):                                                                  # have the "valign='top'" attribute to it, so to scrape from
            if len(tdTag.text) > 0:
                piece_of_info = tdTag.text.lstrip().rstrip()
                piece_of_info = re.sub(r'\s+', ' ', piece_of_info)
                if (len(piece_of_info) != 5) and (counter == 0):                                            # Check to see if this is a class code or course title
                    if current_course is not None:                                                          # If the current_course is not None then that means it contains a course
                        courses.append(current_course)
                    current_course = crs.Course(piece_of_info)                                              # Create a new course i.e. after adding ICS 6B now we are working on 31
                    counter -= 1                                                                            # Account for the automatic counter++ at the bottom.
                elif (len(piece_of_info) == 5) and (counter == 0):                                          # If len is 5 and counter is at 0, then this is a course code, then etc. for the following
                    class_code = int(piece_of_info)
                elif counter == 1:
                    type_of_class = piece_of_info
                elif counter == 2:
                    section = piece_of_info
                elif counter == 3:
                    units = int(piece_of_info)
                elif counter == 4:
                    instructor = piece_of_info
                elif counter == 5:
                    days_and_time = piece_of_info
                elif counter == 6:
                    place = piece_of_info
                elif counter == 7:
                    if type_of_class == "Lec":                                                              # Only lecture classes have finals displayed
                        final = piece_of_info
                    else:
                        final = "None"
                elif counter == 8:
                    capacity = piece_of_info
                    if piece_of_info.isdigit():
                        capacity = int(piece_of_info)
                elif counter == 9:
                    enrolled = piece_of_info
                    if piece_of_info.isdigit():
                        enrolled = int(piece_of_info)
                elif counter == 10:
                    wait_list = piece_of_info
                    if piece_of_info.isdigit():
                        wait_list = int(piece_of_info)
                elif counter == 16:
                    status = piece_of_info
            counter += 1

        if counter > 0:                                                                                 # Since counter is greated than 0, then that means that we just gathered data for one class
            days_and_time = parse_day_and_time(days_and_time)                                           # Call the function "parse_day_and_time()" to get a list containing the days and meeting times
            current_class = crs.Class(
                current_course.name_of_course, type_of_class, section, class_code, units, instructor, days_and_time[0],
                days_and_time[1], days_and_time[2], place, final, capacity, enrolled,
                wait_list, status
            )
            current_course.add_class(type_of_class, current_class)
            counter = 0                                                                                 # Reset counter so that it either finds a new type of course, or another class for the same course

    if current_course is not None:                                                                      # Append the last course (that did not make it into the loop)
        courses.append(current_course)

    return courses


def parse_day_and_time(days_and_time):
    """
    This is a helper function to parse the string scraped from the html table. The string is scraped in the form: "MWF   9:00- 9:50"
    and is fixed to be a list in the form of ["MWF", "09:00", "09:50"].

    :param days_and_time: The string containing the days and meeting times before being processed into a list
    :return: A list containing the days and meeting times
    """

    if days_and_time == "TBA":                                                                                  # Sometimes the UCI class schedule is not fully published and they leave the times as "TBA"
        fixed_days_and_time = ['TBA', 'TBA', 'TBA']
        return fixed_days_and_time

    split_up_days_and_time = re.split('\W', days_and_time)                                                      # Use regular expressions to split the string and filter it
    almost_fixed_days_and_time = list(filter(None, split_up_days_and_time))                                     # Further filtering to remove "blank" strings, after this process it will be almost in the ideal
                                                                                                                # list except that the hours and minutes are split up

    # Pad AM integers that are less than 10 with a "0" and add 12 hours to PM hours
    if 'p' in str(almost_fixed_days_and_time[4]):
        if int(almost_fixed_days_and_time[3]) != 12 and int(almost_fixed_days_and_time[1]) < 10:
            almost_fixed_days_and_time[1] = str(int(almost_fixed_days_and_time[1]) + 12)
            almost_fixed_days_and_time[3] = str(int(almost_fixed_days_and_time[3]) + 12)

        if int(almost_fixed_days_and_time[1]) == 12 and int(almost_fixed_days_and_time[3]) < 12:
            almost_fixed_days_and_time[3] = str(int(almost_fixed_days_and_time[3]) + 12)

    elif int(almost_fixed_days_and_time[1]) < 10:
        almost_fixed_days_and_time[1] = "0" + almost_fixed_days_and_time[1]
        almost_fixed_days_and_time[3] = "0" + almost_fixed_days_and_time[3]

    start_time = str(almost_fixed_days_and_time[1]) + ":" + str(almost_fixed_days_and_time[2])                  # Turn the time into a readable string (Hours:Minutes)
    end_time = str(almost_fixed_days_and_time[3]) + ":" + str(almost_fixed_days_and_time[4]).replace("p", "")
    fixed_days_and_time = [almost_fixed_days_and_time[0], start_time, end_time]

    return fixed_days_and_time
