import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd

st.set_page_config(page_title="FUntech", layout="wide", page_icon=":chart_with_upwards_trend:")

st.title("📈 FUntech - Hisse Fiyatları")

# Hisse seçimi
tickers = ["ASELS.IS", "AKBNK.IS", "AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"]
selected_tickers = st.multiselect("Hisse Seçiniz", tickers, default=["ASELS.IS"])
start_date = st.date_input("Başlangıç Tarihi", pd.to_datetime("2023-01-01"))
end_date = st.date_input("Bitiş Tarihi", pd.to_datetime("today"))

if selected_tickers:
    fig = go.Figure()
    for symbol in selected_tickers:
        df = yf.download(symbol, start=start_date, end=end_date)
        if not df.empty:
            fig.add_trace(go.Scatter(x=df.index, y=df["Close"], mode="lines", name=symbol))
    fig.update_layout(title="Hisse Kapanış Fiyatları", xaxis_title="Tarih", yaxis_title="Fiyat", height=500)
    st.plotly_chart(fig)
else:
    st.warning("Lütfen en az bir hisse seçiniz.")
