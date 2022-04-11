import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go

# Load CSV file from Datasets folder
deaths = pd.read_csv("Data/WHO-COVID-19-global-data.csv")
vaccinations = pd.read_csv("Data/vaccination-data.csv")

app = dash.Dash()


