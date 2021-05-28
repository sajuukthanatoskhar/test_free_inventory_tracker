import json

import pytest
import inventory_tracker

test_free = inventory_tracker.test_free_inventory()


def test_get_stn_files():
    if len(test_free.get_stn_files()) > 0:
        assert True
    else:
        assert False


def test_parse_stn_file():
    test_free.find_station_files()
    if len(test_free.stations) > 0:
        assert True
    else:
        assert False


test_free2 = inventory_tracker.test_free_inventory()


def test_save_stn_file():
    test_free2.find_station_files()

    test_free2.save_stations_to_json_file()

    file1 = open("./stations/demo_station.stn", 'r')
    file2 = open("./stations/demo.stn", 'r')

    assert sorted(json.load(file1)) == sorted(json.load(file2))






