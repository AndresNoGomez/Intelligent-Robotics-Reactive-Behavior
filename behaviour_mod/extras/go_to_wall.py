#
# Comportamiento que hace que el robot se mueva hacia delante
#

from behaviour_mod.behaviour import Behaviour
from robobopy.utils.IR import IR

class GoToWall(Behaviour):
    def __init__(self, robot, supress_list, params):
        super().__init__(robot, supress_list, params)
        self.goal = 50 #Valor objetivo para el IR

    #Método que define cuándo se activa el comportamiento
    def take_control(self):
        if not self.supress:
            return True

    #Método que define qué hace el comportamiento
    def action(self):
        print("----> control: GoToWall")
        self.supress = False

        speed = 10
        while (self.robot.readIRSensor(IR.FrontC) < self.goal) and (not self.supress):
            self.robot.moveWheels(speed, speed)
            self.robot.wait(0.1)

        self.robot.stopMotors()
