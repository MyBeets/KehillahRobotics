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
    def update(self,dt,rNoise= 40,stability=1): # less noise = faster rotation, stability tries to limit angular momentum
        dx = self.waypoint[0]-self.boat.position.xcomp()
        dy = self.waypoint[1]-self.boat.position.ycomp()
        target_angle = Angle(1,math.atan2(dy,dx)*180/math.pi)
        current_angle = self.boat.linearVelocity.angle
        dtheta = (target_angle - current_angle).calc()
        rotV = self.boat.rotationalVelocity*180/math.pi *0.03
        # coeff = 1-(1/(dtheta.calc()*(1/rotV)+1))
        dtheta = printA(dtheta)
        coeff = math.atan((dtheta)/rNoise) - rotV/stability
        self.boat.hulls[-1].angle = Angle(1,-10*coeff)*2

        self.boat.sails[0].angle = (Angle(1,45) - ((self.boat.wind.angle+Angle(1,180)) - self.boat.angle))*-1
        # if dtheta.calc() > 0:
        #     self.boat.hulls[-1].angle = self.boat.hulls[-1].angle*-1
        print(dtheta,target_angle,coeff,-10*coeff,self.boat.hulls[-1].angle)
        
        #self.boat.hulls[-1].angle += dtheta*dt
