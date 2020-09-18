import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output
import urllib

# Import CSV file
df = pd.read_csv('https://raw.githubusercontent.com/avasy/Singapore-GST-Analyst/master/gst-by-economic-sector.csv')

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.Graph(id='graph-with-slider'),
    dcc.Slider(
        id='year-slider',
        min=df['year'].min(),
        max=df['year'].max(),
        value=df['year'].min(),
        marks={str(year): str(year) for year in df['year'].unique()},
        step=None
    )
])

@app.callback(
    Output('graph-with-slider','figure'),
    [Input('year-slider','value')])
def update_figure(selected_year):
    filtered_df = df[df.year == selected_year]

    fig = px.scatter(filtered_df, x='net_gst_contribution', y='percentage_of_net_gst_contribution', size='no_of_businesses',
                     hover_name='economic_sector', log_x=True, size_max=100)

    fig.update_layout(transition_duration=500)
    fig["layout"].pop("updatemenus") #optional, drop animation buttons

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)