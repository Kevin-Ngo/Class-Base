from scrape import class_scraper                                                                    # Scrape function
from genetic_algorithm.class_schedule_solver import get_schedules_using_ga                          # Genetic Algorithm
from classes_and_functions.class_base_exceptions import WorkingScheduleNotFound                     # Exceptions for the script
from classes_and_functions.export_classes import export_text                                        # Exporting functionality

term, departments = class_scraper.get_classes()                                                     # Scrape the classes

try:
    working_schedules = get_schedules_using_ga(departments)                                         # Try to find working schedules
    export_text(term, working_schedules)                                                            # Output the working schedules

except WorkingScheduleNotFound:                                                                     # Using the GA, a schedule was not able to be found.
    print("Unable to create schedule.")
