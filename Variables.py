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
    def data(self):
        if self.type == 1:
            return self.calc2data()
        if self.type == 2:
            return self.display2data()
        return self.value
    
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
    pas+= basicVar.calc() == 10;fail+= basicVar.calc() != 10
    pas+= basicVar.display() == 10;fail+= basicVar.display() != 10
    pas+= str(basicVar) == "Calc: 10";fail+= str(basicVar) != "Calc: 10"

    #Basic Angle Class:
    calcAngle = Angle(1, 40) # calc
    pas+= str(calcAngle) == "Calc: 40";fail+= str(calcAngle) != "Calc: 40"
    pas+= calcAngle.calc2display() == 140;fail+= calcAngle.calc2display() != 140
    pas+= calcAngle.display() == 140;fail+= calcAngle.display() != 140
    pas+= calcAngle.calc2data() == 50;fail+= calcAngle.calc2data() != 50
    pas+= calcAngle.data() == 50;fail+= calcAngle.data() != 50
    pas+= calcAngle.calc() == 40;fail+= calcAngle.calc() != 40

    dataAngle = Angle(0, 90)#data
    pas+= dataAngle.data2calc() == 0;fail+= dataAngle.data2calc() != 0
    pas+= dataAngle.calc() == 0;fail+= dataAngle.calc() != 0
    pas+= dataAngle.data2display() == 180;fail+= dataAngle.data2display() != 180
    pas+= dataAngle.display() == 180;fail+= dataAngle.display() != 180
    pas+= dataAngle.data() == 90;fail+= dataAngle.data() != 90

    displayAngle = Angle(2, 0)#display
    pas+= displayAngle.display2calc() == 180;fail+= displayAngle.display2calc() != 180
    pas+= displayAngle.calc() == 180;fail+= displayAngle.calc() != 180
    pas+= displayAngle.display2data() == -90;fail+= displayAngle.display2data() != -90
    pas+= displayAngle.data() == -90;fail+= displayAngle.data() != -90
    pas+= displayAngle.display() == 0;fail+= displayAngle.display() != 0

    print("passed: " + str(pas) + ", failed: " + str(fail)+ ", of: " +str(pas+fail))