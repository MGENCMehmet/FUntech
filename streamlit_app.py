import streamlit as st
import yfinance as yf
import plotly.express as px
import pandas as pd
import pandas_ta as ta

st.set_page_config(layout="wide")

st.write(
    '<h1 style="text-align: center;">FUntech</h1>',
    unsafe_allow_html=True
)
