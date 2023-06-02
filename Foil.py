from Variables import *
def printA(x):
    x %= 360
    if x > 180:
        x = -180 + x-180
    return x
class foil: # sail, foil, rudder
    def __init__(self, datasheet, material, WA, position = Vector(Angle(1,0),0),rotInertia = -1,size = 1.8, winches = []):
        self.datasheet = datasheet #string file location of csv
        self.polygon = []
        self.size = size #LOA of hull in meter
        self.mat = material # Density of the material the foil comes in contact to in kg/m^3
        self.area = WA #wetted hull or sail
        self.angle = Angle(1,0)# Relative angle to parent object (all is inline with boat)
        self.position = position
        self.I = rotInertia # rotational inertia
        self.winches = winches # winches for sails
        self.rotationalVelocity = 0
        # liftC and dragC just contain key (direction), value (coeffeciant) pairs
        if datasheet.find("naca")!= -1:
            self.liftC = self.read(self.datasheet,"Cl")
            self.dragC = self.read(self.datasheet,"Cd")
            self.polygon = self.readPoly(datasheet)
        elif datasheet.find("mainSailCoeffs") != -1:
            self.liftC = self.read(self.datasheet,"clnc-CLlow")
            self.dragC = self.read(self.datasheet,"cdnc-CDlow")
        else:
            self.liftC = self.read(self.datasheet,"CL")
            self.dragC = self.read(self.datasheet,"CD")
            if datasheet.find("Sail") == -1:
                self.polygon = self.readPoly(datasheet)
        
    def readPoly(self, datasheet):
        datasheet = datasheet.replace("cvs","dat").replace("csv","dat")
        sheet = open(datasheet,"r")
        poly = []
        for line in sheet:
            if line[0].isnumeric():
                poly.append([float(i) for i in line.split()])
                poly[-1][0] = -poly[-1][0]+0.5
        return poly

    def moment(self,force):
        #force here is apparent force
        return -math.sin(force.angle.calc()*math.pi/180)*force.norm*self.position.norm
        # if math.cos(self.position.angle.calc()*math.pi/180)*self.position.norm >= 0: # simple convention on rotation 
        #     return -self.position.norm*force.norm*math.sin((force.angle-(self.position.angle)).calc()*math.pi/180)
        # else:
        #     return self.position.norm*force.norm*math.sin((force.angle-(self.position.angle)).calc()*math.pi/180)

    def drag(self, aparentV):
        # the + Angle(1,180) is to flip the wind from direction pointing to direction of arrival
        # print(self.cd(Angle.norm(aparentV.angle+Angle(1,180))),Angle.norm(aparentV.angle+Angle(1,180)))
        return (self.cd(Angle.norm(aparentV.angle+Angle(1,180))) * self.mat * pow(aparentV.speed(),2) *self.area)/2

    def lift(self, aparentV):
        return (self.cl(Angle.norm(aparentV.angle+Angle(1,180))) * self.mat * pow(aparentV.speed(),2) *self.area)/2


    #CONVENTION: For all this apparent wind stuff wind should always point in the dirrection it's going, so for a hull that's flow direction
    def liftForce(self, aparentV):
        lift = self.lift(aparentV)
        #print(aparentV,self.mat)
        # if self.mat == 1.204:
            #print(Angle.norm(aparentV.angle+Angle(1,180)),lift,self.cd(Angle.norm(aparentV.angle+Angle(1,180))),self.cl(Angle.norm(aparentV.angle+Angle(1,180))))
        if Angle.norm(aparentV.angle).calc() >= 180: # this is to split cases where wind is port or starboard
            if lift < 0: # if lift is negative we flip dirrection such that magnitude is always positive
                return Vector(aparentV.angle+Angle(1,270),-lift)# 180+90
            else:
                return Vector(aparentV.angle+Angle(1,90),lift)
        else:
            if lift < 0:# if lift is negative we flip dirrection such that magnitude is always positive
                return Vector(aparentV.angle+Angle(1,90),-lift) # 180-90
            else:
                return Vector(aparentV.angle-Angle(1,90),lift)

    def dragForce(self, aparentV):
        drag = self.drag(aparentV)
        #print(aparentV,drag)
        #print(aparentV.angle,self.mat)
        #return Vector(aparentV.angle,drag)
        if drag < 0:
            return Vector(aparentV.angle+Angle(1,180),-drag)
        else:
            return Vector(aparentV.angle,drag)
        #return Vector(aparentV.angle,abs(self.drag(aparentV)))

    def setSailRotation(self,angle):
        sailPos = self.position + Vector(Angle(1,180)+angle+self.position.angle, self.size)
        d = [w.distance(sailPos) for w in self.winches] 
        # the reason we must obtain the max is the the shorter cable will be impossibly short until the boom is in position
        for w in self.winches:
            w.length = max(d)
            w.rot = angle
    

    def updateSailRotation(self,dt,wind):
        if len(self.winches) == 0:
            return
        forces = self.liftForce(wind) + self.dragForce(wind) # all this should be apparent to the sail
        ce = 0.49 # 1 meter right now
        moment = -1*math.sin(forces.angle.calc() * math.pi/180)* ce # the -1 is due to convention and format of apparent wind
        rotInteria = 0.54
        alfa = moment/rotInteria
        self.rotationalVelocity += alfa*dt
        pos1 = self.position + Vector(self.angle+self.position.angle+Angle(1,180),self.size)
        angle2 = self.angle + Angle(1,(self.rotationalVelocity*dt+(alfa*dt**2)/2)*180/math.pi)
        pos2 = self.position + Vector(angle2+self.position.angle+Angle(1,180),self.size)
        for w in self.winches:
            if w.distance(pos1) >= w.length and w.distance(pos1) <= w.distance(pos2):#or self.angle.calc() > w.rot.calc()
                if abs(printA((self.angle-w.rot).calc())) > abs(printA((self.angle+w.rot).calc())):
                    for n in self.winches:
                        n.rot = n.rot*-1
                if Angle.norm(w.rot).calc() > 0:
                    self.angle = w.rot-Angle(1,2)
                else:
                    self.angle = w.rot+Angle(1,2)
                self.rotationalVelocity = 0
                alfa = 0
            # check for distances to winches and cord let out, cancel all rotation velocity if nessesary
        if self.rotationalVelocity != 0:
            self.angle = angle2

    def read(self, datasheet, atr):
        sheet = open(datasheet,"r");units = [];values = []
        if datasheet.find("naca")!= -1:
            line = sheet.readline()
            while line.split(",")[0].lower() != "alpha" and line.split(",")[0].lower() != "alfa":
                line = sheet.readline()
            line= line.replace('\n', "").replace('\r', "")
            idx = line.split(",").index(atr)
            line = sheet.readline()
            while len(line) >1:
                units.append(Angle(0,float(line.split(",")[0])))
                values.append(float(line.split(",")[idx]))
                line = sheet.readline()
        else:
            if datasheet.find("mainSailCoeffs") != -1:
                units = [Angle(0,float(x)//2) for x in sheet.readline().split()[1:]]
            else:
                units = [Angle(0,float(x)) for x in sheet.readline().split()[1:]]
            line = sheet.readline()
            while line.split()[0] != atr:
                line = sheet.readline()
            values = [float(x) for x in line.split()[1:]]
        return list(zip(units,values))

    def linearInterpolation(self,list, value):
        idx = 0
        for i in range(len(list)):
            idx = i
            if list[i][0].data() > value:
                idx = i
                break
        idx-=1
        if idx < 0:
            idx = 0
        s = (list[idx+1][1]-list[idx][1])/(list[idx+1][0].data()-list[idx][0].data())
        return s*(value-list[idx][0].data())+list[idx][1]

    def cd(self, a):
        #NOTE: CURRENTLY TESTING bug where data angle shouldn't be used here
        a = abs(a.data())
        a %= 360
        last = self.dragC[-1][0].data()
        if a > last:
            a =last - a%last
        # print(a)
        return self.linearInterpolation(self.dragC,a)
    def cl(self, a):
        a = abs(a.data())
        #if self.mat == 1:
            #print(self.mat,a,self.linearInterpolation(self.liftC,a))
        a %= 360
        last = self.liftC[-1][0].data()
        if a > last: 
            a =last - a%last
        return self.linearInterpolation(self.liftC,a)

class Winch:
    def __init__(self, position, length, radius):
        self.position = position
        self.length = length
        self.radius = radius
        self.rot = Angle(1,0)# this pretty much an internal variable for display
    def setLength(self,length):
        self.length = length
    def distance(self, pos2):
        return math.sqrt((self.position.xcomp()-pos2.xcomp())**2 + (self.position.ycomp()-pos2.ycomp())**2)