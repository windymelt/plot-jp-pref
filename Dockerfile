FROM debian:11

RUN apt-get update -y

RUN apt install -y python3 python3-pip
RUN apt install -y gdal-bin python3-gdal
RUN apt install -y python3-rtree

RUN python3 -m pip install geopandas
# Install Folium for Geographic data visualization
# pip install folium
RUN python3 -m pip install plotly-express
RUN python3 -m pip install --upgrade plotly
RUN python3 -m pip install matplotlib-scalebar
# Use EE in Python
RUN python3 -m pip install geemap
RUN python3 -m pip install ipygee

RUN mkdir /app
WORKDIR /app
ADD plot.py .
ADD example.json .

ADD shape_data shape_data