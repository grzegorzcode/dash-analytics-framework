# package imports
import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
from dash import no_update
from flask import session, copy_current_request_context
import shortuuid
# local imports
from auth import authenticate_user, authenticate_admin_user, validate_login_session
from server import app, server
from pages.home import homelayout
from pages.login import loginlayout
from pages.stats import statslayout
from pages.admin import panellayout
from pages.navigationbar import pageheader
from backend.dbutils import add_user_session_info


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
    args = ('Logout' if session['authed'] else '', 'Admin' if session['isadmin'] else '', f"Welcome noble {session['user'].upper()}!" if session['user'] else '')
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
        return (login_layout(),) + ('', 'Admin' if session['isadmin'] else '', f"Welcome noble {session['user'].upper()}!" if session['user'] else '')
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
# callbacks
###############################################################################


###############################################################################
# run app
###############################################################################

if __name__ == "__main__":
    
    app.run_server(
        debug=True
    )