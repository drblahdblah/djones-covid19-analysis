from datetime import datetime

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px

pd.set_option("display.max_columns", 500)
pd.set_option("display.max_rows", 1000)
pd.set_option("display.width", 1000)
app = dash.Dash(__name__)
server = app.server
date_today = datetime.strftime(datetime.today(), '%d-%m-%Y')

stacked_df_path = f'./data/result.csv'
df = pd.read_csv(stacked_df_path, header=0)
available_indicators = df['indicator'].unique()

days = df.Days.unique()
continents = df.Continent.unique()

pivoted_data_path = f'./data/result_pivoted.csv'
pivoted = pd.read_csv(pivoted_data_path, header=0)
colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}


def plot_animation(df_scatter: pd.DataFrame) -> px.scatter:
    """
    Function to create a good scatter plot of new versus total cases with the date as the
    parameter in the bar.
    :param df_scatter: A Pandas DataFrame to create the scatter plot with
    :return:
    """
    df_scatter = df_scatter.groupby(['Country/Region', 'Date', 'Continent'], as_index=False).sum()

    df_scatter['growth_rate_clip'] = df_scatter['growth_rate'].clip(lower=1)

    df_scatter['New cases per day'] = df_scatter['new_cases'].clip(lower=1)
    df_scatter['Total cases'] = df_scatter['total_cases'].clip(lower=1)

    title = {
        'text': "Covid-19 cases per region: Marker size is growth rate",
        'y': 0.9,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top'}
    # return scatter plot
    return px.scatter(df_scatter, x="Total cases", y="New cases per day",
                      animation_frame="Date", animation_group="Country/Region",
                      size="growth_rate_clip",
                      size_max=100,
                      color="Continent",
                      hover_name="Country/Region",
                      log_x=True,
                      log_y=True,
                      range_x=[1, 3e6],
                      range_y=[1, 1e6],
                      title=title
                      )


fig_animated = plot_animation(pivoted)

app.layout = html.Div([

    html.Title('Corona-virus Dashboard'),
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

    html.Div([
        # Left-hand (X-axis) dropdown and log/linear radio buttons
        html.Div([
            dcc.Dropdown(
                id='crossfilter-xaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
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
                options=[{'label': i, 'value': i} for i in available_indicators],
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
        'backgroundColor': 'rgb(250, 250, 250)',
        'padding': '10px 5px'
    }),

    html.Div([
        html.Div([
            # Main plot
            dcc.Graph(
                id='crossfilter-indicator-scatter',
                hoverData={'points': [{'customdata': 'Spain'}]},
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

        # Slider for time movement
        html.Div(dcc.Slider(
            id='crossfilter-year--slider',
            min=df['Days'].min(),
            max=df['Days'].max(),
            value=df['Days'].max(),
            marks={str(year): str(year) for year in df['Days'].unique()[0::5]},
            step=2
        ), style={'width': '49%',
                  'float': 'left',
                  'padding': '50px 20px 20px 20px'}
        ),
    ], style={
        'borderBottom': 'thin lightgrey solid',
        'backgroundColor': 'rgb(250, 250, 250)',
        'padding': '10px 5px'
    }
    ),

    # fig_animated
    html.Div([
        dcc.Graph(id='cases-animation-slider',
                  figure=fig_animated,
                  style={'height': '700px'})
    ], style={
        'borderBottom': 'thin lightgrey solid',
        'backgroundColor': 'rgb(250, 250, 250)',
        'padding': '10px 5px',
        'vertical-align': 'center'
    }),

    html.Div(children=f'Copyright Dr. David I. Jones, 2020. MIT License. '
                      f'See https://github.com/drblahdblah/covid-19-analysis for the code.',
             style={
                 'textAlign': 'center',
                 'width': '100%'
             }
             )
])


@app.callback(
    dash.dependencies.Output('crossfilter-indicator-scatter', 'figure'),
    [dash.dependencies.Input('crossfilter-xaxis-column', 'value'),
     dash.dependencies.Input('crossfilter-yaxis-column', 'value'),
     dash.dependencies.Input('crossfilter-xaxis-type', 'value'),
     dash.dependencies.Input('crossfilter-yaxis-type', 'value'),
     dash.dependencies.Input('crossfilter-year--slider', 'value')])
def update_graph(xaxis_column_name, yaxis_column_name,
                 xaxis_type, yaxis_type,
                 date_value):
    dff = df[df['Days'] == date_value]
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


@app.callback(
    dash.dependencies.Output('x-time-series', 'figure'),
    [dash.dependencies.Input('crossfilter-indicator-scatter', 'hoverData'),
     dash.dependencies.Input('crossfilter-xaxis-column', 'value'),
     dash.dependencies.Input('crossfilter-xaxis-type', 'value')])
def update_y_timeseries(hover_data, xaxis_column_name, axis_type):
    country_name = hover_data['points'][0]['customdata']
    dff = df[df['Country/Region'] == country_name]
    dff = dff[dff['indicator'] == xaxis_column_name]
    title = f'<b>{country_name}</b><br>{xaxis_column_name}'
    return create_time_series(dff, axis_type, title)


@app.callback(
    dash.dependencies.Output('y-time-series', 'figure'),
    [dash.dependencies.Input('crossfilter-indicator-scatter', 'hoverData'),
     dash.dependencies.Input('crossfilter-yaxis-column', 'value'),
     dash.dependencies.Input('crossfilter-yaxis-type', 'value')]
)
def update_x_timeseries(hover_data, yaxis_column_name, axis_type):
    dff = df[df['Country/Region'] == hover_data['points'][0]['customdata']]
    dff = dff[dff['indicator'] == yaxis_column_name]
    return create_time_series(dff, axis_type, yaxis_column_name)


if __name__ == '__main__':
    app.run_server()
