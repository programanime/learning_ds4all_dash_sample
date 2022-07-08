import pathlib
import os
from dash import Dash, callback, html, dcc, dash_table, Input, Output, State, MATCH, ALL
import dash_bootstrap_components as dbc
import json
from datetime import datetime as dt
from app import app

DATA_DIR = "data"
states_path = os.path.join(DATA_DIR, "states.json")
with open(states_path) as f:
    states = json.loads(f.read())

dropdown = dcc.Dropdown(
    id="state_dropdown",
    options=[{"label": key, "value": states[key]} for key in states.keys()],
    value=["NY", "CA"],
    multi=True,
)

date_picker = dcc.DatePickerRange(
    id="date_picker",
    min_date_allowed=dt(2014, 1, 2),
    max_date_allowed=dt(2017, 12, 31),
    start_date=dt(2016, 1, 1).date(),
    end_date=dt(2017, 1, 1).date(),
    day_size = 40
)

selector = html.Div(
    [
        html.Hr(), 
        dbc.Row([
            dbc.Col([
               html.H5("Select dates"),
               date_picker,

            ]),
            dbc.Col([
               html.H5("Select states"),
               dropdown,

            ]),
        ])
    ],
    className="ds4a-selector",
)
