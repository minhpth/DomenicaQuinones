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
import pandas_datareader.data as web
import datetime as dt
import numpy as np
from datetime import datetime, timedelta
from PIL import Image
import plotly.graph_objects as go
from plotly.offline import iplot, init_notebook_mode
import seaborn as sns
#==============================================================================
# Tab 4: Monte Carlo simulation
#==============================================================================
# - Conduct and present a Monte Carlo simulation for the stock closing price
#   in the next n-days from today.
# - The number of simulations should be selected from a dropdown list of n = 
#   200, 500, 1000 simulations.
# - The time horizon should be selected from a dropdown list of t = 30, 60, 90
#   days from today.
# - Estimate and present the Value at Risk (VaR) at 95% confidence interval.
#==============================================================================

# Layout -----

st.set_page_config(layout="wide")

# Title -----

st.title("MonteCarlo Simulation")
st.write("Source: Yahoo Finance (https://finance.yahoo.com/)")

# Selection boxes -----

## Tickers 
ticker_list = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]['Symbol']

global ticker
ticker = st.sidebar.selectbox("Select a ticker", ticker_list, index = 45)

## Simulations 
number_simulations = [200,500,1000]

global n_simulations
n_simulations = st.sidebar.selectbox("Number of simulations", number_simulations)

## Time horizon
time_horizon_list = [30,60,90]

global t_horizon
t_horizon = st.sidebar.selectbox("Time horizon in days", time_horizon_list)

## Start and End date

global start_date, end_date
col1, col2 = st.sidebar.columns(2)  # Create 2 columns
start_date = col1.date_input("Start date", datetime.today().date() - timedelta(days=30))
end_date = col2.date_input("End date", datetime.today().date())

# Button -----

get = st.sidebar.button("Get data", key="get")

# Data from Yahoo Finance -----
stock_price = web.DataReader(ticker, 'yahoo', start_date, end_date)

close_price = stock_price['Close']
daily_return = close_price.pct_change()
daily_volatility = np.std(daily_return)
last_price = close_price[-1]

# MonteCarlo preparation -----

# Stock price of 30 days
time_horizon = t_horizon
next_price = []

for n in range(time_horizon):
    
    # Variation around the mean (0) and std (daily_volatility)
    future_return = np.random.normal(0, daily_volatility)
    
    # Future price
    future_price = last_price * (1 + future_return)
    
    next_price.append(future_price)
    last_price = future_price

# Monte Carlo simulation
np.random.seed(123)
simulations = n_simulations
time_horizone = t_horizon

# Run simulation
simulation_df = pd.DataFrame()

for i in range(simulations):
    
    # List for next stock price
    next_price = []
    
    # Next stock price
    last_price = close_price[-1]
    
    for j in range(time_horizone):
        #  Variation around the mean (0) and std (daily_volatility)
        future_return = np.random.normal(0, daily_volatility)

        # Future price
        future_price = last_price * (1 + future_return)

        next_price.append(future_price)
        last_price = future_price
    
    # Result of simulation
    next_price_df = pd.Series(next_price).rename('sim' + str(i))
    simulation_df = pd.concat([simulation_df, next_price_df], axis=1)

# Plot of future price simulations -----
fig, ax = plt.subplots()
fig.set_size_inches(18, 7, forward=True)

plt.plot(simulation_df)
plt.title('' + str(ticker) + ' stock price in next ' + str(t_horizon) + ' days')
plt.xlabel('Days')
plt.ylabel('Price')

plt.axhline(y=close_price[-1], color='black')
plt.legend(['Current stock price is: ' + str(np.round(close_price[-1], 2))])
ax.get_legend().legendHandles[0].set_color('black')

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_visible(False)
ax.spines["bottom"].set_visible(False)

ax.set_facecolor('whitesmoke')

#plt.show()

# Value at Risk preparation ----

# Last price of the nth day
last_price = simulation_df.iloc[-1:, :].values[0, ]

# Price at 95% confidence interval
future_price_95ci = np.percentile(last_price, 5)

# Value at Risk
# Interpretation: 95% of the times, the losses will not be more than X USD
VaR = close_price[-1] - future_price_95ci

# Show the plot when the button is clicked -----

if get:
    st.pyplot(fig)
    st.write('**VaR at 95% confidence interval is: ' + str(np.round(VaR, 2)) + ' USD**')

# References:
# https://www.investopedia.com/terms/t/ttm.asp
# Percentage Change
# https://www.investopedia.com/terms/p/percentage-change.asp
# Volatility
# https://www.investopedia.com/terms/v/volatility.asp
# Chart borders
# https://e2eml.school/matplotlib_framing.html#spinesoff
# Install seaborn
# https://anaconda.org/anaconda/seaborn
# Matplotlib background color
# https://pythonguides.com/matplotlib-change-background-color/
# https://stackoverflow.com/questions/22408237/named-colors-in-matplotlib
# Information and code provided on classes of Financial Programming - MBD 

##################################### End #####################################