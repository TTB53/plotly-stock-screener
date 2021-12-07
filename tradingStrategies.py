'''
This is the way that we will identify options strategies by passing in the options (puts,calls) into this we can
can calculate profitability of the selected strategy

Options Meaning and definitions

Long Call - Buy and Own Call Contract - Bullish Sentiment - As Underlying increases value of contract increases
Short Call - Sell Call Contract - Bearish Sentiment - As Underlying decreases, value of option contract you want to buy back cheaper, making profit
Long Put - Buy Put Contract - Bearish Sentiment - As Underlying decreases value of contract increases
Short Put - Sel Put Contract - Bullish Sentiment -As Underlying decreases, value of option contract you want to buy back cheaper, making profit

Basic Options Strategies

Strategies with Underlying
    -Covered Call
        - Two Leg Strategy
            -Long Position in Underlying ("Covers the loss that could be incurred by the short position.)
            -Short Position in a call option on Underlying

        - Objective (Payoff)
            -Max Profit = Strike Price - initial underlying price + premium received
            -Max Loss = Premium Received - initial Underlying price

            -Underlying is at exactly the Strike Price (Maximum Profit) Short Position Expires Worthless
            -Underlying increases more than the Strike Price (Maximum Profit) only this time we get assigned the
            short call, and no longer own the underlying but receive the strike price for the shares. Financially
            the same as the first one minus keeping our shares as well
            - Where we can lose money since we are Long the Underlying and it's price has decreased,
            depends on what was collected for the premium on the short call
            If Underlying falls Below Strike price:
                P/L = underlying price at expiration - initial underlying price + premium received

            B/E = initial underlying price - premium

        -Strike Selection
            -The Higher strike you select, the smaller the premium will be
                - Higher Strike means more risk, however it also means higher chance for profit

            - Best Strike is one Closest to the underlying price at expiration

    -Protective Put
    -Protective Call
    -Collar

Vertical Spreads
    -Bull Call Spread
    -Bear Call Spread
    -Bull Put Spread
    -Bear Put Spread


Non-Directional Strategies
    -Long Straddle
        - Buying a call and put option on the same underlying with the same expiration date. Long Call and a Long put
        at the same strike price
    -Long Strangle
            - Buying a call and put option on the same underlying with the same expiration date. Long Call and a Long put
        but the Call has a higher Strike price.
    -Short Straddle
    -Short Strangle
    -Iron Butterfly
    -Iron Condor
'''

'''

Color Choices 

aliceblue, antiquewhite, aqua, aquamarine, azure, beige, bisque, black, blanchedalmond, blue, 
blueviolet, brown, burlywood, cadetblue, chartreuse, chocolate, coral, cornflowerblue, cornsilk, 
crimson, cyan, darkblue, darkcyan, darkgoldenrod, darkgray, darkgrey, darkgreen, darkkhaki, darkmagenta, 
darkolivegreen, darkorange, darkorchid, darkred, darksalmon, darkseagreen, darkslateblue, darkslategray, 
darkslategrey, darkturquoise, darkviolet, deeppink, deepskyblue, dimgray, dimgrey, dodgerblue, firebrick, 
floralwhite, forestgreen, fuchsia, gainsboro, ghostwhite, gold, goldenrod, gray, grey, green, greenyellow, 
honeydew, hotpink, indianred, indigo, ivory, khaki, lavender, lavenderblush, lawngreen, lemonchiffon, lightblue, 
lightcoral, lightcyan, lightgoldenrodyellow, lightgray, lightgrey, lightgreen, lightpink, lightsalmon, lightseagreen, 
lightskyblue, lightslategray, lightslategrey, lightsteelblue, lightyellow, lime, limegreen, linen, magenta, maroon, 
mediumaquamarine, mediumblue, mediumorchid, mediumpurple, mediumseagreen, mediumslateblue, mediumspringgreen, 
mediumturquoise, mediumvioletred, midnightblue, mintcream, mistyrose, moccasin, navajowhite, navy, oldlace, olive, 
olivedrab, orange, orangered, orchid, palegoldenrod, palegreen, paleturquoise, palevioletred, papayawhip, peachpuff,
 peru, pink, plum, powderblue, purple, red, rosybrown, royalblue, rebeccapurple, saddlebrown, 
 salmon, sandybrown, seagreen, seashell, sienna, silver, skyblue, slateblue, slategray, slategrey, snow, 
 springgreen, steelblue, tan, teal, thistle, tomato, turquoise, violet, wheat, white, whitesmoke, yellow, yellowgreen

'''

