from scrape import class_scraper
from genetic_algorithm.class_schedule_solver import make_a_schedule_using_ga

term, departments = class_scraper.get_classes()         # Scrape the classes
make_a_schedule_using_ga(departments)                   # Try to find a working schedule
