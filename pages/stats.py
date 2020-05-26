import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc


statslayout = html.Div([
            dcc.Location(id='stats-url', pathname='/stats'),
            dbc.Container(
                [
                    dbc.Row(
                        dbc.Col(
                            [
                                html.H2('Stats page.')

                            ],
                        ),
                        justify='center'
                    ),

                    html.Br(),

                    dbc.Row(
                        dbc.Col(
                            html.H3("look at this"),
                            width=4
                        ),
                        justify='center'
                    ),

                    html.Br()
                ],
            )
        ]
        )