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

global_df.rename(columns={"temperature_celsius": "temp (C°)", 
                          "temperature_fahrenheit": "temp (F°)",
                          "condition_text": "condition",
                          "wind_kph": "wind (kph)", "wind_mph": "wind (mph)",
                          "pressure_mb": "pressure (mb)", "pressure_in": "pressure (in)",
                          "precip_mm": "precipitation (mm)", "precip_in": "precipitation (in)",
                          "feels_like_celsius": "feels like (C°)",
                          "feels_like_fahrenheit": "feels like (F°)",
                          "visibility_km": "visibility (km)", "visibility_miles": "visibilit (mi)",
                          "gust_kph": "gust (kph)", "gust_mph": "gust (mph)",
                          "uv_index": "UV index"},
                inplace=True)

metric_df = global_df[['country', 'location_name', 'temp (C°)', 
                       'condition', 'wind (kph)',
        'wind_direction', 'pressure (mb)', 
       'precipitation (mm)', 'humidity', 'cloud', 'feels like (C°)',
       'visibility (km)', 'UV index', 'gust (kph)']]

imp_df = global_df[['country', 'location_name',
       'temp (F°)', 'condition', 'wind (mph)',
       'wind_direction', 'pressure (in)',
       'precipitation (in)', 'humidity', 'cloud',
       'feels like (F°)', 'visibilit (mi)',
       'UV index', 'gust (mph)']
]


app = Dash(__name__)

app.layout = html.Div(children=[
    dcc.RadioItems(options=[{"label": "Metric", "value": "metric_df"}, 
                            {"label": "Imperial", "value": "imp_df"}], 
                    value='metric_df', 
                    id='controls-and-radio-item',
                    inline=True),
    html.Hr(),
    html.Div(
        style={"display": "flex", "flexDirection": "row", "gap": "5px"},
        children=[
            dag.AgGrid(
                id="grid",
                style={"width": "60vw", "height": "95vh", "overflowX": "auto"},
                columnDefs=[{"field": i, "minWidth": 120, "maxWidth": 200, "resizable": True, } 
                            for i in metric_df.columns],
                rowData=metric_df.to_dict("records"),
                columnSize="autoSize",
                dashGridOptions={"suppressColumnVirtualisation": True},
            defaultColDef={
                "wrapText": True,
                "autoHeight": True,
                "cellStyle": {"wordBreak": "normal"}
            }),
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
    return target_df.to_dict('records'), [{"field": i, "minWidth": 20, "resizable": True} 
                            for i in target_df.columns]


if __name__ == '__main__':
    app.run(debug=True)
