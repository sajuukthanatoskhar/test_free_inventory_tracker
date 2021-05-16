import os

import fuzzworks_bpos.eve_blueprint_read_write as bp_lib
import eve_fits_itemiser as efi
import os, sys, csv

class hangar_items:
    def __init__(self, csv_data: ):
        self.name, self.type,self.volume, self.isk_worth = self.populate_data(csv_data)

    def populate_data(self, inputted_csv_data) -> (str, str, float, float):
        """
        Populate the data for each hangar item
        :param inputted_csv_data:
        :return:
        """
        return str, str, float, float


class storage_area:
    def __init__(self, file):
        self.contained_items: [hangar_items]
        self.name: str
        self.is_hangar: bool

        self.is_hangar, self.name, self.contained_items = self.get_csv_file(file)

    def get_csv_file(self, file) -> (bool, str, [hangar_items]):
        is_hangar = ""
        name = ""
        contained_items = [hangar_items]

        # open file

        return is_hangar, name, contained_items


class test_free_station:
    def __init__(self, folder: str):

        # self.Global_Fitting_Multiplier = 1.0
        # self.Global_Material_Multiplier = 1.0
        self.name = ""
        self.folder = folder
        self.config_file : config_file
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

    def no_of_cfg_files(self, directory_contents : [str]) -> int:
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


class config_file_c:
    def __init__(self, data):

        if len(data) != 3:
            raise IndexError('Length Should be 3')

        self.Global_Fitting_Multiplier
        self.Global_Material_Multiplier
        self.name