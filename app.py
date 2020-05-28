# package imports
import dash
import dash_table
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
from dash import no_update
from flask import session, copy_current_request_context
import shortuuid
import numpy as np
import pandas as pd
import plotly.offline as pyo
import plotly.graph_objs as go
import io
import base64
import datetime
import time
# local imports
from auth import authenticate_user, authenticate_admin_user, validate_login_session
from server import app, server
from pages.home import homelayout
from pages.login import loginlayout
from pages.stats import statslayout
from pages.admin import panellayout
from pages.navigationbar import pageheader
from backend.dbutils import add_user_session_info
from backend.quizutils import get_next_question, get_questions_count, save_and_check_answer, get_all_users_answered, get_answers, get_all_questions, write_uploaded_data


# login layout content
def login_layout():
    return loginlayout


# home layout content
@validate_login_session
def home_layout():
    return homelayout


@validate_login_session
def stats_layout():
    return statslayout


@validate_login_session
def panel_layout(restricted):
    return panellayout


# header layout
header = pageheader


# main app layout
app.layout = html.Div(
    [
        header,
        dcc.Location(id='url', refresh=False),
        html.Div(
            login_layout(),
            id='page-content'
        ),
    ]
)


###############################################################################
# utilities
###############################################################################

# router
@app.callback(
    [Output('page-content', 'children'), Output('user-logout', 'children'), Output('admin-panel', 'children'), Output('user-welcome', 'children')],
    [Input('url', 'pathname')]
)
def router(url):
    args = ('Logout' if session['authed'] else '', 'Admin' if session['isadmin'] else '', f"Welcome {session['user'].upper()}!" if session['user'] else '')
    if url == '/home' or url == '/':
        add_user_session_info(session['user'], url, session['session_id'], level=2)
        return (home_layout(),) + args
    elif url == '/stats':
        add_user_session_info(session['user'], url, session['session_id'], level=2)
        return (stats_layout(),) + args
    elif url == '/panel':
        add_user_session_info(session['user'], url, session['session_id'], level=2)
        return (panel_layout(True),) + args
    elif url == '/login':
        add_user_session_info(session['user'], url, session['session_id'], level=2)
        return (login_layout(),) + args
    elif url == '/logout':
        add_user_session_info(session['user'], url, session['session_id'], level=2)
        if session['user']:
            add_user_session_info(session['user'], 'logout', session['session_id'])
        session['authed'] = False
        session['isadmin'] = False
        session['user'] = ''
        session['session_id'] = ''
        return (login_layout(),) + ('', 'Admin' if session['isadmin'] else '', f"Welcome {session['user'].upper()}!" if session['user'] else '')
    else:
        return (login_layout(),) + args


# authenticate 
@app.callback(
    [Output('url', 'pathname'),
     Output('login-alert', 'children')],
    [Input('login-button', 'n_clicks')],
    [State('login-user', 'value'),
     State('login-password', 'value')])
def login_auth(n_clicks, user, pw):
    '''
    check credentials
    if correct, authenticate the session
    otherwise, authenticate the session and send user to login
    '''
    if n_clicks is None or n_clicks == 0:
        return no_update, no_update
    credentials = {'user': user, "password": pw}
    if authenticate_user(credentials):
        session['authed'] = True
        session['isadmin'] = True if authenticate_admin_user(credentials) else False
        session['user'] = credentials['user']
        session['session_id'] = shortuuid.uuid()
        add_user_session_info(session['user'], 'login', session['session_id'])
        return '/home', ''
    session['authed'] = False
    session['isadmin'] = False
    session['user'] = ''
    session['session_id'] = ''
    return no_update, dbc.Alert('Incorrect credentials.', color='danger', dismissable=True)

###############################################################################
# helper functions
###############################################################################


def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    try:
        if 'xlsx' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
            write_uploaded_data(df)
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return html.Div([
        html.H5(filename),
        html.H6(datetime.datetime.fromtimestamp(date)),

        dash_table.DataTable(
            data=df.to_dict('records'),
            columns=[{'name': i, 'id': i} for i in df.columns]
        ),

        html.Hr(),  # horizontal line

        # For debugging, display the raw contents provided by the web browser
        html.Div('Raw Content'),
        html.Pre(contents[0:200] + '...', style={
            'whiteSpace': 'pre-wrap',
            'wordBreak': 'break-all'
        })
    ])


###############################################################################
# callbacks
###############################################################################


