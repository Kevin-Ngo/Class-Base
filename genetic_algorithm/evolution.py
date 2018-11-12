import numpy as np                                              # For more statistical functions
from operator import attrgetter as atg                          # A way to sort custom objects
from classes_and_functions import schedule as sch


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
                self.course_list.append(course)                                                                 # Save the different types of courses
                self.number_of_classes_required_total += course.get_number_of_required_classes()                # Count how many classes are required to completely enroll in that course
                for _class in course.get_all_classes():
                    self.class_list.append(_class)                                                              # Save the different classes open for that course
                    self.dict_for_class_to_course[_class] = course                                              # Link the class to a course

    def get_starting_population(self):
        """
        This is a function to randomly create and return a starting population based on the classes found in 'self.class_list' and 'self.population_size'.

        :return: A list of 'Schedule' objects that contain classes but no fitness score or marked list.
        """
        population = []
        for x in range(self.population_size):                                                                   # Do this N times where N = desired size of population
            individual = []
            for course in self.course_list:
                lecture_list = course.get_lecture_classes()
                discussion_list = course.get_discussion_classes()
                lab_list = course.get_lab_classes()
                if len(lecture_list) > 0:                                                                       # Randomly select a lecture class from the course to add to the schedule
                    index = np.random.randint(0, len(lecture_list))
                    individual.append(lecture_list[index])
                if len(discussion_list) > 0:                                                                    # Randomly select a discussion class from the course to add to the schedule
                    index = np.random.randint(0, len(discussion_list))
                    individual.append(discussion_list[index])
                if len(lab_list) > 0:                                                                           # Randomly select a lab class from the course to add to the schedule
                    index = np.random.randint(0, len(lab_list))
                    individual.append(lab_list[index])
            population.append(sch.Schedule(individual))                                                         # Append 'Schedule' objects to the population
        return population                                                                                       # Return the starting population that was generated randomly

    def rank_fitness(self, schedule):
        """
        This function looks at a schedule and ranks it based on if there are time varying conflictions between classes. i.e. If a class has many conflictions, it will be ranked fairly low
        so that when the genetic algorithm selects the best parents, this will have a lower chance of being selected to "pass its genes" a.k.a classes.

        :param schedule: A list of class objects that collectively represent a schedule.
        :return: None
        """

        from genetic_algorithm.class_schedule_solver import is_between                                          # Function to check if classes conflict - late import to prevent circular importing
        class_list = schedule.get_class_list()
        fitness_score = 0.0
        already_checked = {}
        for _class in class_list:
            for _class_again in class_list:
                if _class is _class_again:
                    continue
                if (_class is not _class_again) and is_between(_class, _class_again):                           # Check time conflictions, if it does then PUNISH the individual
                    fitness_score -= 1
                else:                                                                                           # No time conflictions give individuals bonus points
                    fitness_score += 1
        fitness_score = float(fitness_score)/self.number_of_classes_required_total
        schedule.set_fitness_score(fitness_score)

    @staticmethod
    def select_parents(population, retain_rate=0.4, randomly_retain=0.03):
        """
        This function selects parents (most fit schedules) out of the current population of 'Schedule' objects that have fitness scores.

        :param population: The list of Schedule objects with fitness scores.
        :param retain_rate: The percentage of top-tier schedules to keep.
        :param randomly_retain: The probability of low-tier schedules to keep.
        :return: A list of Schedule objects that represent the most fit of the population and some unfit parents.
        """

        sorted_population_by_fitness = sorted(population, key=atg('fitness_score'), reverse=True)           # Sort by highest->lowest fitness scores
        retain_length = retain_rate * len(sorted_population_by_fitness)                                     # Only save (default) the top 40% of the population
        fittest = sorted_population_by_fitness[:int(retain_length)]                                         # Slice the list and organize by fittest and unfittest individuals
        unfit_parents = sorted_population_by_fitness[int(retain_length):]
        lucky_parents = []
        for unfit_schedule in unfit_parents:
            if randomly_retain > np.random.rand():                                                          # Sometimes, add an unfit individual to the population to stop bottlenecking
                lucky_parents.append(unfit_schedule)
        parents = fittest + lucky_parents
        return parents                                                                                      # Return the selected parents that were chosen based on fitness scores

    def get_next_generation(self, selected_parents, randomly_retain=0.1):
        """
        This function selects, cross-breeds and combines classes from fit parents to make a new generation of schedules.

        :param selected_parents: A list of schedules that represent fit parents found in the population.
        :param randomly_retain: A probability of mutation.
        :return:
        """

        children = []
        target_size = self.population_size - len(selected_parents)
        if len(selected_parents) > 0:
            while len(children) < target_size:                                                              # Run until there are enough children in the next generation
                father = np.random.choice(selected_parents)                                                 # Randomly select a mother and father
                mother = np.random.choice(selected_parents)
                if father != mother:
                    child = []                                                                              # A child's "genes" are a list of classes
                    i = 0
                    while i < self.number_of_classes_required_total:                                        # Ensure that a child will have the correct number of classes
                        for course in self.course_list:
                            lab_classes = []
                            discussion_classes = []
                            lecture_classes = []
                            combined = father.get_class_list() + mother.get_class_list()
                            for _class in combined:                                                         # Organize the parents genes into sections of lab classes, discussion classes, and lecture classes
                                if self.dict_for_class_to_course[_class] == course:
                                    if _class.get_type() == 'Lab':
                                        lab_classes.append(_class)
                                    elif _class.get_type() == 'Dis':
                                        discussion_classes.append(_class)
                                    else:
                                        lecture_classes.append(_class)
                            child.append(lecture_classes[np.random.randint(0, len(lecture_classes))])       # Randomly select a lecture from the list of lecture classes (from mother and father)
                            i += 1                                                                          # Do the same for lab classes and discussion classes if applicable
                            if course.has_lab():
                                child.append(lab_classes[np.random.randint(0, len(lab_classes))])
                                i += 1
                            if course.has_discussion():
                                child.append(discussion_classes[np.random.randint(0, len(discussion_classes))])
                                i += 1
                        if np.random.rand() > randomly_retain:                                              # Based on random probability, add a new schedule to the population
                            child = []                                                                      # Make the new schedule randomly
                            for course in self.course_list:
                                lecture_list = course.get_lecture_classes()
                                discussion_list = course.get_discussion_classes()
                                lab_list = course.get_lab_classes()
                                if len(lecture_list) > 0:
                                    index = np.random.randint(0, len(lecture_list))
                                    child.append(lecture_list[index])
                                if len(discussion_list) > 0:
                                    index = np.random.randint(0, len(discussion_list))
                                    child.append(discussion_list[index])
                                if len(lab_list) > 0:
                                    index = np.random.randint(0, len(lab_list))
                                    child.append(lab_list[index])
                    children.append(sch.Schedule(child))                                                   # Make the class list into a Schedule object
        next_population = children + selected_parents
        return next_population
