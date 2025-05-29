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

st.set_page_config(layout="wide",
                   page_title="FUntech",
                   initial_sidebar_state="expanded",
                   page_icon=":chart_with_upwards_trend:",
                   )

css = """
<style>

body {
    background-color: #f7f7f7;
    color: #444444;
    font-family: 'Roboto', sans-serif;
}


.reportview-container {
    background-color: #ffffff;
    padding: 30px;
    border-radius: 15px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    animation: fadeIn 1s ease-in-out;
}


.sidebar .sidebar-content {
    background-color: #f0f0f0;
    padding: 20px;
    border-radius: 10px;
    animation: slideInLeft 0.5s ease-in-out;
}


h1, h2, h3 {
    color: #1e90ff;
    font-weight: 700;
    animation: fadeInDown 1s ease-in-out;
}


.stButton button {
    background-color: #1e90ff;
    color: #ffffff;
    border: none;
    padding: 10px 25px;
    font-size: 16px;
    border-radius: 5px;
    transition: background-color 0.3s ease, transform 0.3s ease;
    cursor: pointer;
    animation: fadeIn 1s ease-in-out;
}

.stButton button:hover {
    background-color: #1c86ee;
    transform: translateY(-2px);
}

@keyframes fadeIn {
    from {
        opacity: 0;
    }
    to {
        opacity: 1;
    }
}

@keyframes fadeInDown {
    from {
        opacity: 0;
        transform: translateY(-20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes slideInLeft {
    from {
        opacity: 0;
        transform: translateX(-100%);
    }
    to {
        opacity: 1;
        transform: translateX(0);
    }
}
</style>
"""
st.markdown(css, unsafe_allow_html=True)

st.write(
    '<h1 style="text-align: center; font-size: 70px;">FUntech</h1>',
    unsafe_allow_html=True
)


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
    "AKBNK.IS", "GARAN.IS", "SAHOL.IS", "THYAO.IS", "ASELS.IS",
    "BIMAS.IS", "TCELL.IS", "EREGL.IS", "TKFEN.IS"
)

st.sidebar.markdown('<h1 style="text-align: center; font-size: 50px;">FUntech</h1>', unsafe_allow_html=True)

tabs = ["Hisse Fiyatları", "İndikatörler", "CandleStick Grafiği", "Hisseleri Karşılaştır", "Tahmin"]
st.sidebar.markdown("### Özellikler")
if "selected_tab" not in st.session_state:
    st.session_state.selected_tab = "Hisse Fiyatları"

if st.sidebar.button("Hisse Fiyatları"):
    st.session_state.selected_tab = "Hisse Fiyatları"
if st.sidebar.button("İndikatörler"):
    st.session_state.selected_tab = "İndikatörler"
if st.sidebar.button("CandleStick Grafiği"):
    st.session_state.selected_tab = "CandleStick Grafiği"
if st.sidebar.button("Hisseleri Karşılaştır"):
    st.session_state.selected_tab = "Hisseleri Karşılaştır"
if st.sidebar.button("Tahmin"):
    st.session_state.selected_tab = "Tahmin"

page = st.session_state.selected_tab

st.sidebar.markdown("### Uygulamayı Paylaş")
st.sidebar.markdown("[LinkedIn'de Paylaş](https://www.linkedin.com/sharing/share-offsite/?url=funtech.streamlit.app)")

st.sidebar.markdown("### Görüş ve Öneriler")
st.sidebar.text_area("Görüş ve önerilerinizi önemsiyoruz")

if st.sidebar.button("Gönder"):
    st.sidebar.success("Geri Bildiriminizi Aldık")

st.sidebar.markdown("### Bizi Örnek Alan Bazı Sayfalar")
st.sidebar.markdown("[TradingView](https://tr.tradingview.com)")
st.sidebar.markdown("[Binance](https://www.binance.com/)")
st.sidebar.markdown("[İnvesting](https://tr.investing.com)")
st.sidebar.markdown("[Binomo](https://binomo.com/)")
st.sidebar.markdown("[icrypex](https://www.icrypex.com)")
st.sidebar.markdown("[Midas](https://www.getmidas.com)")


