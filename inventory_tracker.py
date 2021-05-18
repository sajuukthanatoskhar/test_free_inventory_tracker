import os
import locale
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

    def __init__(self, csv_data):
        self.name, self.qty, self.category, self.volume, self.isk_worth = self.populate_data(csv_data)

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
            line[1] = float(line[1].replace(',',''))

        for index in range(3, 5):
            if line[index].endswith(common_endings_for_string_input[index]):
                line[index] = float(locale.atof(rchop(line[index], common_endings_for_string_input[index])))

        return str(line[0]), int(line[1]), str(line[2]), float(line[3]), float(line[4])


class storage_area:
    def __init__(self, file):
        self.contained_items = [hangar_item]
        self.name = ""
        self.is_hangar = ""

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

        contents: list
        contents = input(
            "\nInput the copy paste of the hangar using 'list' view in EVE to retain tab characters").split('\n')

        for line in contents:
            self.contained_items.append(hangar_item(line))

    def get_number_of_contained_items(self):
        return len(self.contained_items)


class config_file_c:
    def __init__(self, data):
        if len(data) != 3:
            raise IndexError('Length Should be 3')

        self.Global_Fitting_Multiplier = data[0]
        self.Global_Material_Multiplier = data[1]
        self.name = data[2]


class test_free_station:
    def __init__(self, folder: str):

        # self.Global_Fitting_Multiplier = 1.0
        # self.Global_Material_Multiplier = 1.0
        self.name = ""
        self.folder = folder
        self.config_file: config_file_c
        self.config_file = self.config_setup(folder)
        self.hangars = [storage_area]

    def config_setup(self, folder: str) -> config_file_c:
        # do things
        dir_contents = os.listdir()
        config_file = None
        for file_f in dir_contents:
            if file_f.endswith('.cfg') and self.no_of_cfg_files(dir_contents) == 1:
                try:
                    config_file = open(self.folder + file_f, 'r')
                    break
                except FileNotFoundError:
                    print("File Not Found")
                    sys.exit(2)

        if not config_file:
            sys.exit(2)

        return config_file_c(config_file.readlines())

    def populate_from_hangars_containers(self):
        pass

    def no_of_cfg_files(self, directory_contents: [str]) -> int:
        """
        Just checks that there is only one config file
        :param directory_contents: directory contents of folder
        :return: number of counters (should only be int('1')
        """
        counter = 0
        for files in directory_contents:
            if files.endswith('.cfg'):
                counter += 1

        if counter > 1:
            raise ValueError("Too many config files")

        return counter


class test_free_inventory:
    """
    Master class for grouping all test free stations
    Long live the rifters and tunnelsnakes
    """

    def __init__(self):
        self.stations: [test_free_station]
        self.stations = None

    def list_stations(self):
        pass

    def update_station(self):
        pass

    def make_new_station(self):
        pass
