from dash import Dash, html, dcc
import dash_ag_grid as dag
import pandas as pd
import plotly.express as px


global_df = pd.read_csv("GlobalWeatherRepository.csv")
us_df = pd.read_csv("weather_data.csv")

coords = global_df[["location_name", "latitude", "longitude", "temperature_celsius", "temperature_fahrenheit"]]
fig = px.scatter_map(coords, lat="latitude", lon="longitude", 
                     hover_name="location_name", 
                     hover_data={"latitude": False, "longitude": False, 
                                 "temperature_celsius": True, "temperature_fahrenheit": True},
                     zoom=2, height=600)
fig.update_layout(mapbox_style="open-street-map")



app = Dash(__name__)

app.layout = html.Div(children=[
    html.Div(dag.AgGrid(
        columnDefs=[{"field": i} for i in global_df.columns],
        rowData=global_df.to_dict("records"),
        columnSize="autoSize"
    )),
    dcc.Graph(figure=fig)
])


if __name__ == '__main__':
    app.run(debug=True)
