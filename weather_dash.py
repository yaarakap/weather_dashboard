from dash import Dash, html, dcc, callback, Output, Input
import dash_ag_grid as dag
import pandas as pd
import plotly.express as px


global_df = pd.read_csv("GlobalWeatherRepository.csv")
us_df = pd.read_csv("weather_data.csv")

coords = global_df[["location_name", "latitude", "longitude", 
                    "temperature_celsius", "temperature_fahrenheit", "condition_text"]]
fig = px.scatter_map(coords, lat="latitude", lon="longitude", 
                     hover_name="location_name", 
                     hover_data={"latitude": False, "longitude": False, 
                                 "temperature_celsius": True, "temperature_fahrenheit": True,
                                 "condition_text": True},
                     zoom=2, height=400, width=600)
fig.update_layout(mapbox_style="open-street-map")
fig.update_layout(margin=dict(l=10, r=10, t=10, b=10))


global_df = global_df[["country", "location_name", "temperature_celsius", 
                       "temperature_fahrenheit", "condition_text", "wind_mph", "wind_kph", 
                       "wind_direction", "pressure_mb", "pressure_in", "precip_mm", "precip_in",
                       "humidity", "cloud", "feels_like_celsius", "feels_like_fahrenheit",
                       "visibility_km", "visibility_miles", "uv_index", "gust_mph", "gust_kph",
                       ]]



app = Dash(__name__)

app.layout = html.Div(
    style={"display": "flex", "flexDirection": "row", "gap": "0px"},
    children=[
        dag.AgGrid(
            id="grid",
            style={"width": "65vw", "height": "95vh", "overflowX": "auto"},
            columnDefs=[{"field": i, "minWidth": 120, "resizable": True} 
                        for i in global_df.columns],
            rowData=global_df.to_dict("records"),
            columnSize="autoSize"
        ),
        dcc.Graph(figure=fig, style={"width": "20vw", "height": "95vh"})
    ]
)

@app.callback(
    Output("grid", "columnSize"),
    Input("grid", "rowData"),
)
def resize_columns(_):
    return "autoSize"

if __name__ == '__main__':
    app.run(debug=True)
