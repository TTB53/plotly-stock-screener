from sqlite3 import Error
import logging
import dash

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import talib
from dash.dependencies import Input, Output
from dash import callback

import db
import utils
from stock import MyStock

import assets.candlestickPattens as cp

# Interacts with the Database
dbObj = db.DBConnection()

# Interacts with the yFinance API
StockObj = MyStock()
conn = None

# Connect to DB and  Load Data
DB_FILE = "./stock-db.db"

try:
    conn = dbObj.create_connection(db_file=DB_FILE)
    logging.info("Successfully Connected to the DB from Homepage.")
    # stock_price_df = pd.read_sql('SELECT * FROM stock_price, stock WHERE stock_id= stock.id', conn)
except Error as e:
    logging.error(f"Error Occured |{e}")

companies_df = dbObj.select_table_data(conn=conn, table_name='stock')
patternsDict = cp.candlestick_patterns
stock, pattern = None, None

page_stock_info_ids = {}
page_stock_info_ids['stock-name'] = 'home-stock-name'
page_stock_info_ids['stock-title'] = 'home-stock-title'
page_stock_info_ids['stock-price'] = 'home-stock-price'
page_stock_info_ids['stock-sector'] = 'home-stock-sector'
page_stock_info_ids['stock-subsector'] = 'home-stock-subsector'

'''

Creating the card that holds the pricing chart of the stock that matches the 
patten that was selected from the dropdown.

:param: pattern - String
:param: stock - String
:returns: Card Containing Price Chart of Matching Stock

'''


def create_pattern_chart_card(pattern, stock, data):
    fig = utils.generate_candlestick_graph(data, stock + "-" + pattern)
    fig.update_layout(showlegend=False)

    patternChartCard = dcc.Graph(
        id=stock + "_" + pattern,
        animate=True,
        figure=fig,
    )
    return patternChartCard


# Registering the Dash Page
dash.register_page(__name__,
                   path='/',
                   name='Home',
                   title='Stock Screener - Home - ATB Analytics Group',
                   description='Stock Screener Homepage'
                   )


