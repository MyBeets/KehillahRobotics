#Display and Map
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.transforms as transforms
import matplotlib.patches as patches
from mpl_toolkits.axes_grid1.inset_locator import InsetPosition
from matplotlib.widgets import Slider, Button
from Map import regionPolygon, loadGrib
#Boat and variables
from Foil import foil, Winch
from Variables import *
from Boat import Boat
from Control import Controler, printA
from Compressor import *
#Other
import os
import math
import copy
import re

fps = 70
numCycle = 20
data_dir = os.path.dirname(__file__) #abs dir

def rm_ansi(line):
    ansi_escape =re.compile(r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]')
    return ansi_escape.sub('', line)

class boatDisplayShell():
    def __init__(self,Boat,ax,refLat):
        self.ax = ax
        self.boat = Boat
        self.refLat =refLat
    def initAuto(self):
        #This function needs to be ran after some other stuff
        # waypointsPr = [
        #     [self.boat.position.xcomp()-meter2degreeX(1.5,self.refLat),self.boat.position.ycomp()],
        #     [self.boat.position.xcomp()-meter2degreeX(1.5,self.refLat)-meter2degreeX(25,self.refLat),self.boat.position.ycomp()-meter2degreeY(25*math.sqrt(3))],
        #     [self.boat.position.xcomp()+meter2degreeX(1.5,self.refLat)+meter2degreeX(25,self.refLat),self.boat.position.ycomp()-meter2degreeY(25*math.sqrt(3))],
        #     [self.boat.position.xcomp()+meter2degreeX(1.5,self.refLat),self.boat.position.ycomp()],
        # ]
        waypointsE = [
            [self.boat.position.xcomp()+meter2degreeX(25,self.refLat),self.boat.position.ycomp()],
            [self.boat.position.xcomp()+meter2degreeX(25,self.refLat),self.boat.position.ycomp()+meter2degreeY(15)],
            [self.boat.position.xcomp()-meter2degreeX(25,self.refLat),self.boat.position.ycomp()+meter2degreeY(15)],
            [self.boat.position.xcomp()-meter2degreeX(25,self.refLat),self.boat.position.ycomp()],
        ]
        self.buoy(waypointsE)
        self.autopilot = Controler(self.boat)
        self.autopilot.course = self.autopilot.plan("e",waypointsE)
        self.plotCourse(self.autopilot.course)
    def buoy(self,points):
        for p in points:
            self.ax.add_patch(plt.Circle(p, meter2degreeY(0.4), color='orange'))
    def plotCourse(self,course):
        xs = [x[0] for x in course]
        ys = [x[1] for x in course]
        self.ax.plot(xs,ys, color = 'red')
    def createBoat(self):
        self.hullDisplay = []
        self.sailDisplay = []
        self.connections = []
        self.forceDisplay = []
        self.winches = []
        for i, h in enumerate(self.boat.hulls):
            verts = [(meter2degreeX(p[0]*h.size+ h.position.xcomp(),self.refLat)+self.boat.position.xcomp(),meter2degreeY(p[1]*h.size+h.position.ycomp())+self.boat.position.ycomp()) for p in h.polygon]
            polygon = patches.Polygon(verts, color="gray") 

            #NOTE YOU"LL NEED TO ADD A REAL CENTER OF MASS FUNCTIONALITY
            print("TODO: CENTER OF MASS")
            r = transforms.Affine2D().rotate_deg_around(self.boat.position.xcomp(),self.boat.position.ycomp(),(self.boat.angle+h.angle).calc())

            polygon.set_transform(r+ self.ax.transData)
            self.hullDisplay.append(self.ax.add_patch(polygon))

            print("TODO: CENTER OF LATERAL RESISTANCE")
            #hull lift
            self.forceDisplay.append(self.ax.plot([0,0],[0,0], color = 'red')[0])
            #hull drag
            self.forceDisplay.append(self.ax.plot([0,0],[0,0], color = 'green')[0])


            # if len(self.boat.hulls) > 1:
            #     if cx == -1:
            #         cx = self.boat.position.xcomp()+self.meter2degree(h.position.xcomp())
            #         cy = self.boat.position.ycomp()+self.meter2degree(h.position.ycomp())
            #     else:
            #         self.connections.append(self.ax.plot([cx,self.boat.position.xcomp()+self.meter2degree(h.position.xcomp())],[cy,self.boat.position.ycomp()+self.meter2degree(h.position.ycomp())], color = 'gray')[0])
            #         cx = self.boat.position.xcomp()+self.meter2degree(h.position.xcomp())
            #         cy = self.boat.position.ycomp()+self.meter2degree(h.position.ycomp())
        for s in self.boat.sails:
            #x1, y1 are the points on the mast
            x1 = self.boat.position.xcomp()+meter2degreeX(math.cos((self.boat.angle.calc()+s.position.angle.calc()-90)*math.pi/180)*s.position.norm,self.refLat)
            y1 = self.boat.position.ycomp()+meter2degreeY(math.sin((self.boat.angle.calc()+s.position.angle.calc()-90)*math.pi/180)*s.position.norm)
            x2 = x1+meter2degreeX(math.cos((180+self.boat.angle.calc()+s.angle.calc())*math.pi/180)*s.size,self.refLat)
            y2 = y1+meter2degreeY(math.sin((180+self.boat.angle.calc()+s.angle.calc())*math.pi/180)*s.size)
            self.sailDisplay.append(self.ax.plot([x1,x2],[y1,y2], color = 'yellow')[0])
            print("TODO: CENTER OF EFFORT")
            #sail lift
            self.forceDisplay.append(self.ax.plot([0,0],[0,0], color = 'gold')[0])
            #sail drag
            self.forceDisplay.append(self.ax.plot([0,0],[0,0], color = 'lime')[0])
            for w in s.winches:
                self.winches.append(self.ax.add_patch(plt.Circle((self.boat.position.xcomp()+meter2degreeX(w.position.xcomp(),self.refLat),self.boat.position.ycomp()+meter2degreeY(w.position.ycomp())),meter2degreeY(w.radius), color='r')))
        #boat net forces:
        self.forceDisplay.append(self.ax.plot([0,0],[0,0], color = 'black')[0])
        #Boat velocity
        self.forceDisplay.append(self.ax.plot([0,0],[0,0], color = 'magenta')[0])

    def update(self, auto,showForces):
        for i in range(numCycle):
            self.boat.update(1/fps)#*4
        if auto:
            self.autopilot.update(1/fps)
        forceScale = 0.01
        #hulls
        for i, h in enumerate(self.hullDisplay):
            hull = copy.deepcopy(self.boat.hulls[i])
            hull.position.angle += Angle.norm(self.boat.angle)
            #print(hull.position)
            cx = self.boat.position.xcomp() + meter2degreeX(hull.position.xcomp(),self.refLat)
            cy = self.boat.position.ycomp() + meter2degreeY(hull.position.ycomp())

            r = transforms.Affine2D().rotate_deg_around(cx,cy,(self.boat.angle+self.boat.hulls[i].angle).calc()) # NOTE: This is not a mistake
            sum = r + self.ax.transData

            if showForces:
                self.forceDisplay[2*i].set_linestyle("solid")
                self.forceDisplay[2*i+1].set_linestyle("solid")
                #lift
                self.forceDisplay[2*i].set_xdata([cx,cx+forceScale*meter2degreeX(self.boat.hullLiftForceandMoment(i)[0].xcomp(),self.refLat)])
                self.forceDisplay[2*i].set_ydata([cy,cy+forceScale*meter2degreeY(self.boat.hullLiftForceandMoment(i)[0].ycomp())])
                #drag
                self.forceDisplay[2*i+1].set_xdata([cx,cx+forceScale*meter2degreeX(self.boat.hullDragForceandMoment(i)[0].xcomp(),self.refLat)])
                self.forceDisplay[2*i+1].set_ydata([cy,cy+forceScale*meter2degreeY(self.boat.hullDragForceandMoment(i)[0].ycomp())])
            else:
                self.forceDisplay[2*i].set_linestyle("None")
                self.forceDisplay[2*i+1].set_linestyle("None")
            #tranforms
            verts = [(meter2degreeX(p[0]*self.boat.hulls[i].size,self.refLat)+cx,meter2degreeY(p[1]*self.boat.hulls[i].size)+cy) for p in self.boat.hulls[i].polygon]
            #verts = [(meter2degreeX(p[0]*self.boat.hulls[i].size+ self.boat.hulls[i].position.xcomp(),self.refLat)+self.boat.position.xcomp(),meter2degreeY(p[1]*self.boat.hulls[i].size+self.boat.hulls[i].position.ycomp())+self.boat.position.ycomp()) for p in self.boat.hulls[i].polygon]
            self.hullDisplay[i].set_xy(verts)

            self.hullDisplay[i].set_transform(sum)

        #sails
        for i, s in enumerate(self.sailDisplay):
            x1 = self.boat.position.xcomp()+meter2degreeX(math.cos((self.boat.angle.calc()+self.boat.sails[i].position.angle.calc()-90)*math.pi/180)*self.boat.sails[i].position.norm,self.refLat)
            y1 = self.boat.position.ycomp()+meter2degreeY(math.sin((self.boat.angle.calc()+self.boat.sails[i].position.angle.calc()-90)*math.pi/180)*self.boat.sails[i].position.norm)
            x2 = x1+meter2degreeX(math.cos((180+self.boat.angle.calc()+self.boat.sails[i].angle.calc())*math.pi/180)*self.boat.sails[i].size,self.refLat)
            y2 = y1+meter2degreeY(math.sin((180+self.boat.angle.calc()+self.boat.sails[i].angle.calc())*math.pi/180)*self.boat.sails[i].size)
            
            CEx = x1+meter2degreeX(math.cos((180+self.boat.angle.calc()+self.boat.sails[i].angle.calc())*math.pi/180)*self.boat.sails[i].size/2,self.refLat)
            CEy = y1+meter2degreeY(math.sin((180+self.boat.angle.calc()+self.boat.sails[i].angle.calc())*math.pi/180)*self.boat.sails[i].size/2)
            # CEx = x1
            # CEy = y1
            if showForces:
                #lift
                self.forceDisplay[2*i+len(self.hullDisplay)*2].set_linestyle("solid")
                self.forceDisplay[2*i+1+len(self.hullDisplay)*2].set_linestyle("solid")
                self.forceDisplay[2*i+len(self.hullDisplay)*2].set_xdata([CEx,CEx+forceScale*meter2degreeX(self.boat.sailLiftForce(i).xcomp(),self.refLat)])
                self.forceDisplay[2*i+len(self.hullDisplay)*2].set_ydata([CEy,CEy+forceScale*meter2degreeY(self.boat.sailLiftForce(i).ycomp())])
                #drag
                self.forceDisplay[2*i+1+len(self.hullDisplay)*2].set_xdata([CEx,CEx+forceScale*meter2degreeX(self.boat.sailDragForce(i).xcomp(),self.refLat)])
                self.forceDisplay[2*i+1+len(self.hullDisplay)*2].set_ydata([CEy,CEy+forceScale*meter2degreeY(self.boat.sailDragForce(i).ycomp())])
            else:
                self.forceDisplay[2*i+len(self.hullDisplay)*2].set_linestyle("None")
                self.forceDisplay[2*i+1+len(self.hullDisplay)*2].set_linestyle("None")
            # self.forceDisplay[2*i+len(self.hullDisplay)*2].set_transform(sum)
            # self.forceDisplay[2*i+1+len(self.hullDisplay)*2].set_transform(sum)

            s.set_xdata([x1,x2])
            s.set_ydata([y1,y2])
            for idx, w in enumerate(self.boat.sails[i].winches):
                pos = w.position.meter2degree(self.refLat)
                pos.angle += self.boat.angle - Angle(1,90)
                pos += self.boat.position
                self.winches[idx].set(center =(pos.xcomp(),pos.ycomp()))
        if showForces:
            #boat net forces
            f = self.boat.forces["sails"]+self.boat.forces["hulls"]
            self.forceDisplay[-2].set_xdata([self.boat.position.xcomp(),self.boat.position.xcomp()+forceScale*meter2degreeX(f.xcomp(),self.refLat)])
            self.forceDisplay[-2].set_ydata([self.boat.position.ycomp(),self.boat.position.ycomp()+forceScale*meter2degreeY(f.ycomp())])
            #boat velocity
            self.forceDisplay[-1].set_xdata([self.boat.position.xcomp(),self.boat.position.xcomp()+forceScale*meter2degreeX(self.boat.linearVelocity.xcomp(),self.refLat)])
            self.forceDisplay[-1].set_ydata([self.boat.position.ycomp(),self.boat.position.ycomp()+forceScale*meter2degreeY(self.boat.linearVelocity.ycomp())])
        else:
            self.forceDisplay[-2].set_linestyle("None")
            self.forceDisplay[-1].set_linestyle("None")
        # #connections
        # for c in self.connections:

        #     c.set_transform(sum)



