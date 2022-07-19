"Funciones"

import pandas as pd
import requests
from bs4 import BeautifulSoup
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
import folium
import branca
import geojsoncontour
from folium import plugins
import utm
from statistics import mean
matplotlib.use('Agg')


def getdata(day):
    "Downloads the data from the website"
    temperaturas = {"3": "", "6": "", "9": "", "12": "", "15": "", "18": "", "21": "", "00": ""}
    windirs = {"3": "", "6": "", "9": "", "12": "", "15": "", "18": "", "21": "", "00": ""}
    windvel = {"3": "", "6": "", "9": "", "12": "", "15": "", "18": "", "21": "", "00": ""}
    page = requests.get("""https://www.meteoblue.com/es/tiempo/semana/
                        santiago-de-chile_chile_3871336?day=""" + str(day))
    soup = BeautifulSoup(page.content, 'html.parser')
    #Busca la temperatura por hora
    tempresults = soup.find_all('tr', class_='temperatures')
    for result in tempresults:
        temps = result.find_all('td')
    for elem in zip(temps, temperaturas.keys()):
        temperaturas[elem[1]] = elem[0].text.strip("°")
    #Busca Dirección del viento
    windresults = soup.find_all('tr', class_='winddirs no-mobile')
    for result in windresults:
        winds = result.find_all('td')
    for elem in zip(winds, windirs.keys()):
        windirs[elem[1]] = elem[0].text.strip()
    #Busca Velocidad del viento
    speedresults = soup.find_all('tr', class_='windspeeds')
    for result in speedresults:
        speeds = result.find_all('td')
    for elem in zip(speeds, windirs.keys()):
        texto = elem[0].text.strip("\n SENW")
        digitos = texto[-5:].strip().split('-')
        prom = (int(digitos[0])+int(digitos[1]))/2
        
        windvel[elem[1]] = prom
    return temperaturas, windirs, windvel


def plot_map(data, file):
    "Plots a map with the data"
    df = pd.read_excel(data)

    eastings = df['UTM Este'].tolist()
    northings = df['UTM Norte'].tolist()

    xvals = []
    yvals = []

    for i, (easting, northing) in enumerate(zip(eastings, northings)):
        lat, lon = utm.to_latlon(easting, northing, 18, northern=False)
        xvals.append(lon)
        yvals.append(lat)
    zvals = df['Nivel Ruido'].tolist()

    xlist = np.linspace(np.min(xvals), np.max(xvals), 100)
    ylist = np.linspace(np.min(yvals), np.max(yvals), 100)

    X,Y = np.meshgrid(xlist, ylist)

    Z = griddata((xvals,yvals), zvals, (X,Y), method='linear')

    colors = ['#2b83ba', '#abdda4', '#ffffbf', '#fdae61', '#d7191c']
    vmin = 30
    vmax = 70
    levels = len(colors)-1

    cm = branca.colormap.LinearColormap(colors, vmin=vmin, vmax=vmax)
    
    contourf = plt.contourf(X, Y, Z, levels, alpha = 0.5, colors = colors, linestyles='solid', vmin=vmin, vmax = vmax)

    geojson= geojsoncontour.contourf_to_geojson_overlap(contourf= contourf, ndigits=5, unit='dB')

    #geomap = folium.Map(location=[-33.4, -70.7], zoom_start=8, tiles='https://api.mapbox.com/styles/v1/victorcc88/ckznks9t1001y14kdet8r3sum/tiles/256/{z}/{x}/{y}@2x?access_token=pk.eyJ1IjoidmljdG9yY2M4OCIsImEiOiJja3lhdnl1NzQwOWc5MnBta3A2cjZscThqIn0.M8o_N_BSN_MpTlGAhgGgvA', attr ='Mapbox', name = 'Mapbox')
    geomap = folium.Map(location= [-33.4, -70.7], tiles = None, zoom_start = 8,)
    tile_layer = folium.TileLayer(
        tiles='https://api.mapbox.com/styles/v1/victorcc88/ckznks9t1001y14kdet8r3sum/tiles/256/{z}/{x}/{y}@2x?access_token=pk.eyJ1IjoidmljdG9yY2M4OCIsImEiOiJja3lhdnl1NzQwOWc5MnBta3A2cjZscThqIn0.M8o_N_BSN_MpTlGAhgGgvA',
        name='Mapbox',
        attr='Mapbox',
        max_zoom = 18,
        control = False,
    )

    tile_layer.add_to(geomap)

    countourmap = folium.GeoJson(geojson, style_function = lambda x: {
        'color': x['properties']['stroke'],
        'weight': x['properties']['stroke-width'],
        'fillColor': x['properties']['fill'],
        'opacity': 0.6,
        'fillOpacity': 0.2,
    }).add_to(geomap)

    countourmap.layer_name = 'Nivel de Ruido'

    fuentes = plugins.MarkerCluster(name = "Fuentes de Ruido").add_to(geomap)
    proyectos = plugins.MarkerCluster(name = "Proyectos").add_to(geomap)
    
    for i in range(len(xvals)):
        #Putting markers on map 
        folium.Marker(
            location=[float(yvals[i]), float(xvals[i])],
            popup=str(zvals[i])+'\n'+ str(xvals[i])+ ' '+ str(yvals[i]), 
            icon=folium.Icon(color='blue', icon="cog")
            ).add_to(fuentes)

    folium.Marker(
        location=[mean(yvals), mean(xvals)], 
        popup = 'Proyecto Los Ángeles', 
        icon=folium.Icon(color='red', icon="cog"), 
        name = "Los Angeles").add_to(proyectos)
    cm.caption = "Ruido"
    geomap.add_child(cm)


    plugins.Fullscreen(position='topright', title='Expandir', title_cancel='Retraer', force_separate_button=True).add_to(geomap)
    proyectsearch = plugins.Search(
        placeholder='Buscar...',
        title='Buscar',
        geom_type='Polygon',
        layer=proyectos,
        property_name='name',
        search_label='name',
        collapsed=False,
        search_zoom= 14,
    )

    proyectsearch.default_css = [('Leaflet.Search.css', 'https://cdn.jsdelivr.net/npm/leaflet-search@3.0.2/dist/leaflet-search.src.css')]
    proyectsearch.default_js = [('Leaflet.Search.js', 'https://cdn.jsdelivr.net/npm/leaflet-search@3.0.2/dist/leaflet-search.src.js')]

    proyectsearch.add_to(geomap)

    folium.LayerControl().add_to(geomap)


    geomap.save('templates/' + str(file) + '.html')

    return geomap

def utmotolatlon(zone, east, north):
    "Converts UTM coordinates to Latitude and Longitude"
    return utm.to_latlon(east, north, zone, northern=False)