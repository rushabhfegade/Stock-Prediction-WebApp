import streamlit as st
import pandas as pd
import numpy as np
from prophet import Prophet
from prophet.plot import plot_plotly, plot_forecast_component_plotly, plot_components_plotly
from datetime import datetime, timedelta

# Importing Self-made Libraries
from plot_data import plotly_prophet_forecast

class Stock_Prediction:


    def __init__(self, data, ticker_symbol, company_name):
        self.df = data
        self.ticker_symbol = ticker_symbol
        self.company_name = company_name
    
    @st.cache(suppress_st_warning=True)
    def download_model(self, model, file_name):
        import pickle
        import base64
        output_model = pickle.dumps(model)
        b64 = base64.b64encode(output_model).decode()
        href = f'<a href="data:file/output_model;base64,{b64}" download="{file_name}.pkl">Download Trained Model .pkl File</a>'
        st.markdown(href, unsafe_allow_html=True)

    def Prophet(self):

        st.subheader(f"{self.company_name} Stock Forecasting Using Facebook Prophet")

        with st.form(f"Choose the required hyperparameter for the Facebook Prophet Training and Forecasting"):

            col1, col2 = st.columns(2)
            col3, col4 = st.columns(2)
            col5, col6 = st.columns(2)

            with col1:
                stock_options = ['Open', 'Close', 'High', 'Low']
                selected_stock_option = st.selectbox(f"Select {self.ticker_symbol} Stock Options to be Forecasted",
                                                    options=stock_options, index=1)

            with col2:
                horizon = st.number_input("Input number of days to be Forecasted", min_value=1, max_value=None, value=30)

            with col3:
                trend = st.checkbox("Select to Show Trend along Forecasting")

            with col4:
                changepoints = st.checkbox("Select to Show Changepoints along Forecasting")

            with col5:
                submitted = st.form_submit_button("Train the Model and Forecast")
            
            with col6:
                empty = st.empty()
        
        if submitted: 
            with st.spinner("Training the Facebook Prophet Model"):
                fbdata = self.df[[selected_stock_option]].reset_index()
                fbdata.rename(columns={'Date':'ds', selected_stock_option:'y'}, inplace=True)
                fbdata['ds'] = pd.to_datetime(fbdata['ds']).dt.date

                model = Prophet()
                model.fit(fbdata)
                
                forecast = model.predict(model.make_future_dataframe(periods=horizon))
                
            with st.expander(f"{self.company_name} {selected_stock_option} Stock Price Forecast Plot"):
                st.subheader(f"{self.company_name} {selected_stock_option} Stock Price Forecast Plot")
                plotly_prophet_forecast(model, forecast, selected_stock_option, trend, changepoints)

            with st.expander(f"{self.company_name} {selected_stock_option} Stock Price Time Series Components"):
                st.subheader(f"{self.company_name} {selected_stock_option} Stock Price Time Series Components")
                st.plotly_chart(plot_components_plotly(model, forecast),
                            use_container_width=True)
            
            with st.expander(f"{self.company_name} {selected_stock_option} Forecasted Stock Price Data"):
                st.dataframe(forecast[['ds','yhat_lower','yhat','yhat_upper']][forecast['ds'] > datetime.today()].rename({'ds':'Date', 'yhat_lower':'Lower Bound', 'yhat':'Forecast', 'yhat_upper':'Upper Bound'}, axis=1))

            with st.expander(f"{self.company_name} {selected_stock_option} Forecasted Diagnostics"):
                pass

            with st.expander(f"Download {self.company_name} {selected_stock_option} Stock Price Forecasting Model"):
                    
                self.download_model(model, file_name="Facebook Prophet")

            # Printing the successful retrivial of Stock Analysis
            empty.success(f"{self.ticker_symbol} Stock Forecasting Done!")
            