class display:
    def __init__(self,location,boat):
        self.f, self.axes = plt.subplot_mosaic('AAABD;AAACC', figsize=(12, 5)) #,per_subplot_kw={"B": {"projection": "polar"},},
        self.pause = False
        self.track = False
        self.auto = False
        self.forceShow = True
        self.time = 0

        self.boat = boatDisplayShell(boat,self.axes['A'],boat.position.ycomp())
        self.map(location) # creates map and sets units
        self.boat.initAuto()
        self.boat.createBoat()

        self.axes['B'].set_title('Display Settings')
        self.axes['B'].axis('off')
        self.displaySettings()

        self.axes['C'].set_title('Debug Values')
        self.axes['C'].axis('off')
        self.text = []
        self.text.append(self.axes['C'].text(0, 0.9, "Boat LVelocity V:0", fontsize=9))
        self.text.append(self.axes['C'].text(0, 0.8, "Boat AVelocity V:0", fontsize=9))
        self.text.append(self.axes['C'].text(0, 0.7, "Hull Apparent A:0", fontsize=9))
        self.text.append(self.axes['C'].text(0, 0.6, "Sail Apparent A:0", fontsize=9))
        self.text.append(self.axes['C'].text(0, 0.5, "Hull lift F:0", fontsize=9))
        self.text.append(self.axes['C'].text(0, 0.4, "Hull Drag F:0", fontsize=9))
        self.text.append(self.axes['C'].text(0, 0.3, "Sail lift F:0", fontsize=9))
        self.text.append(self.axes['C'].text(0, 0.2, "Sail Drag F:0", fontsize=9))
        #self.text.append(self.axes['C'].text(0, 0.1, "Net Force F:0", fontsize=9))
        self.text.append(self.axes['C'].text(0, 0.1, "Boat Position V:0", fontsize=9))
        self.text.append(self.axes['C'].text(0, 0, "Time (s):0", fontsize=9))
        self.displayValues()

        self.axes['D'].set_title('Boat Controls')
        self.axes['D'].axis('off')
        self.boatControls()

        #credits
        plt.figtext(0, 0.01, 'Map: © OpenStreetMap contributors', fontsize = 10)


    def bUpdate(self,v):
        # self.boat.boat.angle = Angle(1,self.bRot.val)
        self.boat.boat.hulls[-1].angle = Angle(1,self.bRot.val)

    def sUpdate(self,v):
        if len(self.boat.boat.sails[0].winches) == 0:
            self.boat.boat.sails[0].angle = Angle(1,self.sRot.val)
        else:
            if self.sRot.val != self.boat.boat.sails[0].winches[0].rot.calc():
                self.boat.boat.sails[0].setSailRotation(Angle(1,self.sRot.val))


    def boatControls(self):
        bax = plt.axes([0, 0, 1, 1])
        bforcesInp = InsetPosition(self.axes['D'], [0.6, 0.9, 0.9, 0.1]) #x,y,w,h
        bax.set_axes_locator(bforcesInp)
        self.bRot = Slider(
            ax=bax,
            label="Rudder Rotation:",
            valmin=-20,
            valmax=20,
            valinit=self.boat.boat.angle.calc(),
        )
        self.bRot.on_changed(self.bUpdate)
        sax = plt.axes([0, 0, 1, 1])
        sforcesInp = InsetPosition(self.axes['D'], [0.45, 0.75, 0.9, 0.1]) #x,y,w,h
        sax.set_axes_locator(sforcesInp)
        self.sRot = Slider(
            ax=sax,
            label="Sail Rotation:",
            valmin=-90,
            valmax=90,
            valinit=self.boat.boat.sails[0].angle.calc(),
        )
        self.sRot.on_changed(self.sUpdate)


    def pauseT(self,t):
        self.pause = not self.pause
        if self.pause:
            self.pauseButton.label.set_text('Play Animation')
        else:
            self.pauseButton.label.set_text('Pause Animation')

    def trackZ(self,t):
        self.track = not self.track
        if self.track:
            self.zoomButton.label.set_text('Stop Tracking')
        else:
            self.zoomButton.label.set_text('Track Boat')
    def autoF(self,t):
        self.auto = not self.auto
        if self.auto:
            self.autoButton.label.set_text('Auto Pilot: ON')
        else:
            self.autoButton.label.set_text('Auto Pilot: OFF')
    def forceS(self,t):
        self.forceShow = not self.forceShow
        if self.forceShow:
            self.forceButton.label.set_text('Hide Forces')
        else:
            self.forceButton.label.set_text('Show Forces')
    def displaySettings(self):
        F_button_ax = plt.axes([0, 0, 1, 1])
        forcesInp = InsetPosition(self.axes['B'], [0, 0.9, 0.9, 0.1]) #x,y,w,h
        F_button_ax.set_axes_locator(forcesInp)
        self.forceButton = Button(F_button_ax, 'Hide Forces')
        self.forceButton.on_clicked(self.forceS)

        P_button_ax = plt.axes([0, 0, 1, 1])
        pauseInp = InsetPosition(self.axes['B'], [0, 0.78, 0.9, 0.1]) #x,y,w,h
        P_button_ax.set_axes_locator(pauseInp)
        self.pauseButton = Button(P_button_ax, 'Pause Animation')
        self.pauseButton.on_clicked(self.pauseT)

        Z_button_ax = plt.axes([0, 0, 1, 1])
        zoomInp = InsetPosition(self.axes['B'], [0, 0.66, 0.9, 0.1]) #x,y,w,h
        Z_button_ax.set_axes_locator(zoomInp)
        self.zoomButton = Button(Z_button_ax, 'Track Boat')
        self.zoomButton.on_clicked(self.trackZ)

        A_button_ax = plt.axes([0, 0, 1, 1])
        autoInp = InsetPosition(self.axes['B'], [0, 0.54, 0.9, 0.1]) #x,y,w,h
        A_button_ax.set_axes_locator(autoInp)
        self.autoButton = Button(A_button_ax, 'Auto Pilot: OFF')
        self.autoButton.on_clicked(self.autoF)

    def displayValues(self):
        #Velocity
        self.text[0].set_text("Boat LVelocity V:" + rm_ansi(str(self.boat.boat.linearVelocity)))
        self.text[1].set_text("Boat AVelocity V:" + rm_ansi(str(round(self.boat.boat.rotationalVelocity*180/math.pi*10000)/10000)))
        #Apparent Wind
        self.text[2].set_text("Hull Apparent V:" + rm_ansi(str(self.boat.boat.hullAparentWind(1))).replace("Vector",""))
        self.text[3].set_text("Sail Apparent V:" + rm_ansi(str(self.boat.boat.sailAparentWind(0))).replace("Vector",""))
        #Hull Forces
        self.text[4].set_text("Hull lift F:" + rm_ansi(str(self.boat.boat.hullLiftForceandMoment(1)[0])))
        self.text[5].set_text("Hull Drag F:" + rm_ansi(str(self.boat.boat.hullDragForceandMoment(1)[0])))
        #Sail Forces
        self.text[6].set_text("Sail lift F:" + rm_ansi(str(self.boat.boat.sailLiftForce(0))))
        self.text[7].set_text("Sail Drag F:" + rm_ansi(str(self.boat.boat.sailDragForce(0))))
        #net
        #self.text[8].set_text("Net Force F:" + rm_ansi(str((self.boat.boat.forces["sails"]+self.boat.boat.forces["hulls"]))))
        #pos 
        xs = str(self.boat.boat.position.xcomp())
        ys = str(self.boat.boat.position.ycomp())
        self.text[8].set_text("Boat Position V:" + rm_ansi("("+xs[0:min(10,len(xs))]+", "+ys[0:min(10,len(ys))]+")"))

        self.text[9].set_text("Time (s):"+str(self.time))

    def map(self,location):
        cords = regionPolygon(location)
        x = [i[0] for i in cords]
        y = [i[1] for i in cords]

        mx = min(x)
        my = min(y)

        #the cordinates are typically in degrees
        x = [(i-mx) for i in x] # normalisation
        y = [(i-my) for i in y]

        bx = (self.boat.boat.position.xcomp()-mx)
        by = (self.boat.boat.position.ycomp()-my)
        self.boat.boat.setPos(Vector(Angle(1,round(math.atan2(by,bx)*180/math.pi*10000)/10000),math.sqrt(bx**2+by**2)))

        self.axes['A'].set_title(location.split(" ")[0]+ " map")
        self.axes['A'].fill(x,y,'b')
        self.axes['A'].axis([min(x), max(x),min(y), max(y)])
        self.axes['A'].grid()
    
    def updateCycle(self,f):
        if not self.pause:
            self.boat.update(self.auto,self.forceShow)
            self.time +=1/fps * numCycle
            self.bRot.set_val(printA(self.boat.boat.hulls[-1].angle.calc()))

            if len(self.boat.boat.sails[0].winches) == 0:
                self.sRot.set_val(printA(self.boat.boat.sails[0].angle.calc()))
            else:
                self.sRot.set_val(printA(self.boat.boat.sails[0].winches[0].rot.calc()))
            
            if self.track:
                dx = self.axes['A'].get_xlim()[1]-self.axes['A'].get_xlim()[0]
                dy = self.axes['A'].get_ylim()[1]-self.axes['A'].get_ylim()[0]
                dm = max(dx,dy)#anti-distortion
                self.axes['A'].set_xlim(self.boat.boat.position.xcomp()-dm/2,self.boat.boat.position.xcomp()+dm/2)
                self.axes['A'].set_ylim(self.boat.boat.position.ycomp()-dm/2,self.boat.boat.position.ycomp()+dm/2)
            self.displayValues()
        #return self.boat.forceDisplay+self.boat.hullDisplay+self.boat.sailDisplay+self.text #list(self.axes.values())+

    def runAnimation(self):
        anim = FuncAnimation(self.f, self.updateCycle, interval=1000/fps,cache_frame_data=False)#,blit = True)
        plt.show()
        #anim.save('test.gif')


