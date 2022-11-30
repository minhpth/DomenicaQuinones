# -*- coding: utf-8 -*-
"""
Created on Thu Nov 24 16:51:04 2022

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
# Tab 3: Financials
#==============================================================================
# - Collect and present the financial information of the stock similar to the tab 
#   Yahoo Finance > Financials [5].
# - There should be an option to select between Income Statement, Balance 
#   Sheet and Cash Flow.
# - There should be an option to select between Annual and Quarterly period.
#==============================================================================
# Layout -----

st.set_page_config(layout="wide")

# Title -----

st.title("Financial Statements")
st.write("Source: Yahoo Finance (https://finance.yahoo.com/)")

# Selection box: Tickers -----

ticker_list = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]['Symbol']

global ticker
ticker = st.sidebar.selectbox("Select a ticker", ticker_list, index=45)

# Tabs -----

tab1, tab2, tab3 = st.tabs(["Income Statement", "Balance Sheet", "Cash Flow"])

# Income Statement

with tab1:
   
    tabA, tabB = st.tabs(["Annual", "Quarter"])
    
    with tabA:
        
        income_statement_a = yf.Ticker(ticker).financials
        income_statement_a = income_statement_a.rename(lambda t: t.strftime('%Y-%m-%d'),axis='columns')
        income_statement_a = income_statement_a.astype(float).apply(np.floor)
        st.dataframe(income_statement_a.style.format(formatter='{:,.0f}'))
           
    with tabB:
            
       income_statement_q = yf.Ticker(ticker).quarterly_financials
       income_statement_q= income_statement_q.rename(lambda t: t.strftime('%Y-%m-%d'),axis='columns')
       income_statement_q = income_statement_q.astype(float).apply(np.floor)
       st.dataframe(income_statement_q.style.format(formatter='{:,.0f}'))
          
# Balance Sheet
   
with tab2:
   
    tabA, tabB = st.tabs(["Annual", "Quarter"])
    
    with tabA:
       
       balance_sheet_a = yf.Ticker(ticker).balance_sheet
       balance_sheet_a = balance_sheet_a.rename(lambda t: t.strftime('%Y-%m-%d'),axis='columns')
       balance_sheet_a = balance_sheet_a.astype(float).apply(np.floor)
       st.dataframe(balance_sheet_a.style.format(formatter='{:,.0f}'))
           
    with tabB:
       
       balance_sheet_q = yf.Ticker(ticker).quarterly_balance_sheet
       balance_sheet_q = balance_sheet_q.rename(lambda t: t.strftime('%Y-%m-%d'),axis='columns')
       balance_sheet_q = balance_sheet_q.astype(float).apply(np.floor)
       st.dataframe(balance_sheet_q.style.format(formatter='{:,.0f}'))
   

# Cash Flow

with tab3:
   
    tabA, tabB = st.tabs(["Annual", "Quarter"])
    
    with tabA:
       
       cash_flow_a = yf.Ticker(ticker).cashflow
       cash_flow_a = cash_flow_a.rename(lambda t: t.strftime('%Y-%m-%d'),axis='columns')
       cash_flow_a = cash_flow_a.astype(float).apply(np.floor)
       st.dataframe(cash_flow_a.style.format(formatter='{:,.0f}'))
           
    with tabB:
       
       cash_flow_q = yf.Ticker(ticker).quarterly_cashflow
       cash_flow_q = cash_flow_q.rename(lambda t: t.strftime('%Y-%m-%d'),axis='columns')
       cash_flow_q = cash_flow_q.astype(float).apply(np.floor)
       st.dataframe(cash_flow_q.style.format(formatter='{:,.0f}'))

# References
# Methods for financial statements 
# https://pypi.org/project/yfinance/
# Formats
# https://stackoverflow.com/questions/28665361/change-column-names-in-python-pandas-from-datetime-objects-to-strings

##################################### End #####################################