from datetime import datetime

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
date_today = datetime.strftime(datetime.today(), '%d-%m-%Y')

# Load all the CASES data
stacked_cases_df_path = f'./data/cases/result.csv'
stacked_cases_df = pd.read_csv(stacked_cases_df_path, header=0)
stacked_cases_df.replace({"Slope of power-law": "Slope of power-law (cases)",
                          "Acceleration of power-law": "Acceleration of power-law (cases)",
                          "Growth Rate": "Growth Rate (cases)",
                          "Average Growth Rate": "Average Growth Rate (cases)",
                          "Doubling time": "Doubling time (cases)"
                          },
                         inplace=True)

# Get deaths information
stacked_deaths_df_path = f'./data/deaths/result.csv'
stacked_deaths_df = pd.read_csv(stacked_deaths_df_path, header=0)
stacked_deaths_df.replace({"Total cases": "Total deaths", "New cases": "New deaths",
                           "Total cases per million": "Total deaths per million",
                           "New cases per million": "New deaths per million",
                           "New cases per week per million": "New deaths per week per million",
                           "New cases per week": "New deaths per week",
                           "log10(Total cases)": "log10(Total deaths)",
                           "log10(New cases per week)": "log10(New deaths per week)",
                           "Slope of power-law": "Slope of power-law (deaths)",
                           "Acceleration of power-law": "Acceleration of power-law (deaths)",
                           "Growth Rate": "Growth Rate (deaths)",
                           "Days since first case": "Days since first death",
                           "Average Growth Rate": "Average Growth Rate (deaths)",
                           "Doubling time": "Doubling time (deaths)"
                           },
                          inplace=True)

stacked_complete_df = pd.concat([stacked_cases_df, stacked_deaths_df])

# Get information for sliders/radio buttons/etc.
available_indicators_cases = stacked_cases_df['indicator'].unique()
available_indicators_deaths = stacked_deaths_df['indicator'].unique()

days = stacked_complete_df.Days.unique()
continents = stacked_complete_df.Continent.unique()


