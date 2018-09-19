import bisect


class Course:
    """
    This is a class to hold a course title, its current open classes and other attributes pertaining to a course.

    Attributes:
        name_of_course (string): The name of the course.
        lecture_classes (list of Class objects): The list containing open lecture classes in the named course.
        discussion_classes (list of Class objects): The list containing open discussion classes in the named course.
        lab_classes (list of Class objects): The list containing open lab classes in the named course.
        discussions (Boolean value): True if this course contains discussion classes, else is false.
        labs (Boolean value): True if this course contains lab classes, else is false.
        need_both (Boolean value): True is a course requires both lab and discussion.
        number_of_choices (integer): Contains the number of choices for a given type of class (e.g. if a course has 10 lectures open but only 1 lab open, then number of choices would be 1)
        number_of_choices_for_lecture (integer): Number of lecture classes available.
        number_of_choices_for_discussion (integer): Number of discussion classes available.
        number_of_choices_for_lab (integer): Number of lab classes available.
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
        self.need_both = False
        self.number_of_choices = 100                    # Initialized to a large number so that the lowest will be assigned to it later (see add_class)
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

        :param type_of_class: A string that describes the type of class being added, it can be either 'Lec', 'Dis', or 'Lab'
        :param new_class: A Class object that is to be added to the classes list.
        :return: Nothing.
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
        A function to return the type of class with the least amount of choices (i.e. priotitized in scheduling precedence).

        :return: A list of the classes with the least amount of choices, as well as it's type.
        """

        if self.number_of_choices == self.number_of_choices_for_lab:
            return self.lab_classes.copy(), 'Lab'
        elif self.number_of_choices == self.number_of_choices_for_discussion:
            return self.discussion_classes.copy(), 'Dis'
        else:
            return self.lecture_classes.copy(), 'Lec'

    def get_compliment_classes(self, class_type):
        """
        This function returns other classes that are required, given a class type. (i.e. If this course requires both a lab and discussion in addition to a lecture, when passed
        'Lec', it will return both of the lists

        :return: A list of complimentary-required classes, which can either be one list or two lists.
        If the class type is 'Lec' then it will return either a lab or discussion, or both (Lab, Discussion).
        If the class type is 'Dis' then it will return either a lecture or both (Lecture, Lab).
        If the class type is 'Lab' then it will return either a lecture or both (Lecture, Discussion).
        """

        if class_type == 'Lec':
            if self.need_both:
                return self.lab_classes.copy(), self.discussion_classes.copy()
            elif self.discussions:
                return self.discussion_classes.copy()
            elif self.labs:
                return self.lab_classes.copy()
        elif class_type == 'Dis':
            if self.need_both:
                return self.lecture_classes.copy(), self.lab_classes.copy()
            else:
                return self.lecture_classes.copy()
        else:
            if self.need_both():
                return self.lecture_classes.copy(), self.discussion_classes.copy()
            else:
                return self.lecture_classes.copy()

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
