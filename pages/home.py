import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc


homelayout = html.Div([
            dcc.Location(id='home-url', pathname='/home'),
            dbc.Container(
                [
                    dbc.Row(
                        dbc.Col(
                            [
                                html.H2('Home page.')

                            ],
                        ),
                        justify='center'
                    ),

                    html.Br(),

                    dbc.Row(
                        dbc.Col(
                            dbc.Button('Somebtn', id='some-button', color='danger', block=True, size='sm'),
                            width=2
                        ),
                        justify='center'
                    ),


                    html.Br()
                ],
            )
        ]
    )