import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
import plotly.offline as pyo
import plotly.graph_objs as go


statslayout = html.Div([
            dcc.Location(id='stats-url', pathname='/stats'),
            dbc.Container(
                [
                    dbc.Row(
                        dbc.Col(
                            [
                                dcc.Graph(id='barplot', figure={
                                    'data': [go.Bar(x=['Correct', 'incorrect'], y=[0, 0])],
                                    'layout': go.Layout(title='Current stats')
                                }),
                            ],
                        ),
                        # justify='center'
                    ),
                ],
            )
        ]
        )