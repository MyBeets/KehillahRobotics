import osmnx as ox
import geopandas as gpd
import matplotlib.pyplot as plt

place = "Lake Attitash, Amesbury, Essex County, Massachusetts, USA"

area = ox.geocode_to_gdf(place)

area.plot()
plt.show()
print(area)