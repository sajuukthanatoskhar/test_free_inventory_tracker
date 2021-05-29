import inventory_tracker
import sys, os

choice_list = list(range(1,5))

if __name__ == '__main__':

    test_free_main_hq = inventory_tracker.test_free_inventory()

    print("Hi, this is the test free inventory tracker")
    while(1):
        print("Choose options .... \n\n\n"
          "1.\t  List stations and their details - Shows last update\n"
          "2.\t  Update station\n"
          "3.\t  Make New Station\n"
              "4.\t  Make New Hangar\n"
              "5.\t Quit\n")
        choice = input(" Choose Now $>")

        if int(choice) not in choice_list:
            print("Error")
            continue

        print("Loading Stations")



        if choice == '1':
            test_free_main_hq.list_stations()

        if choice == '2':
            test_free_main_hq.update_station()
            test_free_main_hq.save_stations_to_json_file()

        if choice == '3':
            test_free_main_hq.make_new_station()

        if choice == '4':
            test_free_main_hq.create_new_station_hangar()

        if choice == '5':
            sys.exit(0)



