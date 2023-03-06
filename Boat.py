import math
from Variables import *

class Boat:
    def __init__(self, hulls, sails, wind):
        self.hulls = hulls #array of hulls
        self.sails = sails
        self.wind = wind

        #Forces on the boat
        self.forces = {"sails":Vector(Angle(1,90),0), "hulls":Vector(Angle(1,90),0)}

        #current boat velocity
        self.velocity = Vector(Angle(1,90),0)

        #current boat position
        self.position = Vector(Angle(1,90),0)


    def globalAparentWind(self):
        # returns global aparent wind on boat
        return self.wind-self.velocity

    #TODO: maybe have a method for getting true wind angle from apparent wind for acutal boat