def serve_layout():
    return html.Div(
        children=[
            dcc.Interval(id='page-load-count', ),
            # utils.get_sidebar("", companies_df, page_stock_info_ids),
            dbc.Row([
                dbc.Col(
                    children=[
                        html.Center([
                            html.H1("Simple Screener"),
                            html.H3("Keeping it simple when it comes to screening stocks."),

                            html.Br(),
                            html.P("How to use the App"),

                            html.Ul(
                                id='app-instruction-list',
                                children=[
                                    html.Li(
                                        "Select a Candlestick pattern from the dropdown to populate a list"
                                        "of price graphs that match that pattern."),
                                    html.Li(
                                        "Select the stock that you want to see more information on from the "
                                        "Dropdown in the sidebar."),
                                    html.Li("Choose the Analysis you wish to start with.You can flip between the "
                                            "fundamental and technical analysis tabs without"),
                                ]
                            )
                        ],
                            style={
                                'min-height': '20vh',
                            }
                        ),

                    ],
                    width='8'
                ),

            ]),

            dbc.Row([
                html.H2("Candlestick Patterns"),
                html.Hr(),
                dbc.Col(
                    children=[

                        dbc.Card(
                            className="card",
                            children=[
                                dbc.CardHeader(html.H4("Candlestick Pattern Selection")),
                                dbc.CardBody(children=[
                                    html.P(children=[
                                        "Select a Candlestick Chart pattern below. Upon making your selection the application "
                                        "will search the database of stocks, and return the stocks that match that criteria."
                                        ""]),
                                    dcc.Dropdown(
                                        id="candlestick-pattern-dropdown",
                                        options=[

                                            {'label': patternsDict[pattern], 'value': patternsDict[pattern]} for pattern
                                            in
                                            sorted(patternsDict)
                                        ],
                                        optionHeight=35,
                                        searchable=True,
                                        clearable=False,
                                        placeholder="Select a Candlestick Chart Pattern",
                                    ),
                                    # html.Button('Submit', id='get-pattern-btn', n_clicks=0)
                                ],
                                ),
                            ]
                        ),
                    ],
                    align='center',
                    width=12),
            ]),

            dbc.Row(
                [
                    dbc.Col(
                        children=[
                            html.Div(
                                children=[
                                    dcc.Loading(children=[
                                        dbc.Card(
                                            id='chart-pattern-card',
                                            className="card",
                                            children=[
                                                html.Div(id='chart-pattern-container'),
                                                html.Center(
                                                    html.Div(
                                                        dcc.Graph(
                                                            id='empty',
                                                            figure={}
                                                        ),
                                                        style={'display': 'none'},
                                                    ),
                                                ),
                                            ],
                                            style={
                                                'width': '100%',
                                                # 'height': '25vh',
                                            }
                                        )
                                    ],
                                        type='circle',
                                        color="lightseagreen",
                                    ),

                                ]
                            ),
                        ],
                        align='center',
                        width=12,
                    ),
                ]),

            dbc.Row(
                [
                    dbc.Col(
                        children=[
                            dbc.CardGroup(
                                children=[
                                    dbc.Card(
                                        className="card",
                                        children=[
                                            dbc.CardImg(src="assets/img/fundamentalAnalysis.png"),
                                            dbc.CardBody(
                                                children=[
                                                    html.H4("Fundamental Analysis"),
                                                    html.P(
                                                        "Fundamental Analysis is a method of measuring a security's intrinsic value "
                                                        "by examining related economic and financial factors"
                                                        ""),
                                                ]
                                            ),
                                            html.A(className="btn btn-primary", href="/pages/fundamentals",
                                                   children=["Fundamental Analysis"]),

                                        ]),
                                    dbc.Card(
                                        className="card",
                                        children=[
                                            dbc.CardImg(src="assets/img/technicalAnalysis.png"),
                                            dbc.CardBody(
                                                children=[
                                                    html.H4("Technical Analysis"),
                                                    html.P(
                                                        "Fundamental Analysis is a method of measuring a security's intrinsic value "
                                                        "by examining related economic and financial factors"
                                                        ""),
                                                ]
                                            ),
                                            html.A(className="btn btn-primary", href="/pages/technical",
                                                   children=["Technical Analysis"]),
                                            # dbc.CardLink("Card link", href="/pages/technical"),
                                        ],

                                    ),
                                ]
                            ),

                        ],
                        align='center',
                        width=12,
                    ),

                    dbc.Col(
                        children=[
                            html.H2("Current Returns"),
                            html.Hr(),
                            html.Div(
                                children=[
                                    dcc.Loading(children=[
                                        dbc.Card(
                                            className="card",
                                            children=[
                                                html.Div(),
                                                dbc.CardBody(
                                                    children=[
                                                        html.H2("Sector Returns"),
                                                        html.Br(),
                                                        dcc.Loading(
                                                            id='sector-margins-chart',
                                                            type="circle",
                                                            color='lightseagreen'
                                                        ),
                                                    ]),
                                            ],
                                            style={
                                                'width': '100%',
                                                # 'height': '25vh',
                                            }
                                        ),

                                        dbc.Card(

                                            className="card",
                                            children=[

                                                dbc.CardBody(
                                                    children=[
                                                        html.H2("Top Security Returns"),
                                                        html.Br(),
                                                        dcc.Loading(
                                                            id='stock-rois-chart',
                                                            type="circle",
                                                            color='lightseagreen'
                                                        ),
                                                    ]),
                                            ],
                                            style={
                                                'width': '100%',
                                                # 'height': '25vh',
                                            }
                                        ),
                                    ],
                                        type='circle',
                                        color="lightseagreen",
                                    ),

                                ]
                            ),

                        ],
                        align='center',
                        width=12,
                    )

                ],
            ),
        ]
    )


layout = serve_layout()


@callback(
    Output('chart-pattern-container', 'children'),
    [Input('candlestick-pattern-dropdown', 'value')],
    # Input('get-pattern-btn', 'n_clicks'),
    # State('chart-pattern-container', 'children'),
)
def display_graph(pattern_value):
    pattern_graphs = []
    if pattern_value is None:
        pass
    else:
        conn = None
        try:
            conn = dbObj.create_connection(db_file=DB_FILE)
            # stock_price_df = pd.read_sql('SELECT * FROM stock_price, stock WHERE stock_id= stock.id', conn)
        except Error as e:
            logging.error(f"Error Occurred when Trying to connect to the Database | {e}")

        # Get only the companies column from the companies_df
        companies = companies_df['company']
        all_price_data = pd.read_sql_query(
            '''
            SELECT stock.company, stock.gics_sector,stock.gics_subsector, stock_price.* 
            FROM stock_price, stock 
            WHERE stock_price.stock_id=stock.id
            ''',
            conn)
        for company in companies:
            # Filter the dataset to only look at the current company and use that for analysis of the candlestick
            # pattern
            logging.info(company)
            price_data = all_price_data[(all_price_data.company == company)]

            # Get the pattern key from the value selected by in the dropdown. Reverse of how this is supposed to work.
            pattern_keys = list(patternsDict.keys())
            pattern_values = list(patternsDict.values())
            pattern_pos = pattern_values.index(pattern_value)
            pattern_key = pattern_keys[pattern_pos]

            # Getting the TALIB function for the pattern that we are interested in checking
            # using abstract api will allow for indicators to be used and passed as well.
            pattern_function = getattr(talib, pattern_key)

            try:
                pattern_data = pattern_function(price_data['Open'], price_data['High'], price_data['Low'],
                                                price_data['Close'])
                pattern_col_name = str(pattern_value).replace(" ", "_").replace("/", "_")
                price_data[pattern_col_name] = pattern_data

                if price_data[pattern_col_name].iloc[-1] != 0:
                    logging.info("{} matches the {} pattern".format(company, pattern_value))
                    new_pattern_graph = create_pattern_chart_card(pattern_value, company, price_data)
                    pattern_graphs.append(new_pattern_graph)


            except Exception as e:
                logging.error(f"Failed to get pattern data {e}")

        if pattern_graphs == [] and pattern_value is not None:
            pattern_graphs.append(
                html.Center(
                    html.P("No matches for the {} pattern were found".format(pattern_value))
                )
            )

    return dcc.Loading(children=[
        html.Div(pattern_graphs)
    ],
        type='circle',
        color='lightseagreen'
    )


