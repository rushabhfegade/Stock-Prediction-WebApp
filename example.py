import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
import streamlit as st
import yfinance as yf
import plotly.express as px
from datetime import date, datetime, timedelta
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf, plot_predict
from statsmodels.tsa.arima_model import ARIMA
from statsmodels.tools.sm_exceptions import ValueWarning, HessianInversionWarning, ConvergenceWarning
from statsmodels.tsa.seasonal import seasonal_decompose
from pmdarima.model_selection import train_test_split
from arch import arch_model
from arch.__future__ import reindexing

# Importing Self-made Libraries
import plot_data as plt_data
import misc as misc
import time

#Suppressing the warnings
warnings.filterwarnings('ignore')
#warnings.filterwarnings('ignore', category = ValueWarning)
#warnings.filterwarnings('ignore', category = HessianInversionWarning)
#warnings.filterwarnings('ignore', category = ConvergenceWarning)
reindexing = True

st.title('Stock Prediction Web Application')

#algo = ('AR', 'MA', 'ARMA', 'ARIMA', 'ARCH', 'GARCH')
#selected_algo = st.sidebar.selectbox('Select the Time Series Algorithm to forecast the stock prices', algo)

ticker_symbol = st.sidebar.text_input('Input the Ticker Symbol for the Stock: ').upper()
if not ticker_symbol:
    st.sidebar.warning('Please input a Ticker Symbol.')
    st.stop()
st.sidebar.success('Thank you for inputting the Ticker Symbol.')

st.subheader('''{} Stock Information and it's Forecasting'''.format(ticker_symbol))

ticker = yf.Ticker(ticker_symbol)

stock_options = ('Using Periods', 'Using Start and End Date with an interval')
selected_stock_options = st.sidebar.selectbox('How to you want to observe the Stock prices data?', stock_options)

if selected_stock_options == stock_options[1]:
    start_date = st.sidebar.date_input('Input the Start date from where you want to observe the Stock prices'
                                , min_value=date(1800, 1, 1), max_value=date.today())
    end_date = st.sidebar.date_input('Input the End date until when you want to observe the Stock prices'
                                , max_value=date.today())
    interval_options = ('1m','2m','5m','15m','30m','60m','90m','1d','5d','1wk','1mo','3mo')
    interval = st.sidebar.selectbox('''Select the desired interval between the Start and the End Date selected before:'''
                                    , interval_options, index=7, help='Intraday data cannot extend last 60 days')
    data = ticker.history(start=start_date, end=end_date, interval=interval)
else:
    period_options = ('1d','5d','1mo','3mo','6mo','1y','2y','5y','10y','ytd','max')
    period = st.sidebar.selectbox('''Select the period for which you want to observe the Stock prices: 
                                    ''', period_options, index=2)
    interval_options = ('1m','2m','5m','15m','30m','60m','90m', '1d','5d','1wk','1mo','3mo')
    interval = st.sidebar.selectbox('''Select the desired interval between the selected period:'''
                                    , interval_options, index=7, help='Intraday data cannot extend last 60 days')
    data = ticker.history(period=period, interval=interval)

with st.beta_expander("{} Stock Information".format(ticker_symbol)):
    plt_data.plot_rawdata(data, "{} Stock Prices".format(ticker_symbol))
    if st.checkbox('Show Raw Data'):
        st.subheader('Raw Dataset: ')
        st.write(data.shape)
        st.dataframe(data)

with st.beta_expander("{} Stock Price Selection to be Forecasted".format(ticker_symbol)):
    prices_options = tuple(data.keys()[0:4])
    prices_var = st.selectbox('''Select the option which is needed to be forecasted: ''', prices_options, index=3)
    prices = data[[prices_var]]

    # Data Pre-processing
    prices = prices.asfreq(freq=misc.get_freq(interval)).interpolate(method='time')
    plt_data.plot_1D_data(prices, "{} {} Stock Prices".format(ticker_symbol, prices_var))
    if st.checkbox('Show {} Interpolated Data'.format(prices_var)):
        st.subheader('{} Interpolated Data'.format(prices_var))
        st.write(prices.shape)
        st.dataframe(prices)
     
