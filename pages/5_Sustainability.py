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
#==============================================================================
# Tab 5: Sustainability
#==============================================================================
# You are free to design this tab with any financial analyses or additional 
# information that you are interested in (e.g., news, financial metrics, stocks
# comparison, etc.). You may find some inspirations from: 
# https://stockanalysis.com/stocks/aapl
#==============================================================================

# Layout -----

st.set_page_config(layout="wide")

# Title -----

st.title("ESG Ratings")
st.write("Source: Yahoo Finance (https://finance.yahoo.com/), FTSE Russell (https://www.ftserussell.com/)")

# Get the list of stock tickers from S&P500
ticker_list = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]['Symbol']

# Selection box -----

global ticker
ticker = st.sidebar.selectbox("Select a ticker", ticker_list, index = 45)

st.markdown('''The ESG rating shows the level of risk exposure a 
            company has on Environment :leaves:  , Society :family:  and Government :office:  .
            Issues such as sustainability and energy efficiency will have
            financial implications that should be analyzed into investment decisions.''')
st.markdown('''*The ESG Rating scores are on a scale of 0 - 100. 
            Lower scores mean less unmanaged ESG Risk.''')
col1, col2 = st.columns((1,2))
#col1.metric("Total Score", ((yf.Ticker(ticker).sustainability).T)['totalEsg'])
col1.metric("Social Score", ((yf.Ticker(ticker).sustainability).T)['socialScore'])
col1.metric("Environment Score", ((yf.Ticker(ticker).sustainability).T)['environmentScore'])
col1.metric("Governance Score", ((yf.Ticker(ticker).sustainability).T)['governanceScore'])

#rating = ['AAA','AA','A','BBB','BB','B','CCC']
#score = ['100','[86-100)','[72-86)','[57-72)','[43-57)',
#         '[29-43)','[0-29)']

#list_of_lists = list(zip(rating, score))
#ESGperformance = pd.DataFrame(list_of_lists,
#                  columns=['Rating', 'Score'])
#st.dataframe(ESGperformance)

col2.image("https://content.ftserussell.com/sites/default/files/inline-images/FR_ESG_Wheel_2018_Eng.jpg",
         width = 300) 

# References:
# ESG Ratings
# https://finance.yahoo.com/news/guide-understanding-esg-ratings-151501443.html
# https://esgrisk.ai/esg-india/esg-ratings-for-india/
# https://www.ftserussell.com/data/sustainability-and-esg-data/esg-ratings
# https://earlymetrics.com/esg-ratings-how-can-a-business-environmental-and-social-impact-be-measured/
# Image Format
# https://docs.streamlit.io/library/api-reference/media/st.image
    
##################################### End #####################################