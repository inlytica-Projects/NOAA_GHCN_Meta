import dash
import dash_core_components as dcc
import dash_html_components as html

from app import app


from callbacks import mapbox, measure




mapboxModebar = ['zoom2d',  'select2d',  'zoomIn2d', 'zoomOut2d', 'autoScale2d', 'resetScale2d', 
                'hoverClosestCartesian', 'hoverCompareCartesian', 'zoom3d', 'pan3d', 'resetCameraDefault3d', 'resetCameraLastSave3d',
                 'hoverClosest3d', 'orbitRotation','tableRotation', 'zoomInGeo', 'zoomOutGeo', 'resetGeo', 'hoverClosestGeo',
                'toImage', 'sendDataToCloud', 'hoverClosestGl2d', 'hoverClosestPie', 'toggleHover', 'resetViews', 'toggleSpikelines',
                'resetViewMapbox' ,'zoom2d','zoomInMapbox','zoomOutMapbox']

mapbox = dcc.Graph(id='mapbox',style = {'height':'550px'},
                   config={'modeBarButtonsToRemove': mapboxModebar,'displaylogo':False})

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
fixFilter = dcc.RadioItems(id='fixFilter',options = [{'label':'Lock Stations     ','value':'Mapbox'},
                                                    {'label':'Lock Elements     ','value':'Measures'},
                                                    {'label':'Lock Years     ','value':'Time'}],
                                                    value = 'Time'
                                                    )
clearFiltersButton = html.Button('Reset Defaults',id='clearFiltersButton',n_clicks=0)

dateRangeInsideOutside = dcc.RadioItems(id='dateRangeInsideOutside',options=[{'label':'Station date ranges include Slider Values    ','value':'in'},
                                                                            {'label':'Slider Values include Station date ranges    ','value':'out'},
                                                                            {'label':'Station date ranges equal Slider Values    ','value':'equal'}],                                                                            
                                                                            value='out')
sessionStore = dcc.Store(id='sessionStore')
measureValueStore = dcc.Store(id='measureValueStore')
mapboxCenterStore = dcc.Store(id='mapboxCenterStore')


downloadDataButton = html.Button('Download Filtered Data To Private AWS S3 Bucket',id='downloadDataButton',n_clicks=0)
startDownloadButton = html.Button('Download',id='startDownloadButton',n_clicks=0)

downloadSpinner = dcc.Loading(id='downloadSpinner',type = 'default',children=[html.Div(id = 'downloadSpinnerOutput')])
progressPercent = html.Div(id='progressPercent')
progressInterval = dcc.Interval(id='progressInterval')
downloadCSV = html.A('Download csv',id='downloadCSV')
progressDivInput = html.Div(id='progressDivInput',hidden=True)
inputAwsBucket = dcc.Input(id='inputAwsBucket',placeholder = 'AWS Bucket Name')
inputAwsObject = dcc.Input(id='inputAwsObject',placeholder = 'AWS Object Name')
inputAwsKey = dcc.Input(id='inputAwsKey',placeholder = 'AWS Key',type = 'password',size='40')
inputAwsSecretKey = dcc.Input(id='inputAwsSecretKey',placeholder = 'AWS Secret Key',type = 'password',size='40')

def get_layout():
    return html.Div([
            html.Div([html.Div(['Global Daily Weather Observations'],className='col-6 h1'),
                      html.Div([html.A('(Information and Data Source)',href='https://docs.opendata.aws/noaa-ghcn-pds/readme.html',
                        target='_blank')],
                        className='col-6',style={'text-align':'right'})],className='row',style={'margin-top':'-10px','margin-bottom':'25px'}),
   
            html.Div([
                    html.Div([fixFilter],className='col-6'),
                    html.Div([clearFiltersButton],className='col-6',style={'text-align':'left'})    
                    ],className='row align-items-end'),
            
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
                    html.Div(className='col-2'),
                    html.Div([downloadDataButton],className='col-8',style={'text-align':'center','padding-top':'30px'}),
                    html.Div(className='col-2')
                ],className='row'),
        
        html.Div([ 
                html.Div(className='col-2'),      
                html.Div(
                html.Div([
                html.Div(['Enter private AWS s3 information'],className='card-title h5'),
                html.Div([inputAwsBucket, inputAwsObject],className='card-body'),
                html.Div([inputAwsKey, inputAwsSecretKey],className='card-body'),
                html.Div([html.Div(children = [downloadSpinner]),progressPercent],className='card-body'),
                html.Div([startDownloadButton],className='card-footer',style={'text-align':'center'})
                ],className = 'card'                
                ),className='col-8',style={'text-align':'center'}),                
                html.Div(className='col-2')
                ],className = 'row',id='downloadDataDiv'),
        html.Div([html.A('Merrillmount Consulting',href='http://merrillmount.com/',target='_blank')],style = {'padding-top':'30px'}),
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
    app.run_server(debug=False,host='0.0.0.0')