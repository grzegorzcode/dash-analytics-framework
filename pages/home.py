import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc


homelayout = html.Div([
            dcc.Location(id='home-url', pathname='/home'),
            dbc.Container(
                [
                    dbc.Row(
                      dbc.Col(
                          dbc.Card(
                              dbc.CardBody(
                                  [
                                      html.H4("Quiz", className="card-title"),
                                      html.P("Welcome, you have a privilege to participate in this great quiz experience", className="card-text"),
                                      dbc.Progress(" ", value=0, id="progress-tracker")
                                  ]
                              )
                          )
                      )
                    ),
                    html.Br(),
                    dbc.Row(
                        dbc.Col(
                            dbc.Card(
                              dbc.CardBody(
                                  [
                                      html.H5("Question", className="card-title"),
                                      html.P("Press any button when you're ready", className="card-text", id="question-text"),
                                  ]
                              )
                          ),
                        ),
                    ),
                    html.Br(),
                    dbc.Row([
                        dbc.Col(dbc.Button("A", size="lg", className="mr-1", block=True, id='button-a', n_clicks=0),),
                        dbc.Col(dbc.Button("B", size="lg", className="mr-1", block=True, id='button-b', n_clicks=0),),
                    ]),
                    html.Br(),
                    dbc.Row([
                        dbc.Col(dbc.Button("C", size="lg", className="mr-1", block=True, id='button-c', n_clicks=0),),
                        dbc.Col(dbc.Button("D", size="lg", className="mr-1", block=True, id='button-d', n_clicks=0),),
                    ]),
                ],
            )
        ]
    )

