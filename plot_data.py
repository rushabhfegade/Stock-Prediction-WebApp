import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def plot_rawdata(data, title=None):
    df = data[['Open', 'High', 'Low', 'Close']]
    data_reset_index = df.reset_index()
    fig = px.line(
                    data_reset_index, x=data_reset_index.keys()[0], y=data_reset_index.columns,
                    hover_data={data_reset_index.keys()[0]:"|%B %d, %Y"}, 
                    title=title, labels={"variable":"Stock Price Options", "value":"Price"}
                 )
    fig.update_xaxes(rangeslider_visible=True,
                        rangeselector=dict(
                            buttons=list([
                                dict(count=1, label="1m", step="month", stepmode="backward"),
                                dict(count=3, label="3m", step="month", stepmode="backward"),
                                dict(count=6, label="6m", step="month", stepmode="backward"),
                                dict(count=1, label="YTD", step="year", stepmode="todate"),
                                dict(count=1, label="1y", step="year", stepmode="backward"),
                                dict(count=2, label="2y", step="year", stepmode="backward"),
                                dict(count=5, label="5y", step="year", stepmode="backward"),
                                dict(count=10, label="10y", step="year", stepmode="backward"),
                                dict(step="all")
                            ])))
    
    st.plotly_chart(fig, use_container_width=True)

def plot_1D_data(prices, title=None, label=dict):
        fig = px.line(
                        prices.reset_index(), 
                        x=prices.reset_index().keys()[0], y=prices.columns, 
                        title=title,
                        hover_data={prices.reset_index().keys()[0]:"|%B %d, %Y"},
                        labels=label
                    )
        fig.update_xaxes(rangeslider_visible=True,
                            rangeselector=dict(
                                buttons=list([
                                    dict(count=1, label="1m", step="month", stepmode="backward"),
                                    dict(count=3, label="3m", step="month", stepmode="backward"),
                                    dict(count=6, label="6m", step="month", stepmode="backward"),
                                    dict(count=1, label="YTD", step="year", stepmode="todate"),
                                    dict(count=1, label="1y", step="year", stepmode="backward"),
                                    dict(count=2, label="2y", step="year", stepmode="backward"),
                                    dict(count=5, label="5y", step="year", stepmode="backward"),
                                    dict(count=10, label="10y", step="year", stepmode="backward"),
                                    dict(step="all")
                                ])))
        st.plotly_chart(fig, use_container_width=True)

def plot_seasonal(seasonal_result, title=None):
    
    fig = make_subplots(
                            rows=3, cols=1,
                            subplot_titles=("Trend", "Seasonal", "Residual"),
                            shared_xaxes=True, vertical_spacing=0.04
                        )
    trend_fig = go.Scatter(x=seasonal_result.trend.reset_index().iloc[:,0], y=seasonal_result.trend.reset_index().iloc[:,1], name="Trend")
    sea_fig = go.Scatter(x=seasonal_result.seasonal.reset_index().iloc[:,0], y=seasonal_result.seasonal.reset_index().iloc[:,1], name="Seasonal")
    resid_fig = go.Scatter(x=seasonal_result.resid.reset_index().iloc[:,0], y=seasonal_result.resid.reset_index().iloc[:,1], name="Residual")
    fig.add_trace(trend_fig, row=1, col=1)                    
    fig.add_trace(sea_fig, row=2,col=1)
    fig.add_trace(resid_fig, row=3,col=1)
    fig.update_layout(height=650, width=800)
    st.plotly_chart(fig, use_container_width=True)

