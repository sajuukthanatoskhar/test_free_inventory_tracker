import inspect

import inventory_tracker
import sys, os

global DEBUG

DEBUG = False
choice_list = list(range(1, 8))


def callback(func=None):
    if func == sys.exit:
        func(0)
    print("{}".format(func))
    func()


if __name__ == '__main__':

    test_free_main_hq = inventory_tracker.test_free_inventory()
    print("Hi, this is the test free inventory tracker")

    methodlist = [classmethod[1] for classmethod in inspect.getmembers(test_free_main_hq)
                  if getattr(classmethod[1], "__is_menu_function", False)]
    methodlist.append(sys.exit)
    while True:
        print("Choose options .... \n\n\n")
        for option_number in range(0, len(methodlist)):
            print("{}.\t {}".format(option_number, methodlist[option_number].__doc__.split('\n')[0].lstrip(" ")))

        choice = input("\nChoose Now\t $>")
        if int(choice) not in list(range(0, len(methodlist))):
            print("*** Error! ***")
            continue
        print("Loading Stations")
        callback(methodlist[int(choice)])
        test_free_main_hq.find_station_files()  # deletes al
