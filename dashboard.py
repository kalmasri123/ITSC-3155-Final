import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import sd_material_ui as material
import numpy as np

# Load CSV file from Datasets folder
deaths = pd.read_csv("Data/WHO-COVID-19-global-data.csv")
vaccinations = pd.read_csv("Data/vaccination-data.csv")

app = dash.Dash()

# Layout
app.layout = html.Div(
	children = [
		html.H1(children = "Covid Counter", style = {"margin": "20px 0"}),
		html.Hr(style = {"color": "white"}),

		# Graph 1 - Vaccinations

		html.H3(children = "Vaccination Data Viewer", style = {"margin": "10px 0", "fontWeight": "normal"}),
		material.DropDownMenu(labelText = "Time Range", id = "graph1TimeRange", options = [
			{"primaryText": "1 Week", "value": "week"},
			{"primaryText": "1 Month", "value": "month"},
			{"primaryText": "1 Year", "value": "year"}
		], variant = "filled", value = "week"),
		material.DropDownMenu(labelText = "Reporting Method", id = "graph1Method", options = [
			{"primaryText": "Percentage of Population Fully Vaccinated", "value": "vaccinated"},
			{"primaryText": "Percentage of Popluation with Booster", "value": "booster"},
			{"primaryText": "Percentage of Population Vaccinated by Type", "value": "type"}
		], variant = "filled", value = "vaccinated"),
		material.DropDownMenu(labelText = "Countries", id = "graph1Country", variant = "filled", value = ["USA"], multiple = True,
			options = [{"primaryText": x["COUNTRY"], "value": x["ISO3"]} for idx, x in vaccinations.drop_duplicates("ISO3").iterrows()]),
	],
	style = {
		"padding": "50px 100px",
		"fontFamily": "arial",
		"color": "#333",
		"fontSize": "30pt"
	}
)

if __name__ == '__main__':
	app.run_server(debug = True)
