import datetime
import json
import os
import locale
from typing import Type

locale.setlocale(locale.LC_NUMERIC, "English")
import os, sys, csv

allowed_true_bool_inputs = ["y", "Y", 'yes']
allowed_false_bool_inputs = ['n', "N", 'no']


def rchop(s: str, suffix: str) -> str:
    """
    Chops off the end of a string!
    :param s:
    :param suffix:
    :return:
    """
    if suffix and s.endswith(suffix):
        return s[:-len(suffix)]
    return s


class hangar_item:
    """
    Hangar item in a hangar or container
    """

    def __init__(self, copy_paste_data=None, file_data=None):
        if copy_paste_data:
            self.name, self.qty, self.category, self.volume, self.isk_worth = self.populate_data(copy_paste_data)
            return
        elif file_data:
            self.name = file_data['name']
            self.quantity = file_data['quantity']
            self.category = file_data['category']
            self.volume = file_data['volume']
            self.value = file_data['value']

    def populate_data(self, inputted_csv_data: str) -> (str, str, float, float):
        """
        Populate the data for each hangar item
        :param inputted_csv_data:
        :return: name, qty, category, volume, est price
        """
        common_endings_for_string_input = ['', '', '', ' m3', ' ISK']

        line = inputted_csv_data.split('\t')
        if line[1] in ["", None]:
            line[1] = int(1)
        else:
            line[1] = float(line[1].replace(',', ''))

        for index in range(3, 5):
            if line[index].endswith(common_endings_for_string_input[index]):
                line[index] = float(locale.atof(rchop(line[index], common_endings_for_string_input[index])))

        return str(line[0]), int(line[1]), str(line[2]), float(line[3]), float(line[4])


class storage_area:
    def __init__(self, file=None):
        self.date_updated = datetime.datetime.now()
        self.contained_items = []
        self.name = ""
        self.is_hangar = ""

        if file:
            self.name = file['name']
            self.is_hangar = bool(file['is_hangar'])
            self.date_updated = file['date_updated']
            for item in file['contained_items']:
                self.contained_items.append(hangar_item(file_data=item))
            return

        while True:
            self.is_hangar = input("Is it a hangar? Y/N ?> ")
            if self.is_hangar is 'Y' or 'N':
                if self.is_hangar == 'Y':
                    self.is_hangar = True
                else:
                    self.is_hangar = False
                break
            else:
                print("Error - must be Y/N")

        self.name = input("Name of storage area, if container, make sure you name it according to the \n"
                          "container, case sensitive!\n ?> ")

        for line in input(
                "\nInput the copy paste of the hangar using 'list' view in EVE to retain tab characters").split('\n'):
            self.contained_items.append(hangar_item(line))

    def get_number_of_contained_items(self):
        return len(self.contained_items)


class config_file_c:
    def __init__(self, data):
        if len(data) != 2:
            raise IndexError('Length Should be 2')

        self.Global_Fitting_Multiplier = data["Global_Fitting_Multiplier"]
        self.Global_Material_Multiplier = data["Global_Material_Multiplier"]


class test_free_station:
    def __init__(self, data: dict):
        self.station = data['station']
        self.config: config_file_c
        self.config = config_file_c(data['config'])
        self.hangars = []
        self.parse_hangars(data['hangars'])

    def populate_from_hangars_containers(self):
        pass

    def parse_hangars(self, hangars: dict):
        for hangar in hangars:
            self.hangars.append(storage_area(hangar))
    # def no_of_cfg_files(self, directory_contents: [str]) -> int:
    #     """
    #     Just checks that there is only one config file
    #     :param directory_contents: directory contents of folder
    #     :return: number of counters (should only be int('1')
    #     """
    #     counter = 0
    #     for files in directory_contents:
    #         if files.endswith('.cfg'):
    #             counter += 1
    #
    #     if counter > 1:
    #         raise ValueError("Too many config files")
    #
    #     return counter


class test_free_inventory:
    """
    Master class for grouping all test free stations
    Long live the rifters and tunnelsnakes
    """

    def __init__(self):
        self.stations = []

    def list_stations(self) -> None:
        self.find_station_files()
        print(self.stations, sep='\n')
        return

    def update_station(self) -> None:
        """
        Updates a station
        :return:
        """
        self.find_station_files()
        station_list = []
        print("Choose which station to update")
        individual_station: test_free_station
        for individual_station in self.stations:
            station_list.append(individual_station)
            print("{} - {} station".format(str(len(station_list)), str(individual_station.name)))

    def make_new_station(self) -> None:
        """
        Makes a new station
        User has to do some input
        Saves to *.stn file
        :return:
        """
        pass

    def find_station_files(self) -> None:
        for files_to_open in self.get_stn_files():
            self.stations.append(self.parse_stn_file(files_to_open))

    def get_stn_files(self) -> [str]:
        """
        Gets the *.stn files
        :return:
        """
        station_file_list = ["./stations/" + station for station in os.listdir("./stations")]
        return ["./stations/" + station for station in os.listdir("./stations")]

    def parse_stn_file(self, station: test_free_station) -> test_free_station:
        """
        Parses a station file
        """
        with open(station, 'r') as file:
            t_f_station = test_free_station(json.load(file))
        return t_f_station

    def save_stations_to_json_file(self):
        """
        Saves each station to a json file
        :return:
        """
        # for

        station:test_free_station
        for station in self.stations:

            jsonjson = station.__dict__
            jsonjson['config'] = jsonjson['config'].__dict__

            for count in range(0, len(jsonjson['hangars'])):
                jsonjson['hangars'][count] = jsonjson['hangars'][count].__dict__
                item_list = jsonjson['hangars'][count]['contained_items']
                for countcount in range(0, len(item_list)):
                    item_list[countcount] = item_list[countcount].__dict__

            with open('./stations/demo.stn', 'w') as outfile:
                json.dump(jsonjson, outfile)
