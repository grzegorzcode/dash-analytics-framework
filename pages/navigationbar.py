import dash_bootstrap_components as dbc


pageheader = dbc.Navbar(
    dbc.Container(
        [
            dbc.NavbarBrand("gQuiz", href="/home"),
            dbc.Nav(
                [
                    dbc.NavItem(dbc.NavLink(id='user-welcome', disabled=True, href="#")),
                    dbc.NavItem(dbc.NavLink("Home", href="/home")),
                    dbc.NavItem(dbc.NavLink("Stats", href="/stats")),
                    dbc.NavItem(dbc.NavLink('', id='user-logout', href='/logout')),
                    dbc.NavItem(dbc.NavLink('', id='admin-panel', href='/panel'))
                ]
            )
        ]
    ),
    className="mb-5",
)
