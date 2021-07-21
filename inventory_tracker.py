import datetime
import json
import os
import locale
import pprint
from typing import Type

locale.setlocale(locale.LC_NUMERIC, "English")
import os, sys, csv
from fuzzworks_bpos import fuzzworks
from eve_fits_itemiser import fit_translator
import easygui

ship_type_list = []

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
        # todo: Kevin Spacey's Capsule
        return str(line[0]), int(line[1]), str(line[2]), float(line[3]), float(line[4])

    def get_fit(self) -> list:
        # Get fit from file
        pass


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
        item: hangar_item
        print("{:^40s}\t{:^15s}\t{:^20s}\t{:^20s}\t{:^17s}".format("item.name", "item.quantity", "item.category",
                                                                   'item.value', "item.volume"))
        for item in self.contained_items:
            print("{:>40s}\t{:>15d}\t{:<20s}\t{:>20.2f}\t{:>15.2f}".format(item.name, item.quantity, item.category,
                                                                           item.value, item.volume))
        return

    def update_date_updated(self):
        self.date_updated = datetime.datetime.now()


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


# class MenuMetaClass(type):
#     pas


class test_free_station:
    def __init__(self, data: dict):
        self.station = data['station']  # name of station
        self.config: config_file_c
        self.config = config_file_c(data['config'])
        self.hangars: [storage_area]
        self.hangars = []
        self.parse_hangars(data['hangars'])
        self.fits_required: dict
        self.fits_required = data.get('fits_required', {})
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
            except EOFError or ValueError:
                choice = int(input("1. Update Hangar\n2. Update Config\n3. Return2\n $> "))

    def update_hangars(self) -> None:
        """
        Update Hangars
        :return: None
        """
        choice_not_made = True
        print("Choose the relevant hangar or container (if possible)")
        while choice_not_made:
            for index in range(0, len(self.hangars)):
                print("{}. {}".format(index, self.hangars[index].name))

            choice = int(input("which hangar is being updated? (0, {}) \n >$ ".format(len(self.hangars) - 1)))
            if choice in range(0, len(self.hangars)):
                choice_not_made = False

            self.hangars[choice].input_hangar_items()
            self.hangars[choice].update_date_updated()

    def update_config(self):
        """
        Update Config
        :return: None
        """
        # choice_not_made = True
        #
        # while choice_not_made:
        #     for index in range(0, len(self.hangars)):
        #         print("{}. {}".format(index, self.hangars[index]))
        #     choice: int
        #     choice = int(input("which hangar is being updated? (0, {}) \n >$ ".format(len(self.hangars))))
        #     if choice in range(0, len(self.hangars)):
        #         choice_not_made = False

        choice_not_made: bool = True
        choice = None
        while choice_not_made:
            print("1. Global Fitting Modifier ({})".format(self.config.Global_Fitting_Multiplier))
            print("2. Global Material Modifier ({})".format(self.config.Global_Material_Multiplier))

            choice = input("Which modifier to change? >$ ")

            if int(choice) in [1, 2]:
                choice_not_made = False
        # todo: error checking/handling/exception
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

    def get_all_items(self) -> [hangar_item]:
        """
        Gets all items from all hangars
        :return: list of all items in the station
        """
        contained_items_list: []

        hangar: storage_area
        return [items for hangar in self.hangars for items in hangar.contained_items]

    def update_date_updated(self):
        pass


def method_is_menu_function(f):
    f.__is_menu_function = True
    return f


