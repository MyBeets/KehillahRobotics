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
        return "\033[96mAngle\033[0m: " + super().__str__()
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
    @staticmethod
    def norm(v):
        if v.type == 1 or v.type ==2: #calc and display
            v.value %=360
        return v
    def __add__(self,x):#results are always in the type of the array on which the operation is called
        return Angle(self.type, self.norm(self).value+self.norm(x).nType(self.type))
    def __sub__(self,x):
        return Angle(self.type, self.norm(self).value-self.norm(x).nType(self.type))
    def __mul__(self,x):
        return Angle(self.type, self.norm(self).value*self.norm(x).nType(self.type))

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
        return Vector(Angle(1, round(math.atan2(dy,dx)*180/math.pi*10000)/10000),round(math.sqrt(dx*dx+dy*dy)*10000)/10000)
    def __sub__(self,x):
        y = copy.deepcopy(x)
        y.norm = -y.norm
        return self + y
    def __str__(self):
        return "\033[93mVector\033[0m, norm: " +str(self.norm) + ", " + str(self.angle)