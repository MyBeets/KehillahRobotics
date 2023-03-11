import osmnx as ox
import geopandas as gpd
import matplotlib.pyplot as plt

lakeAttitash = "Lake Attitash, Amesbury, Essex County, Massachusetts, USA"
lakeShoreline = "Shoreline lake, Mountain View, Santa Clara County, California, United States"
area = ox.geocode_to_gdf(lakeAttitash)
area.plot()
plt.figtext(0, 0.1, '© OpenStreetMap contributors', fontsize = 10)
plt.show()
#print(area)