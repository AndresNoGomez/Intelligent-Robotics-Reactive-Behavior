#
# Comportamiento que si ve una pared cerca, se para
#

from behaviour_mod.behaviour import Behaviour
from robobopy.utils.IR import IR
from robobopy.utils.Sounds import Sounds

class FindWall(Behaviour):
    def __init__(self, robot, supress_list, params):
        super().__init__(robot, supress_list, params)
        self.front_distance = 50 #Valor de IR para que se active
        self.goal = 500 #Valor de IR para que pare

    #Método que define cuándo se activa el comportamiento
    def take_control(self):
        if not self.supress:
            return self.robot.readIRSensor(IR.FrontC) >= self.front_distance

    #Método que define qué hace el comportamiento
    def action(self):
        print("----> control: FindWall")
        self.supress = False
        for bh in self.supress_list:
            bh.supress = True

        self.robot.sayText("Me acerco a la pared")
        print("----> action: FindWall")
        speed = -5
        while (self.robot.readIRSensor(IR.FrontC) < self.goal) and (not self.supress):
            self.robot.moveWheels(speed, speed)
            self.robot.wait(0.1)
        
        self.robot.stopMotors()
        self.robot.sayText("Ya estoy")
        self.robot.playSound(Sounds.LAUGH)  
        self.set_stop()
