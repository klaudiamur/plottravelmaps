#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 11 13:50:46 2021

@author: klaudiamur
"""

import pandas as pd
import matplotlib.pyplot as plt
import osmnx
import numpy as np
import geopandas as gpd
import re
from PIL.ExifTags import GPSTAGS
from PIL.ExifTags import TAGS
from PIL import Image
from matplotlib.offsetbox import TextArea, DrawingArea, OffsetImage, AnnotationBbox

import matplotlib.pyplot as plt
import matplotlib.image as mpimg

def get_exif(filename):
    image = Image.open(filename)
    image.verify()
    return image._getexif()


# exif = get_exif('image.jpg')
# print(exif)



def get_geotagging(exif):
    if not exif:
        raise ValueError("No EXIF metadata found")

    geotagging = {}
    for (idx, tag) in TAGS.items():
        if tag == 'GPSInfo':
            if idx not in exif:
                raise ValueError("No EXIF geotagging found")

            for (key, val) in GPSTAGS.items():
                if key in exif[idx]:
                    geotagging[val] = exif[idx][key]

    return geotagging




def dms2dec(dms_str):
    dms_str = re.sub(r'\s', '', dms_str)

    sign = -1 if re.search('[swSW]', dms_str) else 1

    numbers = [*filter(len, re.split('\D+', dms_str, maxsplit=4))]

    degree = numbers[0]
    minute = numbers[1] if len(numbers) >= 2 else '0'
    second = numbers[2] if len(numbers) >= 3 else '0'
    frac_seconds = numbers[3] if len(numbers) >= 4 else '0'

    second += "." + frac_seconds
    return sign * (int(degree) + float(minute) / 60 + float(second) / 3600)


def get_decimal_from_dms(dms, ref):
    degrees = dms[0]
    minutes = dms[1] / 60.0
    seconds = dms[2] / 3600.0

    if ref in ['S', 'W']:
        degrees = -degrees
        minutes = -minutes
        seconds = -seconds

    return round(degrees + minutes + seconds, 5)


def get_coordinates(geotags):
    lat = get_decimal_from_dms(geotags['GPSLatitude'], geotags['GPSLatitudeRef'])
    # lat = dms2dec(geotags['GPSLatitude'])
    # lon = dms2dec(geotags['GPSLatitude'])
    lon = get_decimal_from_dms(geotags['GPSLongitude'], geotags['GPSLongitudeRef'])

    return (lat, lon)


locdict = {}
tdict = {}
# locdata = pd.DataFrame(columns = [longlat, time])

import os

path = '/Users/klaudiamur/Dropbox/nerdstuff/travelmaps/pics'
directory = os.fsencode(path)
### aaaah get time from it as well!!!!
for file in os.listdir(directory):
    filename = os.fsdecode(file)
    if filename.endswith('jpg'):
        p = os.path.join(path, filename)
        exif = get_exif(p)
        t = exif[36867]
        geotags = get_geotagging(exif)
        coords = get_coordinates(geotags)
        locdict[filename] = coords
        tdict[filename] = t

locdata = pd.DataFrame([locdict, tdict]).transpose()
locdata['name'] = locdata.index
locdata = locdata.sort_values(by=[1])
## sort it after 1! (and search for the route based on that, hehe)
## idea: make 1 map with time and km! yaaa
## if distance between 2 points bigger than 50km

#G = osmnx.graph.graph_from_place('Sweden', network_type='drive')
#nodelist = {}
#for index, row in locdata.iterrows():
 #   nn = osmnx.distance.nearest_nodes(G, X=row[0][1], Y=row[0][0])
 #   nodelist[index] = nn

#locdata['nearest_node'] = pd.Series(nodelist)

# i = 0
#path_list = []
#for n in range(len(locdata) - 1):
#    i = locdata['nearest_node'][n]
  #  j = locdata['nearest_node'][n + 1]
 #   p0 = osmnx.distance.shortest_path(G, i, j, weight='length', cpus=1)
#    path_list.append(p0)

#all_nodes = np.unique([i for j in path_list for i in j])
#Gc = G.subgraph(all_nodes)

#fig, ax = osmnx.plot.plot_graph_routes(Gc, path_list, orig_dest_size=100)
#plt.show()


fig, ax = plt.subplots()

#ax.set_xlim(0, 1)
#ax.set_ylim(0, 1)
fig1 = locdata.iloc[0]
arr_lena = mpimg.imread(path+"/"+fig1['name'])
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

# Get just the US
usa = world.query('name == "Sweden"')

# Plot the USA
usa.boundary.plot()
imagebox = OffsetImage(arr_lena, zoom=0.2)

ab = AnnotationBbox(imagebox, fig1[0])

ax.add_artist(ab)

plt.grid()

plt.draw()
#plt.savefig('add_picture_matplotlib_figure.png',bbox_inches='tight')
plt.show()
# route = nx.shortest_path(G, origin_node, destination_node, weight = 'length')


# x = [row[0][0] for index, row in locdata.iterrows()]
# y = [row[0][1] for index, row in locdata.iterrows()]
# plt.scatter(x, y)

world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

# Get just the US
usa = world.query('name == "Sweden"')

# Plot the USA
ax = usa.boundary.plot()
# Overlay my point locations
# gdf.plot(ax=ax)

# Plot the points
# ax = gdf.plot(figsize=(10, 5))

# Add basemap
# ctx.add_basemap(ax=ax)


# Set the projection to WGS84
# gdf.crs = {'init': 'epsg:4326'}
# Modify projection to match what contextily uses
# gdf = gdf.to_crs(epsg=3857)
