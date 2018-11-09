from scrape import class_scraper
from genetic_algorithm.class_schedule_solver import get_schedules_using_ga
from class_base_exceptions import WorkingScheduleNotFound
import schedule
from export_classes import export
import random

term, departments = class_scraper.get_classes()                               # Scrape the classes

try:
    working_schedules = get_schedules_using_ga(departments)                   # Try to find working schedules
    selected_schedule = random.choice(working_schedules)                      # Choose random schedule from the list of non-conflicting, fulfilled schedules
    export(term, selected_schedule)

except WorkingScheduleNotFound:                                               # Using the GA, a schedule was not able to be found.
    print("Unable to create schedule.")
