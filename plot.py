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

pref_subst_table = {
  "北海道": "Hokkaido",
  "青森県": "Aomori",
  "岩手県": "Iwate",
  "宮城県": "Miyagi",
  "秋田県": "Akita",
  "山形県": "Yamagata",
  "福島県": "Fukushima",
  "茨城県": "Ibaraki",
  "宮城県": "Miyagi",
  "栃木県": "Tochigi",
  "群馬県": "Gunma",
  "埼玉県": "Saitama",
  "千葉県": "Chiba",
  "東京都": "Tokyo",
  "神奈川県": "Kanagawa",
  "新潟県": "Niigata",
  "富山県": "Toyama",
  "石川県": "Ishikawa",
  "福井県": "Fukui",
  "山梨県": "Yamanashi",
  "長野県": "Nagano",
  "岐阜県": "Gifu",
  "静岡県": "Shizuoka",
  "愛知県": "Aichi",
  "三重県": "Mie",
  "滋賀県": "Shiga",
  "京都府": "Kyoto",
  "大阪府": "Osaka",
  "兵庫県": "Hyogo",
  "奈良県": "Nara",
  "和歌山県": "Wakayama",
  "鳥取県": "Tottori",
  "島根県": "Shimane",
  "岡山県": "Okayama",
  "広島県": "Hiroshima",
  "山口県": "Yamaguchi",
  "徳島県": "Tokushima",
  "香川県": "Kagawa",
  "愛媛県": "Aichi",
  "高知県": "Kochi",
  "愛媛県": "Ehime",
  "福岡県": "Fukuoka",
  "佐賀県": "Saga",
  "長崎県": "Nagasaki",
  "熊本県": "Kumamoto",
  "大分県": "Oita",
  "宮崎県": "Miyazaki",
  "鹿児島県": "Kagoshima",
  "沖縄県": "Okinawa"
}

# TODO: get json from ARGV or stdin
df_f = pd.read_json("./example.json", orient='records')
df_f.replace(pref_subst_table, inplace=True)

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

combDf.plot(column='val', ax=ax, cmap = 'rainbow', edgecolors='white', legend=True, legend_kwds={'label': "LEGEND HERE",'orientation': "horizontal"})

# Title
plt.title("Foobar Title")

plt.savefig(f"result.png", 
                dpi=200, bbox_inches='tight')