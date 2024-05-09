#Imports
import dash
from dash import dcc, html, dash_table, Input, Output, State, callback, callback_context
import plotly.express as px
import pandas as pd
import mysql.connector


app = dash.Dash(__name__, use_pages=True, external_stylesheets=['/assets/styles.css'])


app.layout = html.Div([
    

    html.Div(children=[
            html.H2('BlightWatch NOLA', style= {'font-family':' Georgia, serif', 'color':'white', 'display':'inline-block',
                                                'margin-left':'2px', }),
            dcc.Link('Home', href= "/", style= {'font-family':' Georgia, serif', 'fontSize': '16px',
                                                            'color':'white', 'display':'inline-block',
                                                'margin-left':'15px', 'textDecoration': 'none'}),
            dcc.Link('Data Sources', href = "/datasources", style= {'font-family':' Georgia, serif', 'color':'white', 'display':'inline-block',
                                                'margin-left':'10px', 'fontSize':'16px', 'textDecoration':'none'}),
            dcc.Link('About', href= "/about", style= {'font-family':' Georgia, serif', 'color':'white', 'display':'inline-block',
                                                'margin-left':'10px', 'fontSize':'16px', 'textDecoration':'none'})
    ], style={'backgroundColor':'black', 'padding':'0px', 'border':'0px', 'margin':'0px'}),
    dash.page_container
])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=False) 