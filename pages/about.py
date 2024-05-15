#Imports
import dash
from dash import html

dash.register_page(__name__,)

layout = html.Div(children=[
                  html.H2("About"),
                  html.P("BlightWatch NOLA was created by Eugene Lim and Joseph McDermott, both Tulane students who are"
                         " Econimics and Computer Science double majors. The project was created under the supervision"
                         " of Professor Nicholas Mattei. The project features contributions from Tulane student Austin Nguyen,"
                         " who had to leave the project due to health problems. The source code is available at the link below."),
                  html.A("BlightWatch-NOLA GitHub Repository", href="https://github.com/jtmcdermott9/BlightWatch-NOLA")
                ]
                  )