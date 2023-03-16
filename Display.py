#Display and Map
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.widgets import Slider, Button
from Map import regionPolygon
#Boat and variables
from Foil import foil
from Variables import *
from Boat import Boat
#Other
import os
import math

data_dir = os.path.dirname(__file__) #abs dir

class display:
    def __init__(self,location,boat):
        self.boat = boat

        #display
        self.f, self.axes = plt.subplot_mosaic('AAA;AAA') #,per_subplot_kw={"B": {"projection": "polar"},},
        # self.axes['B'].set_title('Sail Forces')
        self.map(location)
        # self.sailForces()
        # self.controls()
        #credits
        plt.figtext(0, 0.01, 'Map: © OpenStreetMap contributors', fontsize = 10)
        plt.show()
    def controls(self):
        self.axes['D'].axis('off')
        self.windSlider = Slider(
            ax=self.f.add_axes([2/3+0.1, 0.75, 0.1, 0.03]),
            label="Wind ",
            valmin=0,
            valmax=360,
            valinit=0,
        )
        self.windSlider.on_changed(self.windUpdate)
    def windUpdate(self,val):
        self.boat.wind.angle = Angle(1,val)
        self.sailForces()
    def map(self,location):
        cords = regionPolygon(location)
        x = [i[0] for i in cords]
        y = [i[1] for i in cords]
        self.axes['A'].set_title(location.split(" ")[0]+ " map")
        self.axes['A'].fill(x,y,'c')
        self.axes['A'].axis([min(x), max(x),min(y), max(y)])
        self.axes['A'].grid()
        self.axes['A'].add_patch(patches.Rectangle((self.boat.position.xcomp(),self.boat.position.ycomp()),0.0001,0.0001))
    def sailForces(self):
        self.boat.update()
        self.axes['B'].cla()
        #self.sailf.set_ydata([0,self.boat.forces['sails'].norm])
        #self.sailf.set_xdata([Angle.norm(self.boat.forces['sails'].angle).calc()*math.pi/180]*2)
        self.axes['B'].plot([Angle.norm(self.boat.forces['sails'].angle).calc()*math.pi/180]*2,[0,self.boat.forces['sails'].norm],marker= "o")


if __name__ == "__main__":
    lakeAttitash = "Lake Attitash, Amesbury, Essex County, Massachusetts, USA"
    lakeShoreline = "Shoreline lake, Mountain View, Santa Clara County, California, United States"

    hull = foil(data_dir+"\\data\\xf-naca001034-il-1000000-Ex.csv", 1, 0.5)
    sail = foil(data_dir+"\\data\\mainSailCoeffs.cvs", 0.128, 1)
    wind = Vector(Angle(1,225),10) # Going South wind, 10 m/s
    boat = Boat([hull],[sail],wind)
    xpos = -122.09064
    ypos = 37.431749
    boat.setPos(Vector(Angle(1,round(math.atan2(ypos,xpos)*180/math.pi*10000)/10000),math.sqrt(xpos**2+ypos**2)))
    render = display(lakeShoreline,boat)