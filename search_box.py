from behaviour_mod.behaviour import Behaviour
from robobopy.utils.IR import IR
from utils import *

"""
SearchBox Behaviour

In this behaviour the robot will search for a box. 
It will move forward until it detects an obstacle, then it will turn a few degrees to the right and continue moving forward. 

"""
class SearchBox(Behaviour):
    def __init__(self, robot, supress_list, params):
        super().__init__(robot, supress_list, params)
        self.robot = robot

    # Method that defines when the behaviour should take control
    def take_control(self):
        if not self.supress:
            return (not self.robot.box and not detect_box(self.robot))  and self.robot.battery> self.robot.battery_threshold

    # Method that defines the action of the behaviour
    def action(self):
        print("\n----> action: SearchBox")
        print("... Searching a box ...")
        self.robot.setEmotionTo(Emotions.NORMAL)
        self.supress = False
        
        # Speed of the robot searching a box
        speed = 50


        # Main loop of the behaviour
        while (not self.supress) and (not self.robot.box and not detect_box(self.robot)) and self.robot.battery> self.robot.battery_threshold:
                        
            # If the robot detects an obstacle in front of it, it will turn a few degrees
            if self.robot.readIRSensor(IR.FrontC) >= 4:
                self.robot.moveWheelsByTime(20, -20, 0.9, wait=True)
            self.robot.moveWheels(speed, speed)


            self.robot.wait(0.1)