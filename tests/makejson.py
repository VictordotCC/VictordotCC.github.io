import pandas as pd
import numpy as np
import utm
import matplotlib
import matplotlib.pyplot as plt
import geojsoncontour

from scipy.interpolate import griddata
matplotlib.use('Agg')


def make_geojson():
    df = pd.read_excel('Ejemplo.xlsx')

    eastings = df['UTM Este'].tolist()
    northings = df['UTM Norte'].tolist()

    xvals = []
    yvals = []

    for i, (easting, northing) in enumerate(zip(eastings, northings)):
        lat, lon = utm.to_latlon(easting, northing, 18, northern=False)
        xvals.append(lon)
        yvals.append(lat)
    zvals = [np.random.randint(20, 80) for i in range(len(xvals))]

    xlist = np.linspace(np.min(xvals), np.max(xvals), 100)
    ylist = np.linspace(np.min(yvals), np.max(yvals), 100)

    X,Y = np.meshgrid(xlist, ylist)

    Z = griddata((xvals,yvals), zvals, (X,Y), method='linear')

    colors = ['#2b83ba', '#abdda4', '#ffffbf', '#fdae61', '#d7191c']
    vmin = 30
    vmax = 70
    levels = len(colors)-1

    contourf = plt.contourf(X, Y, Z, levels, alpha = 0.5, colors = colors, linestyles='solid', vmin=vmin, vmax = vmax)
    
    geojson= geojsoncontour.contourf_to_geojson(contourf= contourf, ndigits=5, unit='dB')

    with open('geojson.geojson', 'w') as f:
        f.write(geojson)
        

make_geojson()