def dest(dfa):
    rel = dfa.pct_change()
    cumret = (1+rel).cumprod() - 1
    cumret = cumret.fillna(0)
    return cumret


if page == "Hisse Fiyatları":

    col1, col2, col3 = st.columns(3)
    ticker = col1.multiselect("Hisse Adı Giriniz", tickers, default="ASELS.IS")
    sdate = col2.date_input("Başlangıç Tarihi Giriniz", value=pd.to_datetime("2023-01-1"))
    edate = col3.date_input("Bitiş Tarihi Giriniz", value=pd.to_datetime("today"))
    if len(ticker) > 0:
        dfl = []

        for tick in ticker:
            df = yf.download(tick, start=sdate, end=edate)
            df['Ticker'] = tick
            dfl.append(df)

        dfll = pd.concat(dfl)

        fig = go.Figure()

        for tick in ticker:
            ticker_df = dfll[dfll['Ticker'] == tick]
            fig.add_trace(go.Scatter(x=ticker_df.index, y=ticker_df[('Open', tick)], mode='lines', name=f'{tick} Open'))
            fig.add_trace(go.Scatter(x=ticker_df.index, y=ticker_df[('High', tick)], mode='lines', name=f'{tick} High'))
            fig.add_trace(go.Scatter(x=ticker_df.index, y=ticker_df[('Low', tick)], mode='lines', name=f'{tick} Low'))
            fig.add_trace(go.Scatter(x=ticker_df.index, y=ticker_df[('Close', tick)], mode='lines', name=f'{tick} Close'))


        fig.update_layout(
            title=f'{ticker}  Fiyat Değerleri',
            xaxis_title='Tarih',
            yaxis_title='Fiyat',
            width=900,
            height=500,
        )

        st.plotly_chart(fig)
    else:
        st.write("Bu özelliği kullanabilmek için en az 1 hisse seçiniz")

elif page == "İndikatörler":
    col1, col2, col3 = st.columns(3)
    ticker = col1.multiselect("Hisse Adı Giriniz", tickers, default="ASELS.IS")
    sdate = col2.date_input("Başlangıç Tarihi Giriniz", value=pd.to_datetime("2023-01-01"))
    edate = col3.date_input("Bitiş Tarihi Giriniz", value=pd.to_datetime("today"))
    col12, col22 = st.columns([8, 2])

    if len(ticker) == 1:
        df = yf.download(ticker[0], start=sdate, end=edate)  # MultiIndex yapısı burada geliyor

        # Kolonlara MultiIndex ile erişim
        close = df[("Close", ticker[0])]
        high = df[("High", ticker[0])]
        low = df[("Low", ticker[0])]
        open_ = df[("Open", ticker[0])]
        volume = df[("Volume", ticker[0])]

        ind_list = [
    "sma", "ema", "rsi", "macd", "bbands", "adx", "stoch", "cci", "atr"
]
        selected_indicators = col22.multiselect("İndikatör Seç", options=ind_list)

        idf = pd.DataFrame({"Close": close})

        for technical_indicator in selected_indicators:
            method = technical_indicator
            try:
                indicator = getattr(ta, method)(
                    close=close,
                    high=high,
                    low=low,
                    open=open_,
                    volume=volume
                )
            except Exception as e:
                st.write(f"Maalesef bu özellik şu an kullanımda değil")

            try:
                if isinstance(indicator, pd.DataFrame):
                    for col in indicator.columns:
                        idf[col] = indicator[col]
                else:
                    idf[technical_indicator] = indicator
            except Exception as e:
                st.write("")

        figraph = px.line(idf, x=idf.index, y=idf.columns, title=f'İndikatörler ve {ticker[0]} Kapanış Fiyatı')

        figraph.update_layout(
            xaxis_title='Tarih',
            yaxis_title='Fiyat',
            width=900,
            height=500,
        )

        col12.plotly_chart(figraph)
    else:
        st.write("Bu özelliği kullanabilmek için sadece 1 hisse seçiniz")

