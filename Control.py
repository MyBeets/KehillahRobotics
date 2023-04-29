# I'll start out with a simple test that aims to maintain a certain direction
import math
from Variables import *

def printA(x):
    x %= 360
    if x > 180:
        x = -180 + x-180
    return x


class Controler():
    def __init__(self,Boat, waypoint):
        self.boat = Boat
        self.waypoint = waypoint
    def update(self,dt,rNoise= 2,stability=1): # less noise = faster rotation, stability tries to limit angular momentum
        self.updateRudder(rNoise,stability)
        self.updateSails()
    def updateRudder(self,rNoise,stability):
        dx = self.waypoint[0]-self.boat.position.xcomp()
        dy = self.waypoint[1]-self.boat.position.ycomp()
        target_angle = Angle(1,math.atan2(dy,dx)*180/math.pi)
        current_angle = self.boat.linearVelocity.angle
        dtheta = (target_angle - current_angle).calc()
        rotV = self.boat.rotationalVelocity*180/math.pi *0.03
        # coeff = 1-(1/(dtheta.calc()*(1/rotV)+1))
        dtheta = printA(dtheta)
        coeff = math.atan((dtheta)/40) - rotV/stability
        self.boat.hulls[-1].angle = Angle(1,-10*coeff)*rNoise
        #print(dtheta,target_angle,coeff,-10*coeff,self.boat.hulls[-1].angle)
    
    def updateSails(self):
        print(Angle.norm(self.boat.globalAparentWind().angle+Angle(1,180)))
        self.boat.sails[0].angle = (self.boat.globalAparentWind().angle+Angle(1,180)-Angle(1,45))
