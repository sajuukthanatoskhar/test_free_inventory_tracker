import datetime
import json
import os
import locale
import pprint
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
            self.name, self.quantity, self.category, self.volume, self.value = self.populate_data(copy_paste_data)
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
    def __init__(self, file: dict = None, is_hangar=None):
        self.date_updated = datetime.datetime.now()
        self.contained_items = []
        self.name = ""
        self.is_hangar = None

        if file:
            self.name = file['name']
            self.is_hangar = bool(file['is_hangar'])
            self.date_updated = file['date_updated']
            for item in file['contained_items']:
                self.contained_items.append(hangar_item(file_data=item))
            return

        while True:
            if not self.is_hangar:
                self.is_hangar = input("Is it a hangar? Y/N ?> ")
            if self.is_hangar is 'Y' or self.is_hangar is 'N':
                if self.is_hangar == 'Y':
                    self.is_hangar = True
                else:
                    self.is_hangar = False
                break
            else:
                print("Error - must be Y/N")

        self.name = input("Name of storage area, if container, make sure you name it according to the \n"
                          "container, case sensitive!\n ?> ")

        self.input_hangar_items()

    def get_number_of_contained_items(self):
        return len(self.contained_items)

    def input_hangar_items(self):
        import easygui
        self.contained_items.clear()
        hangar_list = []

        # print("Enter/Paste your content. Ctrl-D or Ctrl-Z ( windows ) to save it.\nInput the copy paste of the hangar using 'list' view in EVE to retain tab characters")
        # hangar_list.append(input("\nInput the copy paste of the hangar using 'list' view in EVE to retain tab characters").split('\n'))
        contents = []

        lines = easygui.textbox(
            msg="Input the copy paste of the hangar using 'list' view in EVE to retain tab characters\nColumns must be (Name, Quantity, Group, Volume, Est Price)").split(
            '\n')
        for line in lines:
            self.contained_items.append(hangar_item(copy_paste_data=line))

    def display_all_items_in_hangar(self) -> None:
        """
        Returns all items in a hangar
        :return:
        """
        item : hangar_item


        for item in self.contained_items:
            print("{}\t{}\t{}\t{}\t{}".format(item.name, item.quantity, item.category, item.value, item.volume))
        return


class config_file_c:
    def __init__(self, data):
        if len(data) != 2:
            raise IndexError('Length Should be 2')

        self.Global_Fitting_Multiplier = data["Global_Fitting_Multiplier"]
        self.Global_Material_Multiplier = data["Global_Material_Multiplier"]

    def update_GFM(self):
        self.Global_Fitting_Multiplier = float(input("What is the value for the Global Fitting Multiplier"))

    def update_GFF(self):
        self.Global_Material_Multiplier = float(input("What is the value for the Global Material Multiplier"))


class test_free_station:
    def __init__(self, data: dict):
        self.station = data['station']
        self.config: config_file_c
        self.config = config_file_c(data['config'])
        self.hangars: [storage_area]
        self.hangars = []
        self.parse_hangars(data['hangars'])

        if len(self.hangars) < 1:
            self.hangars.append(storage_area())

    def populate_from_hangars_containers(self):
        pass

    def parse_hangars(self, hangars: dict):
        for hangar in hangars:
            self.hangars.append(storage_area(file=hangar))

    def update_hangars_config(self) -> None:
        """
        Gives user choice of updating hangars or config
        :return: None
        """
        # choose between updating hangars or config

        while True:
            try:
                choice = int(input("1. Update Hangar\n2. Update Config\n3. Return\n $> "))
                if choice in [1, 2, 3]:
                    if choice == 1:
                        self.update_hangars()  # todo
                    if choice == 2:
                        self.update_config()  # todo
                    if choice == 3:
                        return
                else:
                    print("Must be 1,2,3")
            except EOFError:
                choice = int(input("1. Update Hangar\n2. Update Config\n3. Return2\n $> "))

    def update_hangars(self) -> None:
        """
        Update Hangars
        :return: None
        """
        choice_not_made = True
        while choice_not_made:
            for index in range(0, len(self.hangars)):
                print("{}. {}".format(index, self.hangars[index].name))

            choice = int(input("which hangar is being updated? (0, {}) \n >$ ".format(len(self.hangars) - 1)))
            if choice in range(0, len(self.hangars)):
                choice_not_made = False

            self.hangars[choice].input_hangar_items()

    def update_config(self):
        """
        Update Config
        :return: None
        """
        choice_not_made = True

        while choice_not_made:
            for index in range(0, len(self.hangars)):
                print("{}. {}".format(index, self.hangars[index]))
            choice: int
            choice = int(input("which hangar is being updated? (0, {}) \n >$ ".format(len(self.hangars))))
            if choice in range(0, len(self.hangars)):
                choice_not_made = False

        choice_not_made: bool = True
        choice = None
        while choice_not_made:
            print("1. Global Fitting Modifier ({})".format(self.config.Global_Fitting_Multiplier))
            print("2. Global Material Modifier ({})".format(self.config.Global_Material_Multiplier))

            choice = input("Which modifier to change? >$ ")

            if int(choice) in [1, 2]:
                choice_not_made = False

        if int(choice) == 1:
            self.config.Global_Fitting_Multiplier = float(input("Global Fitting Multiplier set to what? >$ "))
        if int(choice) == 2:
            self.config.Global_Material_Multiplier = float(input("Global Material Multiplier set to what? >$ "))

    def menu_choose_hangar(self) -> storage_area:
        for i in range(0, len(self.hangars)):
            print("{}\t{}".format(i, self.hangars[i].name))
        choice = int(input("Make choice for station >$ "))
        if 0 <= choice < len(self.hangars):
            return self.hangars[choice]


