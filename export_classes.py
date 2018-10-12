from openpyxl import load_workbook  # Output schedules to an Excel sheet

def export(term, working_schedule):
    """
    IN PROGRESS
    :param working_schedule: A Schedule object
    :return:
    """
    workbook_for_classes = load_workbook('Schedule_Template.xlsx')
    workbook_for_finals = load_workbook('Schedule_Template.xlsx')
    class_list_for_classes = workbook_for_classes['Class List']
    class_list_for_finals = workbook_for_finals['Class List']
    days = {
        'M': 'MONDAY',
        'Tu': 'TUESDAY',
        'W': 'WEDNESDAY',
        'Th': 'THURSDAY',
        'F': 'FRIDAY',
        'Mon': 'MONDAY',
        'Tue': 'TUESDAY',
        'Wed': 'WEDNESDAY',
        'Thu': 'THURSDAY',
        'Fri': 'FRIDAY'
    }

    workbook_for_classes.save('Class Schedule - ' + term + ".xlsx")
    workbook_for_finals.save('Finals Schedule - ' + term + ".xlsx")
