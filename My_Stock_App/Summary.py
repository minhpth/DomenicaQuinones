# -*- coding: utf-8 -*-
"""
Created on Thu Oct 13 17:59:42 2022

@author: mquinones
"""

##################### Individual Assignment - My Stock App ####################

#==============================================================================
# Import libraries
#==============================================================================
import streamlit as st
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from PIL import Image
import plotly.graph_objects as go
from plotly.subplots import make_subplots
#==============================================================================
# Tab 1: Summary
#==============================================================================
# - Collect and present the information of the stock similar to the tab Yahoo 
#   Finance > Summary [4].
# - In the chart, there should be an option to select different duration of time 
#   i.e. 1M, 3M, 6M, YTD, 1Y, 3Y, 5Y, MAX. It is not necessary to go below 
#   1 month (1M) of duration. For simplicity, the time intervals should be 
#   fixed at 1 Day.
# - Present also the company profile, description and major shareholders.
#==============================================================================

# Layout -----

st.set_page_config(layout="wide")

# Title -----

st.title("Stock App")
st.write("Source: Yahoo Finance (https://finance.yahoo.com/)")

# Selection box: Tickers -----

## List of stock tickers from S&P500
ticker_list = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]['Symbol']

global tickers
tickers = st.sidebar.selectbox("Select a ticker", ticker_list, index=45)

# Select date time: periods -----

## Get the list periods
period_list = ['1d','5d','1mo','3mo','6mo','1y','2y','5y','10y']

global period
period = st.sidebar.selectbox("Period", period_list, index=2)

# Button -----

get = st.sidebar.button("Get data", key="get")

# Functions for tables, charts, description and holders ----- 

@st.cache
def CompanyInfo(tickers):
    return yf.Ticker(tickers).info
    global get
    
if tickers != '':
    
    info = CompanyInfo(tickers)
    
    keys1 = ['previousClose', 'open', 'bid', 'ask','dayLow','dayHigh',
            'fiftyTwoWeekLow', 'fiftyTwoWeekHigh', 'volume', 'averageVolume']
    
    keys2 = ['marketCap','beta', 'trailingPE', 'trailingEps', 
            'dividendYield','exDividendDate', 'targetMeanPrice',
            'ebitdaMargins','profitMargins','grossMargins']
    
    company_stats1 = {}  # Dictionary
    for key in keys1:
        company_stats1.update({key:info[key]})
    company_stats1 = pd.DataFrame({'Value':pd.Series(company_stats1)})
    #st.dataframe(company_stats1)
    
    company_stats2 = {}  # Dictionary
    for key in keys2:
        company_stats2.update({key:info[key]})
    company_stats2 = pd.DataFrame({'Value':pd.Series(company_stats2)})
    #st.dataframe(company_stats2)
     
@st.cache
def StockData(tickers, period):
    stock_price = pd.DataFrame()
    for tick in tickers:
        stock_df = yf.Ticker(tick).history(period=period)
        stock_df['Ticker'] = tick  # Add the column ticker name
        stock_price = pd.concat([stock_price, stock_df], axis=0)  # Comebine results
    return stock_price.loc[:, ['Ticker', 'Open', 'High', 'Low', 'Close', 'Volume']]

# Add a check box
#show_data = st.checkbox("Show data table")

if tickers != '':
    stock_price = StockData([tickers], period)
    #if show_data:
    #    st.write('Stock price data')
    #    st.dataframe(stock_price)
    
# Add a line plot
if tickers != '':
    #st.write('Close price')
    for tick in [tickers]:
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(go.Scatter(x=stock_price.index,
                                 y=stock_price['Close'],
                                 name='Price', fill='tozeroy'))
        fig.update_layout(title = {'text': 'Close price chart', 'x': 0},
                          autosize = False,
                          width=700,
                          height=400,
                          margin=dict(l=50,r=10,b=50,t=50,pad=4))

# Formats -----
major_shareholders = yf.Ticker(tickers).major_holders.rename(columns={0: '', 1:' '})
major_shareholders.set_index('', inplace=True)

institutional_shareholder = yf.Ticker(tickers).institutional_holders.rename(columns={0: '', 1:' '})
#institutional_shareholder.set_index('', inplace=True)

mutualfund_shareholders = yf.Ticker(tickers).mutualfund_holders.rename(columns={0: '', 1:' '})
#mutualfund_shareholders.set_index('', inplace=True)

# Show -----

c1, c2, c3 = st.columns((1, 1, 2))

col1, col2, col3 = st.columns((4,1,3))

column1, column2 = st.columns(2)

if get:
    c1.dataframe(company_stats1.style.format(formatter='{:,.1f}'))
    c2.dataframe(company_stats2.style.format(formatter='{:,.2f}'))
    c3.plotly_chart(fig, use_container_width=True)
    col1.write('**Business Summary**')
    col1.write(info['longBusinessSummary'])
    col2.write('          ')
    col3.image(info['logo_url'])
    col3.write('**Major Holders**')
    col3.dataframe(major_shareholders)
    column1.write('**Institutional Holders**')
    column1.dataframe(institutional_shareholder)
    column2.write('**Mutual Holders**')
    column2.dataframe(mutualfund_shareholders)
 

# Sources:
# https://plotly.com/python-api-reference/generated/plotly.graph_objects.Scatter.html
# https://medium.com/analytics-vidhya/exploring-stock-data-with-a-yahoo-finance-python-module-319c6b3815ae
# Information and code provided on classes of Financial Programming - MBD 

##################################### End #####################################