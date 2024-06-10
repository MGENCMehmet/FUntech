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
            fig.add_trace(go.Scatter(x=ticker_df.index, y=ticker_df['Open'], mode='lines', name=f'{tick} Open'))
            fig.add_trace(go.Scatter(x=ticker_df.index, y=ticker_df['High'], mode='lines', name=f'{tick} High'))
            fig.add_trace(go.Scatter(x=ticker_df.index, y=ticker_df['Low'], mode='lines', name=f'{tick} Low'))
            fig.add_trace(go.Scatter(x=ticker_df.index, y=ticker_df['Close'], mode='lines', name=f'{tick} Close'))
            fig.add_trace(go.Scatter(x=ticker_df.index, y=ticker_df['Adj Close'], mode='lines',
                                     name=f'{tick} Adj Close'))

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
    sdate = col2.date_input("Başlangıç Tarihi Giriniz", value=pd.to_datetime("2023-01-1"))
    edate = col3.date_input("Bitiş Tarihi Giriniz", value=pd.to_datetime("today"))
    col12, col22 = st.columns([8, 2])
  
    if len(ticker) == 1:
        df = yf.download(ticker[0], start=sdate, end=edate)
        ind_list = df.ta.indicators(as_list=True)
        selected_indicators = col22.multiselect("İndikatör Seç", options=ind_list)

        idf = df[["Close"]]

        for technical_indicator in selected_indicators:
            method = technical_indicator
            try:
              indicator = getattr(ta, method)(low=df["Low"],
                                               close=df["Close"],
                                              high=df["High"],
                                              open=df["Open"],
                                              volume=df["Volume"])
            except Exception as e:
              st.write(f"Maalesef bu özellik şuan kullanımda değil")
            try:  
              if isinstance(indicator, pd.DataFrame):
                  for col in indicator.columns:
                      idf[col] = indicator[col]
              else:
                  idf[technical_indicator] = indicator
            except Exception as e:
              st.write("")
        figraph = px.line(idf, x=idf.index, y=idf.columns,  title=f'İndikatörler ve  {ticker}  Kapanış Fiyatı')

        figraph.update_layout(xaxis_title='Tarih',
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
    sdate = col2.date_input("Başlangıç Tarihi Giriniz", value=pd.to_datetime("2023-01-1"))
    edate = col3.date_input("Bitiş Tarihi Giriniz", value=pd.to_datetime("today"))

    if len(ticker) > 1:
        st.write("{} Değerleri arasındaki ilişki".format(ticker))
        df = dest(yf.download(ticker, start=sdate, end=edate)["Close"])
        st.line_chart(df)
    else:
        st.write("Bu özelliği kullanabilmek için 1'den fazla hisse seçiniz")

elif page == "Tahmin":
    st.write("Pek yakında")
    st.sidebar.markdown("[Tahmin](https://colab.research.google.com/drive/1h_DJiTS2aedMWQqLxPp__gQSlReQEECY?usp=sharing)")