def plotly_prophet_forecast(model, forecast, stock, trend, changepoints):
    
    # Plotly Graph plot of Forecast and Series Components
    prediction_color = '#0072B2'
    error_color = 'rgba(0, 114, 178, 0.2)'  # '#0072B2' with 0.2 opacity
    actual_color = 'black'
    cap_color = 'black'
    trend_color = '#B23B00'
    line_width = 2
    marker_size = 4
    changepoints_threshold = 0.01
    figsize=(900, 600)
    xlabel='Date' 
    ylabel=stock

    data = []
    # Add actual
    data.append(go.Scatter(
        name=f"Actual {stock} Prices",
        x=model.history['ds'],
        y=model.history['y'],
        marker=dict(color=actual_color, size=marker_size),
        mode='markers'))

    # Add lower bound
    data.append(go.Scatter(
        name='Lower Bound',
        x=forecast['ds'],
        y=forecast['yhat_lower'],
        mode='lines',
        line=dict(width=0),
        hoverinfo='skip'))

    # Add prediction
    data.append(go.Scatter(
        name='Prediction',
        x=forecast['ds'],
        y=forecast['yhat'],
        mode='lines',
        line=dict(color=prediction_color, width=line_width),
        fillcolor=error_color,
        fill='tonexty' if model.uncertainty_samples else 'none'))
    
    # Add upper bound
    data.append(go.Scatter(
        name='Upper Bound',
        x=forecast['ds'],
        y=forecast['yhat_upper'],
        mode='lines',
        line=dict(width=0),
        fillcolor=error_color,
        fill='tonexty',
        hoverinfo='skip'))

    # Add caps
    if 'cap' in forecast:
        data.append(go.Scatter(
            name='Cap',
            x=forecast['ds'],
            y=forecast['cap'],
            mode='lines',
            line=dict(color=cap_color, dash='dash', width=line_width),))
    if model.logistic_floor and 'floor' in forecast:
        data.append(go.Scatter(
            name='Floor',
            x=forecast['ds'],
            y=forecast['floor'],
            mode='lines',
            line=dict(color=cap_color, dash='dash', width=line_width),))

    # Add trend
    if trend:
        data.append(go.Scatter(
            name='Trend',
            x=forecast['ds'],
            y=forecast['trend'],
            mode='lines',
            line=dict(color=trend_color, width=line_width),))

    # Add changepoints
    if changepoints and len(model.changepoints) > 0:
        signif_changepoints = model.changepoints[
            np.abs(np.nanmean(model.params['delta'], axis=0)) >= changepoints_threshold
        ]
        data.append(go.Scatter(
            name='Changepoints',
            x=signif_changepoints,
            y=forecast.loc[forecast['ds'].isin(signif_changepoints), 'trend'],
            marker=dict(size=50, symbol='line-ns-open', color=trend_color,
                        line=dict(width=line_width)),
            mode='markers',
            hoverinfo='skip'))

    layout = dict(showlegend=True, width=figsize[0], height=figsize[1],
                yaxis=dict(title=ylabel),
                xaxis=dict(title=xlabel, type='date',
                            rangeselector=dict(
                                buttons=list([
                                    dict(count=7, label='1w', step='day', stepmode='backward'),
                                    dict(count=1, label="1m", step="month", stepmode="backward"),
                                    dict(count=3, label="3m", step="month", stepmode="backward"),
                                    dict(count=6, label="6m", step="month", stepmode="backward"),
                                    dict(count=1, label="YTD", step="year", stepmode="todate"),
                                    dict(count=1, label="1y", step="year", stepmode="backward"),
                                    dict(count=2, label="2y", step="year", stepmode="backward"),
                                    dict(count=5, label="5y", step="year", stepmode="backward"),
                                    dict(step='all')
                                ])
                            ),
                            rangeslider=dict(visible=True),),)

    fig = go.Figure(data=data, layout=layout)
    st.plotly_chart(fig, use_container_width=True)

def plotly_candlestick(data, stock=None, title=None):
    fig = go.Figure(data=[go.Candlestick(x=data.index,
                open=data['Open'],
                high=data['High'],
                low=data['Low'],
                close=data['Close'])])
    
    fig.update_xaxes(rangeslider_visible=True,
                        rangeselector=dict(
                            buttons=list([
                                dict(count=1, label="1m", step="month", stepmode="backward"),
                                dict(count=3, label="3m", step="month", stepmode="backward"),
                                dict(count=6, label="6m", step="month", stepmode="backward"),
                                dict(count=1, label="YTD", step="year", stepmode="todate"),
                                dict(count=1, label="1y", step="year", stepmode="backward"),
                                dict(count=2, label="2y", step="year", stepmode="backward"),
                                dict(count=5, label="5y", step="year", stepmode="backward"),
                                dict(count=10, label="10y", step="year", stepmode="backward"),
                                dict(step="all")
                            ])))
    fig.update_yaxes(fixedrange=False)
    fig.update_layout(title=title, yaxis_title=stock, xaxis_title="Date")
    st.plotly_chart(fig, use_container_width=True)
    return fig
