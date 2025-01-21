#
# Clase que hereda de Thread y se encarga de la gestión de los threads de los 
# comportamientos, y de que la arquitectura funcione correctamente
#

from threading import Thread
import time

# Los comportamientos son extensiones de 'thread', es decir son hilos independientes que se ejecutan simultaneamente
class Behaviour(Thread):
    def __init__(self, robot, supress_list, params, **kwargs):
        super().__init__(**kwargs)
        self.robot = robot
        self.__supress = False
        self.supress_list = supress_list
        self.params = params

    # Metodo abstracto: las subclases tendran que definir el suyo propio obligatoriamente
    def take_control(self):
        pass

    # Metodo Abstracto.
    def action(self):
        pass

    # El metodo run es llamado indirectamente al hacer el metodo behaviour.start() en el main
    #Si algún comportamiento pone params["stop"] a True, se para termina la misión
    def run(self):

        # Mientras params sea false (la mision no ha finalizado) el hilo seguira vigente.
        while not self.params["stop"]:
            # Verificamos continuamente si el comportamiento puede activarse
            while not self.take_control() and not self.params["stop"]:
                time.sleep(0.01)
            # Cuando ya se pueda tomar control, verificamos una ultima vez que params siga en stop y luego ACCION.
            if not self.params["stop"]:
                self.action()


    @property
    # Permite obtener el estado de supress (true o false)
    def supress(self):
        return self.__supress

    @supress.setter
    # Permite alterar el estado de supress
    def supress(self, state):
        self.__supress = state

    def set_stop(self):
        self.params["stop"] = True

    def stopped(self):
        return self.params["stop"]
