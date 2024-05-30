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

col1, col2 = st.columns([1, 1])

col1.subheader("Panel")

tickers = (
    "AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "NVDA", "META", "BRK-B", "V", "JNJ",
    "WMT", "JPM", "PG", "UNH", "HD", "MA", "DIS", "PYPL", "VZ", "ADBE",
    "NFLX", "CMCSA", "KO", "MRK", "PFE", "ABT", "NKE", "PEP", "INTC", "CSCO",
    "XOM", "CVX", "ORCL", "CRM", "ACN", "COST", "AMD", "QCOM", "TXN", "HON",
    "LLY", "MCD", "AMGN", "IBM", "GS", "WFC", "T", "MDT", "BMY", "CAT",
    "GE", "MMM", "BA", "NOW", "SPGI", "NEE", "DHR", "LMT", "BLK", "SCHW",
    "TMO", "ISRG", "AXP", "SYK", "C", "PM", "UNP", "LOW", "GILD", "PLD",
    "USB", "CB", "CCI", "CL", "ZTS", "CI", "MO", "ICE", "BKNG", "ADI",
    "SCHD", "ADP", "SO", "DUK", "NSC", "MMC", "BSX", "ITW", "VRTX", "PGR",
    "HUM", "MDLZ", "PNC", "EL", "BDX", "ECL", "EW", "KMB", "AON", "MRNA",
    "AKBNK.IS", "GARAN.IS", "KCHOL.IS", "SAHOL.IS", "THYAO.IS",
    "ASELS.IS", "BIMAS.IS", "TCELL.IS", "EREGL.IS", "TKFEN.IS"
)

ticker = col1.multiselect("Hisse Gir", tickers)
sdate = st.sidebar.date_input("Başlangıç Tarihi Giriniz", value=pd.to_datetime("2023-01-1"))
edate = st.sidebar.date_input("Bitiş Tarihi Giriniz", value=pd.to_datetime("today"))


def dest(dfa):
    rel = dfa.pct_change()
    cumret = (1+rel).cumprod() - 1
    cumret = cumret.fillna(0)
    return cumret


if len(ticker) == 0:
    df = yf.download("ASELS.IS", start=sdate, end=edate)
    fig = px.line(df, x=df.index, y=df["High"])
    fig.update_layout(
        width=800,
        height=450,
    )
    col1.plotly_chart(fig)
    col1.write("ASELS.IS")
elif len(ticker) == 1:
    df = yf.download(ticker, start=sdate, end=edate)
    fig = px.line(df, x=df.index, y=df["High"])
    fig.update_layout(
        width=800,
        height=450,
    )
    col1.plotly_chart(fig)
else:
    st.write("{} Değerleri arasındaki ilişki".format(ticker))
    df = dest(yf.download(ticker, start=sdate, end=edate)["High"])
    col1.line_chart(df)

if len(ticker) < 2:
    col2.subheader("İndikatör")
    ind_list = df.ta.indicators(as_list=True)
    technical_indicator = col2.selectbox("İndikatör Seç", options=ind_list)
    method = technical_indicator
    indicator = pd.DataFrame(getattr(ta, method)(low=df["Low"],
                                                 close=df["Close"],
                                                 high=df["High"],
                                                 open=df["Open"],
                                                 volume=df["Volume"]))
    indicator["High"] = df["High"]
    figraph = px.line(indicator)
    figraph.update_layout(
        width=800,
        height=450,
    )
    col2.plotly_chart(figraph)
