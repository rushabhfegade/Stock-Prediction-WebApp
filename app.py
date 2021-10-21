# Import Libraries
import pandas as pd
import numpy as np
from datetime import date
import warnings
import streamlit as st
import yfinance as yf

# Importing Self-made Libraries
import plot_data as plt_data
from Stock_Analysis import Stock_Analysis
from Stock_Prediction import Stock_Prediction

# Suppressing the warnings
warnings.filterwarnings('ignore')
reindexing = True

# Title of the Web App
st.title('Stock Prediction Web Application')

# Take Ticker Symbol input from User  
ticker_symbol = st.sidebar.text_input('Input the Ticker Symbol for the Stock: ', max_chars=5).upper()
if not ticker_symbol:
    st.sidebar.warning('Please input a Ticker Symbol.')
    st.stop()

# Create Yahoo finance Ticker object
ticker = yf.Ticker(ticker_symbol)
info = ticker.info
company_name = info['longName']

# Sub-header of the Web App
st.subheader('''{} Stock Information and it's Forecasting'''.format(company_name))

# Take User input regarding retriving stock in a periodic form or from a particular time period
stock_options = ('Using Periods', 'Using Start and End Date with an interval')
selected_stock_options = st.sidebar.selectbox('How to you want to observe the Stock prices data?', stock_options)

# Take User input on information required by the selected way of retriving the stock
if selected_stock_options == stock_options[1]:
    start_date = st.sidebar.date_input('Input the Start date from where you want to observe the Stock prices'
                                , min_value=date(1800, 1, 1), max_value=date.today())
    end_date = st.sidebar.date_input('Input the End date until when you want to observe the Stock prices'
                                , max_value=date.today())
    interval_options = ('1d','5d','1wk','1mo','3mo')
    interval = st.sidebar.selectbox('''Select the desired interval between the Start and the End Date selected before:'''
                                    , interval_options, index=0, help='Intraday data cannot extend last 60 days')

    if (end_date - start_date).days < 30:
        st.sidebar.warning("Please select Time Duration > 29 days.")
        st.stop()
    
    data = ticker.history(start=start_date, end=end_date, interval=interval)

else:
    period_options = ('1mo','3mo','6mo','1y','2y','3y','4y','5y','10y','ytd','max')
    period = st.sidebar.selectbox('''Select the period for which you want to observe the Stock prices: 
                                    ''', period_options, index=3)
    interval_options = ('1d','5d','1wk','1mo','3mo')
    interval = st.sidebar.selectbox('''Select the desired interval between the selected period:'''
                                    , interval_options, index=0, help='Intraday data cannot extend last 60 days')
    data = ticker.history(period=period, interval=interval)

