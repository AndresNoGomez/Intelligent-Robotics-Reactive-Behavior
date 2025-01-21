from behaviour_mod.behaviour import Behaviour
from utils import *

"""
GoToBox Behaviour

In this behaviour the robot will go to the box.
It will center the box in the camera and move forward to pick it up.

"""
class GoToBox(Behaviour):
    def __init__(self, robot, supress_list, params):
        super().__init__(robot, supress_list, params)
        self.front_distance = 5 
        self.goal = 10

    # Method that defines when the behaviour should take control
    def take_control(self):
        if not self.supress:
            return (detect_box(self.robot) and not self.robot.box) and (self.robot.battery> self.robot.battery_threshold)


    # Method that defines the action of the behaviour
    def action(self):
        self.supress = False

        # Supress the behaviours with less priority
        for bh in self.supress_list:
            bh.supress = True

        # Stop the robot before starting the behaviour
        self.robot.stopMotors()

        print("\n----> action: GoToBox")

        # Go directly to the box
        box = detect_box(self.robot)
        print("Found! Going to the box ", box.id)
        self.robot.setEmotionTo(Emotions.SURPRISED)


        # Main loop of the behaviour
        while (box and not self.robot.box) and (not self.supress)  and (self.robot.battery> self.robot.battery_threshold):
            
            # Center the box in the camera
            box = aruco_to_the_middle(self.robot, box)
            
            # If the robot hasn't lost the box, it will move forward
            if box:
                # Aproximate to the box
                picked = aproximate_to_box(self.robot, box)
            
                # If the robot has picked the box, it will stop the behaviour
                if picked:
                    print("Box number ", self.robot.box, " picked!")
                    self.robot.sayText(("Box number", self.robot.box, "picked!"))
                    break


                # Distance to the box
                distancia = box.tvecs['z']

                if distancia > 0.9:
                    self.robot.moveWheelsByTime(50, 50, 2, wait=True)
                elif distancia > 0.5:
                    self.robot.moveWheelsByTime(30, 30, 0.4, wait=True)
                else:
                    self.robot.moveWheelsByTime(30, 30, 0.1, wait=True)


            # Detect the box again
            box = detect_box(self.robot) 
    
            self.robot.wait(0.1)

        # Allow the behaviours with less priority to take control if necessary
        for bh in self.supress_list:
            bh.supress = False

