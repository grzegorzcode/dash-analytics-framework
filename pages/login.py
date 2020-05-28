import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc


loginlayout = html.Div(
        [
            dcc.Location(id='login-url', pathname='/login', refresh=False),
            dbc.Container(
                [
                    dbc.Row(
                        dbc.Col(
                            dbc.Card(
                                [
                                    html.H4('Login', className='card-title'),
                                    html.H6('google auth available soon', style={'color': 'grey'}),
                                    dbc.Input(id='login-user', placeholder='User'),
                                    html.Br(),
                                    dbc.Input(id='login-password', placeholder='Assigned password', type='password'),
                                    html.Br(),
                                    dbc.Button('Submit', id='login-button', color='success', block=True),
                                    html.Br(),
                                    html.Div(id='login-alert')
                                ],
                                body=True
                            ),
                            width=6
                        ),
                        justify='center'
                    )
                ]
            )
        ]
    )