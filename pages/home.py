#Imports
import dash
from dash import dcc, html, dash_table, Input, Output, State, callback, callback_context
import plotly.express as px
import pandas as pd
from data_loader import data

dash.register_page(__name__, path='/')

#Global Vars
#Coordinates of New Orleans to center map
new_orleans_coordinates = {'lat': 29.9511, 'lon': -90.0715}
data_display = data 

#print(data.columns)

#Home page divs
#Quick start modal
quick_start_modal = html.Div(
    id='quick-start-modal',
    className='modal',
    children=[
        html.Div(
            className='modal-content',
            children=[
                html.Span(className='close', id='quick-start-close', children='×'),
                html.H2('Quick Start Guide'),
                html.P('This is the quick start guide. Add your instructions here.')
            ]
        )
    ]
)

#Quadrant 1 subquadrant divs
total_observations = data.shape[0]
subquadrant_1_content = html.Div(children=[
    html.Img(src='/assets/house-png-193.png', style= {'width':'10%', 'height':'10%', 'display':'inline-block'}),
    html.H3('Total Properties Tracked', style={ 'font-style':'italic'}),
    html.H3(f'{total_observations}')
    ],
    style={'text-align':'center', 'border':'2px solid #000000', 'border-radius':'10px', 'padding-top':'20px',
           'backgroundColor':'white'}
    )

pending_311_complaints = data[data["Request Status"] == "Pending"].shape[0]
subquadrant_2_content = html.Div(children=[
    html.Img(src='/assets/phone-clipart.png', style= {'width':'10%', 'height':'10%', 'display':'inline-block', }),
    html.H3('Pending 311 Complaints', style={ 'font-style':'italic'}),
    html.H3(f'{pending_311_complaints}')
    ],
    style={'text-align':'center', 'border':'2px solid #000000', 'border-radius':'10px', 'padding-top':'20px','backgroundColor':'white'}
    )
subquadrant_3_content = html.Div(children=[
    html.Img(src='/assets/gavel-clipart.png', style= {'width':'10%', 'height':'10%', 'display':'inline-block'}),
    html.H3('Oldest Code Enforcement Case', style={ 'font-style':'italic'}),
    html.H3('3639 - 3641 Republic St (01/03/2014)')
    ],
    style={'text-align':'center', 'border':'2px solid #000000', 'border-radius':'10px', 'padding-top':'20px', 'backgroundColor':'white'}
    )

most_effected_zip = data['ZIP'].value_counts().idxmax()
subquadrant_4_content = html.Div(children=[
    html.Img(src='/assets/broken-house-clipart.png', style= {'width':'10%', 'height':'10%', 'display':'inline-block'}),
    html.H3('ZIP Code with Most Tracked Properties', style={ 'font-style':'italic'}),
    html.H3(f'{most_effected_zip} (St Claude/Lower 9th Ward)')
    ],
    style={'text-align':'center', 'border':'2px solid #000000', 'border-radius':'10px', 'padding-top':'10px', 'backgroundColor':'white'}
    )

#Main quadrant divs
quadrant_1_content = html.Div(children=[
    html.H2('Welcome to BlightWatch NOLA', style= {'font-family':'Georgia, serif', 'color':'black'}),
    html.P('This app unifies publicly available 311 call, Code Enforcement, and USPS Vacancy data' + 
           ' to help users track blighted properties in New Orleans. For more information about our sources,' +
            ' click the \'Data Sources\' button in the menu bar.',
           style= {'font-family':'Georgia, serif', 'color':'black'}),
    html.Div(
    style={
        'display': 'grid',
        'gridTemplateColumns': '1fr 1fr',  # Two columns
        'gridTemplateRows': '1fr 1fr',     # Two rows
        'height': '40vh',                 # Full height of the viewport
        'gap': '10px'                       # Gap between grid items
    },
    children=[
        
        html.Div(subquadrant_1_content, style={'gridColumn': '1', 'gridRow': '1'}),
        html.Div(subquadrant_2_content, style={'gridColumn': '2', 'gridRow': '1'}),
        html.Div(subquadrant_3_content, style={'gridColumn': '1', 'gridRow': '2'}),
        html.Div(subquadrant_4_content, style={'gridColumn': '2', 'gridRow': '2'})
    ]
)
    ],
    style={'paddingLeft':'10px'}
)

#Quadrant 2 

