from Variables import *
import os

class foil: # sail, foil, rudder
    def __init__(self, datasheet, material, WA):
        self.datasheet = datasheet #string file location of csv
        self.mat = material # Density of the material the foil comes in contact to in kg/m^3
        self.area = WA #wetted hull or sail

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
        return (self.cd(aparentV.angle) * self.mat * pow(aparentV.speed(),2) *self.area)/2

    def lift(self, aparentV):
        return (self.cl(aparentV.angle) * self.mat * pow(aparentV.speed(),2) *self.area)/2

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


if __name__ == "__main__":
    pas = 0
    fail = 0

    sail = foil("mainSailCoeffs.cvs", 0.128, 1)

    #read method for mainsail lift coeffeciants
    pas+= sail.liftC[0][0].data() == 0;fail+=sail.liftC[0][0].data() != 0 
    pas+= sail.liftC[0][0].calc() == 90;fail+=sail.liftC[0][0].calc() != 90 
    pas+= sail.liftC[0][0].display() == 90;fail+=sail.liftC[0][0].display() != 90 
    pas+= sail.liftC[0][1] == 0 ;fail+=sail.liftC[0][1] != 0 
    pas+= sail.liftC[4][0].data() == 14 ;fail+=sail.liftC[4][0].data() != 14 #the data is halved that's why it's 14 not 28 
    pas+= sail.liftC[9][0].data() == 90 ;fail+=sail.liftC[9][0].data() != 90 
    pas+= sail.liftC[9][0].calc() == 0 ;fail+=sail.liftC[9][0].calc() != 0
    pas+= sail.liftC[9][0].display() == 180;fail+=sail.liftC[9][0].display() != 180 

    #linear interpolation and reading
    pas+= float(sail.cd(Angle(0,45))) == 0.3825;fail+= float(sail.cd(Angle(0,45))) != 0.3825
    pas+= float(sail.cl(Angle(0,14))) == 1.42681;fail+= float(sail.cl(Angle(0,14))) != 1.42681
    pas+= float(sail.cl(Angle(0,100))) == 0.22126333333333334;fail+= float(sail.cl(Angle(0,100))) != 0.22126333333333334

    script_dir = os.path.dirname(__file__) #abs dir
    path = "data\\xf-naca001034-il-1000000-Ex.csv"
    abs_path = os.path.join(script_dir, path)
    hull = foil(abs_path, 1, 0.5)

    #read method for hull drag coeffeciants
    pas+= hull.dragC[0][0].data() == 0;fail+=hull.dragC[0][0].data() != 0
    pas+= hull.dragC[0][1] == 0.0067;fail+=hull.dragC[0][1] != 0.0067
    pas+= hull.dragC[10][1] == 0.0159;fail+=hull.dragC[10][1] != 0.0159
    pas+= hull.dragC[15][1] == 0.1170;fail+=hull.dragC[15][1] != 0.1170

    # lift and drag methods
    pas+= hull.lift(Vector(Angle(1,45),10)) == 27.125;fail+=hull.lift(Vector(Angle(1,45),10)) != 27.125
    pas+= hull.lift(Vector(Angle(1,90),10)) == 0;fail+=hull.lift(Vector(Angle(1,90),10)) != 0
    pas+= hull.lift(Vector(Angle(1,270),10)) == 0;fail+=hull.lift(Vector(Angle(1,270),10)) != 0
    pas+= hull.drag(Vector(Angle(1,270),10)) <= 1;fail+=hull.drag(Vector(Angle(1,270),10)) > 1
    pas+= hull.drag(Vector(Angle(1,-10),10)) >= 40;fail+=hull.drag(Vector(Angle(1,-10),10)) < 40

    print("passed: " + str(pas) + ", failed: " + str(fail)+ ", of: " +str(pas+fail))