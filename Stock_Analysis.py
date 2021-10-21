import ta
import streamlit as st
import pandas as pd
import numpy as np

# Importing Self-made Libraries
from plot_data import plot_1D_data

class Stock_Analysis:

    def __init__(self, data, ticker_symbol, company_name):
        self.df = ta.add_all_ta_features(data, 'Open', 'High', 'Low', 'Close', 'Volume', fillna=True)
        freq = 'D'
        self.df = self.df.asfreq(freq=freq).interpolate(method='time')
        self.df.sort_index(inplace=True)
        self.ticker = ticker_symbol
        self.company_name = company_name

    def Display_Stock_Analysis(self):
        
        with st.form(f"{self.company_name} Stock Analysis Options", clear_on_submit=False):
            trend_options = ['All', 'ADX', 'Aroon', 'CCI', 'DPO', 'EMA', 'Ichimoku', 'KST',
                            'MACD', 'Mass Index', 'PSAR', 'SMA', 'Schaff Trend Cycle', 'Trix', 'Vortex']
            momentum_options = ['All', 'Awesome Oscillator', 'KAMA', 'PPO', 'ROC', 'RSI', 'Stoch RSI',
                                'Stochastic Oscillator', 'TSI', 'Ultimate Oscillator', 'Williams %R']
            volatility_options = ['All', 'ATR', 'Bollinger Bands', 'Donchian Bands', 'Keltner Bands',
                                'Ulcer Index']
            volume_options = ['All', 'ADI', 'CMF', 'EoM', 'Force Index', 'MFI', 'NVI', 'OBV', 'VPT', 'VWAP']
            return_options = ['All', 'Cumulative Return', 'Daily Log Return', 'Daily Return']
            
            col1, col2, col3 = st.columns(3)
            col4, col5 = st.columns(2)
            
            with col1:
                trend = st.multiselect('Select required Trend Indicators for Analysis',
                                        options=trend_options, help='You can unselect this Indicator by selecting Clear all.')
            with col2:
                momentum = st.multiselect('Select required Momentum Indicators for Analysis',
                                        options=momentum_options, help='You can unselect this Indicator by selecting Clear all.')
            with col3:
                volatility = st.multiselect('Select required Volatility Indicators for Analysis',
                                        options=volatility_options, help='You can unselect this Indicator by selecting Clear all.')
            with col4:
                volume = st.multiselect('Select required Volume Indicators for Analysis',
                                        options=volume_options, help='You can unselect this Indicator by selecting Clear all.')
            with col5:
                return_selected = st.multiselect('''Select required Return Indicators for Analysis''',
                                        options=return_options, help='You can unselect this Indicator by selecting Clear all.')

            col6, col7 = st.columns(2)
            with col6:
                submitted = st.form_submit_button("Retrieve selected Stock Analysis Indicators")
            with col7:
                empty = st.empty()

        if not trend and not momentum and not volatility and not volume and not return_selected:
            st.warning('Please select the Indicators for Stock Analysis.')
            st.stop()
        
        if submitted:
            with st.spinner(f"Retrieving {self.ticker} Stock Analysis"):
                # Trend Indicators
                if trend:
                    st.subheader(f'{self.company_name} Stock Trend Indicator')
                    
                    if trend_options[1] in trend or trend_options[0] in trend:
                        with st.expander(f'{self.ticker} Stock Average Directional Movement Index (ADX) Indicator'):
                            plot_1D_data(self.df[['trend_adx', 'trend_adx_pos', 'trend_adx_neg']], 
                                        title=f'{self.ticker} Stock ADX Indicator', 
                                        label={"variable":'ADX Indicator'})

                    if trend_options[2] in trend or trend_options[0] in trend:
                        with st.expander(f'{self.ticker} Stock Aroon Indicator'):
                            plot_1D_data(self.df[['trend_aroon_ind', 'trend_aroon_up', 'trend_aroon_down']],
                                        title=f'{self.ticker} Stock Aroon Indicator',
                                        label={"variable":'Aroon Indicator'})
                    
                    if trend_options[3] in trend or trend_options[0] in trend:
                        with st.expander(f'{self.ticker} Stock Commodity Channel Index (CCI) Indicator'):
                            plot_1D_data(self.df[['trend_cci']],
                                        title=f'{self.ticker} Stock CCI Indicator',
                                        label={"variable":'CII Indicator'})
                    
                    if trend_options[4] in trend or trend_options[0] in trend:
                        with st.expander(f'{self.ticker} Stock Detrended Price Oscillator (DPO) Indicator'):
                            plot_1D_data(self.df[['trend_dpo']],
                                        title=f'{self.ticker} Stock DPO Indicator',
                                        label={"variable":'DPO Indicator'})
                    
                    if trend_options[5] in trend or trend_options[0] in trend:
                        with st.expander(f'{self.ticker} Stock Exponential Moving Average (EMA) Indicator'):
                            plot_1D_data(self.df[['trend_ema_fast', 'trend_ema_slow']],
                                        title=f'{self.ticker} Stock EMA Indicator',
                                        label={"variable":'EMA Indicator'})
                    
                    if trend_options[6] in trend or trend_options[0] in trend:
                        with st.expander(f'{self.ticker} Stock Ichimoku Kinko Hyo (Ichimoku) Indicator'):
                            plot_1D_data(self.df[['trend_ichimoku_a', 'trend_ichimoku_b', 'trend_ichimoku_base', 'trend_ichimoku_conv']],
                                        title=f'{self.ticker} Stock Ichimoku Indicator',
                                        label={"variable":'Ichimoku Indicator'})
                    
                    if trend_options[7] in trend or trend_options[0] in trend:
                        with st.expander(f'{self.ticker} Stock Know Sure Thing (KST) Indicator'):
                            plot_1D_data(self.df[['trend_kst', 'trend_kst_diff', 'trend_kst_sig']],
                                        title=f'{self.ticker} Stock KST Indicator',
                                        label={"variable":'KST Indicator'})
                    
                    if trend_options[8] in trend or trend_options[0] in trend:
                        with st.expander(f'{self.ticker} Stock Moving Average Convergence Divergence (MACD)'):
                            plot_1D_data(self.df[['trend_macd', 'trend_macd_diff', 'trend_macd_signal']],
                                        title=f'{self.ticker} Stock MACD',
                                        label={"variable":'MACD'})

                    if trend_options[9] in trend or trend_options[0] in trend:
                        with st.expander(f'{self.ticker} Stock Mass Index (MI)'):
                            plot_1D_data(self.df[['trend_mass_index']],
                                        title=f'{self.ticker} Stock Max Index (MI)',
                                        label={"variable":'Mass Index'})
                    
                    if trend_options[10] in trend or trend_options[0] in trend:
                        with st.expander(f'{self.ticker} Stock Parabolic Stop and Reverse (PSAR) Indicator'):
                            plot_1D_data(self.df[['trend_psar_down', 'trend_psar_up']],
                                        title=f'{self.ticker} Stock PSAR Indicator',
                                        label={"variable":'PSAR Indicator'})

                    if trend_options[11] in trend or trend_options[0] in trend:
                        with st.expander(f'{self.ticker} Stock Simple Moving Average (SMA) Indicator'):
                            plot_1D_data(self.df[['trend_sma_fast', 'trend_sma_slow']],
                                        title=f'{self.ticker} Stock SMA Indicator',
                                        label={"variable":'SMA Indicator'})

                    if trend_options[12] in trend or trend_options[0] in trend:
                        with st.expander(f'{self.ticker} Stock Schaff Trend Cycle (STC) Indicator'):
                            plot_1D_data(self.df[['trend_stc']],
                                        title=f'{self.ticker} Stock STC Indicator',
                                        label={"variable":'STC Indicator'})

                    if trend_options[13] in trend or trend_options[0] in trend:
                        with st.expander(f'{self.ticker} Stock Trix Indicator'):
                            plot_1D_data(self.df[['trend_trix']],
                                        title=f'{self.ticker} Stock Trix Indicator',
                                        label={"variable":'Trix Indicator'})

                    if trend_options[14] in trend or trend_options[0] in trend:
                        with st.expander(f'{self.ticker} Stock Vortex Indicator (VI)'):
                            plot_1D_data(self.df[['trend_vortex_ind_diff', 'trend_vortex_ind_pos', 'trend_vortex_ind_neg']],
                                        title=f'{self.ticker} Stock Vortex Indicator (VI)',
                                    label={"variable":'Vortex Indicator'})
                    
                # Momentum Indicators
                if momentum:
                    st.subheader(f'{self.company_name} Stock Momentum Indicator')

                    if momentum_options[1] in momentum or momentum_options[0] in momentum:
                        with st.expander(f'{self.ticker} Stock Awesome Oscillator (AO) Indicator'):
                            plot_1D_data(self.df[['momentum_ao']],
                                        title=f'{self.ticker} Stock AO Indicator',
                                        label={"variable":'AO Indicator'})
                    
                    if momentum_options[2] in momentum or momentum_options[0] in momentum:
                        with st.expander(f"{self.ticker} Stock Kaufman's Adaptive Moving Average (KAMA) Indicator"):
                            plot_1D_data(self.df[['momentum_kama']],
                                        title=f'{self.ticker} Stock KAMA Indicator',
                                        label={"variable":'KAMA Indicator'})

                    if momentum_options[3] in momentum or momentum_options[0] in momentum:
                        with st.expander(f"{self.ticker} Stock Percentage Price Oscillator (PPO)"):
                            plot_1D_data(self.df[['momentum_ppo', 'momentum_ppo_hist', 'momentum_ppo_signal']],
                                        title=f'{self.ticker} Stock Percentage Price Oscillator (PPO)',
                                        label={"variable":'PPO'})

                    if momentum_options[4] in momentum or momentum_options[0] in momentum:
                        with st.expander(f"{self.ticker} Stock Rate of Change (ROC) Indicator"):
                            plot_1D_data(self.df[['momentum_roc']],
                                        title=f'{self.ticker} Stock ROC Indicator',
                                        label={"variable":'Rate of Change (ROC)'})

                    if momentum_options[5] in momentum or momentum_options[0] in momentum:
                        with st.expander(f"{self.ticker} Stock Relative Strength Index (RSI) Indicator"):
                            plot_1D_data(self.df[['momentum_rsi']],
                                        title=f'{self.ticker} Stock RSI Indicator',
                                        label={"variable":'RSI Indicator'})
                        
                    if momentum_options[6] in momentum or momentum_options[0] in momentum:
                        with st.expander(f"{self.ticker} Stock Stochastic Relative Strength Index (Stoch RSI) Indicator"):
                            plot_1D_data(self.df[['momentum_stoch_rsi', 'momentum_stoch_rsi_k', 'momentum_stoch_rsi_d']],
                                        title=f'{self.ticker} Stock Stoch RSI Indicator',
                                        label={"variable":'Stoch RSI Indicator'})
                    
                    if momentum_options[7] in momentum or momentum_options[0] in momentum:
                        with st.expander(f"{self.ticker} Stock Stochastic Oscillator"):
                            plot_1D_data(self.df[['momentum_stoch', 'momentum_stoch_signal']],
                                        title=f'{self.ticker} Stock Stochastic Oscillator',
                                        label={"variable":'Stoch Stochastic Oscillator'})

                    if momentum_options[8] in momentum or momentum_options[0] in momentum:
                        with st.expander(f"{self.ticker} Stock True Strength Index (TSI) Indicator"):
                            plot_1D_data(self.df[['momentum_tsi']],
                                        title=f'{self.ticker} Stock TSI Indicator',
                                        label={"variable":'TSI Indicator'})

                    if momentum_options[9] in momentum or momentum_options[0] in momentum:
                        with st.expander(f"{self.ticker} Stock Ultimate Oscillator"):
                            plot_1D_data(self.df[['momentum_uo']],
                                        title=f'{self.ticker} Stock Ultimate Oscillator',
                                        label={"variable":'Ultimate Oscillator'})
                        
                    if momentum_options[10] in momentum or momentum_options[0] in momentum:
                        with st.expander(f"{self.ticker} Stock Williams %R Indicator"):
                            plot_1D_data(self.df[['momentum_wr']],
                                        title=f'{self.ticker} Stock Williams %R Indicator',
                                        label={"variable":'Williams %R Indicator'})
                    
                # Volatility Indicators
                if volatility:
                    st.subheader(f'{self.company_name} Stock Volatility Indicator')

                    if volatility_options[1] in volatility or volatility_options[0] in volatility:
                        with st.expander(f"{self.ticker} Stock Average True Range (ATR)"):
                            plot_1D_data(self.df[['volatility_atr']],
                                        title=f'{self.ticker} Stock Average True Range (ATR)',
                                        label={"variable":'Average True Range (ATR)'})
                        
                    if volatility_options[2] in volatility or volatility_options[0] in volatility:
                        with st.expander(f"{self.ticker} Stock Bollinger Bands"):
                            plot_1D_data(self.df[['volatility_bbm', 'volatility_bbh', 'volatility_bbl']],
                                        title=f'{self.ticker} Stock Bollinger Bands',
                                        label={"variable":'Bollinger Bands'})
                    
                    if volatility_options[3] in volatility or volatility_options[0] in volatility:
                        with st.expander(f"{self.ticker} Stock Donchian Channel"):
                            plot_1D_data(self.df[['volatility_dcl', 'volatility_dch', 'volatility_dcm']],
                                        title=f'{self.ticker} Stock Donchian Channel',
                                        label={"variable":'Donchian Channel'})

                    if volatility_options[4] in volatility or volatility_options[0] in volatility:
                        with st.expander(f"{self.ticker} Stock Keltner Channel"):
                            plot_1D_data(self.df[['volatility_kcc', 'volatility_kch', 'volatility_kcl']],
                                        title=f'{self.ticker} Stock Keltner Channel',
                                        label={"variable":'Keltner Channel'})

                    if volatility_options[5] in volatility or volatility_options[0] in volatility:
                        with st.expander(f"{self.ticker} Stock Ulcer Index"):
                            plot_1D_data(self.df[['volatility_ui']],
                                        title=f'{self.ticker} Stock Ulcer Index',
                                        label={"variable":'Ulcer Index'})
                    
                # Volume Indicators
                if volume:
                    st.subheader(f'{self.company_name} Stock Volume Indicator')

                    if volume_options[1] in volume or volume_options[0] in volume:
                        with st.expander(f"{self.ticker} Stock Accumulation/Distribution Index (ADI) Indicator"):
                            plot_1D_data(self.df[['volume_adi']],
                                        title=f'{self.ticker} Stock ADI Indicator',
                                        label={"variable":'ADI Indicator'})
                    
                    if volume_options[2] in volume or volume_options[0] in volume:
                        with st.expander(f"{self.ticker} Stock Chaikin Money Flow (CMF) Indicator"):
                            plot_1D_data(self.df[['volume_cmf']],
                                        title=f'{self.ticker} Stock CMF Indicator',
                                        label={"variable":'CMF Indicator'})

                    if volume_options[3] in volume or volume_options[0] in volume:
                        with st.expander(f"{self.ticker} Stock Ease of Movement (EoM) Indicator"):
                            plot_1D_data(self.df[['volume_em', 'volume_sma_em']],
                                        title=f'{self.ticker} Stock EoM Indicator',
                                        label={"variable":'EoM Indicator'})

                    if volume_options[4] in volume or volume_options[0] in volume:
                        with st.expander(f"{self.ticker} Stock Force Index (FI) Indicator"):
                            plot_1D_data(self.df[['volume_fi']],
                                        title=f'{self.ticker} Stock Force Index (FI) Indicator',
                                        label={"variable":'Force Index Indicator'})

                    if volume_options[5] in volume or volume_options[0] in volume:
                        with st.expander(f"{self.ticker} Stock Money Flow Index (MFI) Indicator"):
                            plot_1D_data(self.df[['volume_mfi']],
                                        title=f'{self.ticker} Stock Money Flow Index (MFI) Indicator',
                                        label={"variable":'Money Flow Index Indicator'})

                    if volume_options[6] in volume or volume_options[0] in volume:
                        with st.expander(f"{self.ticker} Stock Negative Volume Index (NVI) Indicator"):
                            plot_1D_data(self.df[['volume_nvi']],
                                        title=f'{self.ticker} Stock Negative Volume Index (NVI) Indicator',
                                        label={"variable":'Negative Volume Index Indicator'})
                        
                    if volume_options[7] in volume or volume_options[0] in volume:
                        with st.expander(f"{self.ticker} Stock On-balance Volume (OBV) Indicator"):
                            plot_1D_data(self.df[['volume_obv']],
                                        title=f'{self.ticker} Stock On-balance Volume (OBV) Indicator',
                                        label={"variable":'On-balance Volume Indicator'})
                        
                    if volume_options[8] in volume or volume_options[0] in volume:
                        with st.expander(f"{self.ticker} Stock Volume-price Trend (VPT) Indicator"):
                            plot_1D_data(self.df[['volume_vpt']],
                                        title=f'{self.ticker} Stock Volume-price Trend (VPT) Indicator',
                                        label={"variable":'Volume-price Trend Indicator'})
                    
                    if volume_options[9] in volume or volume_options[0] in volume:
                        with st.expander(f"{self.ticker} Stock Volume Weighted Average Price (VWAP)"):
                            plot_1D_data(self.df[['volume_vwap']],
                                        title=f'{self.ticker} Stock Volume Weighted Average Price (VWAP)',
                                        label={"variable":'VWAP'})

                # General Indicators
                if return_selected:
                    st.subheader(f'{self.company_name} Stock Return Indicator')

                    if return_options[1] in return_selected or return_options[0] in return_selected:
                        with st.expander(f"{self.ticker} Stock Cumulative Return (CR)"):
                            plot_1D_data(self.df[['others_cr']],
                                        title=f'{self.ticker} Stock Cumulative Return (CR)',
                                        label={"variable":'Cumulative Return'})

                    if return_options[2] in return_selected or return_options[0] in return_selected:
                        with st.expander(f"{self.ticker} Stock Daily Log Return (DLR)"):
                            plot_1D_data(self.df[['others_dlr']],
                                        title=f'{self.ticker} Stock Daily Log Return (DLR)',
                                        label={"variable":'Daily Log Return'})

                    if return_options[3] in return_selected or return_options[0] in return_selected:
                        with st.expander(f"{self.ticker} Stock Daily Return (DR)"):
                            plot_1D_data(self.df[['others_dr']],
                                        title=f'{self.ticker} Stock Daily Return (DR)',
                                        label={"variable":'Daily Return'})

        # Printing the successful retrivial of Stock Analysis
        empty.success(f"{self.ticker} Stock Analysis Retrieved")