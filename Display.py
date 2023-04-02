#Display and Map
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.transforms as transforms
import matplotlib.patches as patches
from mpl_toolkits.axes_grid1.inset_locator import InsetPosition
from matplotlib.widgets import Slider, Button
from Map import regionPolygon, loadGrib
#Boat and variables
from Foil import foil
from Variables import *
from Boat import Boat
#Other
import os
import math
import copy
import re


data_dir = os.path.dirname(__file__) #abs dir

def rm_ansi(line):
    ansi_escape =re.compile(r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]')
    return ansi_escape.sub('', line)

class boatDisplayShell():
    def __init__(self,Boat,ax):
        self.ax = ax
        self.boat = Boat
        self.createBoat()
    def createBoat(self):
        self.hullDisplay = []
        self.sailDisplay = []
        self.connections = []
        self.forceDisplay = []
        self.pos = [self.boat.position.xcomp(),self.boat.position.ycomp()]
        cx = -1
        cy = -1
        for i, h in enumerate(self.boat.hulls):
            verts = [(self.meter2degree(p[0]*h.size+ h.position.xcomp())+self.boat.position.xcomp(),self.meter2degree(p[1]*h.size+h.position.ycomp())+self.boat.position.ycomp()) for p in h.polygon]
            polygon = patches.Polygon(verts, color="gray") 

            #NOTE YOU"LL NEED TO ADD A REAL CENTER OF MASS FUNCTIONALITY
            print("TODO: CENTER OF MASS")
            r = transforms.Affine2D().rotate_deg_around(self.boat.position.xcomp(),self.boat.position.ycomp(),(self.boat.angle+h.angle).calc())

            polygon.set_transform(r+ self.ax.transData)
            self.hullDisplay.append(self.ax.add_patch(polygon))

            print("TODO: CENTER OF LATERAL RESISTANCE")
            #lift
            self.forceDisplay.append(self.ax.plot([0,0],[0,0], color = 'red')[0])
            #drag
            self.forceDisplay.append(self.ax.plot([0,0],[0,0], color = 'green')[0])


            if len(self.boat.hulls) > 1:
                if cx == -1:
                    cx = self.boat.position.xcomp()+self.meter2degree(h.position.xcomp())
                    cy = self.boat.position.ycomp()+self.meter2degree(h.position.ycomp())
                else:
                    self.connections.append(self.ax.plot([cx,self.boat.position.xcomp()+self.meter2degree(h.position.xcomp())],[cy,self.boat.position.ycomp()+self.meter2degree(h.position.ycomp())], color = 'gray')[0])
                    cx = self.boat.position.xcomp()+self.meter2degree(h.position.xcomp())
                    cy = self.boat.position.ycomp()+self.meter2degree(h.position.ycomp())
        #print(dir(self.hullDisplay[0]))
        for s in self.boat.sails:
            #x1, y1 are the points on the mast
            x1 = self.boat.position.xcomp()+self.meter2degree(math.cos((self.boat.angle.calc()+s.position.angle.calc()-90)*math.pi/180)*s.position.norm)
            y1 = self.boat.position.ycomp()+self.meter2degree(math.sin((self.boat.angle.calc()+s.position.angle.calc()-90)*math.pi/180)*s.position.norm)
            x2 = x1+self.meter2degree(math.cos((180+self.boat.angle.calc()+s.angle.calc())*math.pi/180)*s.size)
            y2 = y1+self.meter2degree(math.sin((180+self.boat.angle.calc()+s.angle.calc())*math.pi/180)*s.size)
            self.sailDisplay.append(self.ax.plot([x1,x2],[y1,y2], color = 'yellow')[0])
            #self.ax.plot([x1],[y1], color = 'pink') #mast or something
    def update(self):
        self.boat.update(0.2)
        
        t = transforms.Affine2D().translate(self.boat.position.xcomp()-self.pos[0],self.boat.position.ycomp()-self.pos[1])
        r = transforms.Affine2D().rotate_deg_around(self.pos[0],self.pos[1],self.boat.angle.calc())
        sum = r + t + self.ax.transData
        #hulls
        for i, h in enumerate(self.hullDisplay):
            hull = self.boat.hulls[i]
            cx = self.boat.position.xcomp()+self.meter2degree(hull.position.xcomp())
            cy = self.boat.position.ycomp()+self.meter2degree(hull.position.ycomp())
            #lift
            self.forceDisplay[2*i].set_xdata([cx,cx+self.meter2degree(self.boat.hullLiftForce(i).xcomp())])
            self.forceDisplay[2*i].set_ydata([cy,cy+self.meter2degree(self.boat.hullLiftForce(i).ycomp())])
            #drag
            self.forceDisplay[2*i+1].set_xdata([cx,cx+self.meter2degree(self.boat.hullDragForce(i).xcomp())])
            self.forceDisplay[2*i+1].set_ydata([cy,cy+self.meter2degree(self.boat.hullDragForce(i).ycomp())])
            #tranforms
            h.set_transform(sum)
            self.forceDisplay[2*i].set_transform(sum)
            self.forceDisplay[2*i+1].set_transform(sum)


        #sails
        for s in self.sailDisplay:
            s.set_transform(sum)
        #connections
        for c in self.connections:
            c.set_transform(sum)
        self.pos = [self.boat.position.xcomp(),self.boat.position.ycomp()]

    def meter2degree(self, v):
        return v*90/1000000
        return v/111111


