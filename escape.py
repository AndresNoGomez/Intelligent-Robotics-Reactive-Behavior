from behaviour_mod.behaviour import Behaviour
from robobopy.utils.IR import IR
from robobopy.utils.Emotions import Emotions


class Escape(Behaviour):
    def __init__(self, robot, supress_list, params):
        super().__init__(robot, supress_list, params)
        self.threshold = 100  # Threshold to lateral IRs
        self.thresholdF = 70  # Threshold to Front IR
        self.ir_values = {
            "left": 0,
            "right": 0,
            "front": 0,
        }

    # Method that defines when the behaviour should take control
    def take_control(self):
        self.ir_values = {
            "left": self.robot.readIRSensor(IR.FrontL),
            "front": self.robot.readIRSensor(IR.FrontC),    
            "right": self.robot.readIRSensor(IR.FrontR),
        }
        return (self.ir_values["left"] > self.threshold and self.ir_values["front"] > self.thresholdF) or (self.ir_values["right"] > self.threshold and self.ir_values["front"] > self.thresholdF)

    # Method that defines the action of the behaviour
    def action(self):
        print("\n----> action: Escape")
        self.robot.setEmotionTo(Emotions.AFRAID)
        self.supress = False

        # Supress the behaviours with less priority
        for bh in self.supress_list:
            bh.supress = True

        # Escape 
        if self.ir_values["left"] > self.threshold and self.ir_values["front"] > self.thresholdF:
            print("Obstacle at left. Going to right")
            self.robot.moveWheelsByTime(-35, -15, 2, wait=True)
        elif self.ir_values["right"] > self.threshold and self.ir_values["front"] > self.thresholdF:
            print("Obstacle at right. Going to left")
            self.robot.moveWheelsByTime(-15, -35, 2, wait=True)
        
        # Allow the behaviours with less priority to take control if necessary
        for bh in self.supress_list:
            bh.supress = False
