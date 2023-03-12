import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from Map import regionPolygon
from Foil import foil
import os
import math

lakeAttitash = "Lake Attitash, Amesbury, Essex County, Massachusetts, USA"
lakeShoreline = "Shoreline lake, Mountain View, Santa Clara County, California, United States"

f, axes = plt.subplot_mosaic('AAB;AAC')

cords = regionPolygon(lakeAttitash)
x = [i[0] for i in cords]
y = [i[1] for i in cords]
axes['A'].set_title('MAP')
axes['A'].fill(x,y,'c')
axes['A'].axis([min(x), max(x),min(y), max(y)])
axes['A'].grid()

data_dir = os.path.dirname(__file__) #abs dir
hull = foil(data_dir+"\\data\\xf-naca001034-il-1000000-Ex.csv", 1, 0.5)
mod = [[i[0].data()*math.pi/180 for i in hull.liftC],[i[1] for i in hull.liftC]]
axes['B'].set_title('naca001034 liftC')
axes['B'].plot(mod[0],mod[1])
plt.figtext(0, 0.01, '© OpenStreetMap contributors', fontsize = 10)
plt.show()