import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
import plotly.offline as pyo
import plotly.graph_objs as go


statslayout = html.Div([
            dcc.Location(id='stats-url', pathname='/stats'),
            dbc.Container(
                [dbc.Row(
                      dbc.Col(
                          dbc.Card(
                              dbc.CardBody(
                                  [
                                      html.H4("Stats", className="card-title"),
                                      html.P("Select users you would like to check", className="card-text"),
                                  ]
                              )
                          )
                      )
                    ),
                    html.Br(),
                    dbc.Row(
                        dbc.Col([
                            dcc.Dropdown(
                                id="user-selection",
                                options=[
                                    {'label': 'A', 'value': 'A'},
                                    {'label': 'B', 'value': 'B'}
                                ],
                                value=['UPDATE-VIEW'],
                                multi=True
                            )
                        ]),
                    ),
                    html.Br(),
                    dbc.Row(
                        dbc.Col(
                            [
                                dcc.Graph(id='barplot', figure={
                                    'data': [go.Bar(x=['Correct', 'incorrect'], y=[0, 0])],
                                    'layout': go.Layout(title='Current stats', xaxis=dict(dtick = 1))
                                }),
                            ],
                        ),
                        # justify='center'
                    ),
                ],
            )
        ]
        )