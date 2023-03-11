from Variables import *

class foil: # sail, foil, rudder
    def __init__(self, datasheet, material, WA):
        self.datasheet = datasheet #string file location of csv
        self.mat = material # Density of the material the foil comes in contact to in kg/m^3
        self.area = WA #wetted hull or sail
        self.angle = Angle(1,0)# Relative angle to parent object (all is inline with boat)

        # liftC and dragC just contain key (direction), value (coeffeciant) pairs
        if datasheet.find("naca")!= -1:
            self.liftC = self.read(self.datasheet,"Cl")
            self.dragC = self.read(self.datasheet,"Cd")
        elif datasheet.find("mainSailCoeffs") != -1:
            self.liftC = self.read(self.datasheet,"clyc-CLhi")
            self.dragC = self.read(self.datasheet,"cdyc-CDhi")
        else:
            self.liftC = self.read(self.datasheet,"CL")
            self.dragC = self.read(self.datasheet,"CD")

    def drag(self, aparentV):
        # the + Angle(1,180) is to flip the wind from direction pointing to direction of arrival
        return (self.cd(Angle.norm(aparentV.angle+Angle(1,180))) * self.mat * pow(aparentV.speed(),2) *self.area)/2

    def lift(self, aparentV):
        return (self.cl(Angle.norm(aparentV.angle+Angle(1,180))) * self.mat * pow(aparentV.speed(),2) *self.area)/2

    def liftForce(self, aparentV):
        if Angle.norm(self.angle).calc() <= Angle.norm(aparentV.angle+Angle(1,180)).calc():
            return Vector(aparentV.angle+Angle(1,90),self.lift(aparentV))
        else:
            return Vector(aparentV.angle-Angle(1,90),self.lift(aparentV))

    def dragForce(self, aparentV):
        return Vector(aparentV.angle,self.drag(aparentV))

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
            if datasheet.find("mainSailCoeffs"):
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
        a = abs(a.data())
        a %= 360
        last = self.dragC[-1][0].data()
        if a > last:
            a =last - a%last
        return self.linearInterpolation(self.dragC,a)
    def cl(self, a):
        a = abs(a.data())
        a %= 360
        last = self.liftC[-1][0].data()
        if a > last: 
            a =last - a%last
        return self.linearInterpolation(self.liftC,a)