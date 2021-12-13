#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 14 00:17:49 2021

@author: klaudiamur
"""





# get the street network, with retain_all=True to retain all the disconnected islands' networks
G = ox.graph_from_place(place, network_type="drive", retain_all=True)

#world = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))

world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

# Get just the US
sweden = world.query('name == "Sweden"')
sweden.plot()

geo_df_t = gpd.GeoDataFrame(df, geometry=geometry_t)
geo_df_t.plot(ax=ax, markersize = 20, color = "red" , alpha=1)
geo_df_line = gpd.GeoDataFrame(df, geometry=lines)
geo_df_line.plot(ax=ax,  color = "black"  , alpha=1  )
geo_df_r = gpd.GeoDataFrame(df, geometry=geometry_r)
geo_df_r.plot(ax=ax, markersize = 20, color = "green"  , alpha=1    )

fig, ax = osmnx.plot_graph(Gc, show = False, close = False)
#sweden.plot(ax = ax, markersize = 20, color = "red", alpha = 1, zorder = 7)
#sweden.plot(ax = ax, color = "black", alpha = 1, zorder = 8)
#sweden.plot(ax = ax, markersize = 20, color = "green", alpha = 1, zorder = 9)
sweden.boundary.plot(ax =ax, zorder=7)
plt.show()

city = osmnx.gdf_from_place('Sweden')
osmnx.save_gdf_shapefile(city)
city = osmnx.project_gdf(city)
fig, ax = osmnx.plot_shape(city, figsize=(3,3))

city = osmnx.geocode_to_gdf('Sweden')

ax = osmnx.plot_graph(Gc,  show = False, close = False)
osmnx.project_gdf(city).plot(fc='gray', ec='none', ax =ax)
_ = ax.axis('off')
plt.show()



fig, ax = osmnx.plot.plot_graph_routes(Gc, path_list, orig_dest_size=100)
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

# Get just the US
usa = world.query('name == "Sweden"')

# Plot the USA
ax.usa.boundary.plot()
plt.show()


fig, ax = plt.subplots()

#ax.set_xlim(0, 1)
#ax.set_ylim(0, 1)
fig1 = locdata.iloc[0]
arr_lena = mpimg.imread(path+"/"+fig1['name'])


img = mpimg.imread('your_image.png')
imgplot = plt.imshow(arr_lena, extent=[-1,1,-1,1])
plt.show()
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
