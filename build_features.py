'''
This script retrieves Growing Degree Days (gdds) for corn from 
NDAWN and formats the county information for each station location

Author Cody R. Gette

'''

import numpy as np
import pandas as pd
import os
import requests
import datetime

#Gets gdd information via NDAWN API request
def get_gdd(stations, begin_date, end_date):
    #Stations 2-102
    count = 0
    for station in stations:
        
        params = {'station': station, 'begin_date': begin_date,'end_date': end_date, 'ttype': "cogdd", 'd5y': ''}


        r = requests.get('https://ndawn.ndsu.nodak.edu/table.csv', params = params)
        print("Request status code from Station #"+str(station)+': '+str(r.status_code))

        try:
            #output content of request and read back into dataframe
            #Possibly a more elegant way to accomplish this -- for future updates
            with open("Output.csv", "w") as text_file:
                text_file.write(r.content.decode('utf-8'))

            tmp = pd.read_csv('Output.csv', header=[0,1],skiprows=3)

        #Column names to keep as they come from the csv file. Skipping some of the "Flag" columns. 

            tmp=tmp[[('Station Name', 'Unnamed: 0_level_1'),
                     ('Latitude', 'deg'),
                     ('Longitude', 'deg'),
                     ('Elevation', 'ft'),
                     ('Year', 'Unnamed: 4_level_1'),
                     ('Month', 'Unnamed: 5_level_1'),
                     ('Day', 'Unnamed: 6_level_1'),
                     ('Max Temp', 'Degrees F'),
                     ('Min Temp', 'Degrees F'),
                     ('Rainfall', 'inch'),
                     ('Corn Daily Growing Degree Days', 'Degrees F'),
                     ('Corn Accumulated Growing Degree Days', 'Degrees F'),
                     ('Departure from 5 Year Average Corn Accumulated Growing Degree Days',
                      'Degrees F')]]

        #Rename the columns in one line instead of two
            tmp.columns = ['Station Name', 'Latitude (deg)', 'Longitude (deg)', 'Elevation (ft)', 'Year', 'Month','Day', 'Max Temp (F)',
                              'Min Temp (F)', 'Rainfall (in)', 'Corn GDD (F)', 'Corn AGDD (F)', 'Delta GDD (5yr)' ]
            #Assign tmp to new dataframe if the first time through the loop; otherwise combine data
            if count == 0:
                df = tmp
            else:
                df = pd.concat([df,tmp], ignore_index=True)
            count+=1

        #Catch all exceptions for a bad request or missing data
        except:
            print("Error converting Station #"+str(station)+" to csv. Missing?")

    print("Successfully retrieved "+str(count+1)+" stations")
    print("Data exists from "+str(len(df['Station Name'].unique())+1)+" stations")
    os.remove('Output.csv')
    return df

#generate and format gdd dataframe; include county name information for plotting
def make_new_gdd(start, end):
    stations = range(1,103)
    df =  get_gdd(stations, start, end)
    df.to_csv('./data/NDCornGDD'+str(start)+str(end)+'.csv',index=None)
    df_countyNames = pd.read_csv('./data/NDcounties_clean.csv')
    df_final=df.merge(df_countyNames.drop(['Latitude (deg)','Longitude (deg)'], axis=1), on='Station Name', how='left')
    df_final['Date']=df_final.apply(lambda row: datetime.datetime(row['Year'], row['Month'], row['Day']), axis=1)
    return df_final

#Combines station informations for each county in North Dakota. Counties without a weather station are left blank

def build_county_info():
    df_counties = pd.read_csv('./stations.csv')
    df_countyNames = pd.read_csv('./NDcounties.csv')

    df_countyNames['Counties']=df_countyNames['Counties']+', ND'
    df_countyNames = df_countyNames.merge(df_counties, left_on='Counties', right_on='County', how='outer')

    for i,x in enumerate(df_countyNames['County']):
        if(pd.isnull(df_countyNames['County'][i])):
            df_countyNames['County'][i]=df_countyNames['Counties'][i]

    df_countyNames.drop('Counties',axis=1, inplace=True)
    df_countyNames.to_csv('./data/NDcounties_clean.csv', index=None)