# THIS IS CALLBACK RESPONSIBLE OF UPDATING QUESTIONS MECHANISM
@app.callback(
    # output question text
    [Output('question-text', 'children'),
     # output button text
     Output('button-a', 'children'), Output('button-b', 'children'), Output('button-c', 'children'), Output('button-d', 'children'),
     #output progress tracker
     Output('progress-tracker', 'value'), Output('progress-tracker', 'children')],
    #input buttons
    [Input('button-a', 'n_clicks'),Input('button-b', 'n_clicks'), Input('button-c', 'n_clicks'),Input('button-d', 'n_clicks'),
     Input('button-a', 'n_clicks_timestamp'), Input('button-b', 'n_clicks_timestamp'), Input('button-c', 'n_clicks_timestamp'),Input('button-d', 'n_clicks_timestamp')],
    # state based on question text
    [State('question-text', 'children')])
def show_answers(n_clicks,n_clicks2,n_clicks3,n_clicks4, n_clickst,n_clickst2,n_clickst3,n_clickst4, value):
    nrclicks = n_clicks + n_clicks2 + n_clicks3 + n_clicks4
    if nrclicks == 0:
        return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update
    elif nrclicks == 1:
        next_question = get_next_question('GEO', nrclicks)
        return f'{next_question[0]}', f'{next_question[1]}', f'{next_question[2]}', f'{next_question[3]}', f'{next_question[4]}', dash.no_update, dash.no_update
    else:
        next_question = get_next_question('GEO', nrclicks)
        get_questions_nr = get_questions_count('GEO')
        get_perc = round((nrclicks-1)*100/get_questions_nr)
        #if nrclicks <= get_questions_nr + 1:
        which = np.array([item if item is not None else 0 for item in [n_clickst, n_clickst2, n_clickst3, n_clickst4]]).argmax()
        whichdict = {0: 'A', 1: 'B', 2: 'C', 3: 'D'}
        #print('GEO', nrclicks - 1, whichdict[which], session['user'])
        if nrclicks <= get_questions_nr + 1:
            save_and_check_answer('GEO', nrclicks - 1, whichdict[which], session['user'])
        try:
            return f'{next_question[0]}', f'{next_question[1]}', f'{next_question[2]}', f'{next_question[3]}', f'{next_question[4]}', get_perc, f"{get_perc}%"
        except TypeError:
            return f'COMPLETED, CHECK STATS PAGE', 'DONE', 'DONE', 'DONE', 'DONE', 100, "100%"


# THIS IS CALLBACK RESPONSIBLE OF SETTING STATS TO ALL USERS
@app.callback(Output('user-selection', 'options'), [Input('url', 'pathname')])
def refresh_user_list(pathname):
    if pathname == '/stats':
        allusers = get_all_users_answered('GEO')
        options = []
        for user in allusers:
            options.append({'label': user, 'value': user})
        return options
    return no_update


# THIS IS CALLBACK RESPONSIBLE OF UPDATING STATS BARPLOT
@app.callback(Output('barplot', 'figure'), [Input('user-selection', 'value')],)
def update_graph(users):
    traces = []
    for user in users:
        if user != 'UPDATE-VIEW':
            df = get_answers('GEO', user)
            correct = 0
            incorrect = 0
            try:
                correct = df['ISCORRECT'].value_counts().loc['Y']
            except Exception:
                pass
            try:
                incorrect = df['ISCORRECT'].value_counts().loc['N']
            except Exception:
                pass
            traces.append(
                go.Bar(x=['Correct', 'Incorrect'], y=[correct, incorrect], name=user, text=[correct, incorrect], textposition='auto', texttemplate='%{text:.1s}')
            )
    fig = {
        'data': traces,
        'layout': go.Layout(title='Current stats', yaxis=dict(dtick=1), xaxis=dict(categoryorder='category ascending'), barmode='group')
    }
    return fig


# THIS IS CALLBACK RESPONSIBLE OF UPLOADING FILES
@app.callback(Output('output-data-upload', 'children'),
              [Input('upload-data', 'contents')],
              [State('upload-data', 'filename'),
               State('upload-data', 'last_modified')])
def update_output(contents, name, upload_date):
    if contents is not None:
        # print(contents)
        # print(name)
        # print(upload_date)
        children = parse_contents(contents, name, upload_date)
        return children


# THIS IS CALLBACK RESPONSIBLE OF SHOWING QUIZ TABLE
@app.callback(Output('all-data-table', 'children'),  [Input('output-data-upload', 'children')])
def admin_table_update(trigger):
    df = get_all_questions()
    return html.Div([
        dash_table.DataTable(
            data=df.to_dict('records'),
            columns=[{'name': i, 'id': i} for i in df.columns]
        ),
    ])

###############################################################################
# run app
###############################################################################


if __name__ == "__main__":
    
    app.run_server(
        debug=False
    )

    #gunicorn app:server --bind 0.0.0.0:5000
