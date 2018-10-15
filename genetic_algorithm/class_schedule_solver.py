from genetic_algorithm.evolution import Evolution       # A Class to manage Evolution of Schedules


def make_a_schedule_using_ga(courses_per_department):
    """
    IN PROGRESS
    :return: A list containing Class objects that together make a working_schedule.
    """

    population_size = 100                                          # Hard-coded starting population
    darwin = Evolution(courses_per_department, population_size)
    found_working_schedule = False
    current_population = darwin.get_starting_population()
    generation_number = 0

    while not found_working_schedule:
        for schedule in current_population:
            if darwin.satisfied_requirements(schedule):
                found_working_schedule = True
                break
            darwin.rank_fitness(schedule)

        print_generation_information(current_population, generation_number)
        selected_parents = darwin.select_parents(current_population)
        next_population = darwin.get_next_generation(selected_parents)
        current_population = next_population
        generation_number += 1

        if generation_number == 5000:
            current_population = darwin.get_starting_population()


def print_generation_information(population, generation_number):
    """
    This function calculates the average fitness of the population and prints it. This is mainly a debugging feature.

    :param population: The population of current schedules (list of Schedule objects).
    :param generation_number: The n'th generation (an integer).
    :return: None
    """

    total = 0
    for score in population:
        total += score.fitness_score
    avg = float(total) / len(population)
    print('Generation: ' + str(generation_number) + ': ' + str(avg))


def remove_conflicts(chosen_class, class_list):
    """
    A function to remove time-conflicting classes.

    :param chosen_class: The class (Class object) that was chosen.
    :param class_list: The rest of the classes (list of Class objects).
    :return: A class list (list of Class objects) with all time-conflicting classes removed.
    """

    for _class in class_list:
        if chosen_class != _class:
            if is_between(chosen_class, _class) and not (chosen_class.code == _class.code):
                class_list.remove(_class)
    return class_list


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

    if ((time_start_a < time_start_b) and (time_end_a < time_start_b)) and (class_a.days == class_b.days):
        return False
    elif ((time_start_b < time_start_a) and (time_end_b < time_start_a)) and (class_a.days == class_b.days):
        return False
    else:
        return True

