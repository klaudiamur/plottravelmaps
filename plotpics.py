from matplotlib.offsetbox import TextArea, DrawingArea, OffsetImage, AnnotationBbox

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os

path = '/Users/klaudiamur/Dropbox/nerdstuff/travelmaps/pics'
directory = os.fsencode(path)
### aaaah get time from it as well!!!!
for file in os.listdir(directory):
    filename = os.fsdecode(file)
    if filename.endswith('jpg'):
        p = os.path.join(path, filename)
       # exif = get_exif(p)
        #t = exif[36867]
        #geotags = get_geotagging(exif)
        coords = get_coordinates(geotags)
        locdict[filename] = coords
        tdict[filename] = t

locdata = pd.DataFrame([locdict, tdict]).transpose()
locdata['name'] = locdata.index
locdata = locdata.sort_values(by=[1])
fig, ax = plt.subplots()

#ax.set_xlim(0, 1)
#ax.set_ylim(0, 1)
fig1 = locdata.iloc[0]
arr_lena = mpimg.imread(path+fig1['name'])

imagebox = OffsetImage(arr_lena, zoom=0.2)

ab = AnnotationBbox(imagebox, (0.4, 0.6))

ax.add_artist(ab)

plt.grid()

plt.draw()
#plt.savefig('add_picture_matplotlib_figure.png',bbox_inches='tight')
plt.show()