from behaviour_mod.behaviour import Behaviour
from robobopy.utils.IR import IR
from utils import *


"""
SearchChargeZone Behaviour

In this behaviour the robot will search the charging zone to recharge the battery
It will move forward until it detects an obstacle, then it will turn a few degrees.
The zone to search is more restricted than the SearchBox and the SearchContainer to avoid accidentaly pick or drop a box in this behaviour.
"""

class SearchChargeZone(Behaviour):
    def __init__(self, robot, supress_list, params):
        super().__init__(robot, supress_list, params)
        self.robot = robot

    # Method that defines when the behaviour should take control
    def take_control(self):
        if not self.supress:
            return (self.robot.battery < self.robot.battery_threshold and not detect_zone(self.robot, zone_id=16) and not self.robot.reaching_aruco)

    # Method that defines the action of the behaviour
    def action(self):
        print("\n----> action: SearchChargeZone")
        self.robot.setEmotionTo(Emotions.TIRED)
        self.robot.playSound(Sounds.MOAN)

        self.supress = False

        # If the robot is carrying a box, slowly
        if self.robot.box:
            speed = 30
            print("... Searching charging zone ... (slow, i'm carrying a box")
        else:
            speed = 50
            print("... Searching charging zone ... (fast, i'm not carrying a box")

        # Supress the other behaviours
        for bh in self.supress_list:
            bh.supress = True

        # Main loop of the behaviour
        while (not self.supress) and (self.robot.battery < self.robot.battery_threshold and not detect_zone(self.robot, zone_id=16)):
            
            # Search in the middle to avoid an accidentaly drop of the box on a zone
            if self.robot.readIRSensor(IR.FrontC) >= 3:
                self.robot.moveWheelsByTime(20, -20, 0.5, wait=True)
            elif self.robot.readIRSensor(IR.FrontLL) >= 8:
                self.robot.moveWheelsByTime(-20, 20, 0.5, wait=True)
            elif self.robot.readIRSensor(IR.FrontRR) >= 8:
                self.robot.moveWheelsByTime(20, -20, 0.5, wait=True)
            
            self.robot.moveWheels(speed, speed)

            self.robot.wait(0.1)
