import math
from Variables import *

class Boat:
    def __init__(self, hulls, sails, wind,mass =10):
        self.hulls = hulls #array of hulls
        self.sails = sails
        self.wind = wind
        self.mass = mass # mass in in kg
        self.angle = Angle(1,90) # global rotation of boat and all it's parts
        #Forces on the boat
        self.forces = {"sails":Vector(Angle(1,90),0), "hulls":Vector(Angle(1,90),0)}

        #current boat velocities
        self.linearVelocity = Vector(Angle(1,90),0) # m/s
        self.rotationalVelocity = 0 # radians/s, positive is ccw, negative is cw

        #current boat position
        self.position = Vector(Angle(1,90),0)

    def setPos(self,pos):
        self.position = pos
    def update(self,dt=1): #t is in seconds
        #update forces
        self.updateSailForces()
        self.updateHullForces()
        #update velocities
        self.updateLinearVelocity(dt)
        self.updateRotationalVelocity(dt)
        #update position

    def updateLinearVelocity(self,dt):
        #not using extend is on purpose, extend modifies the variable
        ax = (sum(self.forces["sails"])+sum(self.forces["hulls"])).xcomp()/self.mass
        ay = (sum(self.forces["sails"])+sum(self.forces["hulls"])).ycomp()/self.mass
        a = Vector(Angle(1,round(math.atan2(ay,ax)*180/math.pi*10000)/10000),math.sqrt(ax**2+ay**2))
        a *= dt
        self.linearVelocity += a
    def updateRotationalVelocity(self,t):
        pass

    def updateSailForces(self):
        self.forces["sails"] = Vector(Angle(1,90),0)
        for idx in range(len(self.sails)):
            self.forces["sails"] += self.sailLiftForce(idx)
            self.forces["sails"] += self.sailDragForce(idx)
    def updateHullForces(self):
        self.forces["hulls"] = Vector(Angle(1,90),0)
        for idx in range(len(self.hulls)):
            self.forces["hulls"] += self.hullLiftForce(idx)
            self.forces["hulls"] += self.hullDragForce(idx)



    def sailDragForce(self,idx=0):
        aparentForce = self.sails[idx].dragForce(self.sailAparentWind(idx))
        trueForce = Vector(aparentForce.angle + self.angle + self.sails[idx].angle - Angle(1,90),aparentForce.norm)
        trueForce.angle = Angle.norm(trueForce.angle)
        return trueForce
    def sailLiftForce(self,idx=0):
        aparentForce = self.sails[idx].liftForce(self.sailAparentWind(idx))
        trueForce = Vector(aparentForce.angle + self.angle + self.sails[idx].angle - Angle(1,90),aparentForce.norm)
        trueForce.angle = Angle.norm(trueForce.angle)
        return trueForce

    def hullDragForce(self,idx=0):
        aparentForce = self.hulls[idx].dragForce(self.hullAparentWind(idx))
        trueForce = Vector(aparentForce.angle + self.angle + self.hulls[idx].angle - Angle(1,90),aparentForce.norm)
        trueForce.angle = Angle.norm(trueForce.angle)
        return trueForce
    def hullLiftForce(self,idx=0):
        aparentForce = self.hulls[idx].liftForce(self.hullAparentWind(idx))
        trueForce = Vector(aparentForce.angle + self.angle + self.hulls[idx].angle - Angle(1,90),aparentForce.norm)
        trueForce.angle = Angle.norm(trueForce.angle)
        return trueForce

    def globalAparentWind(self):
        # returns global aparent wind on boat
        return self.wind-self.linearVelocity
    
    def sailAparentWind(self,idx=0):
        # returns local aparent wind on boat (ie: wind angle in perspective of given sail)
        ap = self.globalAparentWind()
        ap.angle = ap.angle-(self.sails[idx].angle+self.angle-Angle(1,90))
        return ap

    def hullAparentWind(self,idx=0):
        # returns local aparent wind on boat (ie: wind angle in perspective of given sail)
        ap = self.globalAparentWind()
        ap.angle = ap.angle-(self.hulls[idx].angle+self.angle-Angle(1,90))
        return ap

    #TODO: maybe have a method for getting true wind angle from apparent wind for acutal boat