if __name__ == "__main__":
    lakeAttitash = "Lake Attitash, Amesbury, Essex County, Massachusetts, USA"
    lakeShoreline = "Shoreline lake, Mountain View, Santa Clara County, California, United States"

    vaka = foil(data_dir+"\\data\\xf-naca001034-il-1000000-Ex.csv", 997.77, 0.25,rotInertia = 15,size = 1.8)
    ama1 = foil(data_dir+"\\data\\naca0009-R0.69e6-F180.csv", 997.77, 0.5,position = Vector(Angle(1,90),0.6),rotInertia = 100,size = 1.5)
    ama2 = foil(data_dir+"\\data\\naca0009-R0.69e6-F180.csv", 997.77, 0.5,position = Vector(Angle(1,-90),0.6),rotInertia = 100,size = 1.5)
    rudder = foil(data_dir+"\\data\\naca0015-R7e7-F180.csv", 997.77, 0.5,position = Vector(Angle(1,180),vaka.size/2),rotInertia = 100,size = 0.3)
    offset = 0.45 # 15cm
    BabordWinch = Winch(Vector(Angle(1,180),0.6) + Vector(Angle(1,270),offset), 30, 0.025) #2.5cm radius
    TribordWinch = Winch(Vector(Angle(1,0),0.6) + Vector(Angle(1,270),offset), 30, 0.025) #2.5cm radius
    #sail = foil(data_dir+"\\data\\mainSailCoeffs.cvs", 1.204, 5, position = Vector(Angle(1,90),0.4),rotInertia = 11,size = 0.7, winches = [BabordWinch, TribordWinch])
    sail = foil(data_dir+"\\data\\MarchajSail.cvs", 1.204, 5, position = Vector(Angle(1,90),0.4),rotInertia = 11,size = 0.7, winches = [BabordWinch, TribordWinch])
    sail.setSailRotation(Angle(1,0))
    # sail.angle += Angle(1,10)
    wind = Vector(Angle(1,270),5.3) # Going South wind, 7 kn
    xpos = -122.09064
    ypos = 37.431749
    boat = Boat([ama1,vaka,ama2,rudder],[sail],wind,mass =15,refLat=ypos)
    boat.angle = Angle(1,-93)
    sail.angle = Angle(1,75)
    sail.setSailRotation(sail.angle)
    boat.setPos(Vector(Angle(1,round(math.atan2(ypos,xpos)*180/math.pi*10000)/10000),math.sqrt(xpos**2+ypos**2)))
    polars = input("recalc Polars Y/N:\n")
    if "y" in polars.lower():
        generatePolars(boat,"MarPol")
    render = display(lakeShoreline,boat)
    render.runAnimation()