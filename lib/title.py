import pathlib
from dash import Dash, callback, html, dcc, dash_table, Input, Output, State, MATCH, ALL
import dash_bootstrap_components as dbc
from app import app
import os
import plotly.express as px
import pandas as pd
import json

BASE_FOLDER = os.path.dirname(os.path.dirname(__file__))

df = pd.read_csv(os.path.join(BASE_FOLDER, "data", "superstore.csv"), parse_dates=['Order Date', 'Ship Date'])
with open(os.path.join(BASE_FOLDER, "data", "us.json")) as geo:
    geojson = json.loads(geo.read())

with open(os.path.join(BASE_FOLDER, "data", "states.json")) as f:
    states_dict = json.loads(f.read())
df['State_abbr'] = df['State'].map(states_dict)

dff = df.groupby('State_abbr').sum().reset_index()
Map_Fig = px.choropleth_mapbox(dff,                         
          locations='State_abbr',                   
          color='Sales',                            
          geojson=geojson,                          
          zoom=3,                                   
          mapbox_style="carto-positron",            
          center={"lat": 37.0902, "lon": -95.7129}, 
          color_continuous_scale="Viridis",         
          opacity=0.5,                              
          )
Map_Fig.update_layout(title='US map',paper_bgcolor="#F8F9F9")

map = html.Div([
  dcc.Graph(figure=Map_Fig, id='US_map')
], className="ds4a-body")

Scatter_fig=px.scatter(df, x="Sales", y="Profit", color="Category", hover_data=['State','Sub-Category','Order ID','Product Name'])  
Scatter_fig.update_layout(title='Sales vs. Profit in selected states',paper_bgcolor="#F8F9F9")

df['Order_Month'] = pd.to_datetime(df['Order Date'].dt.to_period('M').astype(str))
states=['California', 'Texas','New York']

ddf=df[df['State'].isin(states)]
ddf=ddf.groupby(['State','Order_Month']).sum().reset_index()

Line_fig=px.line(ddf,x="Order_Month",y="Sales", color="State")
Line_fig.update_layout(title='Montly Sales in selected states',paper_bgcolor="#F8F9F9")

stats=html.Div([ 
    dbc.Row([
        dbc.Col(
            dcc.Graph(figure=Line_fig, id='Line')
        ),
        dbc.Col(
            dcc.Graph(figure=Scatter_fig, id='Scatter')
            )
    ]),
	],className="ds4a-body")

title = dbc.Row(
    [
        map, 
        stats
    ]
)
