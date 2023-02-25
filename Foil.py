from Variables import *

class foil: # sail, foil, rudder
    def __init__(self, datasheet, material, WA):
        self.datasheet = datasheet #string file location of csv
        self.mat = material # Density of the material the foil comes in contact to in kg/m^3
        self.area = WA #wetted hull or sail

        # liftC and dragC just contain key (direction) value (coeffeciant) pairs
        if datasheet.find("naca")!= -1:
            self.liftC = self.read(self.datasheet,"Cl")
            self.dragC = self.read(self.datasheet,"Cd")
        elif datasheet.find("mainSailCoeffs") != -1:
            self.liftC = self.read(self.datasheet,"clyc-CLhi")
            self.dragC = self.read(self.datasheet,"cdyc-CDhi")
        else:
            self.liftC = self.read(self.datasheet,"CL")
            self.dragC = self.read(self.datasheet,"CD")


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


if __name__ == "__main__":
    pas = 0
    fail = 0

    sail = foil("mainSailCoeffs.cvs", 0.128, 1)
    pas+= sail.liftC[0][0].data() == 0 ;fail+=sail.liftC[0][0].data() != 0 
    pas+= sail.liftC[0][0].calc() == 90 ;fail+=sail.liftC[0][0].calc() != 90 
    pas+= sail.liftC[0][0].display() == 90 ;fail+=sail.liftC[0][0].display() != 90 

    pas+= sail.liftC[0][1] == 0 ;fail+=sail.liftC[0][1] != 0 
    # pas+= sail.liftC[0][0].calc() == 90 ;fail+=sail.liftC[0][0].calc() != 90 
    # pas+= sail.liftC[0][0].display() == 90 ;fail+=sail.liftC[0][0].display() != 90 
    print(sail.liftC)
    print("passed: " + str(pas) + ", failed: " + str(fail)+ ", of: " +str(pas+fail))