class test_free_inventory:
    """
    Master class for grouping all test free stations
    Long live the rifters and tunnelsnakes
    """

    def __init__(self):
        self.stations = []
        self.find_station_files()

    def list_stations(self) -> None:
        station: test_free_station
        for station in self.stations:
            print("Name of Station : {}".format(station.station))
            print("Global Fitting Modifier : {}".format(
                station.config.Global_Fitting_Multiplier))
            print("Global Material Modifier : {}\n".format(
                station.config.Global_Material_Multiplier))
        return

    def update_station(self) -> None:
        """
        Updates a station
        :return:
        """
        print("Choose which station to update")

        for i in range(0, len(self.stations)):
            print("{}\t{}".format(i, self.stations[i].station))
        choice = int(input("Make choice for station >$ "))
        if 0 <= choice < len(self.stations):
            self.stations[choice].update_hangars_config()

    def make_new_station(self) -> None:
        """
        Makes a new station
        User has to do some input
        Saves to *.stn file
        :return:
        """
        station_name = input("Name of Station?")
        station_dict = {'station': station_name,
                        'config': {
                            "Global_Fitting_Multiplier": float(input("What is global fitting multiplier?")),
                            "Global_Material_Multiplier": float(input("What is global material multiplier?")),

                        },
                        'hangars': []
                        }

        new_station = test_free_station(station_dict)
        self.stations.append(new_station)

    def find_station_files(self) -> None:
        for files_to_open in self.get_stn_files():
            self.stations.append(self.parse_stn_file(files_to_open))

    def get_stn_files(self) -> [str]:
        """
        Gets the *.stn files
        :return:
        """
        return ["./stations/" + station for station in os.listdir("./stations")]

    def parse_stn_file(self, station: str) -> test_free_station:
        """
        Parses a *.stn file
        :param station:
        :return:
        """

        with open(station, 'r') as file:
            t_f_station = test_free_station(json.load(file))
        return t_f_station

    def save_stations_to_json_file(self):
        """
        Saves each station to a json file
        :return:
        """
        station: test_free_station
        for station in self.stations:

            jsonjson = station.__dict__
            jsonjson['config'] = jsonjson['config'].__dict__

            for count in range(0, len(jsonjson['hangars'])):
                jsonjson['hangars'][count] = jsonjson['hangars'][count].__dict__
                item_list = jsonjson['hangars'][count]['contained_items']
                for countcount in range(0, len(item_list)):
                    item_list[countcount] = item_list[countcount].__dict__

            with open('./stations/{}.stn'.format(station.station), 'w') as outfile:
                json.dump(jsonjson, outfile)

    def create_new_station_hangar(self):
        pass

    def get_materials_for_items_in_hangar(self):
        self.menu_choose_station()

    def display_and_calculate_materials(self):
        self.menu_choose_station()

    def display_hangar_items(self):
        pass

    def menu_choose_station(self) -> test_free_station:
        for i in range(0, len(self.stations)):
            print("{}\t{}".format(i, self.stations[i].station))
        choice = int(input("Make choice for station >$ "))
        if 0 <= choice < len(self.stations):
            return self.stations[choice]

    def display_items_from_hangar(self):
        self.menu_choose_station().menu_choose_hangar().display_all_items_in_hangar()
