from app import app
import dash
from dash.dependencies import Input, Output, State
#import plotly.express as px
from dash.exceptions import PreventUpdate
from data.dataProcess import getRedis
import redis
import pyarrow as pa


import io

#import flask

import os


redis_host = os.environ['RedisEndpoint'] 
redis_port = os.environ['RedisPort']
password = os.environ['RedisPassword']
redis = redis.StrictRedis(host = redis_host, port=redis_port,password = password)


@app.callback(Output('measures','options'),
            [
            Input('dataProcessMeasure','children'),
            Input('sessionStore','data'),             
            ])
def measure(dataProcessMeasure,sessionStoreData): 
   
    return getRedis('measureOptions',sessionStoreData)


@app.callback(Output('measures','value'),
            [
            Input('dataProcessMeasureValue','children'),
            Input('sessionStore','data')       
            ])
def measure(dataProcessMeasureValue,sessionStoreData): 
        return getRedis('measureValue',sessionStoreData)





@app.callback([Output('yearSlider','min'),Output('yearSlider','max'),
                Output('yearSlider','value'),Output('yearSlider','marks'),
                ],
            [
            Input('dataProcessYearSlider','children'),
            Input('sessionStore','data')        
            ])
def measure(dataProcessYearSlider,sessionStoreData):


        return (getRedis('sliderValue',sessionStoreData)['min'], 
        getRedis('sliderValue',sessionStoreData)['max'], 
        getRedis('sliderValue',sessionStoreData)['value'],
        getRedis('sliderValue',sessionStoreData)['marks'],
        )


#*********************************************************************************************************************************************
# Hide / unhide download data Div  
#********************************************************************************************************************************************

@app.callback(Output('downloadDataDiv','style'),
                        [Input('downloadDataButton','n_clicks'),
                        Input('clearFiltersButton','n_clicks') ])
def hidDownload(downloadDataButton,clearFiltersButton):

        ctx = dash.callback_context

        if ctx.triggered[0]['prop_id'].split('.')[0] == 'downloadDataButton':
                return {}
        elif ctx.triggered[0]['prop_id'].split('.')[0] == 'clearFiltersButton': 
                return {'display':'none'}
        else:
                return {'display':'none'}

        
        
#*********************************************************************************************************************************************
# Restore fixFilter and  dateRangeInsideOutside values when reset button pressed.
#********************************************************************************************************************************************

@app.callback([Output('dateRangeInsideOutside','value'),Output('fixFilter','value')],
               [Input('clearFiltersButton','n_clicks')])
def resetRadioItems(clearFiltersButton):

        if clearFiltersButton>0:
                return 'out', 'Time'
        else:
                raise PreventUpdate