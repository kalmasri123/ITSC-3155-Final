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

vaccinationsDf = vaccinations.sort_values(
    "PERSONS_FULLY_VACCINATED", ascending=False).head(10)
vaccinationsRatioData = [
    go.Bar(x=vaccinationsDf['COUNTRY'],
           y=vaccinationsDf['PERSONS_FULLY_VACCINATED_PER100'], name="Vaccinated"),
    go.Bar(x=vaccinationsDf['COUNTRY'],
           y=vaccinationsDf['PERSONS_BOOSTER_ADD_DOSE_PER100'], name="Booster")
]

vaccinationsData = [
    go.Bar(x=vaccinationsDf['COUNTRY'],
           y=vaccinationsDf['PERSONS_FULLY_VACCINATED'], name="Vaccinated"),
    go.Bar(x=vaccinationsDf['COUNTRY'],
           y=vaccinationsDf['PERSONS_BOOSTER_ADD_DOSE'], name="Booster")
]

app = dash.Dash()

# Layout
app.layout = html.Div(
    children=[
        html.H1(children="Covid Counter", style={"margin": "20px 0"}),
        html.Hr(style={"color": "white"}),

        # Graph 1 - Vaccinations

        html.H3(children="Vaccination Data Viewer", style={
                "margin": "10px 0", "fontWeight": "normal"}),
        material.DropDownMenu(labelText="Countries", id="vaccinationCountry", variant="filled", multiple=True,
                              value=[x["ISO3"]
                                     for idx, x in vaccinationsDf.iterrows()],
                              options=[{"primaryText": x["COUNTRY"], "value": x["ISO3"]} for idx, x in vaccinations.iterrows()]),
        dcc.Graph(
            id="vaccinationRatioGraph",
            figure={
                "data": vaccinationsRatioData,
                "layout": go.Layout(
                    title="Vaccination Percentages by Country",
                    xaxis_title="Country",
                    yaxis_title="Vaccination/Booster Percentage",
                    barmode="stack"
                ),
            },
        ),
        dcc.Graph(
            id="vaccinationGraph",
            figure={
                "data": vaccinationsData,
                "layout": go.Layout(
                    title="Total Vaccination by Country",
                    xaxis_title="Country",
                    yaxis_title="Total Vaccination/Booster",
                    barmode="stack"
                ),
            },
        )
    ],
    style={
        "padding": "50px 100px",
        "fontFamily": "arial",
        "color": "#333",
        "fontSize": "30pt"
    }
)


@app.callback([Output("vaccinationRatioGraph", "figure"), Output("vaccinationGraph", "figure")], [Input("vaccinationCountry", "value")])
def update_figure(countries):
    vaccinationsDf = vaccinations[vaccinations.ISO3.isin(countries)].sort_values(
        "PERSONS_FULLY_VACCINATED", ascending=False).head(10)

    vaccinationsRatioDf = vaccinationsDf.sort_values(
        by=["PERSONS_FULLY_VACCINATED_PER100", "PERSONS_BOOSTER_ADD_DOSE_PER100"], ascending=False).head(10)

    vaccinationsRatioData = [
        go.Bar(x=vaccinationsRatioDf['COUNTRY'],
               y=vaccinationsRatioDf['PERSONS_FULLY_VACCINATED_PER100'], name="Fully Vaccinated"),
        go.Bar(x=vaccinationsRatioDf['COUNTRY'],
               y=vaccinationsRatioDf['PERSONS_BOOSTER_ADD_DOSE_PER100'], name="Fully Vaccinated + Booster")
    ]

    vaccinationsData = [
        go.Bar(x=vaccinationsDf['COUNTRY'],
               y=vaccinationsDf['PERSONS_FULLY_VACCINATED'], name="Vaccinated"),
        go.Bar(x=vaccinationsDf['COUNTRY'],
               y=vaccinationsDf['PERSONS_BOOSTER_ADD_DOSE'], name="Booster")
    ]

    ratioFigure = {
        "data": vaccinationsRatioData,
        "layout": go.Layout(
            title="Vaccination Percentages by Country",
            xaxis_title="Country",
            yaxis_title="Vaccination/Booster Percentage",
            barmode="stack"
        ),
    }

    figure = {
        "data": vaccinationsData,
        "layout": go.Layout(
            title="Total Vaccination by Country",
            xaxis_title="Country",
            yaxis_title="Total Vaccination/Booster",
            barmode="stack"
        ),
    }

    return ratioFigure, figure


if __name__ == '__main__':
    app.run_server(debug=True)
