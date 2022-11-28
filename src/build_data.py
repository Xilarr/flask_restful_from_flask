from src import app
from src.report import build_report
from src.config import FOLDER_PATH, ABB_FILE_PATH


def build_drivers_data():
    drivers_dict = {}
    with open(ABB_FILE_PATH) as file:
        try:
            add, driver, car = file.readline().split('_')
            while len(add) == 3:
                drivers_dict[add] = [driver, car]
                add, driver, car = file.readline().split('_')
        except ValueError:
            pass
    return drivers_dict


def find_driver(driver_list):
    for driver in build_report(FOLDER_PATH):
        if driver_list[0] in driver[1]:
            current_driver = driver
        else:
            current_driver = None

        if current_driver:
            return current_driver


if __name__ == '__main__':
    find_driver()
