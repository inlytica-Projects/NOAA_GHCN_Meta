from app import app
import dash
from dash.dependencies import Input, Output, State
import plotly.express as px
from data.dataProcess import getRedis
import redis
import pyarrow as pa


import io

import flask



redis_host = 'localhost'
redis_port = 6379
redis = redis.StrictRedis(host = redis_host, port=redis_port)


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
            Input('sessionStore','data'),             
            ])
def measure(dataProcessMeasureValue,sessionStoreData): 
   
    return getRedis('measureValue',sessionStoreData)



@app.callback([Output('yearSlider','min'),Output('yearSlider','max'),
                Output('yearSlider','value'),Output('yearSlider','marks'),
                ],
            [
            Input('dataProcessYearSlider','children'),
            Input('sessionStore','data'),             
            ])
def measure(dataProcessYearSlider,sessionStoreData):
    return (getRedis('sliderValue',sessionStoreData)['min'], 
    getRedis('sliderValue',sessionStoreData)['max'], 
    getRedis('sliderValue',sessionStoreData)['value'],
   getRedis('sliderValue',sessionStoreData)['marks'],
   )



@app.callback(Output('downloadCSV','href'),
                [Input('generateCsvButton','n_clicks'),
                Input('sessionStore','data')])
def createURL(generateCsvButton,sessionStoreData):
    if generateCsvButton > 0:
        return f'/dash/downloadData?session={sessionStoreData}&key=download'

@app.server.route('/dash/downloadData')
def download_csv():
    session = flask.request.args.get('session')
    key = flask.request.args.get('key')

    noaaData = getRedis(key, session)


    str_io = io.StringIO()
    
    noaaData.to_csv(str_io)

    mem = io.BytesIO()
    mem.write(str_io.getvalue().encode('utf-8'))
    mem.seek(0)
    str_io.close()
    return flask.send_file(mem,
                           mimetype='text/csv',
                           attachment_filename='NOAA_Data_Download.csv',
                           as_attachment=True)

        
        

