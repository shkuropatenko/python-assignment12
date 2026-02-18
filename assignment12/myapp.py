# Task 4: Dash dashboard (Gapminder GDP per Capita)

from __future__ import annotations

import dash
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

df = px.data.gapminder()

countries = df["country"].drop_duplicates().sort_values()
dropdown_options = [{"label": c, "value": c} for c in countries]

app = Dash(__name__)
server = app.server

app = dash.Dash(__name__)

app.layout = html.Div(
  [
    html.H2("GDP per Capita Growth (Gapminder)"),
    dcc.Dropdown(
      id="country-dropdown",
      options=dropdown_options,
      value="Canada",
      clearable=False,
    ),
    dcc.Graph(id="gdp-growth"),
  ],
  style={"maxWidth": "900px", "margin": "0 auto"},
)

@app.callback(
  Output("gdp-growth", "figure"),
  Input("country-dropdown", "value"),
)
def update_graph(country_name: str):
  filtered = df[df["country"] == country_name]

  fig = px.line(
    filtered,
    x="year",
    y="gdpPercap",
    title=f"GDP per Capita Over Time — {country_name}",
    labels={"year": "Year", "gdpPercap": "GDP per Capita"},
  )
  return fig

if __name__ == "__main__":
  app.run_server(debug=True)
