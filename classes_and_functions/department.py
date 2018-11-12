import bisect           # A way to easily keep custom objects sorted
import re               # Use of regular expressions


class Course:
    """
    This is a class to hold a course title, its current open classes and other attributes pertaining to a course.

    Attributes:
        name_of_course (string): The name of the course.
        lecture_classes (list): The list of Class objects containing open lecture classes in the named course.
        discussion_classes (list): The list of Class objects containing open discussion classes in the named course.
        lab_classes (list): The list of Class objects containing open lab classes in the named course.
        discussions (boolean): True if this course contains discussion classes, else is false.
        labs (boolean): True if this course contains lab classes, else is false.
        need_both (boolean): True is a course requires both lab and discussion.
        number_of_choices (integer): Contains the number of choices for a given type of class (e.g. if a course has 10 lectures open but only 1 lab open, then number of choices would be 1)
        number_of_choices_for_lecture (integer): Number of lecture classes available.
        number_of_choices_for_discussion (integer): Number of discussion classes available.
        number_of_choices_for_lab (integer): Number of lab classes available.
    """

    def __init__(self, name_of_course):
        """
        The constructor for the Course class.

        :param name_of_course: A string that is the name of the course.
        :return: Nothing
        """

        self.full_name_of_course = name_of_course
        self.lecture_classes = []
        self.discussion_classes = []
        self.lab_classes = []
        self.discussions = False
        self.labs = False
        self.need_both = False
        self.number_of_choices = 100
        self.number_of_choices_for_lecture = 0
        self.number_of_choices_for_discussion = 0
        self.number_of_choices_for_lab = 0

    def get_lecture_classes(self):
        """
        A get function to return a copy of the list containing lecture classes.

        :return: A copy of the list of discussion classes.
        """

        return self.lecture_classes.copy()

    def get_number_of_lecture_classes(self):
        """
        Returns the number of lecture classes.

        :return: The number of lecture classes.
        """

        return len(self.lecture_classes)

    def get_discussion_classes(self):
        """
        A get function to return a copy of the list containing discussion classes.

        :return: A copy of the list of discussion classes.
        """

        return self.discussion_classes.copy()

    def get_number_of_discussion_classes(self):
        """
        A get function to return the number of discussion classes.

        :return: The number of discussion classes.
        """

        return len(self.discussion_classes)

    def get_lab_classes(self):
        """
        A get function to return a copy of the list containing lab classes.

        :return: A copy of the list of discussion classes.
        """

        return self.lab_classes.copy()

    def get_number_of_lab_classes(self):
        """
        A function to return the number of lab classes.

        :return: The number of lab classes.
        """

        return len(self.lab_classes)

    def get_name_of_course(self):
        """
        A function to get the name of the course.

        :return: A String that is the name of the course.
        """

        return self.full_name_of_course

    def get_all_classes(self):
        """
        A function to return all of the classes for the course.

        :return: A list of classes.
        """

        combined_classes = []
        for _class in self.lab_classes:
            combined_classes.append(_class)
        for _class in self.discussion_classes:
            combined_classes.append(_class)
        for _class in self.lecture_classes:
            combined_classes.append(_class)
        return combined_classes

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

    def need_both(self):
        """
        A function that returns true if a course requires both Lab and Discussion.

        :return: A boolean value, True if a course requires both Lab and Discussion.
        """

        return self.need_both

    def add_class(self, type_of_class, new_class):
        """
        A function to append a new class to the "classes" list.

        :param type_of_class: A string that describes the type of class being added, it can be either 'Lec', 'Dis', or 'Lab'.
        :param new_class: A Class object that is to be added to the classes list.
        :return: Nothing
        """

        if type_of_class == 'Lec':
            bisect.insort_left(self.lecture_classes, new_class)
            self.number_of_choices_for_lecture += 1
            if self.number_of_choices_for_lecture <= self.number_of_choices:
                self.number_of_choices = self.number_of_choices_for_lecture
        elif type_of_class == 'Dis':
            self.discussions = True
            bisect.insort_left(self.discussion_classes, new_class)
            self.number_of_choices_for_discussion += 1
            if self.number_of_choices_for_discussion <= self.number_of_choices:
                self.number_of_choices = self.number_of_choices_for_discussion
        else:
            self.labs = True
            bisect.insort_left(self.lab_classes, new_class)
            self.number_of_choices_for_lab += 1
            if self.number_of_choices_for_lab <= self.number_of_choices:
                self.number_of_choices = self.number_of_choices_for_lab
        if (self.labs is True) and (self.discussions is True):
            self.need_both = True

    def get_type_with_least_choices(self):
        """
        A function to return the type of class with the least amount of choices (i.e. prioritized in scheduling precedence).

        :return: A list of the classes with the least amount of choices, as well as it's type.
        """

        if self.number_of_choices == self.number_of_choices_for_lab:
            return self.lab_classes.copy(), 'Lab'
        elif self.number_of_choices == self.number_of_choices_for_discussion:
            return self.discussion_classes.copy(), 'Dis'
        else:
            return self.lecture_classes.copy(), 'Lec'

    def get_number_of_required_classes(self):
        """
        A function that returns the number of required classes for the course. (i.e. If it needs a discussion or lab in addition to the lecture or both).

        :return: An integer that represents how many classes are required to successfully enroll into the class.
        """

        if self.need_both:
            return 3
        else:
            return 2

    def __repr__(self):
        return "Name of course: " + self.full_name_of_course + "\n"


