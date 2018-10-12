import numpy as np                                              # For more statistical functions
from operator import attrgetter as atg                          # A way to sort custom objects
from genetic_algorithm import schedule as sch                   # Manage 'individuals" (schedules)
from genetic_algorithm.class_schedule_solver import is_between  # Function to check if classes conflict


class Evolution:
    """
    The Evolution class is a way to manage the different steps needed in the genetic algorithm (for classes). It offers different functions to
    get 'populations', select 'parents' and create 'children'.

    Attributes:
        population_size (integer): This is the population size per generation.
        course_list (list): A list holding all of the different courses.
        class_list (list): A list holding all of the different classes.
        dict_for_class_to_course (dictionary): This links different Class objects to Course objects efficiently [dictionary of Classes objects (keys) and Course objects (values)].
        number_of_classes_required_total (integer): A number that specifies how many classes a schedule needs to have all enrollment requirements fulfilled.
    """

    def __init__(self, courses_per_department, population_size=500):
        """
        A constructor for an 'Evolution' class object. The constructor creates and saves general information needed to 'evolve' a population efficiently.

        :param courses_per_department: A list of Course objects that were web-scraped.
        :param population_size: An integer that can be changed, but is default to be a population size of 500 individuals.
        """

        self.population_size = population_size
        self.course_list = []
        self.class_list = []
        self.dict_for_class_to_course = {}
        self.number_of_classes_required_total = 0
        for department in courses_per_department:
            for course in department:
                self.course_list.append(course)                                                     # Save the different types of courses
                self.number_of_classes_required_total += course.get_number_of_required_classes()    # Count how many classes are required to completely enroll in that course
                for _class in course.get_all_classes():
                    self.class_list.append(_class)                                                  # Save the different classes open for that course
                    self.dict_for_class_to_course[_class] = course                                  # Link the class to a course

    def get_starting_population(self):
        """
        This is a function to randomly create and return a starting population based on the classes found in 'self.class_list' and 'self.population_size'.

        :return: A list of 'Schedule' objects that contain classes but no fitness score or marked list.
        """
        population = []
        for x in range(self.population_size):
            individual = []
            for y in range(self.number_of_classes_required_total):
                index = np.random.randint(0, len(self.class_list) - 1)
                individual.append(self.class_list[index])
            population.append(sch.Schedule(individual))                 # Append 'Schedule' objects to the population
        return population

    def rank_fitness(self, schedule):
        """
        IN PROGRESS
        :param schedule:
        :return:
        """

        class_list = schedule.get_class_list()
        fitness_score = 0.0
        marked_list = [False] * len(class_list)

        for _class in class_list:
            course_name = _class.get_name_of_course()
            lab_fulfillment = False
            discussion_fulfillment = False
            lecture_fulfillment = False
            course = self.dict_for_class_to_course[_class]
            counter = 0
            for _class_again in class_list:

                if _class != _class_again:  # check time conflictions
                    if is_between(_class, _class_again):
                        fitness_score -= 1

                if course_name == _class_again.get_name_of_course():  # if same name
                    class_type = _class_again.get_type()
                    if course.has_lab() and class_type == 'Lab':  # if same type
                        if not lab_fulfillment:
                            lab_fulfillment = True
                            fitness_score += 1
                        else:
                            marked_list[counter] = True
                            fitness_score -= 1
                    elif course.has_discussion() and class_type == 'Dis':
                        if not discussion_fulfillment:
                            discussion_fulfillment = True
                            fitness_score += 1
                        else:
                            marked_list[counter] = True
                            fitness_score -= 1
                    elif class_type == 'Lec':
                        if not lecture_fulfillment:
                            marked_list[counter] = True
                            lecture_fulfillment = True
                            fitness_score += 1
                        else:
                            marked_list[counter] = True
                            fitness_score -= 1
                counter += 1

        schedule.set_fitness_score(fitness_score)
        schedule.set_marked_list(marked_list)

    @staticmethod
    def select_parents(population, retain_rate=0.3, randomly_retain=0.03):
        """
        This function selects parents (most fit schedules) out of the current population of 'Schedule' objects that have fitness scores.

        :param population: The list of Schedule objects with fitness scores.
        :param retain_rate: The percentage of top-tier schedules to keep.
        :param randomly_retain: The probability of low-tier schedules to keep.
        :return: A list of Schedule objects that represent the most fit of the population and some unfit parents.
        """

        sorted_population_by_fitness = sorted(population, key=atg('fitness_score'), reverse=True)
        retain_length = retain_rate * len(sorted_population_by_fitness)
        fittest = sorted_population_by_fitness[:int(retain_length)]
        unfit_parents = sorted_population_by_fitness[int(retain_length):]
        lucky_parents = []
        for unfit_schedule in unfit_parents:
            if randomly_retain > np.random.rand():
                lucky_parents.append(unfit_schedule)
        parents = fittest + lucky_parents
        return parents

    def get_next_generation(self, selected_parents, randomly_retain=0.03):
        """
        IN PROGRESS
        :param selected_parents:
        :param randomly_retain:
        :return:
        """

        children = []
        target_size = self.population_size - len(selected_parents)

        if len(selected_parents) > 0:
            while len(children) < target_size:
                father = np.random.choice(selected_parents)
                mother = np.random.choice(selected_parents)
                if father != mother:
                    child = []
                    i = 0
                    while i < self.number_of_classes_required_total:
                        random_index_father = np.random.randint(self.number_of_classes_required_total)
                        random_index_mother = np.random.randint(self.number_of_classes_required_total)

                        marked_father = father.get_marked_list()[random_index_father]
                        marked_mother = mother.get_marked_list()[random_index_mother]

                        father_gene = father.get_class_list()[random_index_father]
                        mother_gene = mother.get_class_list()[random_index_mother]

                        if marked_father and (np.random.rand() > randomly_retain):
                            random_index_father = np.random.randint(len(self.class_list) - 1)
                            father_gene = self.class_list[random_index_father]

                        if marked_mother and (np.random.rand() > randomly_retain):
                            random_index_mother = np.random.randint(len(self.class_list) - 1)
                            mother_gene = self.class_list[random_index_mother]

                        child.append(father_gene)
                        i += 1
                        if i < self.number_of_classes_required_total:
                            child.append(mother_gene)
                            i += 1
                    children.append(sch.Schedule(child))

        for schedule in selected_parents:
            schedule.reset_marks()

        next_population = children + selected_parents
        return next_population

    def satisfied_requirements(self, schedule):
        """
        IN PROGRESS
        :param schedule:
        :return:
        """

        class_list = schedule.get_class_list()
        courses_fulfilled = {}

        for course in class_list:
            if course.get_name_of_course not in courses_fulfilled.keys():
                courses_fulfilled[course.get_name_of_course] = False

        for _class in class_list:
            course_name = _class.get_name_of_course()
            lab_fulfillment = False
            discussion_fulfillment = False
            lecture_fulfillment = False
            number_of_classes_for_course = 0
            course = self.dict_for_class_to_course[_class]

            for _class_again in class_list:
                if course_name == _class_again.get_name_of_course():
                    class_type = _class_again.get_type()
                    if course.has_lab() and class_type == 'Lab':
                        if not lab_fulfillment:
                            lab_fulfillment = True
                            number_of_classes_for_course += 1
                    elif course.has_discussion() and class_type == 'Dis':
                        if not discussion_fulfillment:
                            discussion_fulfillment = True
                            number_of_classes_for_course += 1
                    elif class_type == 'Lec' and not lecture_fulfillment:
                        lecture_fulfillment = True
                        number_of_classes_for_course += 1

            if number_of_classes_for_course == self.number_of_classes_required_total:
                courses_fulfilled[course_name] = True

        so_far_true = True
        for value in courses_fulfilled.values():
            if value is False:
                so_far_true = False
        return so_far_true
