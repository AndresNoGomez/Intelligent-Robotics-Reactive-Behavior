from behaviour_mod.behaviour import Behaviour
from utils import *


"""
GoToContainer Behaviour

In this behaviour the robot will go to a container.
It will center the container in the camera and move forward to enter in the zone

"""

class GoToContainer(Behaviour):
    def __init__(self, robot, supress_list, params):
        super().__init__(robot, supress_list, params)
        self.front_distance = 5 

    # Method that defines when the behaviour should take control
    def take_control(self):
        if not self.supress:
            return (detect_zone(self.robot) and self.robot.box) and (self.robot.battery > self.robot.battery_threshold)


    # Method that defines the action of the behaviour
    def action(self):
        print("\n----> action: GoToContainer")
        
        self.supress = False

        # Supress the behaviours with less priority
        for bh in self.supress_list:
            bh.supress = True

        # Stop the robot before starting the behaviour
        self.robot.stopMotors()

        # Go directly to the container
        container = detect_zone(self.robot)
        if container:
            print("Found! Going to container num ", container.id) 
            self.robot.setEmotionTo(Emotions.SURPRISED)
        else:
            print("\nWARNING! Focused a different container!")
            print("I will search for the correct container.")

        # Main loop of the behaviour
        while (container and self.robot.box) and (not self.supress) and (self.robot.battery> self.robot.battery_threshold):
            
            # Center the container in the camera
            container = aruco_to_the_middle(self.robot, container)
            
            # If the robot hasn't lost the container, it will move forward
            if container:

                # Save the box to print later the advise
                if self.robot.box:
                    box_id = self.robot.box
                
                # Aproximate to the zone
                dropped = aproximate_to_zone(self.robot, container) 

            
                # If has dropped the box
                if dropped:
                    print("Box num. ",box_id, " dropped on the container num. ", container.id)
                    self.robot.sayText('Box dropped!')
                    break

                # Measure the distance to the aruco
                distancia = container.tvecs['z']

                if distancia > 0.9:
                    self.robot.moveWheelsByTime(30, 30, 1.8, wait=True)
                elif distancia > 0.5:
                    self.robot.moveWheelsByTime(30, 30, 0.6, wait=True)
                else:
                    self.robot.moveWheelsByTime(20, 20, 0.1, wait=True)

            container = detect_zone(self.robot) 
            if not container:
                print("\nWARNING! Focused a different container!")
                print("I will search for the correct container.")

            self.robot.wait(0.1)

        # Allow the behaviours with less priority to take control if necessary
        for bh in self.supress_list:
            bh.supress = False

