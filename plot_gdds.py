'''
This script plots Growing Degree Days (gdds) for corn from 
NDAWN onto a map of North Dakota. The accumulated gdds are grouped by county and plotted 
as a color map. A visualization is generated for each day in the specified range. 

Author Cody R. Gette

'''

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from matplotlib.colors import Normalize
import matplotlib
from mpl_toolkits.basemap import Basemap
import datetime

#Makes plot of accumulated gdds for the date provided using Basemap and saves as a png
def make_plot_gdd(date, start_date, end_date, dframe, save=False):
    fig, ax = plt.subplots(figsize=(15,10))
    m = Basemap(
        llcrnrlon=-105.0,
        llcrnrlat=45.4,
        urcrnrlon=-95.7,
        urcrnrlat=49.5,
        projection='merc',
        resolution='h')
    
    cmap = plt.get_cmap('nipy_spectral')
    pc = PatchCollection(dframe.shapes, zorder=2)
    norm = Normalize(vmin=100, vmax=2800)
    pc.set_facecolor(cmap(norm(dframe['Corn AGDD (F)'].fillna(0).values)))
    ax.add_collection(pc)
    m.drawcoastlines()
    m.drawcountries()
    m.drawstates()
    m.readshapefile('./cb_2017_us_county_500k/cb_2017_us_county_500k', 'counties')
    mapper = matplotlib.cm.ScalarMappable(norm=norm, cmap=cmap)
 
    mapper.set_array(dframe['Corn AGDD (F)'])
    cbar= m.colorbar(mapper, location='bottom')
    cbar.set_label('Accumulated GDDs: Corn '+str(date.strftime('%Y-%b-%d')))
    plt.title('Corn Growing Season GDDs for period '+str(start_date)+' to '+str(end_date), fontsize=18)
    if save:
        fig.savefig('./maps/AGDD/gdds-'+str(date.strftime('%Y-%m-%d'))+'.png', format='png')
        
    return m


#Makes plot of the change in accumulated gdds from the 5 year average
#for the date provided using Basemap and saves as a png
def make_plot_delta(date, start_date, end_date, dframe, save=False):
    fig, ax = plt.subplots(figsize=(15,10))
    m = Basemap(
        llcrnrlon=-105.0,
        llcrnrlat=45.4,
        urcrnrlon=-95.7,
        urcrnrlat=49.5,
        projection='merc',
        resolution='h')
    
    
    cmap = plt.get_cmap('seismic')
    pc = PatchCollection(dframe.shapes, zorder=2)
    norm = Normalize(vmin=-500, vmax=500)
    pc.set_facecolor(cmap(norm(dframe['Delta GDD (5yr)'].fillna(0).values)))
    ax.add_collection(pc)
    m.drawcoastlines()
    m.drawcountries()
    m.drawstates()
    m.readshapefile('./cb_2017_us_county_500k/cb_2017_us_county_500k', 'counties')
    mapper = matplotlib.cm.ScalarMappable(norm=norm, cmap=cmap)
 
    mapper.set_array(dframe['Delta GDD (5yr)'])
    cbar= m.colorbar(mapper, location='bottom', ticks = [-500,-250,-100,0,100,250,500])
    cbar.set_label('Delta GDDs: Corn '+str(date.strftime('%Y-%b-%d')))
    plt.title('Difference from 5yr Average: Corn GDDs for period '+str(start_date)+' to '+str(end_date), fontsize=18)
    if save:
        fig.savefig('./maps/Delta/delta5yr-'+str(date.strftime('%Y-%m-%d'))+'.png', format='png')
        
    return m


#gets the shape information for each county and combines it with county names. Additional ND, MN, and MT state info
#is added to the county to remove ambiguity 
def make_shapes():
    m = Basemap(
        llcrnrlon=-105.0,
        llcrnrlat=45.4,
        urcrnrlon=-95.7,
        urcrnrlat=49.5,
        projection='merc',
        resolution='h')
    m.readshapefile('./cb_2017_us_county_500k/cb_2017_us_county_500k', 'counties')
   
    df_poly = pd.DataFrame({
        'shapes': [Polygon(np.array(shape), True) for shape in m.counties],
        'area': [area['NAME'] for area in m.counties_info],
        'fp': [fp['STATEFP'] for fp in m.counties_info]
        })

    df_poly = df_poly.loc[df_poly['fp'].isin(['27','30','38'])]

    conds = [df_poly['fp']=='27', df_poly['fp']=='30', df_poly['fp']=='38']
    choices = [df_poly['area']+', MN', df_poly['area']+', MT', df_poly['area']+', ND',]
    df_poly['County']= np.select(conds, choices)

    return df_poly


#Plots both accumulated gdds and change in gdds for each date in the range on each county
#Weather data from counties with multiple stations is averaged
def plot_gdds(start_date, end_date, df):
    df_countyNames = pd.read_csv('./data/NDcounties_clean.csv')
    df_poly = make_shapes()
    df_poly = df_poly.merge(df_countyNames, left_on='County', right_on='County', how='right')

    for date in pd.date_range(start_date, end_date):
        df_plot_gdd= df[df['Date']==date]
        df_plot_gdd_final = df_plot_gdd.merge(df_poly.drop(['Station Name','Latitude (deg)','Longitude (deg)'],axis=1), on='County', how='left')
        df_mean_gdd = df_plot_gdd_final[['Corn AGDD (F)','Delta GDD (5yr)','County','Station Name','Date','fp','shapes']]
        df_mean_gdd = df_mean_gdd.groupby(['fp','County']).mean().reset_index()
        df_mean_gdd = df_mean_gdd.merge(df_poly.drop(['Station Name','Latitude (deg)','Longitude (deg)','fp'],axis=1), on='County', how='left')
        out = make_plot_gdd(date , start_date, end_date,df_mean_gdd, save=True)

    for date in pd.date_range(start_date, end_date):
        df_plot_delta= df[df['Date']==date]
        df_plot_delta_final = df_plot_delta.merge(df_poly.drop(['Station Name','Latitude (deg)','Longitude (deg)'],axis=1), on='County', how='left')
        df_mean_delta = df_plot_delta_final[['Corn AGDD (F)','Delta GDD (5yr)','County','Station Name','Date','fp','shapes']]
        df_mean_delta = df_mean_delta.groupby(['fp','County']).mean().reset_index()
        df_mean_delta = df_mean_delta.merge(df_poly.drop(['Station Name','Latitude (deg)','Longitude (deg)','fp'],axis=1), on='County', how='left')
        out_delta = make_plot_delta(date , start_date, end_date,df_mean_delta, save=True)
