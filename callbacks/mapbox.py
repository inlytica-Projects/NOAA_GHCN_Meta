from app import app


import numpy as np

from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import dash
from dash.exceptions import PreventUpdate

import redis

import pyarrow as pa

import os


redis_host = os.environ['RedisEndpoint'] 
redis_port = os.environ['RedisPort']
password = os.environ['RedisPassword']
redis = redis.StrictRedis(host = redis_host, port=redis_port,password = password)

from data.dataProcess import getRedis

mapbox_access_token = os.environ['MapboxToken']

@app.callback(Output('mapbox','relayoutData'),
              [Input('clearFiltersButton','n_clicks')])
def clearRelayoutdata(clearFiltersButton):
    if clearFiltersButton>0:
        return {'autosize': True}
    else: 
        raise PreventUpdate
    



@app.callback(Output('mapbox','figure'),
                    [
                    Input('mapboxCenterStore','data'),
                    Input('dataProcessMapBox','children'),
                    Input('sessionStore','data'),
                    ])  
def mapbox(mapboxCenterStoreData,dataProcessDiv,sessionStoreData): 
   


    


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
        selected = {'marker':{'color':'#39FF14','size':3}},
    
    )
                )

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



    

    
   