with st.beta_expander("{} Stock Data Analysis for Selection of Hyperparameter for the Models".format(ticker_symbol)):

    col1, col2 = st.beta_columns(2)
    with col1:
        diff_period = st.slider('Select the Difference element to be compared with current element', 1, 60, 1,
                                help='''Differencing is done to make the Time series Stationary i.e. 
                                to make the mean, standard deviation and autocorrelation constant.''')
        prices_diff = prices.diff(periods=diff_period).dropna()

    with col2:
        misc.check_adfuller(prices_diff)    

    st.subheader("{} {} Difference Plot".format(ticker_symbol, prices_var))
    plt_data.plot_1D_data(prices_diff, "{} {} {}-Difference Plot".format(ticker_symbol, prices_var, diff_period))
    
    st.subheader("{} Autocorrelation and Partial Autocorrelation Plots".format(ticker_symbol))
    lags = st.slider("Select the number of Lags to check ACF and PACF Plot", min_value=2, max_value=60, value=10,
                    help='''Increasing the lags will increase the complexity of the model and hence might overfit the underlying data. \n
                    Note: ACF - Autocorrelation Function and PACF - Partial Autocorrelation Function''')
    st.pyplot(plot_acf(prices_diff, zero = True, lags=lags))
    st.pyplot(plot_pacf(prices_diff, zero = True, lags=lags))

    if period_options.index(period) >= period_options.index('1mo') and interval_options.index(interval) >= interval_options.index('1d'):
        st.subheader("{} Seasonal Decomposition of the Time Series".format(ticker_symbol))
        seasonal_model = st.selectbox("Select the Seasonal Decomposition Model", ('additive','multiplicative'))
        seasonal_result = seasonal_decompose(prices, model=seasonal_model)
        plt_data.plot_seasonal(seasonal_result)

with st.beta_expander("{} Stock Prediction and Forecasting".format(ticker_symbol)):
    
    train_data, test_data = train_test_split(prices, train_size=0.8)
    st.write("The Training Set Size: {}, Test Set Size: {}".format(len(train_data), len(test_data)))

    train_data, test_data = train_data.values, test_data.values

    if st.checkbox("Show Training and Testing Data"):
        col6, col7 = st.beta_columns(2)
        with col6:
            st.write("Training Data")
            st.dataframe(train_data)
        with col7:
            st.write("Testing Data")
            st.dataframe(test_data)

    link = "[Information on ARIMA Model](https://www.investopedia.com/terms/a/autoregressive-integrated-moving-average-arima.asp)"
    st.markdown(link, unsafe_allow_html=True)

    with st.form("Training the ARIMA Model", clear_on_submit=True):
        col3, col4, col5 = st.beta_columns(3)
        with col3:
            AR_p = st.number_input("Input the AR Model Parameter (p):", max_value=60, 
                            help="For reference please use PACF plot to select the desired lag for the parameter value.")
        
        with col4:
            Integral_d = st.number_input("Input the Integral Parameter (d):", max_value=60, 
                            help="For reference please use Difference plot value to select the desired lag for the parameter value.")

        with col5:
            MA_q = st.number_input("Input the MA Model Parameter (q):", max_value=60, 
                            help="For reference please use ACF plot to select the desired lag for the parameter value.")

        submitted = st.form_submit_button("Train the Model and Do the Forecasting")
        empty_place = st.empty()

    if submitted:
        with st.spinner("The Model is being Trained. Please Wait......"):
            history = [x for x in train_data]
            predictions = list()
            # walk-forward validation
            for t in range(len(test_data)):
                model = ARIMA(history, order=(AR_p, Integral_d, MA_q))
                model_fit = model.fit(disp=-1)
                output = model_fit.forecast()
                yhat = output[0]
                predictions.append(yhat)
                obs = test_data[t]
                history.append([obs])

        st.write(model_fit.summary())
        empty_place.success("Training is Done!")




    