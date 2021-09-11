from statsmodels.tsa.stattools import adfuller
import streamlit as st

def get_freq(interval):
    interval_options = ('1m','2m','5m','15m','30m','60m','90m', '1d','5d','1wk','1mo','3mo')
    if interval == interval_options[0]:
        return '60S'
    elif interval == interval_options[1]:
        return '120S'
    elif interval == interval_options[2]:
        return '{}S'.format(str(5*60))
    elif interval == interval_options[3]:
        return '{}S'.format(str(15*60))
    elif interval == interval_options[4]:
        return '{}S'.format(str(30*60))
    elif interval == interval_options[5]:
        return '{}S'.format(str(60*60))
    elif interval == interval_options[6]:
        return '{}S'.format(str(90*60))
    elif interval == interval_options[7]:
        return 'D'
    elif interval == interval_options[8]:
        return '5D'
    elif interval == interval_options[9]:
        return '7D'
    elif interval == interval_options[10]:
        return 'M'
    else:
        return '3M'

def check_adfuller(data):
    result = adfuller(data)
    st.write('1. ADF Statistic: {} \n 2. P-value: {} \n 3. Number of Lags: {} \n 4. Number of Observation Used: {} \n 5. Critical Values: '.format
    (result[0],result[1],result[2],result[3],result[4]))
    for key, value in result[4].items():
        st.write('\t \t %s: %.3f' % (key, value))
