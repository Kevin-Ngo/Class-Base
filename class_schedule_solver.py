from operator import attrgetter     # Sorting with custom objects (class objects)
from openpyxl import load_workbook  # Output schedules to an Excel sheet


class Schedules:
    """
    This class, "Schedules", is a class that creates working schedules for university classes that it is passed.

    Attributes:
        term (string): This is the specific term that the schedule is being made for.
        open_courses (list of departments): The list of departments, i.e. each department has several courses and those courses have several classes.
        workbook_for_classes (openpyxl workbook): This is a workbook that holds the schedule for the classes.
        workbook_for_finals (openpyxl workbook): This is a workdbook that holds the schedule for the finals for the classes.
        class_list_for_classes (openpyxl sheet): This is a sheet that is written to when creating the class schedule.
        class_list_for_finals (openpyxl sheet): This is a sheet that is written to when creating the finals schedule for the classes.
        days (dict): This is a dictionary that is used for quick access to full-day-names given their short abbreviations.

    """

    def __init__(self, term, open_courses):
        """
        The constructor for the Schedules class.

        :param term: A string containing the term of the classes that were scraped (e.g. Fall 2018).
        :param open_courses: A list of departments (all of the classes that were scraped).
        :return: Nothing.
        """

        self.term = term
        self.open_courses = open_courses
        self.workbook_for_classes = load_workbook('Schedule_Template.xlsx')
        self.workbook_for_finals = load_workbook('Schedule_Template.xlsx')
        self.class_list_for_classes = self.workbook_for_classes['Class List']
        self.class_list_for_finals = self.workbook_for_finals['Class List']
        self.days = {
            'M': 'MONDAY',
            'Tu': 'TUESDAY',
            'W': 'WEDNESDAY',
            'Th': 'THURSDAY',
            'F': 'FRIDAY',
            'Mon': 'MONDAY',
            'Tue': 'TUESDAY',
            'Wed': 'WEDNESDAY',
            'Thu': 'THURSDAY',
            'Fri': 'FRIDAY'
        }

    def make_early_schedule(self):
        """
        This function creates a schedule that prioritizes early classes and also writes this schedule to an Excel class schedule template.

        :return: None
        """

        almost_sorted_courses = []

        for department in self.open_courses:
            for course in department:
                almost_sorted_courses.append(course)

        sorted_courses = sorted(almost_sorted_courses, key=attrgetter('number_of_choices'))          # Sort the courses based on how many choices they have for classes (i.e. more choices are less prioritized)

    def __del__(self):
        """
        In the destructor for the Schedules class, the workbooks (Excel sheets) are saved as the file names "Class Schedule - 'TERM'.xlsx" and "Finals Schedule - 'TERM'.xlsx".

        :return: None
        """

        self.workbook_for_classes.save('Class Schedule - ' + self.term + ".xlsx")
        self.workbook_for_finals.save('Finals Schedule - ' + self.term + ".xlsx")