class display:
    def __init__(self,location,boat):
        self.f, self.axes = plt.subplot_mosaic('AAAB;AAAC', figsize=(8, 5)) #,per_subplot_kw={"B": {"projection": "polar"},},
        self.pause = False
        self.map(location)
        self.boat = boatDisplayShell(boat,self.axes['A'])

        self.axes['B'].set_title('Display Settings')
        self.axes['B'].axis('off')
        self.displaySettings()

        self.axes['C'].set_title('Debug Values')
        self.axes['C'].axis('off')
        self.text = []
        self.text.append(self.axes['C'].text(0, 0.9, "Hull Apparent A:0", fontsize=9))
        self.text.append(self.axes['C'].text(0, 0.8, "Sail Apparent A:0", fontsize=9))
        self.text.append(self.axes['C'].text(-0.17, 0.7, "Hull lift F:0", fontsize=6))
        self.text.append(self.axes['C'].text(-0.17, 0.6, "Hull Drag F:0", fontsize=6))
        self.text.append(self.axes['C'].text(0, 0.5, "Sail lift F:0", fontsize=9))
        self.text.append(self.axes['C'].text(0, 0.4, "Sail Drag F:0", fontsize=9))
        self.displayValues()

        #credits
        plt.figtext(0, 0.01, 'Map: © OpenStreetMap contributors', fontsize = 10)

    def pauseT(self,t):
        self.pause = not self.pause
        if self.pause:
            self.pauseButton.label.set_text('Play Animation')
        else:
            self.pauseButton.label.set_text('Pause Animation')

    def displaySettings(self):
        F_button_ax = plt.axes([0, 0, 1, 1])
        forcesInp = InsetPosition(self.axes['B'], [0, 0.9, 0.9, 0.1]) #x,y,w,h
        F_button_ax.set_axes_locator(forcesInp)
        self.forceButton = Button(F_button_ax, 'Show Forces')

        P_button_ax = plt.axes([0, 0, 1, 1])
        pauseInp = InsetPosition(self.axes['B'], [0, 0.78, 0.9, 0.1]) #x,y,w,h
        P_button_ax.set_axes_locator(pauseInp)
        self.pauseButton = Button(P_button_ax, 'Pause Animation')
        self.pauseButton.on_clicked(self.pauseT)

    def displayValues(self):
        #Apparent Wind
        self.text[0].set_text("Hull Apparent V:" + rm_ansi(str(Angle.norm(self.boat.boat.hullAparentWind(1).angle))).replace("Angle: ",""))
        self.text[1].set_text("Sail Apparent V:" + rm_ansi(str(Angle.norm(self.boat.boat.sailAparentWind(0).angle))).replace("Angle: ",""))
        #Hull Forces
        self.text[2].set_text("Hull lift F:" + rm_ansi(str(self.boat.boat.hullLiftForce(0))))
        self.text[3].set_text("Hull Drag F:" + rm_ansi(str(self.boat.boat.hullDragForce(1))))


    def map(self,location):
        cords = regionPolygon(location)
        x = [i[0] for i in cords]
        y = [i[1] for i in cords]
        self.axes['A'].set_title(location.split(" ")[0]+ " map")
        self.axes['A'].fill(x,y,'b')
        self.axes['A'].axis([min(x), max(x),min(y), max(y)])
        self.axes['A'].grid()
    
    def updateCycle(self,f):
        if not self.pause:
            self.boat.update()
            self.displayValues()

    def runAnimation(self):
        anim = FuncAnimation(self.f, self.updateCycle, interval=100, frames=100)
        plt.show()
        #anim.save('test.gif')


if __name__ == "__main__":
    lakeAttitash = "Lake Attitash, Amesbury, Essex County, Massachusetts, USA"
    lakeShoreline = "Shoreline lake, Mountain View, Santa Clara County, California, United States"

    vaka = foil(data_dir+"\\data\\xf-naca001034-il-1000000-Ex.csv", 1, 0.5,rotInertia = 1,size = 1.8)
    ama1 = foil(data_dir+"\\data\\naca0009-R0.69e6-F180.csv", 1, 0.5,position = Vector(Angle(1,90),0.6),rotInertia = 1,size = 1.5)
    ama2 = foil(data_dir+"\\data\\naca0009-R0.69e6-F180.csv", 1, 0.5,position = Vector(Angle(1,-90),0.6),rotInertia = 1.1,size = 1.5)
    sail = foil(data_dir+"\\data\\mainSailCoeffs.cvs", 0.128, 1, position = Vector(Angle(1,90),0.4),rotInertia = 1,size = 0.7)
    sail.angle += Angle(1,10)
    wind = Vector(Angle(1,270),3.6) # Going South wind, 7 kn
    boat = Boat([ama1,vaka,ama2],[sail],wind)
    boat.angle = Angle(1,0)
    sail.angle = Angle(1,30)
    xpos = -122.09064
    ypos = 37.431749
    boat.setPos(Vector(Angle(1,round(math.atan2(ypos,xpos)*180/math.pi*10000)/10000),math.sqrt(xpos**2+ypos**2)))
    render = display(lakeShoreline,boat)
    render.runAnimation()