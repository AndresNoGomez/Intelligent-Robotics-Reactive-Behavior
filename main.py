from robobopy.Robobo import Robobo
from go_to_box import GoToBox
from go_to_container import GoToContainer
from escape import Escape
from search_box import SearchBox
from search_container import SearchContainer
from search_charge_zone import SearchChargeZone
from go_to_charge_battery import GoToChargeBattery
import threading
from utils import thread_battery
import time


def main():
    robobo = Robobo("localhost")
    robobo.connect()

    # Init the pan and tilt
    robobo.moveTiltTo(100, 50)
    robobo.movePanTo(0, 50)
    robobo.moveWheelsByTime(10,10,0.2)

    # Init the variables of the robot
    robobo.box = False # If the robot is carrying a box, the ID, otherwise False
    robobo.battery = 100 # Counter of the battery
    robobo.battery_threshold = 35 # Threshold to go to charge the battery
    robobo.recharging_battery = False # If the robot is recharging the battery
    robobo.reaching_aruco = False # If the robot is reaching an aruco, not interrupt the movement to go to charge the battery
    
    robobo.box_to_zone = {
        2: 3,
        6: 3,
        1: 8,
        4: 8,
        7: 8,
        5: 9
    }
    
    # Params for the threads
    params = {"stop": False}

    # Init the behaviours
    search_box_behaviour = SearchBox(robobo, [], params)
    go_to_box_behaviour = GoToBox(robobo, [search_box_behaviour], params)

    search_container_behaviour = SearchContainer(robobo, [search_box_behaviour,go_to_box_behaviour], params)
    go_to_container_behaviour = GoToContainer(robobo, [search_box_behaviour,go_to_box_behaviour,search_container_behaviour], params)

    search_charge_zone_behaviour = SearchChargeZone(robobo, [search_box_behaviour, go_to_box_behaviour, search_container_behaviour, go_to_container_behaviour], params)
    go_to_charge_battery_behaviour = GoToChargeBattery(robobo, [search_box_behaviour, go_to_box_behaviour, search_container_behaviour, go_to_container_behaviour, search_charge_zone_behaviour], params)

    escape_behaviour = Escape(robobo,[
            search_box_behaviour,
            go_to_box_behaviour,
            search_container_behaviour,
            go_to_container_behaviour,
            search_charge_zone_behaviour,
            go_to_charge_battery_behaviour,
        ],
        params,
    )

    # List with all the threads
    threads = [search_box_behaviour, go_to_box_behaviour, search_container_behaviour, go_to_container_behaviour, escape_behaviour]

    # Initialize the threads
    search_box_behaviour.start()
    go_to_box_behaviour.start()
    search_container_behaviour.start()
    go_to_container_behaviour.start()
    search_charge_zone_behaviour.start()
    go_to_charge_battery_behaviour.start()
    escape_behaviour.start()

    battery_thread = threading.Thread(target=thread_battery, args=(robobo,))
    battery_thread.start()

    # Wait to all stop  
    while not params["stop"]:
        time.sleep(0.1)

    # Wait for the threads to finish
    for thread in threads:
        thread.join()

    robobo.disconnect()

if __name__ == "__main__":
    main()
