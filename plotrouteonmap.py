#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 11 13:50:46 2021

@author: klaudiamur
"""

import pandas as pd
import geopandas as gpd

import os

import contextily as ctx
import shapely

from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

from time import sleep # to limit geocoding rate in for loops

import matplotlib.pyplot as plt
from matplotlib.colors import to_hex
import seaborn as sns
%matplotlib inline


### get locations from folder of pics


image_list = os.listdir('c:\\users\\Aaron\\photo')
image_list = [a for a in image_list if a.endswith('jpg')]


### pick just one location for pics close to each other, get info about loc name, date

world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

# Get just the US
usa = world.query('name == "Sweden"')

# Plot the USA
ax = usa.boundary.plot()
# Overlay my point locations
gdf.plot(ax=ax)

# Plot the points
ax = gdf.plot(figsize=(10, 5))

# Add basemap
ctx.add_basemap(ax=ax)


# Set the projection to WGS84
gdf.crs = {'init': 'epsg:4326'}
# Modify projection to match what contextily uses
gdf = gdf.to_crs(epsg=3857)

