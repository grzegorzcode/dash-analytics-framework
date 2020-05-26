import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc


panellayout = html.Div([
            dcc.Location(id='panel-url', pathname='/panel'),
            dbc.Container(
                [
                    dbc.Row(
                        dbc.Col(
                            [
                                html.H2('to be implemented')

                            ],
                        ),
                        justify='center'
                    ),
                ],
            )
        ])
