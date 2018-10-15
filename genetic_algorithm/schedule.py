class Schedule:
    """
    The Schedule class is a class to just hold information pertaining to an 'individual' in a 'population' of other Schedules.

    Attributes:
        class_list (list): A list of Class objects that represent a "schedule".
        marked_list (list): A boolean list that represents (at indices) which classes should be replaced due to conflictions.
        fitness_score (float): A floating point value that represents the fitness of the "schedule".
    """

    def __init__(self, class_list, marked_list=None, fitness_score=None):
        """
        A constructor for a "Schedule" object. This requires a list of Class objects and occasionally a boolean list or fitness score for the "schedule".

        :param class_list: A list of "Class" objects.
        :param marked_list: A list of boolean values that represent (at indices) which classes should be removed.
        :param fitness_score: A floating point value that represents the fitness of the "schedule".
        """

        self.class_list = class_list
        self.marked_list = marked_list
        self.fitness_score = fitness_score

    def get_class_list(self):
        """
        A get-function for the list of Class objects.

        :return: A copy of the list of Class objects.
        """

        return self.class_list.copy()

    def reset_marks(self):
        """
        Resets the marked_list, a boolean list, to be all False.

        :return: Nothing
        """

        for mark in self.marked_list:
            mark = False

    def get_marked_list(self):
        """
        A get-function for the list of boolean values, the 'marked_list'.

        :return: A list of boolean values (marked_list).
        """

        return self.marked_list

    def set_fitness_score(self, fitness_score):
        """
        A set-function for fitness scores of the Schedule object.

        :param fitness_score: A floating point value representing the fitness score of the Schedule.
        :return: Nothing
        """

        self.fitness_score = fitness_score

    def set_marked_list(self, marked_list):
        """
        A set-function for the marked_list, a list of Boolean values.

        :param marked_list: A boolean list.
        :return: Nothing
        """

        self.marked_list = marked_list

    def get_indices_of_marked(self):
        if len(self.marked_list) > 0:
            index = 0
            index_list = []
            for mark in self.marked_list:
                if mark is True:
                    index_list.append(index)
                index += 1