@callback(
    Output('stock-rois-chart', 'children'),
    Input('candlestick-pattern-dropdown', 'value'),
    # State('page-content', 'children')
)
def update_roi_chart(pattern_value):
    if pattern_value:
        conn = dbObj.create_connection(dbObj.DB_FILE)
        # all_price_sql = dbObj.create_sql_string('data/SQL/AllStockPricesByCompanyDate.sql')

        all_price_sql = '''
        SELECT stock_price.*, stock.company
        FROM stock_price, stock
        WHERE stock_price.stock_id = stock.id
        ORDER BY stock.company    
        '''

        roi_df = pd.read_sql(all_price_sql, conn)
        roi_df = utils.add_daily_return_to_df(roi_df)
        roi_df['daily_return'] = roi_df['daily_return'] * 100

        roi_df_copy = roi_df.copy()
        roi_df_copy['max_date'] = roi_df.groupby(by="company", sort=False).date.transform('max')
        roi_df_copy['min_date'] = roi_df.groupby(by='company', sort=False).date.transform('min')
        logging.info(roi_df_copy.head())

        roi_df_copy = roi_df_copy[['date', 'company', 'adjusted_close', 'daily_return', 'max_date', 'min_date']]

        roi_df_copy.drop_duplicates(subset=['date', 'company'], inplace=True)

        min_roi_df = pd.DataFrame()
        max_roi_df = pd.DataFrame()

        for index, row in roi_df_copy.iterrows():
            if roi_df_copy[(roi_df_copy['date'][index] == row['max_date'])]:
                max = roi_df_copy[(roi_df_copy['date'][index] == row['max_date'])][
                    (roi_df_copy['company'] == row['company'])]
                # logging.info(max.head())
                max_roi_df = max_roi_df.append(max, ignore_index=True)
                logging.info("Max ROI DF\n{}\n".format(max_roi_df.head()))

            min = roi_df_copy[(roi_df_copy['date'] == row['min_date'])][(roi_df_copy['company'] == row['company'])]
            # logging.info(min.head())
            min_roi_df = min_roi_df.append(min, ignore_index=True)
            logging.info("Min ROI DF\n{}\n".format(min_roi_df.head()))

        max_roi_df.drop_duplicates(inplace=True)
        min_roi_df.drop_duplicates(inplace=True)

        roi_df_copy = pd.concat([max_roi_df, min_roi_df])

        roi_df_copy['total_return'] = roi_df_copy.apply(
            lambda row: utils.roi_between_dates_df(roi_df_copy, row['company'],
                                                   row['max_date'],
                                                   row['min_date']), axis=1)

        roi_df = utils.generate_generic_dash_datatable(roi_df, id='sector-margins-data-table')
        return dcc.Loading(children=[roi_df], type='circle', color='lightseagreen')


@callback(
    Output('sector-margins-chart', 'children'),
    Input('candlestick-pattern-dropdown', 'value'),
    # State('page-content', 'children')
)
def update_sector_roi_chart(pattern_value):
    if pattern_value:
        conn = dbObj.create_connection(dbObj.DB_FILE)
        sector_balancesheet_sql = dbObj.create_sql_string('data/SQL/sector_analysis/SectorandSubsectorTotalsTable.sql')
        sector_earnings_sql = dbObj.create_sql_string('data/SQL/sector_analysis/SectorandSubsectorEarnings.sql')

        sector_balancesheet_sql = '''
        SELECT * FROM sector_subsector_totals;
        '''

        sector_bs_df = pd.read_sql(sector_balancesheet_sql, conn)
        # sector_earn_df = pd.read_sql(sector_earnings_sql, conn)
        # roi_df = pd.melt(frames=[sector_bs_df, sector_earn_df],)
        roi_df = sector_bs_df
        roi_df = utils.generate_generic_dash_datatable(roi_df, id='sector-margins-data-table')

        return dcc.Loading(
            children=[
                html.Div(roi_df,
                         # style={'height': '25vh'}

                         )
            ],
            type='circle',
            color='lightseagreen'
        )