#Map figure

map_fig = px.scatter_mapbox(
                #Use df from database
                data,
                #Use Lat/Long in Data
                lat = 'Latitude',
                lon = 'Longitude',

                #Find correct projection and zoom to display city of New Orleans
            
                #?TO DO: Make this parameter toggalable by user to change map style
                mapbox_style='carto-positron',

                center = new_orleans_coordinates,

                #Title of data set being used
                title='Tracked Properties',
                zoom = 10,
                
                #Hover Options
                color='Source',
                color_discrete_map= {'311 Calls': 'blue', 'Code Enforcement': 'red'},
                hover_name= 'Address',
                hover_data= {'Request Status':True, 'Source':True, 'Object ID':True, 'Case Filed Date':True, 
                             'ZIP':True, "Stage":True})#Controls columns that display on hover

map_fig.update_layout(paper_bgcolor='white')
            
quadrant_2_content = html.Div(

        dcc.Graph(
        #Set id
            id='new-orleans-map',
            figure=map_fig
        ), 
        style={'width': '75vw', 
               'margin': '10px', 
               'marginTop': '20vh', 
               'marginBottom':'0px', 
               'textAlign': 'center',
               'padding-top': '0px',
               'padding-bottom': '0px',
               'padding':'5px',
               'left':'50%',
               'backgroundColor':'white', 'border':'2px solid #000000', 'border-radius':'10px'}) #end map div

#Pie Chart 
source_counts = data.groupby('Source').size().reset_index(name='counts')
pie_fig = px.pie(source_counts, names='Source', values='counts', title='Pie Chart')
pie_fig.update_layout(title='Breakdown of Data Sources')
pie_fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='white')

#Bar chart - Code Enforcement Stages
stages_counts = data.groupby('Stage').size().reset_index(name='counts')
ce_barchart = px.bar(stages_counts, 
                     x="Stage", y='counts', 
                     color="Stage", 
                     color_discrete_map= {'n/a':'gray'})

#Bar Chart - Tracked Properties by ZIP Code
zip_counts = data.groupby('ZIP').size().reset_index(name='counts')
zip_barchart = px.bar(zip_counts,
                      x='ZIP', y='counts',

)
quadrant_3_content = html.Div(children=[
    dcc.Tabs(children=[
        dcc.Tab(label="Code Enforcement Stage Counts", children=[
            dcc.Graph(
                id='ce-barchart',
                figure=ce_barchart,
                
                #style= {}
            )
        ]),
        dcc.Tab(label="Data Sources", children=[
            dcc.Graph(
                id='pie-chart',
                figure=pie_fig
            )
        ]),
         dcc.Tab(label="Tracked Properties by ZIP Code", children=[
            dcc.Graph(
                id='zip-barchart',
                figure=zip_barchart
            )
        ]),
    
    ])
    
    
    ],
    style={'width':'75vw', 'height':'75vh', 'margin':'10px',
           'border':'2px solid #000000', 
           'border-radius':'10px',
           'padding':'5px',
           'margin':'5px',
           'backgroundColor':'white',
           'position':'center'           
           } #Q3 Div style
)
quadrant_4_content = html.Div(
        style={'textAlign': 'center', 'left': '60%'},  # Center align content inside this div
        children=[
            html.Div(
                          
                children=[
      

                    #table component
                    dash_table.DataTable(
                        id='nola-blight-table',
                        columns=[{'name': col, 'id': col} for col in data_display.columns],  # Define columns for the table
                        data=data_display.to_dict('records'),  # Convert DataFrame to a format suitable for DataTable
                        style_table={'width': '10%', 'marginTop': '10px'},  # Style for the table
                        filter_action='native',  # Set data filter to native dash type
                        #filter_query='',  # Initial filter query

                        style_cell_conditional=[  # Set width for specific columns
                            {'if': {'column_id': 'Address'}, 'width': '30px'},
       
                            ],
                        

                        #tooltip specs
                        tooltip_header={
                        "Address": "The address of the property.",
                        "Source": "The data source of the tracked property. Read more about the data sources in the \'About\' section.",
                        "Request Status": "311 request status of the property.",
                        "Object ID": "Code Enforcement: The case identification number.",
                        "Case Filed Date": "Code Enforcement: The date the case was filed.",
                        #"Open/Closed": "Code Enforcement: Whether the case is open or closed/",
                        "Latitude": "The latitude coordinate of the property",
                        "Longitude": "The longitude coordinate \n of the property",
                        "ZIP": "The ZIP Code of the property",
                        "Stage":"Code Enforcement: The stage of the property in the code enforcement process. It is a value 1-4,"
                        " where 1 is Inspection, 2 is Title Research, 3 is Hearing, and 4 is Judgement",
                        },
                    tooltip_duration=None
        ), #end table
        
    ],
    style={'position': 'relative', 
           'width': '75vw', 
           'height': '75vh',
           'textAlign': 'center',
           'display': 'flex',  # Ensures children are displayed as flex items
            'flexDirection': 'column',
            'left': '0%', #This moves the table to the center
            'display': 'inline-block', 'maxHeight': '500px', 'overflowY': 'scroll', 'paddingLeft': '10px', #Controls for scroll frame
            #'backgroundColor':'gray'
            'border':'2px solid #000000', 
           'border-radius':'10px',
           'backgroundColor':'white'}   
        )#end table div
    ]
) #end table container div