elif page == "CandleStick Grafiği":
    col1, col2, col3 = st.columns(3)
    ticker = col1.multiselect("Hisse Adı Giriniz", tickers, default="ASELS.IS")
    sdate = col2.date_input("Başlangıç Tarihi Giriniz", value=pd.to_datetime("2023-01-1"))
    edate = col3.date_input("Bitiş Tarihi Giriniz", value=pd.to_datetime("today"))

    if len(ticker) == 1:
        df = yf.download(ticker[0], start=sdate, end=edate)
        figcs = go.Figure(data=[go.Candlestick(x=df.index,
                          open=df['Open'],
                          high=df['High'],
                          low=df['Low'],
                          close=df['Close'],
                          increasing_line_color='#39FF14',
                          decreasing_line_color='#FF073A')])

        figcs.update_layout(
            title=f'{ticker}  CandleStick Grafiği',
            xaxis_title='Tarih',
            yaxis_title='Fiyat',
            width=1000,
            height=600,
        )

        st.plotly_chart(figcs)

    else:
        st.write("Bu özelliği kullanabilmek için sadece 1 hisse seçiniz")

elif page == "Hisseleri Karşılaştır":
    col1, col2, col3 = st.columns(3)
    ticker = col1.multiselect("Hisse Adı Giriniz", tickers, default=["ASELS.IS", "AAPL"])
    sdate = col2.date_input("Başlangıç Tarihi Giriniz", value=pd.to_datetime("2003-01-1"))
    edate = col3.date_input("Bitiş Tarihi Giriniz", value=pd.to_datetime("today"))

    if len(ticker) > 1:
        st.write("{} Değerleri arasındaki ilişki".format(ticker))
        df = dest(yf.download(ticker, start=sdate, end=edate)["Close"])
        st.line_chart(df)
    else:
        st.write("Bu özelliği kullanabilmek için 1'den fazla hisse seçiniz")

elif page == "Tahmin":
    col1, col2, col3 = st.columns(3)
    ticker = col1.multiselect("Hisse Adı Giriniz", tickers)
    sdate = col2.date_input("Başlangıç Tarihi Giriniz", value=pd.to_datetime("2003-01-1"))
    edate = col3.date_input("Bitiş Tarihi Giriniz", value=pd.to_datetime("today"))
    if len(ticker) == 1:
      df = yf.download(ticker, sdate, edate)
      df = df["Close"]
      df_values = df.values.reshape(-1, 1)

      df_train_len = int(np.ceil(len(df_values) * .95))

      mms = MinMaxScaler()
      scaled_df = mms.fit_transform(df_values)

      train_df = scaled_df[0:df_train_len, :]
      x_train = []
      y_train = []

      for i in range(3, len(train_df)):
          x_train.append(train_df[i - 3:i, 0])
          y_train.append(train_df[i, 0])

      x_train, y_train = np.array(x_train), np.array(y_train)
      x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

      if st.button('Tahmin Et'):
          with st.spinner('Tahmin Ediliyor...'):
              model = Sequential()
              model.add(LSTM(128, return_sequences=True, input_shape=(x_train.shape[1], 1)))
              model.add(LSTM(64, return_sequences=False))
              model.add(Dense(25))
              model.add(Dense(1))

              model.compile(optimizer="adam", loss="mean_squared_error")
              model.fit(x_train, y_train, batch_size=1, epochs=1)
              st.success('Model Eğitildi')

              test_df = scaled_df[df_train_len - 3:, :]
              x_test = []
              y_test = df_values[df_train_len:, :]

              for i in range(3, len(test_df)):
                  x_test.append(test_df[i - 3:i, 0])

              x_test = np.array(x_test)
              x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))

              preds = model.predict(x_test)
              preds = mms.inverse_transform(preds)

              ticker_name = ticker[0]

              train = df[:df_train_len]
              valid = df[df_train_len:]
              preds = pd.Series(index=valid.index, data=preds.reshape(1, len(preds))[0])
              
              figp = px.line(train, title=f'{ticker[0]} için Tahminlerimiz')
              figp.add_trace(go.Scatter(x=valid.index, y=valid.values, mode='lines', name='Valid', line=dict(color='orange')))
              figp.add_trace(go.Scatter(x=valid.index, y=preds, mode='lines', name='Preds', line=dict(color='green')))
              
              st.plotly_chart(figp)


    else:
      st.write("Bu özelliği kullanabilmek için 1 hisse seçiniz")