class test_free_inventory:
    """
    Master class for grouping all test free stations
    Long live the rifters and tunnelsnakes
    """

    def __init__(self):
        self.stations = []
        self.find_station_files()

    def choose_station(self):
        while True:
            for i in range(0, len(self.stations)):
                print("{}\t{}".format(i, self.stations[i].station))
            choice = int(input("Make choice for station >$ "))
            if 0 <= choice < len(self.stations):
                return self.stations[choice]
            else:
                print("Invalid choice")

    @method_is_menu_function
    def list_stations(self) -> None:
        """List all stations and their GFM and GMM
        :return: None
        """

        station: test_free_station
        for station in self.stations:
            print("Name of Station : {}".format(station.station))
            print("Global Fitting Modifier : {}".format(
                station.config.Global_Fitting_Multiplier))
            print("Global Material Modifier : {}\n".format(
                station.config.Global_Material_Multiplier))
        return

    @method_is_menu_function
    def update_fit(self, fit_exists = True) -> str:
        """Update fits"""
        lines = easygui.textbox(msg="Input the copy paste of the fit.  Must be EFT format.\nDon't fuck it up").split(
            '\n')
        fit_translator.make_fit_file(lines)
        return fit_translator.new_get_fit_name(lines)

    @method_is_menu_function
    def update_required_fits(self, fit_name=None):
        """Update Required Fit number"""
        station: test_free_station = self.choose_station()

        if fit_name is not None:
            print("Fit name is {}".format(fit_name))
        else:
            print("What is fit name?")
            fit_choices = [fit for fit in station.fits_required.keys()]
            fit_name = easygui.choicebox(msg = "What is the fit name?", choices=fit_choices)

        new_qty = -1
        while type(new_qty) == int and new_qty <= -1:
            new_qty = input("What is the new quantity needed? (Old : {})".format(station.fits_required.get(fit_name, "None")))
        station.fits_required[fit_name] = new_qty
        self.save_stations_to_json_file()
        return None

        # lines = easygui.textbox(
        #     msg="Input the copy paste of the fit.  Must be EFT format").split('\n')
        # for line in lines:
        #     self.contained_items.append(hangar_item(copy_paste_data=line))

    @method_is_menu_function
    def create_new_fit(self) -> None:
        """Create new fit"""
        self.update_required_fits(fit_name= self.update_fit(fit_exists = False))
        # self.save_stations_to_json_file() # This is not needed as it is done in updated_required
        return None

    @method_is_menu_function
    def update_station(self) -> None:
        """Updates a station's GMM, GFM or Hangars
        :return: None
        """
        print("Choose which station to update")

        for i in range(0, len(self.stations)):
            print("{}\t{}".format(i, self.stations[i].station))
        choice = int(input("Make choice for station >$ "))
        if 0 <= choice < len(self.stations):
            self.stations[choice].update_hangars_config()
        self.save_stations_to_json_file()

        return

    @method_is_menu_function
    def make_new_station(self) -> None:
        """Makes a new station
        User has to do some input
        Saves to *.stn file
        :return: None
        """
        station_name = input("Name of Station?")
        station_dict = {'station': station_name,
                        'config': {
                            "Global_Fitting_Multiplier": float(input("What is global fitting multiplier?")),
                            "Global_Material_Multiplier": float(input("What is global material multiplier?")),

                        },
                        'hangars': [],
                        'fits_required': {},
                        }

        new_station = test_free_station(station_dict)
        self.stations.append(new_station)
        self.save_stations_to_json_file()

    def find_station_files(self) -> None:
        for files_to_open in self.get_stn_files():
            self.stations.append(self.parse_stn_file(files_to_open))

    def get_stn_files(self, straighttomem=False) -> [str]:
        """
        Deletes all stations in memory and then gets the ones from *.stn files
        :type straighttomem: boolean if we want to put it directly to the object
        :return:
        """
        self.stations = []
        if not straighttomem:
            return ["./stations/" + station for station in os.listdir("./stations")]
        else:
            self.stations = ["./stations/" + station for station in os.listdir("./stations")]
            return

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

    @method_is_menu_function
    def create_new_station_hangar(self):
        """Creates new station hangar (Not implemented)
        """
        # New station hangar
        self.save_stations_to_json_file()

    @method_is_menu_function
    def get_materials_for_items_in_hangar(self) -> None:
        """Get all items in hangar
        :return: None
        """
        self.menu_choose_station().menu_choose_hangar().display_all_items_in_hangar()
        return None

    @method_is_menu_function
    def display_and_calculate_required_materials(self):
        """Calculate and save required materials for required fits
        Calculates the required materials by:
        1. Getting fits for the station
        2. Getting the
            a. Amount of fits required
            b. Amount of reserve fits required (GFM)
            c. Amount of materials required (Using GMM)
        :return: None, it will print and display the results
        """

        selected_station = self.menu_choose_station()

        fits_needed = selected_station.fits_required  # Get a copy of the fits from the selected station

        # Get and parse required fits allocated to station
        # Get fit
        # Parse fit into useable fit --> qty

        from math import ceil
        req_itemised_fits_list = []
        reserve_itemised_fits_list = []
        materials_required_list = []

        fit: dict
        # Get total amount of fits required for station
        req_itemised_fits_list = fit_translator.get_total_order(
            fit_translator.get_order(["{}.fit {}".format(fitname, fits_needed[fitname]) for fitname in fits_needed]))
        # Using GFM, we get the reserve fits
        # This is on top of the required fits
        reserve_itemised_fits_list = fit_translator.get_total_order(
            fit_translator.get_order(["{}.fit {}".format(fitname, ceil(
                fits_needed[fitname] * float(selected_station.config.Global_Fitting_Multiplier))) for fitname in
                                      fits_needed]))

        # Using GMM, we will get the total materials needed in order to build a new batch of ships
        # that would replace these
        materials_required_list = fit_translator.get_total_order(
            fit_translator.get_order(["{}.fit {}".format(fitname, ceil(
                fits_needed[fitname] * float(selected_station.config.Global_Fitting_Multiplier) * float(
                    selected_station.config.Global_Material_Multiplier))) for fitname in fits_needed]))

        materials_required_dictlist = []
        item: str
        print("Computing material requirements")
        for item in materials_required_list:
            # Get the blueprint details
            material_to_be_extended_list_dict = fuzzworks.get_manufacturing_materials(
                fuzzworks.get_blueprint_details(fuzzworks.get_single_id(item[:-1 * (len(item.split(" ")[-1]) + 1)])))

            for dictitem in material_to_be_extended_list_dict:
                dictitem['quantity'] = float(item.split(" ")[-1]) * dictitem['quantity']

                for material_req_item in materials_required_dictlist:  # if there is a material already in the materials
                    # required, add it in
                    if dictitem['typeid'] == material_req_item['typeid']:
                        material_req_item['quantity'] += dictitem['quantity']
                        break
                    else:
                        continue
                else:
                    materials_required_dictlist.append(dictitem)  # if not, we add it in at the end
        """End of materials section"""
        # Save these to file

        required_items_for_build = dict

        # Subtracting currently held stuff from fits needed

        """******* Setting up net dictionaries *********"""

        net_req_itemised_fits_dict = {}
        net_reserve_itemised_fits_dict = {}
        net_materials_required_dict = {}

        for ind_item in req_itemised_fits_list:
            print(ind_item)
            key, value = fit_translator.split_item_qty(ind_item)
            net_req_itemised_fits_dict[key] = value
        req_itemised_fits_list = dict(net_req_itemised_fits_dict)
        for ind_item in reserve_itemised_fits_list:
            key, value = fit_translator.split_item_qty(ind_item)
            net_reserve_itemised_fits_dict[key] = value
        reserve_itemised_fits_list = dict(net_reserve_itemised_fits_dict)

        net_materials_required_dict = {entry['name']: entry['quantity'] for entry in materials_required_dictlist}
        materials_required_dictlist = dict(net_materials_required_dict)
        """******* Finish setting up net dictionaries *********"""

        materials_required_list_to_dict = {}
        for list_item in materials_required_list:
            materials_required_list_to_dict[list_item.split(" ")[0]] = int(list_item.split(" ")[-1])

        # Compare items with what you have vs what you should have
        stored_hangar_item: hangar_item
        for stored_hangar_item in selected_station.get_all_items():
            if stored_hangar_item.name in fits_needed.keys():  # fits
                print(stored_hangar_item.quantity)
                fits_needed[stored_hangar_item.name] -= stored_hangar_item.quantity
            if any(stored_hangar_item.name in required_mat for required_mat in materials_required_list):  # fits
                matching_item_names = [matched_items for matched_items in materials_required_list if
                                       stored_hangar_item.name in matched_items]
                for matching_ind_items in matching_item_names:
                    k, v = fit_translator.split_item_qty(matching_ind_items)
                    net_req_itemised_fits_dict[k] -= v
                    net_reserve_itemised_fits_dict[k] -= v
            if any(stored_hangar_item.name in required_mat for required_mat in net_materials_required_dict):  # fits
                matching_item_names = [matched_items for matched_items in net_materials_required_dict if
                                       stored_hangar_item.name in matched_items]
                for matching_ind_items in matching_item_names:
                    k, v = fit_translator.split_item_qty(matching_ind_items)
                    net_materials_required_dict[k] -= v
        # End of total hangar comparation

        with open("./required_items/{}.reqmat".format(selected_station.station), 'w') as reqmat_file:

            reqmat_file.write("Fits required to be built for station {}\n\n".format(selected_station.station))
            reqmat_file.write("Required Items:quantity\n")
            for key, value in fits_needed.items():
                reqmat_file.write("{}:{}\n".format(key,value))

            reqmat_file.write("\nItems for station {}\n\n".format(selected_station.station))

            reqmat_file.write("Required Items\n")
            reqmat_file.write(
                "{}:{}:{}:{}\n".format("Name", "Existing", "Net Quantity Required", "Planned Quantity Required"))
            for key, value in net_req_itemised_fits_dict.items():
                reqmat_file.write("{}:{}:{}:{}\n".format(key, req_itemised_fits_list[key] - value, value,
                                                         req_itemised_fits_list[key]))

            reqmat_file.write("\n\n\nRequired Reserve Items\n")
            reqmat_file.write(
                "{}:{}:{}:{}\n".format("Name", "Existing", "Net Quantity Required", "Planned Quantity Required"))
            for key, value in net_reserve_itemised_fits_dict.items():
                reqmat_file.write("{}:{}:{}:{}\n".format(key, + reserve_itemised_fits_list[key] - value, value,
                                                         reserve_itemised_fits_list[key]))

            reqmat_file.write("\n\n\nRequired Materials needed\n")
            reqmat_file.write(
                "{}:{}:{}:{}\n".format("Name", "Existing", "Net Quantity Required", "Planned Quantity Required"))
            for key, value in net_materials_required_dict.items():
                reqmat_file.write("{}:{}:{}:{}\n".format(key, materials_required_dictlist[key] - value, value,
                                                         materials_required_dictlist[key]))

        # item: hangar_item # todo add in later version
        # for item in selected_station.get_all_items():
        #     if item.category in ship_type_list and item.quantity == 1:
        #         for fit_item in item.get_fit():
        #             pass

    def display_hangar_items(self):
        pass

    def menu_choose_station(self) -> test_free_station:
        for i in range(0, len(self.stations)):
            print("{}\t{}".format(i, self.stations[i].station))
        choice = int(input("Make choice for station >$ "))
        if 0 <= choice < len(self.stations):
            return self.stations[choice]

    def display_items_from_hangar(self):
        station = self.menu_choose_station()
