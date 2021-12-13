#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 11 13:50:46 2021

@author: klaudiamur
"""

import pandas as pd
import matplotlib.pyplot as plt
import osmnx as ox
import numpy as np
import geopandas as gpd
import re
from PIL.ExifTags import GPSTAGS
from PIL.ExifTags import TAGS
from PIL import Image
from matplotlib.offsetbox import TextArea, DrawingArea, OffsetImage, AnnotationBbox

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from descartes import PolygonPatch
from shapely.geometry import MultiPolygon
from shapely.geometry import Polygon

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


#G = ox.graph_from_point(locdata[0][0], dist=10000, simplify=True, network_type='drive')
#nodes_proj, edges_proj = ox.graph_to_gdfs(G, nodes=True, edges=True)
#ox.plot_graph(G,node_color='r')



## sort it after 1! (and search for the route based on that, hehe)
## idea: make 1 map with time and km! yaaa
## if distance between 2 points bigger than 50km

G = ox.graph.graph_from_place('Sweden', network_type='drive')
nodelist = {}
for index, row in locdata.iterrows():
    nn = ox.distance.nearest_nodes(G, X=row[0][1], Y=row[0][0])
    nodelist[index] = nn

locdata['nearest_node'] = pd.Series(nodelist)

path_list = []
for n in range(len(locdata) - 1):
    i = locdata['nearest_node'][n]
    j = locdata['nearest_node'][n + 1]
    p0 = ox.distance.shortest_path(G, i, j, weight='length', cpus=1)
    path_list.append(p0)
# i = 0
#path_list = []
#for n in range(len(locdata) - 1):
#    i = locdata['nearest_node'][n]
  #  j = locdata['nearest_node'][n + 1]
 #   p0 = osmnx.distance.shortest_path(G, i, j, weight='length', cpus=1)
#    path_list.append(p0)

all_nodes = np.unique([i for j in path_list for i in j])
Gc = G.subgraph(all_nodes)

place = "Sweden"
gdf = ox.geocode_to_gdf(place)

# plot the network, but do not show it or close it yet
fig, ax = ox.plot_graph_routes(Gc, path_list,
    route_colors='black',
    show=False,
    close=False,
    bgcolor="white",
    edge_color="w",
    edge_linewidth=0.3,
    node_size=0,
)

# to this matplotlib axis, add the place shape as descartes polygon patches
for geometry in gdf["geometry"].tolist():
    if isinstance(geometry, (Polygon, MultiPolygon)):
        if isinstance(geometry, Polygon):
            geometry = MultiPolygon([geometry])
        for polygon in geometry:
            patch = PolygonPatch(polygon, fc="k", 
                                 #ec="#666666", 
                                 ec = 'black',
                                 lw=1, alpha=1, zorder=-1)
            ax.add_patch(patch)

# optionally set up the axes extents
#plt.imshow(arr_lena, extent=(57.64384, 57.64398, 11.8952, 11.8968), zorder=10)
margin = 0.02
west, south, east, north = gdf.unary_union.bounds
margin_ns = (north - south) * margin
margin_ew = (east - west) * margin
ax.set_ylim((south - margin_ns, north + margin_ns))
ax.set_xlim((west - margin_ew, east + margin_ew))

plt.show()


