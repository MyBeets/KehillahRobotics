import math

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
    def __str__(self):
        if self.type == 0:
            return "Data: "+ str(self.value)
        if self.type == 1:
            return "Calc: "+ str(self.value)
        if self.type == 2:
            return "Display: "+ str(self.value)

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
    def display2data(self):
        if self.value <= 180:
            return self.value -90
        else: # to avoid negatives
            return 180-(self.value -90)%180
    def display2calc(self):
        return 180 - self.value
    def data2Display(self):
        return self.value + 90
    def data2calc(self): # this shouldn't happen too much as there would be a loss of information
        return 90- self.value 
    def calc2display(self):
        return -self.value +180
    def calc2data(self):
        return abs(90-self.value)



class Force(Variable):
    pass

class Location(Variable):
    pass


if __name__ == "__main__":
    pas = 0
    fail = 0

    #Basic Variable Class:
    basicVar = Variable(1,10)#calc
    pas+= basicVar.data() == 10;fail+= basicVar.data() != 10
    pas+= str(basicVar) == "Calc: 10";fail+= str(basicVar) != "Calc: 10"

    #Basic Angle Class:
    angleVar = Angle(1, 40) # calc
    pas+= str(angleVar) == "Calc: 40";fail+= str(angleVar) != "Calc: 40"
    pas+= angleVar.calc2display() == 140;fail+= angleVar.calc2display() != 140
    pas+= Angle(1, 270).calc2data() == 180;fail+= Angle(1, 270).calc2data() != 180

    print("passed: " + str(pas) + ", failed: " + str(fail)+ ", of: " +str(pas+fail))