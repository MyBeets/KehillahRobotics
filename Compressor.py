from Variables import *
from Control import *
import copy
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
    cont = Controler(boat)
    #speeds = [0.3,0.5,1,1.5,2,2.5,3,3.5,4,4.5,5,5.5,6,6.5,7] #.58 kt to 13.6kt
    speeds = [0.3,1,3,5,5.5,6,6.5,7]
    output = open(filename + ".pol","w")
    output.write("twa/tws;"+str(speeds).replace(", ", ";")[1:-1] + "\n")
    for aoa in range(90,-91,-10):#3
        #if True:
        #aoa = 0
        comp = []
        for s in tqdm(speeds, desc="Computing "+str(90-aoa)+"..."):
            #clean slate
            boat.resetValues()
            #Set wind
            boat.wind = Vector(Angle(1,270),s)
            #Boat going in a direction
            boat.angle = Angle(1,aoa)
            # cont.setTarget(Angle(1,aoa))

            num =20
            time = 0.01
            for s in range(2):
                for ms in range(100): # this must be kept high as to avoid over amplifying innacuracy loops 
                    #We then set optimal sail configuration and all
                    # cont.update(time)
                    cont.updateRudderAngle(2,1,Angle(1,aoa))
                    cont.updateSails()
                    #update velocities
                    for i in range(num):
                        boat.updateSailForcesandMoments(time/num)
                        boat.updateHullForcesandMoments()
                        boat.updateLinearVelocity(time/num)
                        boat.updateRotationalVelocity(time/num)
                    boat.angle = Angle(1,aoa)
            F = boat.linearVelocity#boat.forces["sails"]#.norm #+boat.forces["hulls"]
            #print(F.xcomp(),F.ycomp(),Vector(boat.angle,F.norm).xcomp(),Vector(boat.angle,F.norm).ycomp())
            F = abs(F * Vector(boat.angle,F.norm))#*math.cos(aoa*math.pi/180)
            # print("(","f",",",F,")")
            comp.append(round(F*100000)/100000)
            #print("(",math.cos(aoa*math.pi/180)*F,",",math.sin(aoa*math.pi/180)*F,")")
        #print(comp)
        output.write(str(90-aoa) + ";"+str(comp).replace(", ", ";")[1:-1] + "\n")
    output.close()





def Compressor(boat,filename):
    # here we generate polars and find stuff like best VMG
    pass