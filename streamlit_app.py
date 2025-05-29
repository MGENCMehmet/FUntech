# FUntech - Geliştirilmiş Versiyon

import streamlit as st
import yfinance as yf
import plotly.express as px
import pandas as pd
import pandas_ta as ta
import plotly.graph_objects as go
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from sklearn.preprocessing import MinMaxScaler

# Sayfa Ayarları
st.set_page_config(
    page_title="FUntech",
    page_icon=":chart_with_upwards_trend:",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS
with open("style.css", "w") as f:
    f.write("""
    <style>
    body {
        background-color: #f7f7f7;
        color: #333;
        font-family: 'Segoe UI', sans-serif;
    }
    .reportview-container, .sidebar .sidebar-content {
        background: #fff;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    h1, h2, h3 {
        color: #1e90ff;
        font-weight: bold;
    }
    .stButton button {
        background-color: #1e90ff;
        color: white;
        padding: 10px 20px;
        border-radius: 8px;
        border: none;
        transition: 0.3s ease;
    }
    .stButton button:hover {
        background-color: #1c86ee;
        transform: scale(1.02);
    }
    </style>
    """)

st.markdown(open("style.css").read(), unsafe_allow_html=True)

# Başlık
st.markdown("""<h1 style='text-align:center;font-size:60px;'>📊 FUntech</h1>""", unsafe_allow_html=True)

# Hisse Listesi
tickers = sorted([
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
    "AKBNK.IS", "GARAN.IS", "SAHOL.IS", "THYAO.IS", "ASELS.IS",
    "BIMAS.IS", "TCELL.IS", "EREGL.IS", "TKFEN.IS"
])

# Sidebar
st.sidebar.markdown("""<h1 style='text-align:center;font-size:40px;'>📈 FUntech</h1>""", unsafe_allow_html=True)

menu = st.sidebar.radio("Menü", ["Hisse Fiyatları", "İndikatörler", "CandleStick", "Karşılaştır", "Tahmin"])

# Kullanıcıdan tarih ve hisse bilgisi al
@st.cache_data
def load_data(ticker, start, end):
    return yf.download(ticker, start=start, end=end)

def show_prices():
    col1, col2, col3 = st.columns(3)
    selected = col1.multiselect("Hisse Seçiniz", tickers, default=["ASELS.IS"])
    start = col2.date_input("Başlangıç Tarihi", pd.to_datetime("2023-01-01"))
    end = col3.date_input("Bitiş Tarihi", pd.to_datetime("today"))

    if selected:
        with st.spinner("Veriler yükleniyor..."):
            all_data = pd.concat([load_data(t, start, end).assign(Ticker=t) for t in selected])
        fig = go.Figure()
        for t in selected:
            df = all_data[all_data['Ticker'] == t]
            for col in ["Open", "High", "Low", "Close"]:
                fig.add_trace(go.Scatter(x=df.index, y=df[col], name=f"{t} {col}"))
        fig.update_layout(title="Fiyatlar", xaxis_title="Tarih", yaxis_title="Fiyat", width=1000, height=500)
        st.plotly_chart(fig)
    else:
        st.info("Lütfen en az bir hisse seçiniz.")

def show_indicators():
    col1, col2, col3 = st.columns(3)
    selected = col1.selectbox("Hisse Seçiniz", tickers)
    start = col2.date_input("Başlangıç Tarihi", pd.to_datetime("2023-01-01"))
    end = col3.date_input("Bitiş Tarihi", pd.to_datetime("today"))

    df = load_data(selected, start, end)
    available = df.ta.indicators(as_list=True)
    chosen = st.multiselect("İndikatör Seçiniz", options=available)

    result = df[["Close"]].copy()
    for ind in chosen:
        try:
            indicator = getattr(ta, ind)(low=df["Low"], close=df["Close"], high=df["High"], open=df["Open"], volume=df["Volume"])
            if isinstance(indicator, pd.DataFrame):
                result = result.join(indicator)
            else:
                result[ind] = indicator
        except:
            st.warning(f"'{ind}' yüklenemedi.")

    fig = px.line(result, x=result.index, y=result.columns, title=f"{selected} İndikatörler")
    fig.update_layout(width=1000, height=500)
    st.plotly_chart(fig)

def show_candlestick():
    col1, col2, col3 = st.columns(3)
    selected = col1.selectbox("Hisse Seçiniz", tickers)
    start = col2.date_input("Başlangıç Tarihi", pd.to_datetime("2023-01-01"))
    end = col3.date_input("Bitiş Tarihi", pd.to_datetime("today"))

    df = load_data(selected, start, end)
    fig = go.Figure(data=[go.Candlestick(
        x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'],
        increasing_line_color='#39FF14', decreasing_line_color='#FF073A')])
    fig.update_layout(title="CandleStick", xaxis_title="Tarih", yaxis_title="Fiyat", width=1000, height=600)
    st.plotly_chart(fig)

def show_comparison():
    selected = st.multiselect("Hisseler", tickers, default=["AAPL", "ASELS.IS"])
    start = st.date_input("Başlangıç Tarihi", pd.to_datetime("2010-01-01"))
    end = st.date_input("Bitiş Tarihi", pd.to_datetime("today"))
    if len(selected) > 1:
        df = yf.download(selected, start=start, end=end)["Close"]
        df_pct = (df.pct_change() + 1).cumprod()
        st.line_chart(df_pct)
    else:
        st.warning("Lütfen en az iki hisse seçiniz.")

def show_prediction():
    selected = st.selectbox("Hisse Seçiniz", tickers)
    start = st.date_input("Başlangıç Tarihi", pd.to_datetime("2010-01-01"))
    end = st.date_input("Bitiş Tarihi", pd.to_datetime("today"))

    df = yf.download(selected, start=start, end=end)["Close"]
    df = df.values.reshape(-1, 1)
    scaler = MinMaxScaler()
    scaled = scaler.fit_transform(df)

    train_len = int(len(scaled) * 0.95)
    train = scaled[:train_len]

    x_train, y_train = [], []
    for i in range(3, len(train)):
        x_train.append(train[i-3:i, 0])
        y_train.append(train[i, 0])
    x_train = np.array(x_train).reshape(-1, 3, 1)
    y_train = np.array(y_train)

    if st.button("Tahmin Et"):
        model = Sequential([
            LSTM(128, return_sequences=True, input_shape=(3, 1)),
            LSTM(64),
            Dense(25),
            Dense(1)
        ])
        model.compile(optimizer="adam", loss="mean_squared_error")
        model.fit(x_train, y_train, batch_size=1, epochs=1, verbose=0)

        test = scaled[train_len-3:]
        x_test = np.array([test[i-3:i, 0] for i in range(3, len(test))]).reshape(-1, 3, 1)
        preds = scaler.inverse_transform(model.predict(x_test))

        valid_index = pd.date_range(start=start, periods=len(df))[train_len:]
        fig = px.line(x=pd.date_range(start=start, periods=len(df[:train_len])), y=df[:train_len].reshape(-1))
        fig.add_trace(go.Scatter(x=valid_index, y=df[train_len:].reshape(-1), name="Gerçek", line=dict(color='orange')))
        fig.add_trace(go.Scatter(x=valid_index, y=preds.flatten(), name="Tahmin", line=dict(color='green')))
        st.plotly_chart(fig)

# Sayfa Yönlendirme
if menu == "Hisse Fiyatları":
    show_prices()
elif menu == "İndikatörler":
    show_indicators()
elif menu == "CandleStick":
    show_candlestick()
elif menu == "Karşılaştır":
    show_comparison()
elif menu == "Tahmin":
    show_prediction()
