import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from Map import regionPolygon
from Foil import foil
import os
import math

lakeAttitash = "Lake Attitash, Amesbury, Essex County, Massachusetts, USA"
lakeShoreline = "Shoreline lake, Mountain View, Santa Clara County, California, United States"

fig = plt.figure()

cords = regionPolygon(lakeShoreline)
x = [i[0] for i in cords]
y = [i[1] for i in cords]

ax1 = plt.subplot(121) # more here: https://stackoverflow.com/questions/3584805/what-does-the-argument-mean-in-fig-add-subplot111/3584933#3584933

ax1.fill(x,y,'c')
ax1.axis([min(x), max(x),min(y), max(y)])
ax1.grid()

data_dir = os.path.dirname(__file__) #abs dir
hull = foil(data_dir+"\\data\\xf-naca001034-il-1000000-Ex.csv", 1, 0.5)
ax2 = plt.subplot(222)
mod = [[i[0].data()*math.pi/180 for i in hull.liftC],[i[1] for i in hull.liftC]]
print(mod)
#ax2.plot([0.0, 1.0*math.pi/180, 2.0*math.pi/180, 3.0*math.pi/180, 4.0*math.pi/180, 5.0*math.pi/180, 6.0*math.pi/180, 7.0*math.pi/180, 8.0*math.pi/180,math.pi/2],[0.0, 0.11, 0.22, 0.33, 0.44, 0.55, 0.66, 0.77, 0.88,1])
ax2.plot(mod[0],mod[1])
ax3 = plt.subplot(224)
plt.figtext(0, 0.01, '© OpenStreetMap contributors', fontsize = 10)
plt.show()