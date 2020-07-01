from app import app


import numpy as np

from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import dash

import redis

import pyarrow as pa

redis_host = 'localhost'
redis_port = 6379
redis = redis.StrictRedis(host = redis_host, port=redis_port)

from data.dataProcess import getRedis

mapbox_access_token = 'pk.eyJ1IjoiZ2hhdnJhbmVrIiwiYSI6ImNrOXZtd2c2aTAwdXkza250aDd5Yjl3a2cifQ.cPjzrOP_Pi45wIANslXswQ'



@app.callback(Output('mapbox','figure'),
                    [
                    Input('mapboxCenterStore','data'),
                    Input('dataProcessMapBox','children'),
                    Input('sessionStore','data'),
                    ])  
def mapbox(mapboxCenterStoreData,dataProcessDiv,sessionStoreData): #,relayoutData
   


    


    uniqueStations = getRedis('mapbox',sessionStoreData)
    
    centerLon = mapboxCenterStoreData['centerLon']
    centerLat = mapboxCenterStoreData['centerLat']
    zoom = mapboxCenterStoreData['zoom']

    fig = go.Figure(go.Scattermapbox(
        lat=uniqueStations.latitude,
        lon=uniqueStations.longitude,
        mode='markers',
        name = '',
        marker=go.scattermapbox.Marker(
            size=2,
            color='red'
        ),
        text = uniqueStations['station'],
        hovertemplate ="station: %{text}",
        selected = {'marker':{'color':'#39FF14','size':3}}
        
    ))

    fig.update_layout(
        autosize=False,
        hovermode='closest',
        # width = 1000,
        #height = 600,
        mapbox=dict(
            accesstoken=mapbox_access_token,
            bearing=0,
            center=dict(
            lat=centerLat,
            lon=centerLon
            ),
            pitch=0,
            zoom=zoom,
            style = 'dark'

        ),
        margin={"r":0,"t":0,"l":0,"b":0}
    
    )
    
    return fig



    

    
   