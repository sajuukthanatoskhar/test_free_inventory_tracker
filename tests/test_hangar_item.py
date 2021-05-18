import pytest
import inventory_tracker



def test_hangar_item_creation():

    line = "Javelin S	1,263,509	Charge	3,158.77 m3	66,271,047.05 ISK"
    hangaritem = inventory_tracker.hangar_item(line)
    if hangaritem.name == "Javelin S" and hangaritem.qty == 1263509\
            and hangaritem.volume == 3158.77 and hangaritem.category == "Charge":
        assert True
    else:
        assert False