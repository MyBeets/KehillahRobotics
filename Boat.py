import math
from Variables import *

class Boat:
    def __init__(self, hulls, sails, wind, hull_placement = 0):
        self.hulls = hulls #array of hulls
        self.sails = sails
        self.wind = wind
        self.angle = Angle(1,90) # global rotation of boat and all it's parts
        #Forces on the boat
        self.forces = {"sails":Vector(Angle(1,90),0), "hulls":Vector(Angle(1,90),0)}

        #current boat velocity
        self.velocity = Vector(Angle(1,90),0)

        #current boat position
        self.position = Vector(Angle(1,90),0)
    def setPos(self,pos):
        self.position = pos
    def update(self,t=1): #t is in seconds
        #update forces
        self.updateSailForces()
        self.updateHullForces()
        #update velocities

        #update position
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
        return self.wind-self.velocity
    
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