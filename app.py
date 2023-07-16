import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html, callback, State
import plotly.io as pio

import assets.templates.atbanalyticsgrp_dark as ATBDEFAULTTHEME

pio.templates.default = "atbAnalyticsGroupDefaultDark"

# BOOSTRAP APPLICATION THEME
#   CYBORG, DARKLY, LUX, MINTY, SOLAR, VAPOR,YETI -- All Cool can also create your own as well.
BS = "https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css"
# app = dash.Dash(external_stylesheets=[BS])

ATBLOGO = './assets/img/logo/atb-analytics-group-logo.png'
FONTS = './assets/css/fonts.css'
BOOTSTRAP_THEME = dbc.themes.CYBORG
MAIN_STYLESHEET = "assets/css/style.css"

external_stylesheets = [ATBDEFAULTTHEME, FONTS, MAIN_STYLESHEET]

ALLOWED_TYPES = (
    "text", "number", "password", "email", "search",
    "tel", "url", "range", "hidden",
)

# TODO until this bug is fixed - make __name__ something else like stockScreener
app = dash.Dash("StockScreener",
                # use_pages=True,
                meta_tags=[
                    {'name': 'viewport',
                     'content': 'width=device-width, '
                                'initial-scale=1.0'}
                ],
                external_stylesheets=external_stylesheets,
                title="Stock Screener | ATB Analytics Group",
                update_title="Gathering Data...",
                assets_folder="./assets",
                )

server = app.server
app.config.suppress_callback_exceptions = True
app.title = "Stock Screener"
