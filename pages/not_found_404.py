'''
404 Not Found

------------------------------------------------------------------------------
Program Description
-------------------------------------------------------------------------------

Not Found Page (404)

----------------------------------------------------------------------------------

'''
from dash import html
import dash
import dash_bootstrap_components as dbc

dash.register_page(__name__, path="/404")

layout = dbc.Container(
    children=[
        html.H1("Ohhh No, you've reached a page you were not looking for!"),
        html.Br(),
        html.Img(
            id='404-page-img',
            alt='Stock Screener ',
            className='img-fluid mb-3 img-responsive',
            src='assets/img/logo/atb-analytics-group-logo.png',
            title='ATB Analytics Group Logo',
            width="100%"
        ),
        html.P(
            """
                These are not the links you're looking for. If you are truly looking for the links you can go to the
                homepage, if you are not. Stop now. I do not have the particular set of skills to stop you, but I
                figured the obviously empty threat and laugh, would hopefully make you choose another target lol.
            """
        )
    ]
)
