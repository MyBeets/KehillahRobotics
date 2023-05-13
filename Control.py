# I'll start out with a simple test that aims to maintain a certain direction
import math
from Variables import *

def printA(x):
    x %= 360
    if x > 180:
        x = -180 + x-180
    return x

def aoa(x):
    return -0.5*printA(x)+44#4/9

class Controler():
    def __init__(self,Boat, waypoint):
        self.boat = Boat
        self.waypoint = waypoint
        self.target_angle = Angle(1,0)
    def plan(self,plantype,waypoints):
        #type can either E(ndurance), S(tation Keeping), Pr(ecision Navigation), P(ayload),
        plantype = plantype.lower()
        if plantype == "e":
            # Format of waypoints is as such
            # 4 Buoy in order of navigation
            pass
        elif plantype == "s":
            #4 Buoy in any order
            pass
        elif plantype == "Pr":
            # 4 Buoy in order of navigation
            pass
    def setTarget(self,angle):
        self.target_angle = angle

    def update(self,dt,rNoise= 2,stability=1): # less noise = faster rotation, stability tries to limit angular momentum
        self.updateRudder(rNoise,stability)
        self.updateSails()
    def updateRudder(self,rNoise,stability):
        # dx = self.waypoint[0]-self.boat.position.xcomp()
        # dy = self.waypoint[1]-self.boat.position.ycomp()
        # target_angle = Angle(1,math.atan2(dy,dx)*180/math.pi)
        # target_angle = angle
        current_angle = self.boat.linearVelocity.angle
        dtheta = (self.target_angle - current_angle).calc()
        rotV = self.boat.rotationalVelocity*180/math.pi *0.03
        # coeff = 1-(1/(dtheta.calc()*(1/rotV)+1))
        dtheta = printA(dtheta)
        coeff = 2/math.pi * math.atan((dtheta)/40 - rotV/stability)
        self.boat.hulls[-1].angle = Angle(1,-10*coeff)*rNoise
    
    def updateSails(self):
        self.boat.sails[0].setSailRotation(Angle(1,aoa(Angle.norm(self.boat.angle + Angle(1,90)-self.boat.globalAparentWind().angle+Angle(1,180)).calc())))