# Display the plot of the Stock and it's Raw Data
with st.expander("{} Stock Information".format(company_name)):
    
    plt_data.plot_rawdata(data, f"{company_name} Stock Prices")
    plt_data.plotly_candlestick(data, stock=f"{ticker_symbol} Stock Prices", title=f"Candlestick Chart of {company_name} Stock Prices")

    with st.form(f"Select {company_name} Information to be Retrived"):
        info_options = ['Profile', 'Fundamental Information', 'General Stock Information', 'Market Information', 'Stock Prices Raw Data']
        info_selected = st.multiselect('Select required Information to be retrived',
                                        options=info_options)
        col1, col2 = st.columns(2)                                
        with col1:
            submitted = st.form_submit_button("Retrieve selected Information")
        with col2:
            empty = st.empty()
    
    if submitted:
        with st.spinner(f"Retrieving {company_name} Information"): 
            if info_options[0] in info_selected:
                st.subheader(info['longName']) 
                st.markdown('** Sector **: ' + info['sector'])
                st.markdown('** Industry **: ' + info['industry'])
                st.markdown('** Phone **: ' + info['phone'])
                st.markdown('** Address **: ' + info['address1'] + ', ' + info['city'] + ', ' + info['zip'] + ', '  +  info['country'])
                st.markdown('** Website **: ' + info['website'])
                st.markdown('** Business Summary **')
                st.info(info['longBusinessSummary'])

            if info_options[1] in info_selected:
                fundInfo = {
                'Enterprise Value (USD)': info['enterpriseValue'],
                'Enterprise To Revenue Ratio': info['enterpriseToRevenue'],
                'Enterprise To Ebitda Ratio': info['enterpriseToEbitda'],
                'Net Income (USD)': info['netIncomeToCommon'],
                'Profit Margin Ratio': info['profitMargins'],
                'Forward PE Ratio': info['forwardPE'],
                'PEG Ratio': info['pegRatio'],
                'Price to Book Ratio': info['priceToBook'],
                'Forward EPS (USD)': info['forwardEps'],
                'Beta ': info['beta'],
                'Book Value (USD)': info['bookValue'],
                'Dividend Rate (%)': info['dividendRate'], 
                'Dividend Yield (%)': info['dividendYield'],
                'Five year Avg Dividend Yield (%)': info['fiveYearAvgDividendYield'],
                'Payout Ratio': info['payoutRatio']
                }
        
                fundDF = pd.DataFrame.from_dict(fundInfo, orient='index')
                fundDF = fundDF.rename(columns={0: 'Value'})
                st.subheader(f'{company_name} Fundamental Information') 
                st.table(fundDF)

            if info_options[2] in info_selected:
                st.subheader(f'{company_name} General Stock Information')
                st.markdown('** Market **: ' + info['market'])
                st.markdown('** Exchange **: ' + info['exchange'])
                st.markdown('** Quote Type **: ' + info['quoteType'])

            if info_options[3] in info_selected:
                marketInfo = {
                "Volume": info['volume'],
                "Average Volume": info['averageVolume'],
                "Market Cap": info["marketCap"],
                "Float Shares": info['floatShares'],
                "Regular Market Price (USD)": info['regularMarketPrice'],
                'Bid Size': info['bidSize'],
                'Ask Size': info['askSize'],
                "Share Short": info['sharesShort'],
                'Short Ratio': info['shortRatio'],
                'Share Outstanding': info['sharesOutstanding']
                }

                st.subheader(f'{company_name} Market Information')
                marketDF = pd.DataFrame(data=marketInfo, index=[0])
                st.table(marketDF.transpose().rename(columns={0: 'Value'}))

            if info_options[4] in info_selected:
                st.subheader(f"{company_name} Stock Prices Raw Data: ")
                st.write("The Size of the Raw Dataset is: ",data.shape)
                st.dataframe(data)
        empty.success(f"{company_name} Information Retrieved")

task_options = ('', f'{ticker_symbol} Stock Analysis', f'{ticker_symbol} Stock Prediction')
task = st.sidebar.selectbox('''Select what needs to done with the {} Stock Data'''.format(ticker_symbol), options=task_options, index=0)

if task == '':
    st.sidebar.warning('Please select the task to be performed.')
    st.stop()

if task == task_options[1]:
    st.subheader(f"{company_name} Stock Analysis")
    sa = Stock_Analysis(data, ticker_symbol, company_name)
    sa.Display_Stock_Analysis()

else:
    algo = ('', 'AR', 'MA', 'ARMA', 'ARIMA', 'ARCH', 'GARCH', 'Linear Regression', 'Facebook Prophet', 'LTSM', 'Transfomer')
    selected_algo = st.sidebar.selectbox('Select the Time Series Algorithm to predict the stock prices', algo, index=0)

    sp = Stock_Prediction(data, ticker_symbol, company_name)
    
    if selected_algo == algo[0]:
        st.sidebar.warning('Please select the Algorithm for prediction.')
        st.stop()
    elif selected_algo == algo[1]:
        pass
    elif selected_algo == algo[2]:
        pass
    elif selected_algo == algo[3]:
        pass
    elif selected_algo == algo[4]:
        pass
    elif selected_algo == algo[5]:
        pass
    elif selected_algo == algo[6]:
        pass
    elif selected_algo == algo[7]:
        pass
    elif selected_algo == algo[8]:
        sp.Prophet()
    elif selected_algo == algo[9]:
        pass
    else:
        pass
    