app.layout = html.Div(children=[

    # Titles Div
    html.Div([
        html.Title(['Corona-virus Dashboard']),

        # Dashboard heading
        html.H1(
            children='Corona-virus Dashboard',
            style={
                'textAlign': 'center',
            }
        ),

        # Dashboard sub-heading
        html.Div(children=f'A dashboard for visualising my analyses of the Johns Hopkins Univerisity\'s (JHUs)'
                          f' corona-virus dataset.',
                 style={
                     'textAlign': 'center',
                 }),

    ],
    ),
    # END Titles Div

    html.Hr([]),

    # CASES DIVS

    # Cases heading
    html.H3(
        children='Worldwide Cases Plots',
        style={
            'textAlign': 'center',
        }
    ),

    # Dropdown menu & log/linear toggle div
    html.Div([
        html.Div([
            dcc.Dropdown(
                id='crossfilter-xaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators_cases],
                value='Total Cases (cumulative cases / country)'
            ),
            dcc.RadioItems(
                id='crossfilter-xaxis-type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ], style={'width': '49%',
                  'float': 'left',
                  'display': 'inline-block'}
        ),

        # Right-hand (Y-axis) dropdown and log/linear radio buttons
        html.Div([
            dcc.Dropdown(
                id='crossfilter-yaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators_cases],
                value='New cases / day / country'
            ),
            dcc.RadioItems(
                id='crossfilter-yaxis-type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ], style={'width': '49%', 'float': 'right', 'display': 'inline-block'})
    ], style={
        'borderBottom': 'thin lightgrey solid',
        'padding': '10px 5px'
    }),
    # END Dropdown menu & log/linear toggle div

    # Top plots (main scatter & timeseries)
    html.Div([
        html.Div([
            # Main plot
            dcc.Graph(
                id='crossfilter-indicator-scatter',
                hoverData={'points': [{'customdata': 'Netherlands'}]},
            )
        ], style={'width': '49%',
                  'float': 'left',
                  'display': 'inline-block',
                  'padding': '10 10',
                  'borderRight': 'thin lightgrey solid',
                  }
        ),

        # Right-hand-side X and Y time series
        html.Div([
            dcc.Graph(id='x-time-series'),
            dcc.Graph(id='y-time-series'),
        ], style={'display': 'inline-block',
                  'width': '49%',
                  'borderLeft': 'thin lightgrey solid'
                  }
        ),

    ], style={
        'borderBottom': 'thin lightgrey solid',
        'padding': '10px 5px'
    }
    ),
    # END Top plots CASES (main scatter & timeseries)

    # START Top plots DEATHS (main scatter & timeseries)
    # Dropdown menu & log/linear toggle div
    # Deaths heading
    html.H3(
        children='Worldwide Deaths Plots',
        style={
            'textAlign': 'center',
        }
    ),
    html.Div([
        html.Div([
            dcc.Dropdown(
                id='crossfilter-deaths-xaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators_deaths],
                value='Total deaths (cumulative deaths / country)'
            ),
            dcc.RadioItems(
                id='crossfilter-deaths-xaxis-type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ], style={'width': '49%',
                  'float': 'left',
                  'display': 'inline-block'}
        ),

        # Right-hand (Y-axis) dropdown and log/linear radio buttons
        html.Div([
            dcc.Dropdown(
                id='crossfilter-deaths-yaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators_deaths],
                value='New deaths / day / country'
            ),
            dcc.RadioItems(
                id='crossfilter-deaths-yaxis-type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ], style={'width': '49%', 'float': 'right', 'display': 'inline-block'})
    ], style={
        'borderBottom': 'thin lightgrey solid',
        'padding': '10px 5px'
    }),
    # END Dropdown menu & log/linear toggle div

    # Top plots (main scatter & timeseries)
    html.Div([
        html.Div([
            # Main plot
            dcc.Graph(
                id='crossfilter-deaths-indicator-scatter',
                hoverData={'points': [{'customdata': 'Netherlands'}]},
            )
        ], style={'width': '49%',
                  'float': 'left',
                  'display': 'inline-block',
                  'padding': '10 10',
                  'borderRight': 'thin lightgrey solid',
                  }
        ),

        # Right-hand-side X and Y time series
        html.Div([
            dcc.Graph(id='x-deaths-time-series'),
            dcc.Graph(id='y-deaths-time-series'),
        ], style={'display': 'inline-block',
                  'width': '49%',
                  'borderLeft': 'thin lightgrey solid'
                  }
        ),
    ], style={
        'borderBottom': 'thin lightgrey solid',
        'padding': '10px 5px'
    }
    ),

    # Footer div
    html.Div(children=f'Copyright Dr. David I. Jones, 2020. MIT License. '
                      f'See https://github.com/drblahdblah/djones-covid19-analysis for the code.',
             style={
                 'textAlign': 'center',
                 'width': '100%'
             }
             )
])


def create_time_series(dff, axis_type, title):
    return {
        'data': [dict(
            x=dff['Date'],
            y=dff['value'],
            mode='lines+markers'
        )],
        'layout': {
            'height': 225,
            'margin': {'l': 40, 'b': 30, 'r': 10, 't': 10},
            'annotations': [{
                'x': 0, 'y': 0.85, 'xanchor': 'left', 'yanchor': 'bottom',
                'xref': 'paper', 'yref': 'paper', 'showarrow': False,
                'align': 'left', 'bgcolor': 'rgba(255, 255, 255, 0.5)',
                'text': title
            }],
            'yaxis': {'type': 'linear' if axis_type == 'Linear' else 'log'},
            'xaxis': {'showgrid': False}
        }
    }


# WORLD CASES CALLBACKS
@app.callback(
    dash.dependencies.Output('crossfilter-indicator-scatter', 'figure'),
    [dash.dependencies.Input('crossfilter-xaxis-column', 'value'),
     dash.dependencies.Input('crossfilter-yaxis-column', 'value'),
     dash.dependencies.Input('crossfilter-xaxis-type', 'value'),
     dash.dependencies.Input('crossfilter-yaxis-type', 'value')])
def update_cases_graph(xaxis_column_name, yaxis_column_name,
                       xaxis_type, yaxis_type,
                       ):
    dff = stacked_cases_df[stacked_cases_df['Days'] == stacked_cases_df.Days.max()]
    return {
        'data': [dict(
            x=dff[(dff['indicator'] == xaxis_column_name) & (dff['Continent'] == i)]['value'],
            y=dff[(dff['Continent'] == i) & (dff['indicator'] == yaxis_column_name)]['value'],
            text=dff[(dff['indicator'] == yaxis_column_name) & (dff['Continent'] == i)]['Country/Region'],
            customdata=dff[(dff['indicator'] == yaxis_column_name) & (dff['Continent'] == i)]['Country/Region'],
            mode='markers',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            },
            name=i
        ) for i in dff['Continent'].unique()
        ],
        'layout': dict(
            xaxis={
                'title': xaxis_column_name,
                'type': 'linear' if xaxis_type == 'Linear' else 'log'
            },
            yaxis={
                'title': yaxis_column_name,
                'type': 'linear' if yaxis_type == 'Linear' else 'log'
            },
            margin={'l': 40, 'b': 30, 't': 10, 'r': 0},
            height=450,
            hovermode='closest'
        )
    }


@app.callback(
    dash.dependencies.Output('x-time-series', 'figure'),
    [dash.dependencies.Input('crossfilter-indicator-scatter', 'hoverData'),
     dash.dependencies.Input('crossfilter-xaxis-column', 'value'),
     dash.dependencies.Input('crossfilter-xaxis-type', 'value')])
def update_cases_y_timeseries(hover_data, xaxis_column_name, axis_type):
    country_name = hover_data['points'][0]['customdata']
    dff = stacked_cases_df[stacked_cases_df['Country/Region'] == country_name]
    dff = dff[dff['indicator'] == xaxis_column_name]
    title = f'<b>{country_name}</b><br>{xaxis_column_name}'
    return create_time_series(dff, axis_type, title)


@app.callback(
    dash.dependencies.Output('y-time-series', 'figure'),
    [dash.dependencies.Input('crossfilter-indicator-scatter', 'hoverData'),
     dash.dependencies.Input('crossfilter-yaxis-column', 'value'),
     dash.dependencies.Input('crossfilter-yaxis-type', 'value')]
)
def update_cases_x_timeseries(hover_data, yaxis_column_name, axis_type):
    dff = stacked_cases_df[stacked_cases_df['Country/Region'] == hover_data['points'][0]['customdata']]
    dff = dff[dff['indicator'] == yaxis_column_name]
    return create_time_series(dff, axis_type, yaxis_column_name)
# END WORLD CASES callback functions


# WORLD DEATHS callback functions
@app.callback(
    dash.dependencies.Output('crossfilter-deaths-indicator-scatter', 'figure'),
    [dash.dependencies.Input('crossfilter-deaths-xaxis-column', 'value'),
     dash.dependencies.Input('crossfilter-deaths-yaxis-column', 'value'),
     dash.dependencies.Input('crossfilter-deaths-xaxis-type', 'value'),
     dash.dependencies.Input('crossfilter-deaths-yaxis-type', 'value')])
def update_deaths_graph(xaxis_column_name, yaxis_column_name,
                        xaxis_type, yaxis_type):
    dff = stacked_deaths_df[stacked_deaths_df['Days'] == stacked_deaths_df.Days.max()]
    return {
        'data': [dict(
            x=dff[(dff['indicator'] == xaxis_column_name) & (dff['Continent'] == i)]['value'],
            y=dff[(dff['Continent'] == i) & (dff['indicator'] == yaxis_column_name)]['value'],
            text=dff[(dff['indicator'] == yaxis_column_name) & (dff['Continent'] == i)]['Country/Region'],
            customdata=dff[(dff['indicator'] == yaxis_column_name) & (dff['Continent'] == i)]['Country/Region'],
            mode='markers',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            },
            name=i
        ) for i in dff['Continent'].unique()
        ],
        'layout': dict(
            xaxis={
                'title': xaxis_column_name,
                'type': 'linear' if xaxis_type == 'Linear' else 'log'
            },
            yaxis={
                'title': yaxis_column_name,
                'type': 'linear' if yaxis_type == 'Linear' else 'log'
            },
            margin={'l': 40, 'b': 30, 't': 10, 'r': 0},
            height=450,
            hovermode='closest'
        )
    }


@app.callback(
    dash.dependencies.Output('x-deaths-time-series', 'figure'),
    [dash.dependencies.Input('crossfilter-deaths-indicator-scatter', 'hoverData'),
     dash.dependencies.Input('crossfilter-deaths-xaxis-column', 'value'),
     dash.dependencies.Input('crossfilter-deaths-xaxis-type', 'value')])
def update_deaths_y_timeseries(hover_data, xaxis_column_name, axis_type):
    country_name = hover_data['points'][0]['customdata']
    dff = stacked_deaths_df[stacked_deaths_df['Country/Region'] == country_name]
    dff = dff[dff['indicator'] == xaxis_column_name]
    title = f'<b>{country_name}</b><br>{xaxis_column_name}'
    return create_time_series(dff, axis_type, title)


@app.callback(
    dash.dependencies.Output('y-deaths-time-series', 'figure'),
    [dash.dependencies.Input('crossfilter-deaths-indicator-scatter', 'hoverData'),
     dash.dependencies.Input('crossfilter-deaths-yaxis-column', 'value'),
     dash.dependencies.Input('crossfilter-deaths-yaxis-type', 'value')]
)
def update_deaths_x_timeseries(hover_data, yaxis_column_name, axis_type):
    dff = stacked_deaths_df[stacked_deaths_df['Country/Region'] == hover_data['points'][0]['customdata']]
    dff = dff[dff['indicator'] == yaxis_column_name]
    return create_time_series(dff, axis_type, yaxis_column_name)
# END WORLD DEATHS callback functions


if __name__ == '__main__':
    app.run_server(port=8299)
