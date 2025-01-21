from behaviour_mod.behaviour import Behaviour
from utils import *


"""
GoToChargeBattery Behaviour

In this behaviour the robot will go to the recharging zone.
It will center the zone in the camera and move forward to enter in the zone

"""

class GoToChargeBattery(Behaviour):
    def __init__(self, robot, supress_list, params):
        super().__init__(robot, supress_list, params)

    # Method that defines when the behaviour should take control
    def take_control(self):
        if not self.supress:
            return (detect_zone(self.robot, zone_id=16) and self.robot.battery < self.robot.battery_threshold and not self.robot.reaching_aruco)


    # Method that defines the action of the behaviour
    def action(self):
        print("\n----> action: GoToChargeBattery")
        self.supress = False

        # If we are carrying a box, slowly
        if self.robot.box:
            speed = 30 
            print("Found! Going to the charging zone slowly, I'm carrying a box")
        else:
            speed = 50
            print("Found! Going to the charging zone quickly, not carrying a box")
            

        for bh in self.supress_list:
            bh.supress = True

        self.robot.stopMotors()
        self.robot.setEmotionTo(Emotions.TIRED)

        charge_zone = detect_zone(self.robot, zone_id=16)

        # Main loop of the behaviour
        while (charge_zone and self.robot.battery < self.robot.battery_threshold) and (not self.supress):
            
            # Center the aruco in the middle of the camera
            charge_zone = aruco_to_the_middle(self.robot, charge_zone)
            
            if charge_zone:
                battery_charging = aproximate_to_zone(self.robot, charge_zone)

                if battery_charging:
                    print("... Charging battery ...")

                    self.robot.setEmotionTo(Emotions.SLEEPING)
                    self.robot.recharging_battery = True
                    self.robot.wait(7)
                    self.robot.battery = 100
                    self.robot.recharging_battery = False
                    print("Battery charged at 100%")
                    

                distancia = charge_zone.tvecs['z']

                if distancia > 0.9:
                    self.robot.moveWheelsByTime(speed, speed, 2, wait=True)
                elif distancia > 0.5:
                    self.robot.moveWheelsByTime(30, 30, 0.6, wait=True)
                else:
                    self.robot.moveWheelsByTime(20, 20, 0.1, wait=True)

            # Detect again the zone
            charge_zone = detect_zone(self.robot, zone_id=16)
    
            self.robot.wait(0.1)

        # Allow the behaviours with less priority to take control if necessary
        for bh in self.supress_list:
            bh.supress = False

