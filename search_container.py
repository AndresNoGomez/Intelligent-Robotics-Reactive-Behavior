from behaviour_mod.behaviour import Behaviour
from robobopy.utils.IR import IR
from utils import *

"""
SearchContainer Behaviour

In this behaviour the robot will search for a container to deposit the box.
It will move forward until it detects an obstacle, then it will turn a few degrees.
"""

class SearchContainer(Behaviour):
    def __init__(self, robot, supress_list, params):
        super().__init__(robot, supress_list, params)
        self.robot = robot

    # Method that defines when the behaviour should take control
    def take_control(self):
        if not self.supress:
            return (self.robot.box and not detect_zone(self.robot))  and self.robot.battery > self.robot.battery_threshold

    # Method that defines the action of the behaviour
    def action(self):
        print("\n----> action: SearchContainer")

        zone_id = self.robot.box_to_zone.get(int(self.robot.box), 16)
        print("... Searching container ", zone_id, " to deposit the box ", self.robot.box, " ...")
        self.robot.setEmotionTo(Emotions.NORMAL)

        self.supress = False

        # The robot is carrying a box, so it will move slower
        speed = 35

        # Supress the behaviours with less priority
        for bh in self.supress_list:
            bh.supress = True


        # Main loop of the behaviour
        while (not self.supress) and (self.robot.box and not detect_zone(self.robot)) and self.robot.battery> self.robot.battery_threshold:             
            
            # If the robot detects an obstacle in front of it, it will turn a few degrees
            if self.robot.readIRSensor(IR.FrontC) >= 7:
                self.robot.moveWheelsByTime(20, -20, 0.7, wait=True)
            
            self.robot.moveWheels(speed, speed)

        
            self.robot.wait(0.1)
        
        # Allow the behaviours with less priority to take control if necessary
        for bh in self.supress_list:
            bh.supress = False

