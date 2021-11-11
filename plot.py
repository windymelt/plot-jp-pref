import pandas as pd
import numpy as np
import os
import geopandas as gpd
from shapely.geometry import Point
import matplotlib
import matplotlib.pyplot as plt 
import folium
import plotly_express as px
from datetime import datetime
import geemap
from ipygee import*

# Scale
from matplotlib_scalebar.scalebar import ScaleBar
from mpl_toolkits.axes_grid1 import make_axes_locatable

df_f = pd.read_json("./example.json", orient='records')

df_f.info()

print(df_f.loc[df_f.val == df_f.val.max(),:])

jpnShp = gpd.read_file('/app/shape_data/gadm36_JPN_1.shp')
japan = jpnShp.loc[:,['NAME_1','NL_NAME_1','geometry']].copy()

# fix map data bug
# Nagasaki -> Naoasaki
# Hyogo -> Hyōgo
japan.replace({'Naoasaki': 'Nagasaki', 'Hyōgo': 'Hyogo'}, inplace=True)

combDf = japan.merge(df_f, left_on='NAME_1',right_on='pref', how='left')

ax = combDf.plot(figsize=(16, 16))

# Label
# use NAME_1 for Pref. name
# use val for value
combDf.apply(lambda x: ax.annotate(text=x.val, xy=x.geometry.centroid.coords[0], ha='center', color = 'black', size = 6), axis=1)

# North Arrow
ax.text(x=153.215-0.55, y=40.4, s='N', fontsize=30)
ax.arrow(153.215, 39.36, 0, 1, length_includes_head=True,
          head_width=0.8, head_length=1.5, overhang=.1, facecolor='k')

# Scale bar
scalebar = ScaleBar(50, location='lower right',units='km')
ax.add_artist(scalebar)

combDf.plot(column='val', ax=ax, cmap = 'rainbow', edgecolors='white', legend=True,legend_kwds={'label': "LEGEND HERE",'orientation': "horizontal"})

# Title
plt.title("Foobar Title")

plt.savefig(f"result.png", 
                dpi=200, bbox_inches='tight')