from genetic_algorithm.evolution import Evolution           # A Class to manage Evolution of Schedules
from classes_and_functions.class_base_exceptions import WorkingScheduleNotFound   # Exception for finding working schedules
import random                                               # To randomly test population


def get_schedules_using_ga(courses_per_department):
    """
    This function uses the genetic algorithm to over time create optimized schedules (non-conflicting schedules).

    :return: A list containing Class objects that together make a working_schedule.
    """

    population_size = 100                                                               # Hard-coded starting population
    darwin = Evolution(courses_per_department, population_size)                         # Create an evolution object, with a specified population_size
    found_working_schedule = False
    current_population = darwin.get_starting_population()
    generation_number = 0
    working_schedules = []

    while not found_working_schedule:
        for schedule in current_population:
            if satisfied_requirements(schedule):
                found_working_schedule = True
                working_schedules.append(schedule)
            darwin.rank_fitness(schedule)                                               # Rank individuals in the population

        # avg = print_generation_information(current_population, generation_number)     # This is a debugging feature
        selected_parents = darwin.select_parents(current_population)                    # Select most fit parents (best schedules)
        next_population = darwin.get_next_generation(selected_parents)                  # "Cross-mutate" the "genes (classes)" for a better population of schedules
        current_population = next_population
        generation_number += 1

        if generation_number == 100:                                                    # If it hasn't found a working schedule in 100 generations, the population was bottle-necked
            current_population = darwin.get_starting_population()
        if generation_number == 200:                                                    # Possibly schedule not found because it is impossible
            raise WorkingScheduleNotFound
    return working_schedules


def print_one_individual(current_population):
    """
    This function is mainly a debugging feature that allows users to randomly inspect one individual from a population (the first one).

    :param current_population: List of Schedule objects (together represent a population)
    :return: None
    """
    schedule = random.choice(current_population)
    class_list = schedule.get_class_list()
    for _class in class_list:
        print(str(_class.get_name_of_course()) + " " + str(_class.get_type()))


def print_generation_information(population, generation_number):
    """
    This function is a debugging feature that calculates the average fitness of the population and prints it.

    :param population: The population of current schedules (list of Schedule objects).
    :param generation_number: The n'th generation (an integer).
    :return: None
    """

    total = 0
    for score in population:
        total += score.fitness_score
    avg = float(total) / len(population)
    print('Generation: ' + str(generation_number) + ': ' + str(avg))
    return avg


def remove_conflicts(chosen_class, class_list):
    """
    A function to remove time-conflicting classes.

    :param chosen_class: The class (Class object) that was chosen.
    :param class_list: The rest of the classes (list of Class objects).
    :return: None
    """

    for _class in class_list.copy():
        if chosen_class != _class:
            if is_between(chosen_class, _class) and not (chosen_class.code == _class.code):
                class_list.remove(_class)


def print_conflicts(class_list):
    """
    This function is a debugging function that prints out classes that conflict with each other.

    :param class_list: A list of classes that collectively are a schedule.
    :return: None
    """

    for _class in class_list:
        for _class_again in class_list:
            if is_between(_class_again, _class) and not (_class_again.code == _class.code):
                print(_class)


def satisfied_requirements(schedule):
    """
    This function will check if there are any time conflicting classes.

    :param schedule: A list of classes that collectively are a schedule.
    :return: True if there are no time conflictions, false is there are time conflictions.
    """

    class_list = schedule.class_list
    satisfied = True
    for _class in class_list:
        for _class_again in class_list:
            if is_between(_class_again, _class) and not (_class_again.code == _class.code):
                satisfied = False
    return satisfied


def remove_same_type(chosen_class, class_list):
    """
    A function to remove classes of the same type (i.e. 'Lectures', 'Labs', and 'Discussions' of the same course).

    :param chosen_class: The class (Class object) that was chosen.
    :param class_list: The rest of the classes (list of Class objects).
    :return: A list of Class objects that do not have the same type (and course) as the chosen class.
    """

    class_type = chosen_class.get_type()
    name_of_course = chosen_class.get_name_of_course()
    for _class in class_list:
        if (_class.get_type() == class_type) and (_class.get_name_of_course() == name_of_course) and (_class is not chosen_class):
            if chosen_class.code == _class.code:
                pass
            else:
                class_list.remove(_class)
    return class_list


def is_between(class_a, class_b):
    """
    A function to check if "class b's" time overlaps "class_a's"

    :param class_a: A class object.
    :param class_b: A class object.
    :return: True if the meeting times overlap, False if the classes do not overlap.
    """

    time_start_a, time_end_a = class_a.get_time()
    time_start_b, time_end_b = class_b.get_time()
    days_a = class_a.get_days_as_list()
    days_b = class_b.get_days_as_list()

    if time_start_a == 'TBA' or time_end_b == 'TBA':                                                             # If classes overlap, nothing can be concluded
        return False

    if ((time_end_a < time_start_b) and (time_start_a < time_start_b)) or not days_overlap(days_a, days_b):      # If the time does not overlap, classes are not in-between each other
        return False                                                                                             # If the time does, check if the days do, if they do not, then
    elif (time_end_b < time_start_a) and (time_start_b < time_start_a):                                          # the classes are not in-between each other
        return False
    else:
        return True


def days_overlap(day_a, day_b):
    """
    This function checks if class_a and class_b have common meeting times. e.g. day_a = ['M', 'Tu'], day_b = ['M', 'W']
    then this function will return True because, the two classes have Monday meeting times in common.
    :param day_a: A list of strings that represent the meeting days of class_a.
    :param day_b: A list of strings that represent the meeting days of class_b.
    :return: True if the days overlap, False if they do not.
    """
    for day in day_a:
        if day in day_b:
            return True
    return False

