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

class Angle(Variable):
    pass

class Force(Variable):
    pass

class Location(Variable):
    pass