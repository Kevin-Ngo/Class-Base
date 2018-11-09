import numpy as np                                              # For more statistical functions
from operator import attrgetter as atg                          # A way to sort custom objects
import schedule as sch


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
            # for y in range(self.number_of_classes_required_total):
            #     index = np.random.randint(0, len(self.class_list))
            #     individual.append(self.class_list[index])
            for course in self.course_list:
                lecture_list = course.get_lecture_classes()
                discussion_list = course.get_discussion_classes()
                lab_list = course.get_lab_classes()

                if len(lecture_list) > 0:
                    index = np.random.randint(0, len(lecture_list))
                    individual.append(lecture_list[index])
                if len(discussion_list) > 0:
                    index = np.random.randint(0, len(discussion_list))
                    individual.append(discussion_list[index])
                if len(lab_list) > 0:
                    index = np.random.randint(0, len(lab_list))
                    individual.append(lab_list[index])
            population.append(sch.Schedule(individual))                 # Append 'Schedule' objects to the population
        return population

    def rank_fitness(self, schedule):
        """
        IN PROGRESS
        :param schedule:
        :return:
        """
        from genetic_algorithm.class_schedule_solver import is_between  # Function to check if classes conflict - late import to prevent circular importing

        class_list = schedule.get_class_list()
        fitness_score = 0.0
        marked_list = [False] * len(class_list)
        lab_counter = 0
        discussion_counter = 0
        lecture_counter = 0
        already_checked = {}
        for _class in class_list:
            course_name = _class.get_name_of_course()
            lab_fulfillment = False
            discussion_fulfillment = False
            lecture_fulfillment = False
            course = self.dict_for_class_to_course[_class]
            counter = 0
            for _class_again in class_list:
                if course_name in already_checked.keys():
                    break
                elif _class is _class_again:
                    continue

                if (_class is not _class_again) and is_between(_class, _class_again):  # check time conflictions
                    marked_list[counter] = True
                    fitness_score -= 1

                if (course_name == _class_again.get_name_of_course()) and (_class is not _class_again):  # if same name
                    class_type = _class_again.get_type()
                    if course.has_lab() and class_type == 'Lab':  # if same type
                        if not lab_fulfillment:
                            lab_fulfillment = True
                            fitness_score += 1
                            lab_counter += 1
                        else:
                            marked_list[counter] = True
                            lab_counter += 1
                            #fitness_score -= 1
                    elif course.has_discussion() and class_type == 'Dis':
                        if not discussion_fulfillment:
                            discussion_fulfillment = True
                            fitness_score += 1
                            discussion_counter += 1
                        else:
                            marked_list[counter] = True
                            discussion_counter += 1
                            #fitness_score -= 1
                    elif class_type == 'Lec':
                        if not lecture_fulfillment:
                            lecture_fulfillment = True
                            lecture_counter += 1
                        else:
                            marked_list[counter] = True
                            #fitness_score -= 1
                counter += 1

            lab_discussion_lecture = [lab_fulfillment, discussion_fulfillment, lecture_fulfillment]
            already_checked[course_name] = lab_discussion_lecture

        # if lecture_counter > 1:
        #     fitness_score -= 1
        # if discussion_counter > 1:
        #     fitness_score -= 1
        # if lab_counter > 1:
        #     fitness_score -= 1

        fitness_score = float(fitness_score)/self.number_of_classes_required_total
        schedule.set_fitness_score(fitness_score)
        schedule.set_marked_list(marked_list)

    @staticmethod
    def select_parents(population, retain_rate=0.4, randomly_retain=0.03):
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

    def get_next_generation(self, selected_parents, randomly_retain=0.1):
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
                        # random_index_father = np.random.randint(self.number_of_classes_required_total)
                        # random_index_mother = np.random.randint(self.number_of_classes_required_total)

                        for course in self.course_list:
                            lab_classes = []
                            discussion_classes = []
                            lecture_classes = []
                            combined = father.get_class_list() + mother.get_class_list()
                            for _class in combined:
                                if self.dict_for_class_to_course[_class] == course:
                                    if _class.get_type() == 'Lab':
                                        lab_classes.append(_class)
                                    elif _class.get_type() == 'Dis':
                                        discussion_classes.append(_class)
                                    else:
                                        lecture_classes.append(_class)

                            child.append(lecture_classes[np.random.randint(0, len(lecture_classes))])
                            i += 1
                            if course.has_lab():
                                child.append(lab_classes[np.random.randint(0, len(lab_classes))])
                                i += 1
                            if course.has_discussion():
                                child.append(discussion_classes[np.random.randint(0, len(discussion_classes))])
                                i += 1

                        if np.random.rand() > randomly_retain:
                            if len(child) > 0:
                                random_index_super_mutation = np.random.randint(len(child))
                                change_this_gene = child[random_index_super_mutation]
                                course_for_gene = self.dict_for_class_to_course[change_this_gene]
                                choices = None
                                if change_this_gene.get_type() == 'Lab':
                                    choices = course_for_gene.get_lab_classes()
                                elif change_this_gene.get_type() == 'Dis':
                                    choices = course_for_gene.get_discussion_classes()
                                else:
                                    choices = course_for_gene.get_lecture_classes()

                                if len(choices) > 1:
                                    rand_index = np.random.randint(len(choices))
                                    replace_with = change_this_gene
                                    while change_this_gene is replace_with:
                                        replace_with = choices[rand_index]
                                        rand_index = np.random.randint(len(choices))
                                    child[random_index_super_mutation] = replace_with

                        if np.random.rand() > 0.1:
                            child = []
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

                        # if np.random.rand() > 0.03:
                        #     for _class in child:
                        #         for _class_again in child:
                        #             if (_class is not _class_again) and is_between(_class, _class_again):
                        #                 course_for_class = self.dict_for_class_to_course[_class]
                        #                 course_for_class_again = self.dict_for_class_to_course[_class_again]
                        #                 type_for_class = _class.get_type()
                        #                 type_for_class_again = _class_again.get_type()
                        #                 type = None
                        #
                        #                 if np.random.randint(0, 2) == 1:
                        #                     replace_index = child.index(_class_again)
                        #                     lecture_classes = course_for_class_again.get_lecture_classes()
                        #                     discussion_classes = course_for_class_again.get_discussion_classes()
                        #                     lab_classes = course_for_class_again.get_lab_classes()
                        #                     type = type_for_class_again
                        #                 else:
                        #                     replace_index = child.index(_class)
                        #                     lecture_classes = course_for_class.get_lecture_classes()
                        #                     discussion_classes = course_for_class.get_discussion_classes()
                        #                     lab_classes = course_for_class.get_lab_classes()
                        #                     type = type_for_class
                        #
                        #                 if type == 'Lec':
                        #                     child[replace_index] = lecture_classes[np.random.randint(0, len(lecture_classes))]
                        #                 elif type == 'Dis':
                        #                     child[replace_index] = discussion_classes[np.random.randint(0, len(discussion_classes))]
                        #                 else:
                        #                     child[replace_index] = lab_classes[np.random.randint(0, len(discussion_classes))]

                                # mutated_child = remove_same_type(change_this_gene, child.copy())
                                # mutated_child = remove_conflicts(change_this_gene, mutated_child)
                                # child = mutated_child
                                # i = len(child)
                                # fathers_list = father.get_indices_of_marked()
                                # mothers_list = mother.get_indices_of_marked()
                                #
                                # for x in fathers_list:
                                #     if np.random.rand() > randomly_retain:
                                #         father.get_class_list()[x] = self.class_list[np.random.randint(len(self.class_list))]
                                #
                                # for y in mothers_list:
                                #     if np.random.rand() > randomly_retain:
                                #         mother.get_class_list()[y] = self.class_list[np.random.randint(len(self.class_list))]

                        # marked_father = father.get_marked_list()[random_index_father]
                        # marked_mother = mother.get_marked_list()[random_index_mother]

                        # father_gene = father.get_class_list()[random_index_father]
                        # mother_gene = mother.get_class_list()[random_index_mother]

                        # For some reason, commenting out this code, yields better results.

                        # if marked_father and (np.random.rand() > randomly_retain):
                        #     random_index_father = np.random.randint(len(self.class_list))
                        #     father_gene = self.class_list[random_index_father]
                        #
                        # if marked_mother and (np.random.rand() > randomly_retain):
                        #     random_index_mother = np.random.randint(len(self.class_list))
                        #     mother_gene = self.class_list[random_index_mother]

                        # child.append(father_gene)
                        # i += 1
                        # if i < self.number_of_classes_required_total:
                        #     child.append(mother_gene)
                        #     i += 1

                    children.append(sch.Schedule(child))

        # for schedule in selected_parents:
        #     m_list = [False] * len(schedule.get_class_list())
        #     schedule.set_marked_list(m_list)

        next_population = children + selected_parents
        return next_population

    # @staticmethod
    # def purge(father, mother):

    # @staticmethod
    # def select_genes_from_parents(father, mother):
    #
    #
    # def organize_genes(individual):
    #     genes = individual.get_class_list()
    #     for course in self.course_list:
    #         for _class in genes:
    #             if self.dict_for_class_to_course[_class] ==

    def print_conflicts(class_list):
        for _class in class_list:
            for _class_again in class_list:
                if is_between(_class_again, _class) and not (_class_again.code == _class.code):
                    print(_class)

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
