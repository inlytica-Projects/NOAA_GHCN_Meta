from app import app
import dash
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import plotly.express as px
from data.dataGen import inventory

import numpy as np

import pyarrow as pa

import uuid
import redis

redis_host = 'localhost'
redis_port = 6379
redis = redis.StrictRedis(host = redis_host, port=redis_port)






@app.callback(Output('sessionStore','data'),
            [
                Input('sessionGenFakeDiv','children')
                ]
            )
def sessionStore(fakeDiv):
    return str(uuid.uuid4())



@app.callback([Output('dataProcessDiv','children'),Output('sessionDiv','children')],
                    [
                        Input('mapbox','relayoutData'),
                        Input('measures','value'),
                        Input('sessionStore','data')
                    ])
def dataParse(relayoutData,value,data):
    df = inventory


    if relayoutData != {'autosize': True} and relayoutData is not None:

 
        array=np.array((relayoutData['mapbox._derived']['coordinates']))
        minLon = array[:,0].min()
        maxLon = array[:,0].max()
        minLat = array[:,1].min()
        maxLat = array[:,1].max()

        df = df.query('@minLat <= latitude <= @maxLat & @minLon <= longitude <= @maxLon') #& @measure.isin(value)

    dataParse = pa.serialize(df).to_buffer()
    dataParseLength = len(dataParse)
    dataParseCompress= pa.compress(dataParse,asbytes=True)

    dataParseDict = {'dataParseLength':dataParseLength,'dataParseCompress':dataParseCompress}
    #dataParseDict = {'dataParseLength':10,'dataParseCompress':'test'}

    dataCacheKey = f'dataCache{data}'

    redis.hmset(dataCacheKey,dataParseDict)
    #redis.hmset(dataCacheKey,{'test':2})

    

    return 'test',f'len df:{len(df)}-------'


    



# Need to create another fake div so that fakeDiv does not fire and create a new session id everytime data is updated.