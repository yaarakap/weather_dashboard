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
                     zoom=2, height=400, width=560)
fig.update_layout(mapbox_style="open-street-map")
fig.update_layout(margin=dict(l=10, r=10, t=10, b=10))

metric_df = global_df[['country', 'location_name', 'temperature_celsius', 
                       'condition_text', 'wind_kph',
    'wind_direction', 'pressure_mb', 
       'precip_mm', 'humidity', 'cloud', 'feels_like_celsius',
       'visibility_km', 'uv_index', 'gust_kph']]

imp_df = global_df[['country', 'location_name',
       'temperature_fahrenheit', 'condition_text', 'wind_mph',
       'wind_direction', 'pressure_in',
       'precip_in', 'humidity', 'cloud',
       'feels_like_fahrenheit', 'visibility_miles',
       'uv_index', 'gust_mph']
]


app = Dash(__name__)

app.layout = html.Div(children=[
    dcc.RadioItems(options=[{"label": "Metric", "value": "metric_df"}, 
                            {"label": "Imperial", "value": "imp_df"}], 
                    value='metric_df', 
                    id='controls-and-radio-item'),
    html.Hr(),
    html.Div(
        style={"display": "flex", "flexDirection": "row", "gap": "5px"},
        children=[
            dag.AgGrid(
                id="grid",
                style={"width": "60vw", "height": "95vh", "overflowX": "auto"},
                columnDefs=[{"field": i, "minWidth": 120, "resizable": True} 
                            for i in metric_df.columns],
                rowData=metric_df.to_dict("records"),
                columnSize="autoSize"
            ),
            dcc.Graph(figure=fig, style={"width": "15vw", "height": "95vh"})
        ]
    )
])

@app.callback(
    Output("grid", "columnSize"),
    Input("grid", "rowData"),
)
def resize_columns(_):
    return "autoSize"

@app.callback(
    Output('grid', 'rowData'),
    Output('grid', 'columnDefs'),
    Input('controls-and-radio-item', 'value')
)
def update_grid(selected_df):
    target_df = metric_df if selected_df == 'metric_df' else imp_df
    
    # Return new data and new column definitions
    return target_df.to_dict('records'), [{"field": i, "minWidth": 120, "resizable": True} 
                            for i in target_df.columns]


if __name__ == '__main__':
    app.run(debug=True)
