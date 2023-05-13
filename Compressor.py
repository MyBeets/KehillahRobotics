from Foil import foil
from Variables import *
# from Boat import Boat
import copy
import math
from Control import *
from tqdm import tqdm

def roundNum(x):
    return round(x*10000)/10000
def printA(x):
    x %= 360
    if x > 180:
        x = -180 + x-180
    return x

def generatePolars(boat,filename):
    boat = copy.deepcopy(boat)
    cont = Controler(boat,[])
    # speeds = [0.3,0.5,1,1.5,2,2.5,3,3.5,4,4.5,5,5,5.5,6,6.5,7] #.58 kt to 13.6kt
    speeds = [1] #.58 kt to 13.6kt
    output = open(filename + ".pol","w")
    output.write("twa/tws;"+str(speeds).replace(", ", ";")[1:-1] + "\n")
    for aoa in range(-90,90,15):
        comp = []
        for s in speeds:
            #clean slate
            boat.resetValues()
            #Set wind
            boat.wind = Vector(Angle(1,270),s)
            #Boat going in a direction
            boat.angle = Angle(1,aoa)
            cont.setTarget(Angle(1,aoa))

            num =10
            time = 0.01
            for s in tqdm(range(30), desc="Computing "+str(90-aoa)+"..."):
                for ms in range(100): # this must be kept high as to avoid over amplifying innacuracy loops 
                    #We then set optimal sail configuration and all
                    cont.update(time)
                    #update velocities
                    for i in range(num):
                        boat.updateSailForcesandMoments(time/num)
                        boat.updateHullForcesandMoments()
                        boat.updateLinearVelocity(time/num)
                        boat.updateRotationalVelocity(time/num)
            F = boat.linearVelocity#boat.forces["sails"]#.norm #+boat.forces["hulls"]
            #print("(",aoa,",",F,")")
            F = abs(F * Vector(boat.angle,F.norm))#*math.cos(aoa*math.pi/180)
            comp.append(F)
            #print("(",math.cos(aoa*math.pi/180)*F,",",math.sin(aoa*math.pi/180)*F,")")
        output.write(str(90-aoa) + ";"+str(comp).replace(", ", ";")[1:-1] + "\n")
    output.close()





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