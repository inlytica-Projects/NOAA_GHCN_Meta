import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State


import plotly.express as px
from app import app


from callbacks import mapbox, measure
from data import dataProcess

from data.dataProcess import getRedis
import redis
import pyarrow as pa

import time

mapbox = dcc.Graph(id='mapbox',style = {'height':'550px'})

measures = dcc.Checklist(id='measures')
measureChooseAll = html.Button('All',id='measureChooseAll',n_clicks=0)
measureChooseCore = html.Button('Core',id='measureChooseCore',n_clicks=0)
measureChooseSelf = html.Button('Self',id='measureChooseSelf',n_clicks=0)

yearSlider = dcc.RangeSlider(id='yearSlider')
yearRange = html.Div(id='yearRange')

sessionGenDiv = html.Div(id='sessionGenDiv',style = {'display':'none'})  
dataProcessMapBox = html.Div(id='dataProcessMapBox',style = {'display':'none'})
dataProcessMeasure = html.Div(id='dataProcessMeasure',style = {'display':'none'})
dataProcessDownloadData = html.Div(id='dataProcessDownloadData',style = {'display':'none'})
dataProcessMeasureValue = html.Div(id='dataProcessMeasureValue',style = {'display':'none'})
dataProcessYearSlider = html.Div(id='dataProcessYearSlider',style = {'display':'none'})
fixFilter = dcc.RadioItems(id='fixFilter',options = [{'label':'Time     ','value':'Time'},
                                                    {'label':'Mapbox     ','value':'Mapbox'},
                                                    {'label':'Measures     ','value':'Measures'}],
                                                    value = 'Time',
                                                    #labelStyle={'display': 'inline-block'}
                                                    )

dateRangeInsideOutside = dcc.RadioItems(id='dateRangeInsideOutside',options=[{'label':'Station date ranges include Slider Values    ','value':'in'},
                                                                            {'label':'Slider Values include Station date ranges    ','value':'out'},
                                                                            {'label':'Station date ranges equal Slider Values    ','value':'equal'}],                                                                            
                                                                            value='out')
sessionStore = dcc.Store(id='sessionStore')
measureValueStore = dcc.Store(id='measureValueStore')
mapboxCenterStore = dcc.Store(id='mapboxCenterStore')

generateCsvButton = html.Button('Generate CSV',id='generateCsvButton',n_clicks=0)
downloadSpinner = dcc.Loading(id='downloadSpinner',type = 'default',children=[html.Div(id = 'downloadSpinnerOutput')])
progressPercent = html.Div(id='progressPercent')
progressInterval = dcc.Interval(id='progressInterval')
downloadCSV = html.A('Download csv',id='downloadCSV')
progressDivInput = html.Div(id='progressDivInput',hidden=True)

inputAwsBucket = dcc.Input(id='inputAwsBucket',placeholder = 'AWS Bucket Name')
inputAwsObject = dcc.Input(id='inputAwsObject',placeholder = 'AWS Object Name')
inputAwsKey = dcc.Input(id='inputAwsKey',placeholder = 'AWS Key',type = 'password')
inputAwsSecretKey = dcc.Input(id='inputAwsSecretKey',placeholder = 'AWS Secret Key',type = 'password')

def get_layout():
    return html.Div([
            html.Div([html.Div(['NOAA Global Historical Climatology Network Daily (GHCN-D)'],className='col-12')],className='h1 row',
                            style={'margin-top':'-10px','margin-bottom':'25px'}
                    ),
            html.Div([
                    html.Div([html.Div(['Fix Filter Element'],className='h6'),
                            fixFilter],className='col-12'),
                    ],className='row'),
            
            html.Div([
                html.Div([
                    html.Div([
                            html.Div(['Stations'],className='card-title h5'),
                            html.Div([mapbox],className='card-body')],className = 'card', style = {'height':'75%'}),
                html.Div([],style={'height':'1%'}),

                    html.Div([
                            html.Div(['Years'],className='card-title h5'),
                            html.Div([dateRangeInsideOutside,yearSlider],className='card-body'),
                            html.Div([yearRange],className='card-footer')
                            ],className='card',style = {'height':'24%'})
                ],className = 'col-8'),

                html.Div([
                        html.Div([
                            html.Div(['Elements'],className='card-title h5'),
                            html.Div([html.Div(['Choose:   ',measureChooseAll,measureChooseCore,measureChooseSelf]),
                                                measures], className='card-body'),
                            ],className='card',style={'height':'100%'})

                        ],className = 'col-4')

            ],className = 'row'
            ),
        html.Div([
                html.Div([generateCsvButton,html.Div(children = [downloadSpinner]),progressPercent,downloadCSV,
                inputAwsBucket, inputAwsObject, inputAwsKey, inputAwsSecretKey],className = 'col-12',
                style = {'text-align': 'center','padding-top':'30px'}
                )            

        ],className = 'row'),
        html.Div([html.A('Produced by: Merrillmount Consulting',href='http://merrillmount.com/',target='_blank')],style = {'padding-top':'30px'}),
        progressDivInput,
        sessionStore,
        sessionGenDiv,
        dataProcessMapBox,
        dataProcessMeasure,
        dataProcessMeasureValue,
        dataProcessYearSlider,
        dataProcessDownloadData,
        mapboxCenterStore,
        progressInterval
    ])

app.layout = get_layout


if __name__ == '__main__':
    app.run_server(debug=True,host='0.0.0.0')