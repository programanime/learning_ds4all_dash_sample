import pathlib
import os
from dash import Dash, callback, html, dcc, dash_table, Input, Output, State, MATCH, ALL
import dash_bootstrap_components as dbc
import json
from datetime import datetime as dt
from app import app
BASE_FOLDER = os.path.dirname(os.path.dirname(__file__))
path_states = os.path.join(BASE_FOLDER, "data", "states.json")
with open(path_states, "r") as f:
    states = json.load(f)

options=[{"label":key, "value":states[key]} for key in states.keys()]

DS4A_Img = html.Div(
    children=[
        html.Img(
            src=app.get_asset_url("c1_logo_tagline.svg"),
            id="ds4a-image",
        )
    ],
)

date_picker=dcc.DatePickerRange(
    id='date_picker',
    min_date_allowed=dt(2014, 1, 2),
    max_date_allowed=dt(2017, 12, 31),
    start_date=dt(2016,1,1).date(),
    end_date=dt(2017, 1, 1).date()
)

sidebar = html.Div(
    [
        DS4A_Img, 
        html.Hr(),  
        date_picker,
        dcc.Dropdown(
            id="category-dropdown",
            options=options, 
            value=["NY",'CA'],
            multi=True
        ),
    ],
    className="ds4a-sidebar",
)
