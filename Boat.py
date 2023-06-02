import math
from Variables import *
import copy

class Boat:
    def __init__(self, hulls, sails, wind,mass =55,refLat=37):
        self.hulls = hulls #array of hulls
        self.sails = sails
        self.wind = wind
        self.mass = mass # mass in in kg
        self.angle = Angle(1,90) # global rotation of boat and all it's parts
        #Forces on the boat
        self.forces = {"sails":Vector(Angle(1,90),0), "hulls":Vector(Angle(1,90),0)}
        self.moments = {"sails":0, "hulls":0}

        #current boat velocities
        self.linearVelocity = Vector(Angle(1,90),0) # m/s
        self.rotationalVelocity = 0 # radians/s, positive is ccw, negative is cw
        self.refLat = refLat
        #current boat position
        self.position = Vector(Angle(1,90),0)

    def setPos(self,pos):
        self.position = pos
    def resetValues(self):
        self.rotationalVelocity = 0
        self.linearVelocity = Vector(Angle(1,0),0)
        self.forces = {"sails":Vector(Angle(1,0),0), "hulls":Vector(Angle(1,0),0)}
        self.moments = {"sails":0, "hulls":0}
    def update(self,dt=1): #t is in seconds
        num =30
        #update forces and moments
        self.updateSailForcesandMoments(dt/(num+1))
        self.updateHullForcesandMoments()
        #update velocities
        for i in range(num):
            self.updateLinearVelocity(dt/num)
            self.updateRotationalVelocity(dt/(num+1))
            self.updateSailForcesandMoments(dt/(num+1))
            self.updateHullForcesandMoments()

        #update position and rotation
        self.updatePosition(dt)
        self.updateRotation(dt)

    def updatePosition(self, dt):
        ax = (self.forces["sails"]+self.forces["hulls"]).xcomp()/self.mass
        ay = (self.forces["sails"]+self.forces["hulls"]).ycomp()/self.mass
        a = Vector(Angle(1,round(math.atan2(ay,ax)*180/math.pi*10000)/10000),math.sqrt(ax**2+ay**2))
        #d = v*dt +1/2*a*dt^2
        disp = self.linearVelocity*dt+(a*(dt**2))*0.5
        self.position += disp.meter2degree(self.refLat)
        
    # def degree2meter(self, vect): # DEPRECATED 
    #     vect2 = copy.deepcopy(vect)
    #     #vect2.norm *= 1000000/90
    #     vect2.norm *=(111.32 * 1000 * math.cos(self.position.ycomp() * (math.pi / 180)))/3
    #     return vect2
    
    def updateRotation(self, dt):
        sMoments = self.moments["sails"] + self.moments["hulls"]
        sI = sum([h.I for h in self.hulls]) + sum([s.I for s in self.sails])
        alfa = sMoments/sI
        #d theta = w*dt +1/2*alfa*dt^2
        self.angle += Angle(1,(self.rotationalVelocity*dt+(alfa*dt**2)/2)*180/math.pi)#
        #self.angle += Angle(1,self.rotationalVelocity*dt+(sI*dt**2)/2)

    def updateLinearVelocity(self,dt):
        #not using extend is on purpose, extend modifies the variable
        #vf=v0+a*dt
        ax = (self.forces["sails"]+self.forces["hulls"]).xcomp()/self.mass
        ay = (self.forces["sails"]+self.forces["hulls"]).ycomp()/self.mass
        a = Vector(Angle(1,round(math.atan2(ay,ax+0.000000001)*180/math.pi*1000000)/1000000),math.sqrt(ax**2+ay**2))
        a *= dt
        self.linearVelocity += a

    def updateRotationalVelocity(self,dt):
        #Sum of the torque = I ( rotational inertia) * alfa (angular acceleration) thus alfa = sum of torque / I, and then classic angular kinematics
        #wf=w0+alfa*dt
        sMoments = self.moments["sails"] + self.moments["hulls"]
        sI = sum([h.I for h in self.hulls]) + sum([s.I for s in self.sails])
        alfa = sMoments/sI
        self.rotationalVelocity += alfa*dt

    def updateSailForcesandMoments(self,dt):
        self.forces["sails"] = Vector(Angle(1,0),0)
        self.moments["sails"] = 0
        for idx in range(len(self.sails)):
            force = self.sailLiftForce(idx) + self.sailDragForce(idx)
            self.forces["sails"] += force
            self.sails[idx].updateSailRotation(dt,self.sailAparentWind(idx))
            #NOTE: For sail torque things become a bit more complex
            #self.moments["sails"] += self.sails[idx].moment(force) # slightly unnecessary for a sail but could be usefull

    def updateHullForcesandMoments(self):
        self.forces["hulls"] = Vector(Angle(1,0),0)
        self.moments["hulls"] = 0
        for idx in range(len(self.hulls)):
            liftForce, liftMoment = self.hullLiftForceandMoment(idx)
            dragForce, dragMoment = self.hullDragForceandMoment(idx)
            self.forces["hulls"] += liftForce + dragForce
            self.moments["hulls"] += liftMoment + dragMoment


    def sailDragForce(self,idx=0):
        aparentForce = self.sails[idx].dragForce(self.sailAparentWind(idx))
        trueForce = Vector(aparentForce.angle + self.angle + self.sails[idx].angle,aparentForce.norm)
        trueForce.angle = Angle.norm(trueForce.angle)
        return trueForce
    def sailLiftForce(self,idx=0):
        aparentForce = self.sails[idx].liftForce(self.sailAparentWind(idx))
        trueForce = Vector(aparentForce.angle + self.angle + self.sails[idx].angle,aparentForce.norm)
        trueForce.angle = Angle.norm(trueForce.angle)
        return trueForce

    def hullDragForceandMoment(self,idx=0):
        aparentForce = self.hulls[idx].dragForce(self.hullAparentWind(idx))
        moment = self.hulls[idx].moment(aparentForce)
        trueForce = Vector(aparentForce.angle + self.angle + self.hulls[idx].angle,aparentForce.norm)
        trueForce.angle = Angle.norm(trueForce.angle)
        return trueForce, moment
    def hullLiftForceandMoment(self,idx=0):
        aparentForce = self.hulls[idx].liftForce(self.hullAparentWind(idx))
        moment = self.hulls[idx].moment(aparentForce)
        trueForce = Vector(aparentForce.angle + self.angle + self.hulls[idx].angle,aparentForce.norm)
        trueForce.angle = Angle.norm(trueForce.angle)
        return trueForce, moment

    def globalAparentWind(self):
        # returns global aparent wind on boat
        return self.wind-self.linearVelocity
    

    #CONVENTION: For all this apparent wind stuff wind should always point in the dirrection it's going, so for a hull that's flow direction
    def sailAparentWind(self,idx=0):
        # # returns local aparent wind on boat (ie: wind angle in perspective of given sail)
        # wind = self.globalAparentWind()
        # ap = Angle(1,math.acos((wind * Vector(self.sails[idx].angle+self.angle,1))/wind.norm)*180/math.pi)

        # if Angle.norm(wind.angle+Angle(1,180)).calc() > Angle.norm(ap).calc(): #NOTE HERE"S THE PROBLEM
        #     ap *= -1
        # ap = self.globalAparentWind() 
        # ap.angle += Angle(1,180)
        # ap.angle = (self.sails[idx].angle+self.angle)-ap.angle
        # ap.angle += Angle(1,180)
        ap = self.globalAparentWind() 
        ap.angle += Angle(1,180)
        ap.angle = ap.angle-(self.sails[idx].angle+self.angle)
        ap.angle += Angle(1,180)
        return ap#Vector(ap,wind.norm)

    def hullAparentWind(self,idx=0):
        # returns aparent water velocity on a hull 
        # #First get current angular velocity (tangential to roation)
        V = Vector(self.angle,self.rotationalVelocity*self.hulls[idx].position.norm)
        # Then combine with linear velocity, NOTE: if you disactivate rotational added speed use deepcopy for the next line
        #V = copy.deepcopy(self.linearVelocity)
        V += self.linearVelocity
        #Finally make aparent
        V.angle -= (self.angle+self.hulls[idx].angle)
        #flip it as we wish to mesure the flow AGAINST hull
        V.angle += Angle(1,180)
        return V

    #TODO: maybe have a method for getting true wind angle from apparent wind for acutal boat