import yfinance as yf

data = yf.Ticker(ticker="VOO")
print(data.info)
'''
YFINANCE INFO returns the following dictionary 

{'zip': '95014', 
'sector': 'Technology', 
'fullTimeEmployees': 147000, 
'longBusinessSummary': 'Apple Inc. designs, manufactures, and markets smartphones, personal computers, tablets, wearables,
 and accessories worldwide. It also sells various related services. The company offers iPhone, a line of smartphones; 
 Mac, a line of personal computers; iPad, a line of multi-purpose tablets; and wearables, 
 home, and accessories comprising AirPods, Apple TV, Apple Watch, Beats products, HomePod, 
 iPod touch, and other Apple-branded and third-party accessories. It also provides AppleCare support services; 
 cloud services store services; and operates various platforms, including the App Store, that allow customers to discover 
 and download applications and digital content, such as books, music, video, games, and podcasts. In addition, the company 
 offers various services, such as Apple Arcade, a game subscription service; Apple Music, which offers users a curated 
 listening experience with on-demand radio stations; Apple News+, a subscription news and magazine service; Apple TV+, 
 which offers exclusive original content; Apple Card, a co-branded credit card; and Apple Pay, a cashless payment service, 
 as well as licenses its intellectual property. The company serves consumers, and small and mid-sized businesses; 
 and the education, enterprise, and government markets. It sells and delivers third-party applications for its 
 products through the App Store. The company also sells its products through its retail and online stores, 
 and direct sales force; and third-party cellular network carriers, wholesalers, retailers, and resellers. 
 Apple Inc. was founded in 1977 and is headquartered in Cupertino, California.', 
 'city': 'Cupertino', 
 'phone': '408-996-1010', 
 'state': 'CA', 
 'country': 'United States', 
 'companyOfficers': [], 
 'website': 'http://www.apple.com', 
 'maxAge': 1, 
 'address1': 'One Apple Park Way', 
 'industry': 'Consumer Electronics', 
 'ebitdaMargins': 0.31955, 
 'profitMargins': 0.25004, 
 'grossMargins': 0.41005, 
 'operatingCashflow': 104414003200, 
 'revenueGrowth': 0.364, 
 'operatingMargins': 0.28788, 
 'ebitda': 110934999040, 
 'targetLowPrice': 132, 
 'recommendationKey': 
 'buy', 
 'grossProfits': 104956000000, 
 'freeCashflow': 80625876992, 
 'targetMedianPrice': 168, 
 'currentPrice': 151.12, 
 'earningsGrowth': 1, 
 'currentRatio': 1.062, 
 'returnOnAssets': 0.19302, 
 'numberOfAnalystOpinions': 41, 
 'targetMeanPrice': 165.87, 
 'debtToEquity': 210.782, 
 'returnOnEquity': 1.27125, 
 'targetHighPrice': 190, 
 'totalCash': 61696000000, 
 'totalDebt': 135491002368, 
 'totalRevenue': 347155005440, 
 'totalCashPerShare': 3.732, 
 'financialCurrency': 'USD', '
 revenuePerShare': 20.61, 
 'quickRatio': 0.887, 
 'recommendationMean': 2, 
 'exchange': 'NMS', 
 'shortName': 'Apple Inc.', 
 'longName': 'Apple Inc.', 
 'exchangeTimezoneName': 'America/New_York', 
 'exchangeTimezoneShortName': 'EDT', 
 'isEsgPopulated': False, 
 'gmtOffSetMilliseconds': '-14400000', 
 'quoteType': 'EQUITY', 
 'symbol': 'AAPL', 
 'messageBoardId': 'finmb_24937', 
 'market': 'us_market', 
 'annualHoldingsTurnover': None, 
 'enterpriseToRevenue': 7.312, 
 'beta3Year': None, 
 'enterpriseToEbitda': 22.882, 
 '52WeekChange': 0.29021096, 
 'morningStarRiskRating': None, 
 'forwardEps': 5.67, 
 'revenueQuarterlyGrowth': None, 
 'sharesOutstanding': 16530199552, 
 'fundInceptionDate': None, 
 'annualReportExpenseRatio': None, 
 'totalAssets': None, 
 'bookValue': 3.882, 
 'sharesShort': 93114834, 
 'sharesPercentSharesOut': 0.0056, 
 'fundFamily': None, 
 'lastFiscalYearEnd': 1601078400, 
 'heldPercentInstitutions': 0.59114, 
 'netIncomeToCommon': 86801997824, 
 'trailingEps': 5.108, 
 'lastDividendValue': None, 
 'SandP52WeekChange': 0.3180796, 
 'priceToBook': 38.928387, 
 'heldPercentInsiders': 0.00071000005, 
 'nextFiscalYearEnd': 1664150400, 
 'yield': None, 
 'mostRecentQuarter': 1624665600, 
 'shortRatio': 1.03, 
 'sharesShortPreviousMonthDate': 1625011200, 
 'floatShares': 16508015578, 
 'beta': 1.202797, 
 'enterpriseValue': 2538442850304, 
 'priceHint': 2, 
 'threeYearAverageReturn': None, 
 'lastSplitDate': None, 
 'lastSplitFactor': None, 
 'legalType': None, 
 'lastDividendDate': None, 
 'morningStarOverallRating': None, 
 'earningsQuarterlyGrowth': 0.932, 
 'priceToSalesTrailing12Months': 7.1957583, 
 'dateShortInterest': 1627603200, 
 'pegRatio': 1.34, 
 'ytdReturn': None, 
 'forwardPE': 26.652555, 
 'lastCapGain': None, 
 'shortPercentOfFloat': 0.0056, 
 'sharesShortPriorMonth': 90213531, 
 'impliedSharesOutstanding': None, 
 'category': None, 
 'fiveYearAverageReturn': None, 
 'previousClose': 149.1, 
 'regularMarketOpen': 148.535, 
 'twoHundredDayAverage': 132.21489, 
 'trailingAnnualDividendYield': 0.005600268, 
 'payoutRatio': 0.16309999, 
 'volume24Hr': None, 
 'regularMarketDayHigh': 151.13, 
 'navPrice': None, 
 'averageDailyVolume10Day': 59605340, 
 'regularMarketPreviousClose': 149.1, 
 'fiftyDayAverage': 144.8403, 
 'trailingAnnualDividendRate': 0.835, 
 'open': 148.535, 
 'toCurrency': None, 
 'averageVolume10days': 59605340,
 'expireDate': None, 
 'algorithm': None, 
 'dividendRate': 0.88, 
 'exDividendDate': 1628208000, 
 'circulatingSupply': None, 
 'startDate': None, 
 'regularMarketDayLow': 146.47, 
 'currency': 'USD', 
 'trailingPE': 29.584965, 
 'regularMarketVolume': 103558782, 
 'lastMarket': None, 
 'maxSupply': None, 
 'openInterest': None, 
 'marketCap': 2498043576320, 
 'volumeAllCurrencies': None, 
 'strikePrice': None, 
 'averageVolume': 77016828, 
 'dayLow': 146.47,
 'ask': 0,
 'askSize': 1800, 
 'volume': 103558782, 
 'fiftyTwoWeekHigh': 151.13, 
 'fromCurrency': None, 
 'fiveYearAvgDividendYield': 1.29, 
 'fiftyTwoWeekLow': 103.1, 
 'bid': 0, 
 'tradeable': False, 
 'dividendYield': 0.0058999998, 
 'bidSize': 3100, 
 'dayHigh': 151.13, 
 'regularMarketPrice': 151.12,
 'logo_url': 'https://logo.clearbit.com/apple.com'}
 
 
 
 
 {'exchange': 'NMS', 
 'shortName': 'Invesco QQQ Trust, Series 1', 
 'longName': 'Invesco QQQ Trust', 
 'exchangeTimezoneName': 'America/New_York', 
 'exchangeTimezoneShortName': 'EDT', 
 'isEsgPopulated': False, 
 'gmtOffSetMilliseconds': '-14400000', 
 'quoteType': 'ETF', 
 'symbol': 'QQQ', 
 'messageBoardId': 'finmb_8108558', 
 'market': 'us_market', 
 'annualHoldingsTurnover': None, 
 'enterpriseToRevenue': None, 
 'beta3Year': 1.02, 
 'profitMargins': None, 
 'enterpriseToEbitda': None, 
 'fiftyTwoWeekChange': None, 
 'morningStarRiskRating': None, 
 'forwardEps': None, 
 'revenueQuarterlyGrowth': None, 
 'fundInceptionDate': 921024000, 
 'annualReportExpenseRatio': None, 
 'totalAssets': 174510718976, 
 'bookValue': None, 
 'fundFamily': 'Invesco', 
 'lastFiscalYearEnd': None, 
 'netIncomeToCommon': None, 
 'trailingEps': None, 
 'lastDividendValue': None, 
 'SandP52WeekChange': None, 
 'priceToBook': None, 
 'nextFiscalYearEnd': None, 
 'yield': 0.0049, 
 'mostRecentQuarter': None, 
 'enterpriseValue': None, 
 'priceHint': 2, 
 'threeYearAverageReturn': 0.2789,
 'lastSplitDate': None, 
 'lastSplitFactor': None, 
 'legalType': 'Exchange Traded Fund', 
 'lastDividendDate': None, 
 'morningStarOverallRating': None, 
 'earningsQuarterlyGrowth': None, 
 'priceToSalesTrailing12Months': None, 
 'pegRatio': None, 
 'ytdReturn': None, 
 'forwardPE': None, 
 'maxAge': 1, 
 'lastCapGain': None, 
 'category': 'Large Growth', 
 'fiveYearAverageReturn': 0.268, 
 'phone': '800-983-0903', 
 'longBusinessSummary': 'The investment seeks investment results that generally correspond to the price and yield 
 performance of the NASDAQ-100 IndexÂ®.\n To maintain the correspondence between the composition and weights of the
 securities in the trust (the "securities") and the stocks in the NASDAQ-100 IndexÂ®, the adviser adjusts the 
  securities from time to time to conform to periodic changes in the identity and/or relative weights of index 
  securities. The composition and weighting of the securities portion of a portfolio deposit are also adjusted to 
  conform to changes in the index.', 
  'companyOfficers': [], 
  'previousClose': 362.21, 
  'regularMarketOpen': 360.22, 
  'twoHundredDayAverage': 338.27438, 
  'trailingAnnualDividendYield': 0.004500152, 
  'payoutRatio': None, 
  'volume24Hr': None, 
  'regularMarketDayHigh': 365.675, 
  'navPrice': 362.14, 
  'averageDailyVolume10Day': 32337800, 
  'regularMarketPreviousClose': 362.21, 
  'fiftyDayAverage': 363.51657, 
  'trailingAnnualDividendRate': 1.63, 
  'open': 360.22, 
  'toCurrency': None, 
  'averageVolume10days': 32337800, 
  'expireDate': None, 
  'algorithm': None, 
  'dividendRate': None, 
  'exDividendDate': None, 
  'beta': None, 
  'circulatingSupply': None, 
  'startDate': None, 
  'regularMarketDayLow': 359.96, 
  'currency': 'USD', 
  'trailingPE': 4.2806168, 
  'regularMarketVolume': 37377581, 
  'lastMarket': None, 
  'maxSupply': None, 
  'openInterest': None, 
  'marketCap': None, 
  'volumeAllCurrencies': None, 
  'strikePrice': None, 
  'averageVolume': 35635681, 
  'dayLow': 359.96, 
  'ask': 364.45, 
  'askSize': 1200, 
  'volume': 37377581, 
  'fiftyTwoWeekHigh': 369.91, 
  'fromCurrency': None, 
  'fiveYearAvgDividendYield': None, 
  'fiftyTwoWeekLow': 260.11, 
  'bid': 364.44, 
  'tradeable': False, 
  'dividendYield': None, 
  'bidSize': 1300, 
  'dayHigh': 365.675, 
  'regularMarketPrice': 364.67, 
  'logo_url': ''
  }
 
 
'''

'''

Balance Sheet Create Table 

CREATE TABLE IF NOT EXISTS "stock_balance_sheet" (
"id" INTEGER PRIMARY KEY, 
"stock_id" INTEGER,
"Intangible Assets" REAL,
"Capital Surplus" REAL,
"Total Liab" REAL,
"Total Stockholder Equity" REAL,
"Other Current Liab" REAL,
"Total Assets" REAL,
"Common Stock" REAL,
"Other Current Assets" REAL,
"Retained Earnings" REAL,
"Other Liab" REAL,
"Good Will" REAL,
"Treasury Stock" REAL,
"Other Assets" REAL,
"Cash" REAL,
"Total Curent Liabilities" REAL,
"Deferred Long Term Asset Charges" REAL,
"Short Long Term Debt" REAL,
"Other Stockholder Equity" REAL,
"Property Plant Equipment" REAL,
"Total Current Assets" REAL,
"Long Term Investments" REAL,
"Net Tangible Assets" REAL,
"Short Term Investments" REAL,
"Net Recievables" REAL,
"Long Term Debt" REAL,
"date" TIMESTAMP,
);



'''
