from Foil import foil
from Variables import *
# from Boat import Boat
import copy
import math
def roundNum(x):
    return round(x*10000)/10000

def generateSailPolars(boat,filename):
    boat = copy.deepcopy(boat)
    boat.rotationalVelocity = 0
    for aoa in range(0,180):
        #Set wind
        boat.wind = Vector(Angle(1,180),1)
        #Boat going in a direction
        boat.angle = Angle(1,30)

        boat.sails[0].angle = Angle(1,aoa)
        boat.updateSailForcesandMoments(1)

        F= abs(boat.forces["sails"].xcomp())
        print("(",math.cos(aoa*math.pi/180)*F,",",math.sin(aoa*math.pi/180)*F,")")

def generatePolars(boat,filename):
    generateSailPolars(boat,filename)
    return
    boat = copy.deepcopy(boat)
    boat.rotationalVelocity = 0
    for aoa in range(0,-180,-1):
        #Set wind
        boat.wind = Vector(Angle(1,180),1)
        #Boat going in a direction
        boat.angle = Angle(1,aoa)
        # boat.linearVelocity = Vector(Angle(1,aoa),1)

        #We then set optimal sail configuration
        # boat.sails[0].angle = Angle(1,38)
        boat.updateSailForcesandMoments()
        # boat.updateHullForcesandMoments()
        # F= abs((boat.forces["sails"]+boat.forces["hulls"]).xcomp())4
        F= abs((boat.forces["sails"]).xcomp())
        #print(boat.forces["sails"])
        print("(",math.cos(aoa*math.pi/180)*F,",",math.sin(aoa*math.pi/180)*F,")")
        # for sAOA in range(0,90):
        #     boat.sails[0].angle = Angle(1,sAOA)
        #     boat.updateSailForcesandMoments()
        #     print("(",sAOA,",",boat.forces["sails"].norm,")")
        # break





def Compressor(boat,filename):
    boat = copy.deepcopy(boat)
    speeds = 1
    #file = open(filename,"w+")
    sails = []
    hulls = []
    rudder= []
    for aoa in range(0,180):
        hullForces = Vector(Angle(1,0),0)
        sailForces = Vector(Angle(1,0),0)
        boat.rotationalVelocity = 0
        boat.angle = Angle(1,0)
        boat.linearVelocity = Vector(Angle(1,180+aoa),1)
        for idx in range(len(boat.hulls)-1):
            force = boat.hullLiftForce(idx) + boat.hullDragForce(idx)
            hullForces += force
        
        rudderForce = boat.hullLiftForce(len(boat.hulls)-1) + boat.hullDragForce(len(boat.hulls)-1)
        
        boat.linearVelocity = Vector(Angle(1,0),0)
        boat.wind = Vector(Angle(1,180+aoa),1)
        for idx, s in enumerate(boat.sails):
            s.angle = Angle(1,0)
            force = boat.sailLiftForce(idx) + boat.sailDragForce(idx)
            sailForces += force

        hulls.append("(" +str(aoa)+ ","+str(roundNum(hullForces.xcomp()))+")")
        sails.append("(" +str(aoa)+ ","+str(roundNum(sailForces.xcomp()))+")")
        rudder.append("(" +str(aoa)+ ","+str(roundNum(rudderForce.ycomp()-rudderForce.xcomp()*10))+")")
        # hulls.append("(" + str(roundNum(hullForces.norm))+ ","+str(roundNum(hullForces.angle.calc()))+")")
    # print(str(hulls).replace("'",""))
    #print(str(rudder).replace("'",""))