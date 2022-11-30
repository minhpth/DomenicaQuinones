# -*- coding: utf-8 -*-
"""
Created on Mon Nov 28 13:39:35 2022

@author: mquinones
"""

###############################################################################
##                          Individual Assignment                            ##
###############################################################################

#==============================================================================
# Import libraries
#==============================================================================

import streamlit as st
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import pandas_datareader.data as web
import datetime as dt
import numpy as np
from datetime import datetime, timedelta
from PIL import Image
import plotly.graph_objects as go
from plotly.subplots import make_subplots

#==============================================================================
# Tab 2: Financials
#==============================================================================
# Collect and present the stock price similar to the tab Yahoo Finance>Chart. 
# The chart should be able to:
# - Select the date range for showing the stock price.
# - Show the stock price for different duration of time i.e. 1M, 3M, 6M, YTD, 
#   1Y, 3Y, 5Y, MAX. It is not necessary to go below 1 month (1M) of duration.
# - Switch between different time intervals i.e. Day, Month, Year. 
#   It is not necessary to go below 1 Day time interval.
# - Switch between line plot and candle plot for the stock price.
# - Show the trading volume at the bottom of the chart.
# - Show the simple moving average (MA) for the stock price using a 
#window size of 50 days.

#==============================================================================

# Layout -----

st.set_page_config(layout="wide")

# Title -----

st.title("Stock Prices Chart")
st.write("Source: Yahoo Finance (https://finance.yahoo.com/)")

# Selection boxes -----

## Tickers
ticker_list = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]['Symbol']

global ticker
ticker = st.sidebar.selectbox("Select a ticker", ticker_list, index = 45)

## Start and End date
global start_date, end_date
col1, col2 = st.sidebar.columns(2)  # Create 2 columns
start_date = col1.date_input("Start date", datetime.today().date() - timedelta(days=360))
end_date = col2.date_input("End date", datetime.today().date())

## Period
period_list = ['1d','5d','1mo','3mo','6mo','1y','2y','5y','10y','ytd','max']

global period
period = st.sidebar.selectbox("Period", period_list, index = 5)

## Intervals
interval_list = ['1d','5d','1wk','1mo','3mo']

global interval
interval = st.sidebar.selectbox("Interval", interval_list)

## Type of chart
chart_list = ['Candle','Line']

global stock_chart
stock_chart = st.sidebar.selectbox("Chart type", chart_list)

# Button -----

get = st.sidebar.button("Get data", key="get")

# Download info -----

stock_price = yf.download(ticker, 
                          period = period, 
                          interval = interval, 
                          start = start_date,
                          end = end_date)

# Plots -----

stock_price['diff'] = stock_price['Close'] - stock_price['Open']
stock_price.loc[stock_price['diff']>=0, 'color'] = 'green'
stock_price.loc[stock_price['diff']<0, 'color'] = 'red'

## Candle Stick Plot -----

fig_candle,ax = plt.subplots() 
fig_candle = make_subplots(specs=[[{"secondary_y": True}]])
fig_candle.add_trace(go.Candlestick(x=stock_price.index,
                              open=stock_price['Open'],
                              high=stock_price['High'],
                              low=stock_price['Low'],
                              close=stock_price['Close'],
                              name='Price'))
fig_candle.add_trace(go.Scatter(x=stock_price.index, 
                            y=stock_price['Close'].rolling(window=50).mean(), 
                            marker_color='skyblue', name='MA 50 days'))
fig_candle.add_trace(go.Bar(x=stock_price.index,
                        y=stock_price['Volume'], 
                        name='Volume', 
                        marker={'color':stock_price['color']}),secondary_y=True)
fig_candle.update_layout(xaxis_rangeslider_visible=False,
                         autosize = False,
                         width=1000,
                         height=500,
                         margin=dict(l=50,r=10,b=50,t=50,pad=4))  # hide rangeslider below the Candlestick Chart
#fig_candle.update_layout(title={'text': 'Stock Price Chart', 'x': 0.5})
#fig.update_yaxes(range=[0,5000])
fig_candle.update_yaxes(range=[0,5e9],secondary_y=True)
fig_candle.update_yaxes(visible=False, secondary_y=True)
# fig_candle.show()
  
# Line Plot -----

fig_line = make_subplots(specs=[[{"secondary_y": True}]])
fig_line.add_trace(go.Scatter(x=stock_price.index, 
                            y=stock_price['Close'].rolling(window=50).mean(), 
                            marker_color='skyblue', name='MA 50 days'))
fig_line.add_trace(go.Scatter(x=stock_price.index,
                          y=stock_price['Close'],
                          marker_color='blue',
                          name='Price'),secondary_y=False)
fig_line.add_trace(go.Bar(x=stock_price.index,
                      y=stock_price['Volume'],
                      name='Volume',
                      marker={'color':stock_price['color']}),secondary_y=True)
#fig_line.update_yaxes(range=[0,5000])  # scale up the price
fig_line.update_yaxes(range=[0,5e9],secondary_y=True)  # scale down the volume
fig_line.update_yaxes(visible=False, secondary_y=True)
fig_line.update_layout(autosize = False,
                         width=1000,
                         height=500,
                         margin=dict(l=50,r=10,b=50,t=50,pad=4))
#fig2.update_layout(title={'text': 'Stock Price Chart', 'x': 0.5})

# Show charts

if get:
    if 'Candle' in stock_chart: # If user selects Candle  do next
        st.plotly_chart(fig_candle, use_container_width=True)
    else:
        st.plotly_chart(fig_line, use_container_width=True)
        
# Resources:
# Plots
# https://wire.insiderfinance.io/how-to-get-stock-price-data-and-draw-charts-like-yahoo-finance-3beeec7b3f4f

###############################################################################
##                                   End                                     ##
###############################################################################