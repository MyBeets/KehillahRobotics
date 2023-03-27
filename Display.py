#Display and Map
import matplotlib.pyplot as plt
import matplotlib.transforms as transforms
import matplotlib.patches as patches
from matplotlib.widgets import Slider, Button
from Map import regionPolygon, loadGrib
#Boat and variables
from Foil import foil
from Variables import *
from Boat import Boat
#Other
import os
import math
data_dir = os.path.dirname(__file__) #abs dir

class boatDisplayShell():
    def __init__(self,Boat,ax):
        self.ax = ax
        self.boat = Boat
    def show(self):
        cx = -1
        cy = -1
        for h in self.boat.hulls:
            verts = [(self.meter2degree(i[0]*h.size +h.position.xcomp())+self.boat.position.xcomp(),self.meter2degree(i[1]*h.size+h.position.ycomp())+self.boat.position.ycomp()) for i in h.polygon]
            polygon = patches.Polygon(verts, color="red") 
            #NOTE YOU"LL NEED TO ADD A REAL CENTER OF MASS FUNCTIONALITY
            r = transforms.Affine2D().rotate_deg_around(self.boat.position.xcomp()+self.meter2degree(h.position.xcomp()),self.boat.position.ycomp()+self.meter2degree(h.position.ycomp()),(self.boat.angle+h.angle).display())
            polygon.set_transform(r+ self.ax.transData)
            self.ax.add_patch(polygon)
            if len(self.boat.hulls) > 1:
                if cx == -1:
                    cx = self.boat.position.xcomp()+self.meter2degree(h.position.xcomp())
                    cy = self.boat.position.ycomp()+self.meter2degree(h.position.ycomp())
                else:
                    self.ax.plot([cx,self.boat.position.xcomp()+self.meter2degree(h.position.xcomp())],[cy,self.boat.position.ycomp()+self.meter2degree(h.position.ycomp())], color = 'gray')
                    cx = self.boat.position.xcomp()+self.meter2degree(h.position.xcomp())
                    cy = self.boat.position.ycomp()+self.meter2degree(h.position.ycomp())

        for s in self.boat.sails:
            #x1, y1 are the points on the mast
            x1 = self.boat.position.xcomp()+self.meter2degree(math.cos((boat.angle.calc()+s.position.angle.calc()-90)*math.pi/180)*s.position.norm)
            y1 = self.boat.position.ycomp()+self.meter2degree(math.sin((boat.angle.calc()+s.position.angle.calc()-90)*math.pi/180)*s.position.norm)
            x2 = x1+self.meter2degree(math.cos((self.boat.angle.display()+s.angle.display())*math.pi/180)*s.size)
            y2 = y1+self.meter2degree(math.sin((self.boat.angle.display()+s.angle.display())*math.pi/180)*s.size)
            self.ax.plot([x1,x2],[y1,y2], color = 'yellow')
            #self.ax.plot([x1],[y1], color = 'pink') #mast or something


    def meter2degree(self, v):
        return v*90/1000000
        return v/111111


class display:
    def __init__(self,location,boat):
        self.f, self.axes = plt.subplot_mosaic('AAA;AAA') #,per_subplot_kw={"B": {"projection": "polar"},},
        self.boat = boatDisplayShell(boat,self.axes['A'])
        # self.axes['B'].set_title('Sail Forces')
        self.map(location)
        self.boat.show()
        # self.sailForces()
        # self.controls()
        #credits
        plt.figtext(0, 0.01, 'Map: © OpenStreetMap contributors', fontsize = 10)
        plt.show()
    def map(self,location):
        cords = regionPolygon(location)
        x = [i[0] for i in cords]
        y = [i[1] for i in cords]
        self.axes['A'].set_title(location.split(" ")[0]+ " map")
        self.axes['A'].fill(x,y,'b')
        self.axes['A'].axis([min(x), max(x),min(y), max(y)])
        self.axes['A'].grid()

if __name__ == "__main__":
    lakeAttitash = "Lake Attitash, Amesbury, Essex County, Massachusetts, USA"
    lakeShoreline = "Shoreline lake, Mountain View, Santa Clara County, California, United States"

    vaka = foil(data_dir+"\\data\\xf-naca001034-il-1000000-Ex.csv", 1, 0.5,rotInertia = 1,size = 1.8)
    ama1 = foil(data_dir+"\\data\\naca0009-R0.69e6-F180.csv", 1, 0.5,position = Vector(Angle(1,0),0.6),rotInertia = 1,size = 1.5)
    ama2 = foil(data_dir+"\\data\\naca0009-R0.69e6-F180.csv", 1, 0.5,position = Vector(Angle(1,180),0.6),rotInertia = 1,size = 1.5)
    sail = foil(data_dir+"\\data\\mainSailCoeffs.cvs", 0.128, 1, position = Vector(Angle(1,90),0.4),rotInertia = 1,size = 0.7)
    wind = Vector(Angle(1,225),10) # Going South wind, 10 m/s
    boat = Boat([ama1,vaka,ama2],[sail],wind)
    xpos = -122.09064
    ypos = 37.431749
    boat.setPos(Vector(Angle(1,round(math.atan2(ypos,xpos)*180/math.pi*10000)/10000),math.sqrt(xpos**2+ypos**2)))
    render = display(lakeShoreline,boat)