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
    def __init__(self,Boat, waypoint, polars = "test3.pol"):
        self.boat = Boat
        self.waypoint = waypoint
        self.polars = self.readPolar(polars)
        self.target_angle = Angle(1,0)
        self.course = self.plan("p",waypoint)

    def plan(self,plantype,waypoints):
        course = []
        #type can either E(ndurance), S(tation Keeping), p(ecision Navigation), w(eight/payload),
        if plantype == "e":
            # Format of waypoints is as such
            # 4 Buoy in order of navigation
            pass
        elif plantype == "s":
            #4 Buoy in any order
            pass
        elif plantype == "p":
            # 4 Buoy in order of navigation'
            course.extend(self.leg([self.boat.position.xcomp(), self.boat.position.ycomp()], waypoints[1]))
            course.extend(self.leg(waypoints[1],waypoints[2]))
            course.extend(self.leg(waypoints[2],[(waypoints[0][0]+waypoints[3][0])/2,(waypoints[0][1]+waypoints[3][1])/2]))
        return course

    def leg(self, start, stop):
        angle = math.atan2(stop[1]-start[1],stop[0]-start[0])*180/math.pi
        print(angle)
        return []
    def BestCNM(self, angle, wind): # best course to next mark
        pass
    def VB(self,angle, wind): # reading boat polars
        for i, a in enumerate(self.polar[1:]):
            if a[0] > angle:
                for j, s in enumerate(self.polar[0][1:]):
                    if s > wind:
                        return self.polar[i+1][s+1] #TODO add interpolation
        return -1
            

    def readPolar(self,polar):
        rtn =[]
        text = open(polar).read().split('\n')
        c = "\t"
        if text[0].find(";") != -1:
            c = ";"
        rtn.append([0]+[float(x) for x in text[0].split(c)[1:]])
        for i in text[1:]:
            if i.split(c)[0] != '':
                rtn.append([float(x) for x in i.split(c)])
        return rtn

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