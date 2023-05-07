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
    data = {}
    for baoa in range(-90,90):
    #if True:
        #baoa = 0
        mAngle = 0
        mValue = 0
        for aoa in range(0,90-baoa):
            #Set wind
            boat.wind = Vector(Angle(1,270),1)
            #Boat going in a direction
            boat.angle = Angle(1,baoa)
            boat.sails[0].angle = Angle(1,aoa)

            # boat.sails[0].angle = Angle(1,aoa)
            #F = boat.sails[0].liftForce(boat.sailAparentWind(0)).xcomp()
            boat.updateSailForcesandMoments(1)
            boat.updateHullForcesandMoments()
            F = boat.forces["sails"]#+boat.forces["hulls"]
            #Now we compute how much it contributes to thrust by a simple dot product
            F = abs(F * Vector(boat.angle,F.norm))*math.cos(aoa*math.pi/180)
            #print(F)
            # F= abs(boat.forces["sails"].norm)
            if F > mValue:
                mValue = F
                mAngle = aoa
            #print("(",boat.forces["sails"].xcomp(),",",boat.forces["sails"].ycomp(),")")
            #print("(",math.cos(aoa*math.pi/180)*F,",",math.sin(aoa*math.pi/180)*F,")")
        data[str(baoa)]=mAngle
        print("(",baoa,",",mAngle,")")
        #print("(",math.cos(baoa*math.pi/180)*mAngle,",",math.sin(baoa*math.pi/180)*mAngle,")")
    print(data)


def generatePolars(boat,filename):
    generateSailPolars(boat,filename)
    return
    boat = copy.deepcopy(boat)
    boat.rotationalVelocity = 0
    for aoa in range(-90,90):
        #Set wind
        boat.wind = Vector(Angle(1,180),1)
        #Boat going in a direction
        boat.angle = Angle(1,aoa)
        # boat.linearVelocity = Vector(Angle(1,aoa),1)

        for s in range(30):
            for ms in range(100): # this must be kept high as to avoid over amplifying innacuracy loops 
                # boat.sails[0].angle = Angle(1,38)
                #We then set optimal sail configuration
                boat.sails[0].setSailRotation(boat.globalAparentWind().angle+Angle(1,180)-Angle(1,38))
                num =2
                time = 0.01
                #update velocities
                for i in range(num):
                    boat.updateLinearVelocity(time/num)
                    boat.updateRotationalVelocity(time/num)
                    boat.updateSailForcesandMoments(time/num)
                    boat.updateHullForcesandMoments()
                # boat.updatePosition(time)
                # F= abs((boat.forces["sails"]+boat.forces["hulls"]).xcomp())4
        F= abs((boat.forces["sails"]).xcomp())
        # print("(",s,",",F,")")
        print("(",math.cos(aoa*math.pi/180)*F,",",math.sin(aoa*math.pi/180)*F,")")





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