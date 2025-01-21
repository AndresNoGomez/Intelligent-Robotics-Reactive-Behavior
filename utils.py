import time
from robobopy.utils.IR import IR
from robobopy.utils.Emotions import Emotions
from robobopy.utils.Sounds import Sounds

def detect_box(robot):
    """
    Function that returns the aruco tag of the box if it is detected, otherwise returns False
    """
    aruco = robot.readArucoTag()
    
    if aruco.id not in ['', '3', '8', '9', '16']:
        return aruco
    else:
        return False
    

def detect_zone(robot, zone_id=None):
    """
    Function that returns the arugo tag of the target zone if it is detected, otherwise returns False
    """
    # If there is no box and no zone_id, return False
    if not robot.box and not zone_id:
        return False

    box_id = int(robot.box) 

    # If there is no zone_id, get the zone_id corresponding to the box_id, if it is not in the dictionary, use 16
    if not zone_id:
        zone_id = robot.box_to_zone.get(box_id, 16)

    aruco = robot.readArucoTag()

    # If the detected aruco is the one that corresponds to the zone_id, return it
    if aruco and str(aruco.id) == str(zone_id):
        return aruco
    else:
        return False


def aruco_to_the_middle(robot, aruco):
    """
    Function that center the aruco tag in the middle of the camera
    """
    # Obtain the middle of the box
    middle_box = (aruco.cor3['x'] + aruco.cor4['x']) / 2

    # Variables to control the direction of the movement
    if middle_box < 235:
        dir = -4
        izquierda = True
    else:
        dir = 4
        izquierda = False

    # Move the robot until the aruco tag is in the middle of the camera
    while ((middle_box < 230) if izquierda else middle_box > 240) and aruco:

        robot.moveWheelsByTime(dir, -dir, 0.1, wait=True)
        
        # Update the middle of the box
        if not robot.box:
            aruco = detect_box(robot) 
        else:
            aruco = detect_zone(robot)

        # If the aruco tag is detected again, update the middle of the box, otherwise, finish the loop because the robot has lost the aruco tag
        if aruco:
            middle_box = (aruco.cor3['x'] + aruco.cor4['x']) / 2

        robot.wait(0.1)

    return aruco



def aproximate_to_box(robot, aruco):
    """
    Function that returns True if has catched the box or false if not
    """
    # Thresholds to approach the box
    umbralIR = 8
    umbralAZ = 0.4


    # If the robot is close to the box and the aruco tag is in the correct position, catch the box
    if robot.readIRSensor(IR.FrontC)>umbralIR and aruco.tvecs['z'] < umbralAZ:
            
            robot.setEmotionTo(Emotions.LAUGHING)
            
            # Do not interrupt going to recharge baterry if the robot is going to catch the box
            robot.reaching_aruco = True

            robot.moveWheelsByTime(30, 30, 1.8, wait=True)

            # Establish the box that the robot has caught
            robot.box = aruco.id
            
            # Allow the robot to go to recharge the battery again
            robot.reaching_aruco = False

            return True
    else:
        return False
    

def aproximate_to_zone(robot, aruco):
    """
    Function that returns True if the robot has reached the target zone, otherwise returns False
    """

    # Thresholds to approach the zone
    umbralIR = 8
    umbralAZ = 0.4

    
    if robot.readIRSensor(IR.FrontC)>umbralIR and aruco.tvecs['z'] < umbralAZ:

        # Do not interrupt going to recharge baterry if the robot is entering the zone
        robot.reaching_aruco = True

        # Aproximate to the zone 16 more (its smaller than the others)
        if int(aruco.id) == 16:
            robot.moveWheelsByTime(15, 15, 2, wait=True) 

            # If the robot has a box, and have leaved it in the zone 16, robot.box = False
            if robot.box and int(robot.box) not in [2, 6, 1, 4, 7, 5]:
                robot.box = False


        # Other zones
        else:
            robot.setEmotionTo(Emotions.LAUGHING)
            robot.moveWheelsByTime(15, 15, 1.5, wait=True)
            robot.box = False

        robot.reaching_aruco = False

        return True
    else:
        return False



def thread_battery(robot):
    """
    Function that simulates the battery consumption of the robot
    """

    while True:

        # For each second, the battery decreases by 1%
        time.sleep(1)

        if robot.battery > 0:
            robot.battery -= 1
            
        # Print the battery level
        if int(time.time()) % 7 == 0:
            if not robot.recharging_battery:
                print(f"Battery level: {robot.battery}%")
