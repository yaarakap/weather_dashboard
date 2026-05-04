from dash import Dash, html, dcc, callback, Output, Input
import dash_ag_grid as dag
import pandas as pd
import plotly.express as px


global_df = pd.read_csv("GlobalWeatherRepository.csv")
us_df = pd.read_csv("weather_data.csv")

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


coords = global_df[["location_name", "latitude", "longitude", 
                    "temp (C°)", "temp (F°)", "condition"]]
fig = px.scatter_map(coords, lat="latitude", lon="longitude", 
                     hover_name="location_name", 
                     hover_data={"latitude": False, "longitude": False, 
                                 "temp (C°)": True, "temp (F°)": True,
                                 "condition": True},
                     zoom=2, height=400, width=560)
fig.update_layout(mapbox_style="open-street-map")
fig.update_layout(margin=dict(l=10, r=10, t=10, b=10))

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
                    'UV index', 'gust (mph)']]

title = html.Div(children=["My Weather Dashboard"], 
             style={"font-family": "Verdana", "font-size": "24px", 
                    "font-weight": "bold", "marginBottom": "13px", 
                    "text-align": "center", "color": "blue"})

global_dag = dag.AgGrid(
                id="grid",
                style={"height": "90vh", "overflowX": "auto"},
                columnDefs=[
                    {"field": i, "minWidth": 140, "resizable": True,
                    } for i in metric_df.columns],
                rowData=metric_df.to_dict("records"),
                columnSize="sizeToFit",
                defaultColDef={
                    "resizable": True,
                    "sortable": True,
                    # Wrap cell values
                    "wrapText": True,
                    "autoHeight": True,
                    # Wrap header text
                    "wrapHeaderText": True,
                    "autoHeaderHeight": True,
                    # Optional: ensure word breaks are normal
                    "cellStyle": {
                            "lineHeight": "1.5",    # Reduces space between lines of text
                            "paddingTop": "7px",    # Reduces top padding
                            "paddingBottom": "5px",  # Reduces bottom padding
                            "wordBreak": "normal"
                        }
                },
                dashGridOptions={"suppressColumnVirtualisation": True,
                                 "theme": {
                                    "function": "themeQuartz.withParams({ rowVerticalPaddingScale: 0.8, headerHeight: 40 })"
                                    }
                                },
            )

radio_items = dcc.RadioItems(options=[{"label": "Metric", "value": "metric_df"}, 
                            {"label": "Imperial", "value": "imp_df"}], 
                    value='metric_df', 
                    id='controls-and-radio-item',
                    inline=True)


app = Dash(__name__)

app.layout = html.Div(children=[
    title,    
    html.Div(
        style={"display": "flex", "flexDirection": "row", "gap": "7px"},
        children=[
            global_dag,
            html.Div(children=[
                html.Hr(),
                radio_items,
                html.Hr(),
                dcc.Graph(figure=fig, style={"height": "95vh"})
                ]
            )
        ]
    )
])


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
