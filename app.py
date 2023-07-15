import dash
import dash_bootstrap_components as dbc


# BOOSTRAP APPLICATION THEME
#   CYBORG, DARKLY, LUX, MINTY, SOLAR, VAPOR,YETI -- All Cool can also create your own as well.
BS = "https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css"
# app = dash.Dash(external_stylesheets=[BS])

BOOTSTRAP_THEME = dbc.themes.CYBORG
MAIN_STYLESHEET = "assets/css/style.css"

external_stylesheets = [BOOTSTRAP_THEME, MAIN_STYLESHEET]

ALLOWED_TYPES = (
    "text", "number", "password", "email", "search",
    "tel", "url", "range", "hidden",
)

# TODO until this bug is fixed - make __name__ something else like stockScreener
app = dash.Dash("StockScreener",
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, '
                                       'initial-scale=1.0'}
                           ],
                external_stylesheets=external_stylesheets,
                )

server = app.server
app.config.suppress_callback_exceptions = True
app.title = "Stock Screener"

