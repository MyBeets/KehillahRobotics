import math
import copy

class Variable:
    value = 0
    type = 0 # 0 is data variable, 1 is calc variable, 2 is display variable
    def __init__(self, type, value):
        self.value = value
        self.type = type
    def data(self):
        return self.value
    def calc(self):
        return self.value
    def display(self):
        return self.value
    def changeType(self,type): #takes in integer types
        if type == 0:
            self.value = self.data()
        if type == 1:
            self.value = self.calc()
        if type == 2:
            self.value = self.display()
        self.type = type
    
    def nType(self,type): #takes in integer types
        if type == 0:
            return self.data()
        if type == 1:
            return self.calc()
        else:
            return self.display()

    def __str__(self):
        if self.type == 0:
            return "Data: "+ str(round(self.value*100)/100)
        if self.type == 1:
            return "Calc: "+ str(round(self.value*100)/100)
        if self.type == 2:
            return "Display: "+ str(round(self.value*100)/100)
    def __add__(self,x):#results are always in the type of the array on which the operation is called
        return Variable(self.type, self.value+x.nType(self.type))
    def __sub__(self,x):
        return Variable(self.type, self.value-x.nType(self.type))
    def __mul__(self,x):
        return Variable(self.type, self.value*x.nType(self.type))

class Angle(Variable):
    """
    Display (do not loop, can be negative)

       | 90
     0--- 180 
       |270

    data angles (no negatives, 0-180)

       |0
 (-)90--- 90
       |180


    Calc (unit circle)

       |90
   180---0
       |270
    """
    # 0 is data variable, 1 is calc variable, 2 is display variable
    def data(self):
        if self.type == 1:
            return self.calc2data()
        if self.type == 2:
            return self.display2data()
        return self.value
    def __str__(self):
        return "Angle: " + super().__str__()
    def calc(self):
        if self.type == 0:
            return self.data2calc()
        if self.type == 2:
            return self.display2calc()
        return self.value
    
    def display(self):
        if self.type == 0:
            return self.data2display()
        if self.type == 1:
            return self.calc2display()
        return self.value

    def display2data(self):
        if self.value <= 180:
            return self.value -90
        else: # to avoid negatives
            return 180-(self.value -90)%180
    def display2calc(self):
        return 180 - self.value
    def data2display(self):
        return self.value + 90
    def data2calc(self): # this shouldn't happen too much as there would be a loss of information
        return 90-self.value 
    def calc2display(self):
        return -self.value +180
    def calc2data(self):
        return abs(90-self.value)
    def __add__(self,x):#results are always in the type of the array on which the operation is called
        return Angle(self.type, self.value+x.nType(self.type))
    def __sub__(self,x):
        return Angle(self.type, self.value-x.nType(self.type))
    def __mul__(self,x):
        return Angle(self.type, self.value*x.nType(self.type))

class Vector():
    def __init__(self,Angle,magnitude):
        self.angle = Angle
        self.norm = magnitude
    def speed(self): # this is for displacement/speed vectors
        return self.norm
    def xcomp(self): # x component of vector in calc format
        return math.cos(self.angle.calc()*math.pi/180)*self.speed()
    def ycomp(self): # y component of vector in calc format
        return math.sin(self.angle.calc()*math.pi/180)*self.speed()
    def __add__(self,x):#Returns vector addition in calc format
        #NOTE: I don't like this current method, the use of x components and trig is bad for precision, this should be replaced
        dx = self.xcomp() + x.xcomp() + 0.0000000001
        dy = self.ycomp() + x.ycomp()
        return Vector(Angle(1, round(math.atan(dy/dx)*180/math.pi*10000)/10000),round(math.sqrt(dx*dx+dy*dy)*10000)/10000)
    def __sub__(self,x):
        y = copy.deepcopy(x)
        y.angle += Angle(y.angle.type,180)
        return self + y
    def __str__(self):
        return "Vector, norm: " +str(self.norm) + ", " + str(self.angle)

def color(fail):
    if fail==0:
        return '.  \x1b[6;30;42m' + 'Success!' + '\x1b[0m'
    else:
        return '.  \x1b[7;31;40m' + 'Failure!' + '\x1b[0m'
    
