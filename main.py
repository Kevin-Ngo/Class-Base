from scrape import class_scraper
from class_schedule_solver import Schedules

term, departments = class_scraper.get_classes()
fall = Schedules(term, departments)
fall.make_a_schedule()
