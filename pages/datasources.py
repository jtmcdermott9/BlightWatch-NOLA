#Imports
import dash
from dash import dcc, html, dash_table, Input, Output, State, callback, callback_context
import plotly.express as px
import pandas as pd

dash.register_page(__name__,)

layout = html.Div(children=[
    html.H2("Data Sources"),
    html.A("311 Data", href= "https://data.nola.gov/City-Administration/311-OPCD-Calls-2012-Present-/2jgv-pqrq/about_data" ),
    html.P("Citizens of New Orleans can call the number 311 to request city services. among these services, residents"
           " can report properties that they suspect violate city ordinances and properties that are unstable or leaning."
           " These represent potentially blighted properties. BlightWatch NOLA uses data from the table \"311 OCPD (2012-Present)\""
           " taken from City of New Orleans Open Data and filtered to only include requests related to code enforcement violations"
           " and unstable properties."),
    html.A("Code Enforcement Data", href="https://data.nola.gov/Housing-Land-Use-and-Blight/Code-Enforcement-All-Cases/u6yx-v2tw/about_data"),
    html.P("The New Orleans Department of Code Enforcement is responsible for enforcing the city's rules regarding property"
           " maintenance. They review 311 complaints, inspect properties, and then take legal action if necessary."
           " BlightWatch NOLA uses data from the table \"Code Enforcement All Inspections\" to track the properties currently"
           " being processed by the city government. Read more about the city's rules "),
            html.P(html.A("here.", href= "https://nola.gov/next/code-enforcement/topics/fighting-blight-what-is-the-code/")),
    html.A("USPS and HUD Vacancy Data", href= "https://www.huduser.gov/portal/datasets/usps.html"),
    html.P("Since 2005, the US Department of Housing and Urban Development has received data from the Postal Service on"
           " properties that are identified as \"Vacant\" or \"No-Stat\" each quarter. This means a postal worker has"
           " attempted to deliver mail to an address unsuccessfully for 90 days. It serves as a proxy for blighted properties"
           " as their owners in their negclect fail to collect mail. However, it is possible the addresses tallied are not"
           " blighted but instead refuse mail for other reasons, such as being a vacation rental.")
]
)