if __name__ == "__main__":
    pas = 0;fail = 0

    #Basic Variable Class:
    basicVar = Variable(1,10)#calc
    pas+= basicVar.data() == 10;fail+= basicVar.data() != 10
    pas+= basicVar.calc() == 10;fail+= basicVar.calc() != 10
    pas+= basicVar.display() == 10;fail+= basicVar.display() != 10
    pas+= basicVar.type == 1;fail+= basicVar.type != 1
    pas+= str(basicVar) == "Calc: 10.0";fail+= str(basicVar) != "Calc: 10.0"
    basicVar.changeType(2)
    pas+= basicVar.data() == 10;fail+= basicVar.data() != 10
    pas+= basicVar.calc() == 10;fail+= basicVar.calc() != 10
    pas+= basicVar.display() == 10;fail+= basicVar.display() != 10  
    pas+= basicVar.type == 2;fail+= basicVar.type != 2
    print("Variable, passed: " + str(pas) + ", failed: " + str(fail)+ ", of: " +str(pas+fail) + color(fail))
    pas = 0;fail = 0

    #Basic Angle Class:
    calcAngle = Angle(1, 40) # calc
    pas+= str(calcAngle) == "Angle: Calc: 40.0";fail+= str(calcAngle) != "Angle: Calc: 40.0"
    pas+= calcAngle.calc2display() == 140;fail+= calcAngle.calc2display() != 140
    pas+= calcAngle.display() == 140;fail+= calcAngle.display() != 140
    pas+= calcAngle.calc2data() == 50;fail+= calcAngle.calc2data() != 50
    pas+= calcAngle.data() == 50;fail+= calcAngle.data() != 50
    pas+= calcAngle.calc() == 40;fail+= calcAngle.calc() != 40
    pas+= calcAngle.type == 1;fail+= calcAngle.type != 1
    basicVar.changeType(2)
    pas+= calcAngle.display() == 140;fail+= calcAngle.display() != 140
    pas+= calcAngle.data() == 50;fail+= calcAngle.data() != 50
    pas+= calcAngle.calc() == 40;fail+= calcAngle.calc() != 40
    pas+= basicVar.type == 2;fail+= basicVar.type != 2
    print("Calc Angle, passed: " + str(pas) + ", failed: " + str(fail)+ ", of: " +str(pas+fail) + color(fail))
    pas = 0;fail = 0

    dataAngle = Angle(0, 90)#data
    pas+= dataAngle.data2calc() == 0;fail+= dataAngle.data2calc() != 0
    pas+= dataAngle.calc() == 0;fail+= dataAngle.calc() != 0
    pas+= dataAngle.data2display() == 180;fail+= dataAngle.data2display() != 180
    pas+= dataAngle.display() == 180;fail+= dataAngle.display() != 180
    pas+= dataAngle.data() == 90;fail+= dataAngle.data() != 90
    pas+= dataAngle.type == 0;fail+= dataAngle.type != 0
    dataAngle.changeType(2)
    pas+= dataAngle.calc() == 0;fail+= dataAngle.calc() != 0
    pas+= dataAngle.display() == 180;fail+= dataAngle.display() != 180
    pas+= dataAngle.data() == 90;fail+= dataAngle.data() != 90
    pas+= dataAngle.type == 2;fail+= dataAngle.type != 2
    print("Data Angle, passed: " + str(pas) + ", failed: " + str(fail)+ ", of: " +str(pas+fail) + color(fail))
    pas = 0;fail = 0

    displayAngle = Angle(2, 0)#display
    pas+= displayAngle.display2calc() == 180;fail+= displayAngle.display2calc() != 180
    pas+= displayAngle.calc() == 180;fail+= displayAngle.calc() != 180
    pas+= displayAngle.display2data() == -90;fail+= displayAngle.display2data() != -90
    pas+= displayAngle.data() == -90;fail+= displayAngle.data() != -90
    pas+= displayAngle.display() == 0;fail+= displayAngle.display() != 0
    pas+= dataAngle.type == 2;fail+= dataAngle.type != 2
    dataAngle.changeType(0)
    pas+= displayAngle.calc() == 180;fail+= displayAngle.calc() != 180
    pas+= displayAngle.data() == -90;fail+= displayAngle.data() != -90
    pas+= displayAngle.display() == 0;fail+= displayAngle.display() != 0
    pas+= dataAngle.type == 0;fail+= dataAngle.type != 0
    print("Display Angle, passed: " + str(pas) + ", failed: " + str(fail)+ ", of: " +str(pas+fail) + color(fail))
    pas = 0;fail = 0

    #Simple Vector
    v1 = Vector(Angle(1,10),10)
    v2 = Vector(Angle(1,10),10)
    v3 = v1+v2
    v4 = v1-v2
    v5 = v3+v4
    pas+= v3.angle.calc() == 10.0;fail+= v3.angle.calc() !=10.0
    pas+= v3.speed() == 20;fail+= v3.speed() != 20
    pas+= round(v4.angle.calc()) == 0;fail+= round(v4.angle.calc()) !=0
    pas+= v4.speed() == 0;fail+= v4.speed() != 0
    pas+= v5.angle.calc() == 10.0;fail+= v5.angle.calc() !=10.0
    pas+= v5.speed() == 20;fail+= v5.speed() != 20
    #Harder Vector calculations
    v6 = Vector(Angle(1,10),10)
    v7 = Vector(Angle(1,-20),-5.5) # 160 with norm 5.5
    v8 = v6+v7
    pas+= v8.angle.calc() == 37.705;fail+= v8.angle.calc() !=37.705
    pas+= v8.speed() == 5.915;fail+= v8.speed() != 5.915
    print("Vector, passed: " + str(pas) + ", failed: " + str(fail)+ ", of: " +str(pas+fail) + color(fail))
    pas = 0;fail = 0