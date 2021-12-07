Simple S&P500 Screener
---
***

## Application Purpose

***
Utilizing Python, yFinance, TA-LIB, and Plotly Dash this is a simple multi-page stock screener that allows you select a
candlestick pattern of interest, and see the stocks matching that pattern in the database.

After finding the stock of interest, you can then dive into the fundamentals and a very basic look at some Technical
Analysis.

## Motivation

***
To find stocks on the S&P500 that match a desired pattern, and see if there is an investment opportunity. I built this
to strip out all the various things in a screener that are not relevant to my investment level and skillset. This is not
intended to be a tool to be used for actual investments, but to learn how to identify trends and start to get an
understanding of financial datasets pertaining to the stock market.

## Lessons Learned

***

1. Candlestick Analysis using Python and TA-Lib
2. Multi-Page Plotly Dash
    1. Homepage
    2. Fundamental Analysis
    3. Technical Analysis
    4. #### Planned Pages
        1. Options Page - Currently at the bottom of both Technical and Fundamentals Pages
        2. Stock vs Top N Stocks in

4. Calling API Service
    1. yFinance - option to use Pandareader
5. Database Development
    1. SQLite - option to use SQLAlchemy
6. Interactive Data Visualization

## Features

***

* Search Candlestick Patterns to identify potential investment opportunities.
* Fundamental Analysis comparing Stock to Industry
* Technical Analysis
    * Bollinger Bands
    * Moving Averages
        * 50MA
        * 72MA
        * 200MA
    * On Balance Volume
    * Average True Range
    * Moving Average Convergance - Divergance

### Planned Features/Enhancements

***

* Better UI/UX flow
* Top ROI by Sector and/or Stock
* Machine Learning
* Pulling in RSS Feeds/insider trading information
* Job Scheduling for Daily Updates
* Possible Hosting on Heroku 



