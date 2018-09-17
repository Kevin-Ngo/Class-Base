import bisect


class Course:
    """
    This is a class to hold a course title and its current open classes.

    Attributes:
        name_of_course (string): The name of the course.
        lecture_classes (list of Class objects): The list containing open lecture classes in the named course.
        discussion_classes (list of Class objects): The list containing open discussion classes in the named course.
        lab_classes (list of Class objects): The list containing open lab classes in the named course.
        discussions (Boolean value): True if this course contains discussion classes, else is false.
        labs (Boolean value): True if this course contains lab classes, else is false.
    """

    def __init__(self, name_of_course):
        """
        The constructor for the Course class.

        :param name_of_course: A string that is the name of the course.
        :return: Nothing.
        """

        self.name_of_course = name_of_course
        self.lecture_classes = []
        self.discussion_classes = []
        self.lab_classes = []
        self.discussions = False
        self.labs = False

    def get_lecture_classes(self):
        """
        A get function to return a copy of the list containing lecture classes.

        :return: A copy of the list of discussion classes.
        """

        return self.lecture_classes.copy()

    def get_discussion_classes(self):
        """
        A get function to return a copy of the list containing discussion classes.

        :return: A copy of the list of discussion classes.
        """

        return self.discussion_classes.copy()

    def get_lab_classes(self):
        """
        A get function to return a copy of the list containing lab classes.

        :return: A copy of the list of discussion classes.
        """

        return self.lab_classes.copy()

    def has_discussion(self):
        """
        A function that returns true if this course has discussion classes.

        :return: A boolean value, True if this course has discussion classes.
        """

        return self.discussions

    def has_lab(self):
        """
        A function that returns true if this course has lab classes.

        :return: A boolean value, True if this course has lab classes.
        """

        return self.labs

    def add_class(self, type_of_class, new_class):
        """
        A function to append a new class to the "classes" list.

        :param type_of_class: A string that describes the type of class being added, it can be either 'Lec', 'Dis', or 'Lab'
        :param new_class: A Class object that is to be added to the classes list.
        :return: Nothing.
        """

        if type_of_class == 'Lec':
            bisect.insort_left(self.lecture_classes, new_class)
        elif type_of_class == 'Dis':
            self.discussions = True
            bisect.insort_left(self.discussion_classes, new_class)
        else:
            self.labs = True
            bisect.insort_left(self.lab_classes, new_class)

    def __repr__(self):
        return "Name of course: " + self.name_of_course + "\n"


class Class:
    """
    This is a class to hold the data of an open class.

    Attributes:
        type_of_class (string): A string that represents the type of class that this is ('Lab', 'Lecture' or 'Discussion').
        name_of_course (string): The name of the course.
        section (string): A string that represents the Section number or letter identifier for an individual class.
        code (int): An integer that represents the class code.
        units (int): An integer that is the units of the class.
        instructor (string): A string that is the full name of the instructor.
        days (list of strings): A list of strings containing the days that the class meets.
        start (int): An integer that is the start time of the class (military time).
        end (int): An integer that is the end time of the class (military time).
        place (string): A string containing the location of the class.
        final (string): A string containing the finals day/date/time for the class.
        capacity (int): An integer that represents the maximum number of enrolled students allowed in the class.
        enrolled (int): An integer that represents the current number of enrolled students in the class.
        wait_list (int): An integer representing the number of people on the wait list for a class.
        status (string): A string that represents the status of the class ('Open' or 'New Only')
        percent_full (float): A float that represents the percentage full a class is, if over 80% full, will mark the
         class as nearly full.
    """

    def __init__(self, name_of_course,
                 type_of_class, section, code,
                 units, instructor, days, start, end,
                 place, final, capacity,
                 enrolled, wait_list, status):
        """
        A constructor for the Class class.
        """

        self.name_of_course = name_of_course
        self.type_of_class = type_of_class
        self.section = section
        self.code = code
        self.units = units
        self.instructor = instructor
        self.days = days
        self.start = start
        self.end = end
        self.place = place
        self.final = final
        self.capacity = capacity
        self.enrolled = enrolled
        self.wait_list = wait_list
        self.status = status
        self.percent_full = float(enrolled) / capacity

    def __lt__(self, other):
        return self.end < other.end

    def __repr__(self):
        return "Name of course: " + self.name_of_course + "\n"\
                "Type of class: " + self.type_of_class + "\n"\
                "Section: " + self.section + "\n "\
                "Class code: " + self.code + "\n"\
                "Units: " + self.units + "\n"\
                "Instructor: " + self.instructor + "\n"\
                "Class meeting times: " + self.days + self.start + " - " + self.end + "\n"\
                "Classroom: " + self.place + "\n"\
                "Final: " + self.final + "\n"\
                "Capacity: " + self.capacity + "\n"\
                "Enrolled: " + self.enrolled + "\n"\
                "Wait list: " + self.wait_list + "\n"\
                "Status: " + self.status + "\n"\
                "Percent full: " + self.percent_full + "\n"
