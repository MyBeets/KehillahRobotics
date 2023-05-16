# I'll start out with a simple test that aims to maintain a certain direction
import math
from Variables import *

def printA(x):
    x %= 360
    if x > 180:
        x = -180 + x-180
    return x

def aoa(x):
    x = printA(x)
    if x > 90:
        x = 90 - x%90
    if x < -90:
        x = -(x%90)
    return -0.5*x+44#4/9

class Controler():
    def __init__(self,Boat, waypoint, polars = "test.pol"):
        self.boat = Boat
        self.waypoint = waypoint
        self.polars = self.read(polars)
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

    def readPolar(self,polar):
        rtn =[]
        text = open(polar).read().split('\n')
        c = "\t"
        if text[0].find(";") != -1:
            c = ";"
        rtn.append([0]+[float(x) for x in text[0].split(c)[1:]])
        for i in text[1:]:
            rtn.append([float(x) for x in i.split(c)])
        return rtn
    
    def nearestA(self,a):
        if a < 0:
            a = abs(a)
        if a > 180:
            a = 180-a%180
        for i,an in enumerate(self.polars[1:]):
            if i+1 == len(self.polars)-1 or a <= an[0]:
                return i+1
        print("realy bad angle")
        return -1

    def nearestS(self,s):
        for i,sp in enumerate(self.polars[0][1:]):
            if i == len(self.polars)-1 or s == sp:
                return i+1
            if s < sp:
                return i
        print("realy bad speed")
        return -1
    
    def VB(self,angle,speed):
        return self.polars[self.nearestA(angle)][self.nearestS(speed)]

    def VB2VMG(self,angle,speed):
        #this automaticaly changes from data angles to unit circle by switching the sin with cos
        return math.cos(angle*math.pi/180)*speed

    def VMG(self, angle, speed):
        return abs(self.VB2VMG(angle,self.VB(angle,speed)))
    def MAXVMG(self,ws):
        ws = self.nearestS(ws)
        vmg = 0
        a = [0,0,0,0]
        for an, speed in enumerate(self.polars[1:self.nearestA(self.polars[-1][0]//2)+1]):
            an +=1
            newvmg = self.VB2VMG(self.polars[an][0],speed[ws])
            if newvmg > vmg:
                vmg = newvmg
                a[0] = self.polars[an][0]
                a[2] = 360-self.polars[an][0]
        
        #speeds are negative so we look for the smallest
        vmg = 0
        for an, speed in enumerate(self.polars[self.nearestA(self.polars[-1][0]//2)+1:]):
            an += self.nearestA(self.polars[-1][0]//2)+1
            newvmg = self.VB2VMG(self.polars[an][0],speed[ws])
            if newvmg < vmg:
                vmg = newvmg
                a[1] = self.polars[an][0]
                a[3] = 360-self.polars[an][0]
        return a
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
        angle = Angle.norm(self.boat.angle + Angle(1,90)-self.boat.globalAparentWind().angle+Angle(1,180)).calc()
        self.boat.sails[0].setSailRotation(Angle(1,aoa(angle)))