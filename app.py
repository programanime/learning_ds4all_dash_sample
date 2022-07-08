from dash import Dash, callback, html, dcc, dash_table, Input, Output, State, MATCH, ALL
import dash_bootstrap_components as dbc
import os
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],meta_tags=[{'name':'viewport', 'content':'width=device-width, initial-scale=1.0'}])
app.title = 'Map - Correlation One'  
app.config.suppress_callback_exceptions = True