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
        self.moments = {"sails":Vector(Angle(1,90),0), "hulls":Vector(Angle(1,90),0)}

        #current boat velocities
        self.linearVelocity = Vector(Angle(1,90),0) # m/s
        self.rotationalVelocity = 0 # radians/s, positive is ccw, negative is cw

        #current boat position
        self.position = Vector(Angle(1,90),0)

    def setPos(self,pos):
        self.position = pos
    def update(self,dt=1): #t is in seconds
        #update forces and moments
        self.updateSailForcesandMoments()
        self.updateHullForcesandMoments()
        #update velocities
        self.updateLinearVelocity(dt)
        self.updateRotationalVelocity(dt)
        #update position

    def updateLinearVelocity(self,dt):
        #not using extend is on purpose, extend modifies the variable
        #vf=v0+a*dt
        ax = (sum(self.forces["sails"])+sum(self.forces["hulls"])).xcomp()/self.mass
        ay = (sum(self.forces["sails"])+sum(self.forces["hulls"])).ycomp()/self.mass
        a = Vector(Angle(1,round(math.atan2(ay,ax)*180/math.pi*10000)/10000),math.sqrt(ax**2+ay**2))
        a *= dt
        self.linearVelocity += a

    def updateRotationalVelocity(self,dt):
        #Sum of the torque = I ( rotational inertia) * alfa (angular acceleration) thus alfa = sum of torque / I, and then classic angular kinematics
        #wf=w0+alfa*dt
        sMoments = sum(self.moments["sails"]) + sum(self.moments["hulls"])
        sI = sum([h.rotInertia for h in self.hulls]) + sum([s.rotInertia for s in self.sails])
        alfa = sMoments/sI
        self.rotationalVelocity += alfa*dt

    def updateSailForcesandMoments(self):
        self.forces["sails"] = Vector(Angle(1,90),0)
        self.moments["sails"] = Vector(Angle(1,90),0)
        for idx in range(len(self.sails)):
            force = self.sailLiftForce(idx) + self.sailDragForce(idx)
            self.forces["sails"] += force
            self.moments["sails"] += self.sails[idx].moment(force) # slightly unnecessary for a sail but could be usefull

    def updateHullForcesandMoments(self):
        self.forces["hulls"] = Vector(Angle(1,90),0)
        self.moments["hulls"] = Vector(Angle(1,90),0)
        for idx in range(len(self.hulls)):
            force = self.hullLiftForce(idx) + self.hullDragForce(idx)
            self.forces["hulls"] += force
            self.moments["hulls"] += self.hulls[idx].moment(force)

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