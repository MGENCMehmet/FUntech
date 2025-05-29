import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd

st.set_page_config(page_title="FUntech", layout="wide")

st.title("📈 Hisse Fiyatları")

# Örnek hisse listesi
tickers = ["ASELS.IS", "AKBNK.IS", "AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"]
selected_tickers = st.multiselect("Hisse Seçiniz", tickers, default=["ASELS.IS"])

# Tarih aralığı
col1, col2 = st.columns(2)
start_date = col1.date_input("Başlangıç Tarihi", value=pd.to_datetime("2023-01-01"))
end_date = col2.date_input("Bitiş Tarihi", value=pd.to_datetime("today"))

# Geçerli giriş kontrolü
if start_date >= end_date:
    st.error("Başlangıç tarihi, bitiş tarihinden küçük olmalı.")
elif not selected_tickers:
    st.warning("Lütfen en az bir hisse seçiniz.")
else:
    fig = go.Figure()
    for ticker in selected_tickers:
        df = yf.download(ticker, start=start_date, end=end_date)
        if df.empty:
            st.warning(f"{ticker} için veri alınamadı.")
        else:
            fig.add_trace(go.Scatter(x=df.index, y=df["Close"], mode="lines", name=ticker))
    
    if fig.data:
        fig.update_layout(
            title="Seçilen Hisselerin Kapanış Fiyatları",
            xaxis_title="Tarih",
            yaxis_title="Fiyat",
            height=500
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.error("Hiçbir hisse için geçerli veri alınamadı.")
