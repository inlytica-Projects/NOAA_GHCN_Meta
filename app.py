import dash
import dash_bootstrap_components as dbc

#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
external_stylesheets = ['https://codepen.io/ghav65/pen/PoZWPyZ.css']



app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

app.config.suppress_callback_exceptions = True


# Add title and favicon

@server.route("/")
def MyDashApp():
    return app.index()

app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>Global Daily Weather</title>
        {%favicon%}
        
        {%css%}
    </head>
    <body>
        {%app_entry%}
         {%config%}
            {%scripts%}
            {%renderer%}
    </body>
</html>
'''

#{%favicon%}