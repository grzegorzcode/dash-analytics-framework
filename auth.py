from functools import wraps
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from flask import session
from backend.dbutils import check_password, check_admin


def authenticate_user(credentials):
    '''
    generic authentication function
    returns True if user is correct and False otherwise
    '''
    #
    authed = check_password(credentials['user'], credentials['password'])
    #
    #
    return authed


def authenticate_admin_user(credentials):
    '''
    generic authentication function
    returns True if user is correct and False otherwise
    '''
    #
    # replace with your code
    is_admin = check_admin(credentials['user'])
    #
    #
    return is_admin






# ###################################################################
def validate_login_session(f):
    '''
    takes a layout function that returns layout objects
    checks if the user is logged in or not through the session. 
    If not, returns an error with link to the login page
    '''
    @wraps(f)
    def wrapper(*args, **kwargs):
        unauthorized = html.Div(
            dbc.Row(
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                html.H2('401 - Unauthorized',className='card-title'),
                                html.A(dcc.Link('Login',href='/login'))
                            ],
                            body=True
                        )
                    ],
                    width=5
                ),
                justify='center'
            )
        )

        unauthorized_admin = html.Div(
            dbc.Row(
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                html.H2('401 - Unauthorized', className='card-title'),
                            ],
                            body=True
                        )
                    ],
                    width=5
                ),
                justify='center'
            )
        )

        if session.get('authed',None)==True:
            isrestricted = int(*args)
            if isrestricted:
                return f(*args, **kwargs) if session['isadmin'] else unauthorized_admin
            else:
                return f(*args, **kwargs)
        return unauthorized
    return wrapper
