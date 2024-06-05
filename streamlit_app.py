import streamlit as st
import yfinance as yf
import plotly.express as px
import pandas as pd
import pandas_ta as ta
import plotly.graph_objects as go

st.set_page_config(layout="wide",
                   page_title="FUntech",
                   initial_sidebar_state="expanded",
                   page_icon=":chart_with_upwards_trend:",
                   )

st.write(
    '<h1 style="text-align: center; font-size: 70px;">FUntech</h1>',
    unsafe_allow_html=True
)

