# I'll start out with a simple test that aims to maintain a certain direction
import math
from Variables import *
import numpy as np

def printA(x):
    x %= 360
    if x > 180:
        x = -180 + x-180
    return x

def aoa(x):
    x = printA(x)
    if x < 0:
        return -44/90*x
    return 44/90*x
    # return -0.5*x+44#4/9

class Controler():
    def __init__(self,Boat, polars = "test.pol"):
        self.boat = Boat
        self.polars = self.readPolar(polars)
        self.course = []

    def plan(self,plantype,waypoints):
        course = [[self.boat.position.xcomp(),self.boat.position.ycomp()]]# Course will comprise of a sequence of checkpoints creating a good path
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
        angle = Angle(1,math.atan2(stop[1]-start[1],stop[0]-start[0])*180/math.pi)
        apparentAngle = Angle.norm(self.boat.wind.angle+Angle(1,180)-angle)
        steps = 3
        if abs(printA(apparentAngle.calc())) < self.polars[-1][0]: # upwind
            # We want to get to stop only using the upwind BVMG
            v = Vector(Angle(1,round(math.atan2(stop[1]- start[1],stop[0]- start[0])*180/math.pi*10000)/10000),math.sqrt((stop[0]- start[0])**2+(stop[1]- start[1])**2))
            k = Vector(self.boat.wind.angle+Angle(1,180+self.polars[-1][0]),1)
            j = Vector(self.boat.wind.angle+Angle(1,180-self.polars[-1][0]),1)
            D = np.linalg.det(np.array([[k.xcomp(),j.xcomp()],[k.ycomp(),j.ycomp()]]))
            Dk = np.linalg.det(np.array([[v.xcomp(),j.xcomp()],[v.ycomp(),j.ycomp()]]))
            Dj = np.linalg.det(np.array([[k.xcomp(),v.xcomp()],[k.ycomp(),v.ycomp()]]))
            a = Dk/D # number of k vectors
            b = Dj/D # number of j vectors
            k.norm *= a
            j.norm *= b
            ans = [[start[0]+k.xcomp(),start[1]+k.ycomp()],stop]
            return  ans
        elif abs(printA(apparentAngle.calc())) < self.polars[-1][1]: #downwind
            v = Vector(Angle(1,round(math.atan2(stop[1]- start[1],stop[0]- start[0])*180/math.pi*10000)/10000),math.sqrt((stop[0]- start[0])**2+(stop[1]- start[1])**2))
            k = Vector(self.boat.wind.angle+Angle(1,180+self.polars[-1][1]),1)
            j = Vector(self.boat.wind.angle+Angle(1,180-self.polars[-1][1]),1)
            D = np.linalg.det(np.array([[k.xcomp(),j.xcomp()],[k.ycomp(),j.ycomp()]]))
            Dk = np.linalg.det(np.array([[v.xcomp(),j.xcomp()],[v.ycomp(),j.ycomp()]]))
            Dj = np.linalg.det(np.array([[k.xcomp(),v.xcomp()],[k.ycomp(),v.ycomp()]]))
            a = Dk/D # number of k vectors
            b = Dj/D # number of j vectors
            k.norm *= a
            j.norm *= b
            ans = [[start[0]+k.xcomp(),start[1]+k.ycomp()],stop]
            return  ans

        return [stop]
    
    # NOTE: I've desided using best course to next mark while probably the optimal solution brings in a level of complexity that we do not
    # have the time to handle, thus we'll be simplifying.
    # def BestCNM(self, angle, wind): # best course to next mark
    #     # angle is relative to wind
    #     ma = 0
    #     mcnm = 0
    #     for a in range(-180,180):
    #         l = self.VB(Angle(1,a), wind)
    #         CNM = Vector(Angle(1,a),l) * Vector(angle,l)
    #         if mcnm < CNM:
    #             ma = a
    #             mcnm = CNM
    #     axis  = printA(angle.calc())
    #     return [ma,ma-(ma - axis)*2]
    def VB(self,angle, wind): # reading boat polars
        angle =abs(angle.calc())
        angle %= 180
        for i, a in enumerate(self.polars[1:-1]):
            if a[0] > angle:
                for j, s in enumerate(self.polars[0][1:]):
                    if s > wind:
                        return self.polars[i+1][j+1] #TODO add interpolation
        return -1
            

    def readPolar(self,polar):
        rtn =[]
        text = open(polar).read().split('\n')
        c = "\t"
        if text[0].find(";") != -1:
            c = ";"
        rtn.append([0]+[float(x) for x in text[0].split(c)[1:]])
        for i in text[1:-1]:
            if i.split(c)[0] != '':
                rtn.append([float(x) for x in i.split(c)])
        rtn.append([float(x) for x in text[-1].split(";")[1:]])
        return rtn

    def update(self,dt,rNoise= 2,stability=1): # less noise = faster rotation, stability tries to limit angular momentum
        self.updateRudder(rNoise,stability)
        self.updateSails()
    def updateRudder(self,rNoise,stability):
        dx = self.course[1][0]-self.boat.position.xcomp()
        dy = self.course[1][1]-self.boat.position.ycomp()
        target_angle = Angle(1,math.atan2(dy,dx)*180/math.pi)
        #target_angle = angle
        current_angle = self.boat.linearVelocity.angle
        dtheta = (target_angle - current_angle).calc()
        rotV = self.boat.rotationalVelocity*180/math.pi *0.03
        # coeff = 1-(1/(dtheta.calc()*(1/rotV)+1))
        dtheta = printA(dtheta)
        coeff = 2/math.pi * math.atan((dtheta)/40 - rotV/stability)
        self.boat.hulls[-1].angle = Angle(1,-10*coeff)*rNoise
    
    def updateSails(self):
        #angle = Angle.norm(self.boat.angle + Angle(1,90)-self.boat.globalAparentWind().angle+Angle(1,180)).calc()
        wind = self.boat.globalAparentWind()
        angle = Angle(1,math.acos((wind * Vector(self.boat.angle,1))/wind.norm)*180/math.pi)
        if Angle.norm(wind.angle+Angle(1,180)).calc() > angle.calc():
            angle = Angle(1,180) -angle
        angle = angle.calc()
        self.boat.sails[0].setSailRotation(Angle(1,aoa(angle)))