#Home page layout - Desktop
layout = html.Div(children=[



    #Quick Start modal div, commented out for now because it isn't working right
    #html.Button('Open Quick Start Guide', id='quick-start-open'),
    #quick_start_modal,


    #4-quadrants div
    html.Div(id="grid-container",
      style={
        'display': 'flex',         # Use flexbox layout
        'flexDirection': 'column', # Stack items vertically
        'justifyContent': 'center',# Center items horizontally
        'alignItems': 'center',    # Center items vertically
        #'height': '100vh'          # Full viewport height
    },
    children=[
        
        html.Div(quadrant_1_content, style={'gridColumn': '1', 'gridRow': '1', 'margin-bottom':'20px'}),
        html.Div(quadrant_2_content, style={'gridColumn': '2', 'gridRow': '1', 'margin-bottom':'20px'}),
        html.Div(quadrant_4_content, style={'gridColumn': '1', 'gridRow': '2', 'margin-bottom':'20px'}),
        html.Div(quadrant_3_content, style={'gridColumn': '2', 'gridRow': '2', 'margin-bottom':'20px'})
    ]
)
], )#end of desktop_layout div







#Map -> Table - this actually works!!
@callback(
        Output('nola-blight-table', 'data'),
        Input('new-orleans-map', 'selectedData')
)
def update_table(selectedData):
    if selectedData is None:
        return data.to_dict('records')
    
    # Filter data based on selected points on the map
    selected_points = [point['pointIndex'] for point in selectedData['points']]
    filtered_df = data.iloc[selected_points]
    
    return filtered_df.to_dict('records')

#Table -> Map 
@callback(
    Output('new-orleans-map', 'figure'),
    [Input('nola-blight-table', 'filter_query'),]
    #State('nola-blight-table', 'data')
)

def update_map(filter_query):
    
    #print(f"This is the filter query: {filter_query}")
    
    filtered_data = data.query(filter_query)

    figure = dcc.Graph(
        #Set id
            id='new-orleans-map',
            figure=px.scatter_mapbox(
                #Use df from database
                filtered_data,
                #Use Lat/Long in Data
                lat = 'Latitude',
                lon = 'Longitude',

                #Find correct projection and zoom to display city of New Orleans
            
                #?TO DO: Make this parameter toggalable by user to change map style
                mapbox_style='carto-positron',

                center = new_orleans_coordinates,

                #Title of data set being used
                title='Tracked Properties',
                zoom = 10,
                
                #Hover Options
                color='Source',
                color_discrete_map= {'311 Calls': 'blue', 'Code Enforcement': 'red'},
                hover_name= 'Address',
                hover_data= {'Request Status':True, 'Source':True, 'Object ID':True, 'Case Filed Date':True, 
                             'Open/Closed':True,} #Controls columns that display on hover
            


        ))
    return figure

# Callback to toggle the display of the quick start guide modal
@callback(
    Output('quick-start-modal', 'style'),
    [Input('quick-start-open', 'n_clicks'),
     Input('quick-start-close', 'n_clicks')],
    [State('quick-start-modal', 'style')]
)
def toggle_modal(open_clicks, close_clicks, style):
    if open_clicks or close_clicks:
        if 'none' in style.get('display', 'none'):
            style['display'] = 'block'
        else:
            style['display'] = 'none'
    return style
