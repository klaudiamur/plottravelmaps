#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 11 13:50:46 2021

@author: klaudiamur
"""

import pandas as pd
import matplotlib.pyplot as plt
import osmnx
#%matplotlib inline



from geopy.geocoders import Here

from PIL import Image

def get_exif(filename):
    image = Image.open(filename)
    image.verify()
    return image._getexif()

#exif = get_exif('image.jpg')
#print(exif)
from PIL.ExifTags import GPSTAGS
from PIL.ExifTags import TAGS

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


import re


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
    #lat = dms2dec(geotags['GPSLatitude'])
    #lon = dms2dec(geotags['GPSLatitude'])
    lon = get_decimal_from_dms(geotags['GPSLongitude'], geotags['GPSLongitudeRef'])

    return (lat,lon)


locdict = {}
tdict = {}
#locdata = pd.DataFrame(columns = [longlat, time])

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
locdata = locdata.sort_values(by=[1])
## sort it after 1! (and search for the route based on that, hehe)
## idea: make 1 map with time and km! yaaa
## if distance between 2 points bigger than 50km

G = osmnx.graph.graph_from_place('Sweden', network_type = 'drive')
nodelist = {}
for index, row in locdata:
    nn = osmnx.distance.nearest_nodes(G, X=row[0][0], Y=row[0][1])
    nodelist[index] = nn

locdata['nearest_node'] = pd.Series(nodelist)

#i = 0
path_list = []
for n in range(len(locdata)-1):
    i = locdata['nearest_node'][n]
    j = locdata['nearest_node'][n+1]
    p0 = osmnx.distance.shortest_path(G, i, j, weight='length', cpus=1)
    path_list.append(p0)

osmnx.plot.plot_graph_routes(G, path_list, orig_dest_size = 100)
#route = nx.shortest_path(G, origin_node, destination_node, weight = 'length')


#x = [row[0][0] for index, row in locdata.iterrows()]
#y = [row[0][1] for index, row in locdata.iterrows()]
#plt.scatter(x, y)