class Class:
    """
    This is a class to hold the data of an open class.

    Attributes:
        type_of_class (string): A string that represents the type of class that this is ('Lab', 'Lecture' or 'Discussion').
        name_of_course (string): The name of the course.
        section (string): A string that represents the Section number or letter identifier for an individual class.
        code (integer): An integer that represents the class code.
        units (integer): An integer that is the units of the class.
        instructor (string): A string that is the full name of the instructor.
        days (list): A list of strings containing the days that the class meets.
        start (string): An string that is the start time of the class (military time).
        end (string): An string that is the end time of the class (military time).
        place (string): A string containing the location of the class.
        final (string): A string containing the finals day/date/time for the class.
        capacity (integer): An integer that represents the maximum number of enrolled students allowed in the class.
        enrolled (integer): An integer that represents the current number of enrolled students in the class.
        wait_list (integer): An integer representing the number of people on the wait list for a class.
        status (string): A string that represents the status of the class ('Open' or 'New Only').
        percent_full (float): A float that represents the percentage full a class is, if over 80% full, will mark the
         class as nearly full.
        normal_time_start (string): A string representing the starting time in standard time.
        noormal_time_end (string): A string representing the ending time in standard time.
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
        self.normal_time_start = None
        self.normal_time_end = None
        try:
            self.percent_full = float(enrolled) / capacity
        except ZeroDivisionError:
            print("Class " + str(self.code) + " (" + self.name_of_course + ")" + " is unavailable.")
            self.percent_full = 1

    def get_name_of_course(self):
        """
        A function that returns the name of the course.

        :return: A string that is the name of the course.
        """

        return self.name_of_course

    def get_days(self):
        """
        A function to return the days the class meets.

        :return: A string that is the days the class meets.
        """

        return self.days

    def get_type(self):
        """
        A function that returns the type of class that the object is. (i.e. Lab, Lecture or Discussion).

        :return: A string that is either "Lec", "Lab" or "Dis".
        """

        return self.type_of_class

    def get_time(self):
        """
        A function that returns two strings that respectively represent the starting and ending time of the class.

        :return: Two separate strings containing start and end times in the format HH:MM.
        """

        return self.start, self.end

    def update_time_to_normal_format(self):
        """
        This function initializes attributes inside the main class, to also hold time in standard time rather than military time.

        :return: None
        """

        if self.start == 'TBA':
            self.normal_time_start = self.normal_time_end = 'TBA'
        else:
            normal_time = None
            pm = False
            temp_time = self.start.split(':')
            temp_time[0] = int(temp_time[0])
            if temp_time[0] > 12:
                pm = True
                temp_time[0] -= 12
            normal_time = str(temp_time[0]) + ':' + temp_time[1]
            if pm or temp_time[0] == 12:
                normal_time += ' PM'
            else:
                normal_time += ' AM'
            self.normal_time_start = normal_time

            normal_time = None
            pm = False
            temp_time = self.end.split(':')
            temp_time[0] = int(temp_time[0])
            if temp_time[0] > 12:
                pm = True
                temp_time[0] -= 12
            normal_time = str(temp_time[0]) + ':' + temp_time[1]
            if pm or temp_time[0] == 12:
                normal_time += ' PM'
            else:
                normal_time += ' AM'
            self.normal_time_end = normal_time

    def get_days_as_list(self):
        """
        Uses regular expressions to split days up by first seen uppercase, e.g. TuTh = ['Tu', 'Th'].

        :return: A list of days that are split up by uppercase letters.
        """

        return re.findall('[A-Z][^A-Z]*', self.days)

    def __lt__(self, other):
        """
        A way to compare objects.

        :param other: Another Class object.
        :return: A string of the smaller end time.
        """
        return self.end < other.end

    def __repr__(self):
        """
        A way to print details of a Class object.

        :return: A string of information pertaining to the Class object.
        """
        return "Name of course: " + self.name_of_course + "\n"\
                "Type of class: " + self.type_of_class + "\n"\
                "Section: " + self.section + "\n "\
                "Class code: " + str(self.code) + "\n"\
                "Units: " + self.units + "\n"\
                "Instructor: " + self.instructor + "\n"\
                "Class meeting times: " + self.days + self.start + " - " + self.end + "\n"\
                "Classroom: " + self.place + "\n"\
                "Final: " + self.final + "\n"\
                "Capacity: " + self.capacity + "\n"\
                "Enrolled: " + self.enrolled + "\n"\
                "Wait list: " + self.wait_list + "\n"\
                "Status: " + self.status + "\n"\
                "Percent full: " + str(self.percent_full) + "\n"
