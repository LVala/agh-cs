import dash
import numpy as np
import plotly.graph_objects as go
import pandas as pd
import plotly.express as px
import sys

from dash import dcc, html
from dash.dependencies import Input, Output
from dash import html, dcc
from simulation import Space, Types

app = None
cells = None
X, Y, Z = None, None, None
X1, Y1, Z1 = None, None, None
LENGTH, WIDTH, HEIGHT = None, None, None

sys.setrecursionlimit(1000)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

PAD = '0.3%'
OPACITY_SCATTER = 0.6
OPACITY_VOLUME = 0.6
OPACITY_HOUSE = 0.6
MIN_TEMP = 15
MAX_TEMP = 30

colors = {
    'text': "#111111",
}

colors_discrete_map = {
    Types.air: "#e5ecf6",
    Types.wall_poor: "#c8bba3",
    Types.wall_good: "#606060",
    Types.window: "#00008b",
    Types.heat_source: "#e25822",
}

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


def main():
    global cells, X, Y, Z, LENGTH, WIDTH, HEIGHT, app, X1, Y1, Z1, MIN_TEMP, MAX_TEMP

    X_LENGTH = 4
    Y_LENGTH = 3
    Z_LENGTH = 3
    CELL_LENGTH = 0.3
    OUTSIDE_TEMP = 15
    INSIDE_TEMP = 15
    HEAT_TEMP = 30
    TIME = 1

    MIN_TEMP = OUTSIDE_TEMP
    MAX_TEMP = HEAT_TEMP

    cells = Space(X_LENGTH, Y_LENGTH, Z_LENGTH, CELL_LENGTH, OUTSIDE_TEMP, INSIDE_TEMP, HEAT_TEMP, TIME)

    LENGTH, WIDTH, HEIGHT = len(cells.space), len(cells.space[0]), len(cells.space[0][0])
    X, Y, Z = np.mgrid[:LENGTH, :WIDTH, :HEIGHT]
    X1, Y1, Z1 = np.mgrid[1:LENGTH - 1, 1:WIDTH - 1, 1:HEIGHT - 1]
    X, Y, Z = X.flatten(), Y.flatten(), Z.flatten()
    X1, Y1, Z1 = X1.flatten(), Y1.flatten(), Z1.flatten()


@app.callback(Output('volume_graph', 'figure'),
              Output('iterations_per_refresh', 'value'),
              Input('interval_component', 'n_intervals'),
              Input('iterations_per_refresh', 'value'))
def update_graph_live(n_intervals, no_iterations_per_refresh):
    temp = np.array(
        [cells.space[i][j][k].temperature
         for i in range(1, LENGTH - 1) for j in range(1, WIDTH - 1) for k in range(1, HEIGHT - 1)])

    fig = go.Figure(data=go.Volume(
        x=X1, y=Y1, z=Z1,
        value=temp.flatten(),
        isomin=MIN_TEMP + 0.1,  # lower bound on drawing temperature
        isomax=MAX_TEMP,  # upper bound on drawing temperature
        opacity=OPACITY_VOLUME,
        surface_count=25
    ))

    fig.update_layout(scene_xaxis_showticklabels=False,
                      scene_yaxis_showticklabels=False,
                      scene_zaxis_showticklabels=False,
                      uirevision='dont restore to default position after change',
                      margin=dict(l=0, r=0, b=0, t=0)
                      )

    for _ in range(no_iterations_per_refresh):
        cells.iter()

    return fig, no_iterations_per_refresh


@app.callback(Output('scatter_graph', 'figure'),
              Input('interval_component', 'n_intervals'))
def update_graph_live(n_intervals):
    temp = np.array(
        [cells.space[i][j][k].temperature
         for i in range(1, LENGTH - 1) for j in range(1, WIDTH - 1) for k in range(1, HEIGHT - 1)])

    df = pd.DataFrame({"x": X1, "y": Y1, "z": Z1, "T": temp.flatten()})

    fig = px.scatter_3d(df, x='x', y='y', z='z',
                        color='T', opacity=OPACITY_SCATTER,
                        range_color=(MIN_TEMP, MAX_TEMP))

    fig.update_layout(margin=dict(l=0, r=0, b=0, t=0),
                      scene_xaxis_showticklabels=False,
                      scene_yaxis_showticklabels=False,
                      scene_zaxis_showticklabels=False,
                      uirevision='dont restore to default position after change')
    return fig


@app.callback(
    Output('interval_component', 'interval'),
    Input('refresh_time', 'value'))
def update_refresh_time(value):
    return value


def get_house_graph():
    cell_types = np.array(
        [cells.space[i][j][k].type for i in range(LENGTH) for j in range(WIDTH) for k in range(HEIGHT)])

    df = pd.DataFrame({"x": X, "y": Y, "z": Z, "T": cell_types.flatten()})

    fig = px.scatter_3d(df, x='x', y='y', z='z', color="T", opacity=OPACITY_HOUSE,
                        color_discrete_map=colors_discrete_map,
                        )
    fig.update_layout(margin=dict(l=0, r=0, b=0, t=0),
                      scene_xaxis_showticklabels=False,
                      scene_yaxis_showticklabels=False,
                      scene_zaxis_showticklabels=False,
                      uirevision='dont restore to default position after change')
    return fig


def set_app_layout():
    global app
    app.layout = html.Div([
        html.H1('Room heating simulation',
                style={
                    'textAlign': 'center',
                    'color': colors['text']
                }),

        html.H5(
            children='Number of iterations per refresh',
            style={
                'textAlign': 'center',
                'color': colors['text']
            }
        ),

        dcc.Slider(0, 100, 2,
                   value=0,
                   id='iterations_per_refresh',
                   updatemode='drag'),

        html.H5(
            children='Refresh time [ms]',
            style={
                'textAlign': 'center',
                'color': colors['text']
            }
        ),

        dcc.Slider(500, 5000, 500,
                   value=1600,
                   id='refresh_time',
                   updatemode='drag'),
        html.Div(children=[
            dcc.Graph(id='scatter_graph', style={'display': 'inline-block', 'padding-left': PAD, 'padding-right': PAD}),

            dcc.Graph(id='volume_graph', style={'display': 'inline-block', 'padding-left': PAD, 'padding-right': PAD}),

            dcc.Graph(id='house_graph', figure=get_house_graph(), style={'display': 'inline-block', 'padding-left': PAD,
                                                                         'padding-right': PAD}),
        ], style={'width': '90%', 'padding-left': '2%', 'padding-right': '0.5%'}),
        dcc.Interval(
            id='interval_component',
            interval=1600,
            n_intervals=0
        )
    ]
    )


if __name__ == '__main__':
    main()
    set_app_layout()
    app.run_server(debug=True)