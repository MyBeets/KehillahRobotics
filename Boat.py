import math
import os

from Foil import foil
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


    def pointingAngle(self):
        #data angle between course and true wind (0 = upwind, 180 = downwind)
        #print(self.wind.angle.data(),self.velocity.angle.data())
        rtn = Angle(0,180-(self.wind.angle.data()-self.velocity.angle.data())) # calculations are done in data type as it's a bit easier
        return rtn

    def apparentWindVelocity(self):
        #law of cosines, suprizingly clean
        # Yes I'm using data angles on purpose here
        return math.sqrt(math.pow(self.wind.speed(),2) + math.pow(self.velocity.speed(),2) + 2*self.wind.speed()*self.velocity.speed()*math.cos(self.pointingAngle().data()*math.pi/180))

    def apparentWindAngle(self):
        # Yes I'm using data angles on purpose here
        return Angle(0,math.acos((self.wind.speed()*math.cos(self.pointingAngle().data()*math.pi/180)+self.velocity.speed())/self.apparentWindVelocity())*180/math.pi)

    def apparentWind(self):
        return Vector(self.apparentWindAngle(),self.apparentWindVelocity())
    #TODO: maybe have a method for getting true wind angle from apparent wind for acutal boat



if __name__ == "__main__":
    pas = 0
    fail = 0
    data_dir = os.path.dirname(__file__) #abs dir
    hull = foil(data_dir+"\\data\\xf-naca001034-il-1000000-Ex.csv", 1, 0.5)
    sail = foil(data_dir+"\\data\\mainSailCoeffs.cvs", 0.128, 1)
    wind = Vector(Angle(1,270),10) # South degree wind 10 m/s
    boat = Boat([hull],[sail],wind)

    pas+= boat.pointingAngle().data() == 0; fail+=boat.pointingAngle().data() != 0
    pas+= boat.apparentWindAngle().data() == 0; fail+=boat.apparentWindAngle().data() != 0

    wind.angle += Angle(1,10) # now wind is going 280* calc south
    pas+= str(boat.wind) == "Vector, norm: 10, Calc: 280"; fail+=str(boat.wind) != "Vector, norm: 10, Calc: 280"
    pas+= boat.wind.angle.data() == 190; fail+=boat.wind.angle.data() != 190
    pas+= boat.pointingAngle().data() == -10; fail+=boat.pointingAngle().data() != -10
    pas+= int(boat.apparentWindAngle().data()*100)/100 == 10; fail+=int(boat.apparentWindAngle().data()*100)/100 != 10

    print("passed: " + str(pas) + ", failed: " + str(fail)+ ", of: " +str(pas+fail))