import inventory_tracker
import sys, os

global DEBUG

DEBUG = False
choice_list = list(range(1,8))

if __name__ == '__main__':

    test_free_main_hq = inventory_tracker.test_free_inventory()
    print("Hi, this is the test free inventory tracker")

    if DEBUG:
        test_free_main_hq.display_and_calculate_required_materials()
    else:
        while True:
            print("Choose options .... \n\n\n"
                  "1.\t  List stations and their details - Shows last update\n"
                  "2.\t  Update station\n"
                  "3.\t  Make New Station\n"
                  "4.\t  Make New Hangar\n"
                  "5.\t  Display station inventory\n"
                  "6.\t  Calculate materials for replacement (GFM and GMM)\n"
                  "7.\t Display Hangar Items\n"
                  "8.\t Quit\n")
            choice = input("\nChoose Now\t $>")

            if int(choice) not in choice_list:
                print("*** Error! ***")
                continue

            print("Loading Stations")



            if choice == '1':
                test_free_main_hq.list_stations()
            if choice == '2':
                test_free_main_hq.update_station()
                test_free_main_hq.save_stations_to_json_file()
            if choice == '3':
                test_free_main_hq.make_new_station()
                test_free_main_hq.save_stations_to_json_file()
            if choice == '4':
                test_free_main_hq.create_new_station_hangar()
                test_free_main_hq.save_stations_to_json_file()
            if choice == '5':
                test_free_main_hq.get_materials_for_items_in_hangar()
            if choice == '6': # Get materials
                test_free_main_hq.display_and_calculate_required_materials()
            if choice == '7': # Display items from a hangar
                test_free_main_hq.display_items_from_hangar()
            if choice == '8': # Quit
                sys.exit(0)

            test_free_main_hq.find_station_files() # deletes al













