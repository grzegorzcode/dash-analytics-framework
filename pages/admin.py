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
                                dcc.Upload(
                                    id='upload-data',
                                    children=html.Div([
                                        'Drag and Drop or ',
                                        html.A('Select Files')
                                    ]),
                                    style={
                                        'width': '100%',
                                        'height': '60px',
                                        'lineHeight': '60px',
                                        'borderWidth': '1px',
                                        'borderStyle': 'dashed',
                                        'borderRadius': '5px',
                                        'textAlign': 'center',
                                        'margin': '10px'
                                    },
                                    # Allow multiple files to be uploaded
                                    multiple=False
                                ),

                            ],
                        ),
                        justify='center'
                    ),
                    dbc.Row(
                        dbc.Col(
                            [
                            html.Div(id='output-data-upload'),
                            ]
                        )
                    ),
                    html.Hr(),
                    dbc.Row(
                        dbc.Col(
                            [
                                html.H5("all data"),
                            html.Div(id='all-data-table'),
                            html.Div(id='admin-table-trigger')
                            ]
                        )
                    ),
                ],
            )
        ])
