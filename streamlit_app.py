import streamlit as st                                                                                                                                    
import yfinance as yf                                                                                                                                     
import plotly.express as px                                                                                                                               
import pandas as pd                                                                                                                                       
import pandas_ta as ta                                                                                                                                    
import plotly.graph_objects as go                                                                                                                         
from keras.models import Sequential                                                                                                                       
from keras.layers import Dense, LSTM                                                                                                                      
import numpy as np                                                                                                                                        
from sklearn.preprocessing import MinMaxScaler                                                                                                            
                                                                                                                                                          
st.set_page_config(layout="wide",                                                                                                                         
                   page_title="FUntech",                                                                                                                  
                   initial_sidebar_state="collapsed",                                                                                                     
                   page_icon=":chart_with_upwards_trend:",                                                                                                
                   )                                                                                                                                      
                                                                                                                                                          
st.write(                                                                                                                                                 
    '<h1 style="text-align: center;">FUntech</h1>',                                                                                                       
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
st.sidebar.markdown("### Hisse Hakkındaki Bilgileri Giriniz")                                                                                             
                                                                                                                                                          
ticker = st.sidebar.multiselect("Hisse Adı Giriniz", tickers, default="ASELS.IS")                                                                         
sdate = st.sidebar.date_input("Başlangıç Tarihi Giriniz", value=pd.to_datetime("2023-01-1"))                                                              
edate = st.sidebar.date_input("Bitiş Tarihi Giriniz", value=pd.to_datetime("today"))                                                                      
                                                                                                                                                          
st.sidebar.markdown("### Görüş ve Öneriler")                                                                                                              
st.sidebar.text_area("Tabii ki görüş ve önerilerinizi önemsiyoruz")                                                                                       
                                                                                                                                                          
if st.sidebar.button("Gönder"):                                                                                                                           
    st.sidebar.success("Geri Bildiriminizi Aldık")                                                                                                        
                                                                                                                                                          
st.sidebar.markdown("### Uygulamayı Paylaş")                                                                                                              
st.sidebar.markdown("[LinkedIn'de Paylaş](https://www.linkedin.com/sharing/share-offsite/?url=funtech.streamlit.app)")                                    
                                                                                                                                                          
def dest(dfa):                                                                                                                                            
    rel = dfa.pct_change()                                                                                                                                
    cumret = (1+rel).cumprod() - 1                                                                                                                        
    cumret = cumret.fillna(0)                                                                                                                             
    return cumret                                                                                                                                         
                                                                                                                                                          
                                                                                                                                                          
if len(ticker) == 0:                                                                                                                                      
    st.write("Lütfen bir hisse seçiniz")                                                                                                                  
                                                                                                                                                          
else:                                                                                                                                                     
                                                                                                                                                          
    with st.expander("Hisse Fiyatları"):                                                                                                                  
                                                                                                                                                          
        dfl = []                                                                                                                                          
                                                                                                                                                          
        for tick in ticker:                                                                                                                               
            df = yf.download(tick, start=sdate, end=edate, progress=False)                                                                                                
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
            fig.add_trace(go.Scatter(x=ticker_df.index, y=ticker_df['Adj Close'], mode='lines', name=f'{tick} Adj Close'))                                
                                                                                                                                                          
        fig.update_layout(                                                                                                                                
            title=f'{ticker}  Fiyat Değerleri',                                                                                                           
            xaxis_title='Tarih',                                                                                                                          
            yaxis_title='Fiyat',                                                                                                                          
            width=900,                                                                                                                                    
            height=500,                                                                                                                                   
        )                                                                                                                                                 
                                                                                                                                                          
        st.plotly_chart(fig)                                                                                                                              
                                                                                                                                                          
    with st.expander("İndikatörler"):                                                                                                                     
                                                                                                                                                          
        if len(ticker) == 1:                                                                                                                              
                ind_list = df.ta.indicators(as_list=True)                                                                                                 
                selected_indicators = st.multiselect("İndikatör Seç", options=ind_list)                                                                   
                                                                                                                                                          
                idf = df[["Close"]]                                                                                                                       
                                                                                                                                                          
                for technical_indicator in selected_indicators:                                                                                           
                    method = technical_indicator                                                                                                          
                    indicator = getattr(ta, method)(low=df["Low"],                                                                                        
                                                    close=df["Close"],                                                                                    
                                                    high=df["High"],                                                                                      
                                                    open=df["Open"],                                                                                      
                                                    volume=df["Volume"])                                                                                  
                                                                                                                                                          
                    if isinstance(indicator, pd.DataFrame):                                                                                               
                        for col in indicator.columns:                                                                                                     
                            idf[col] = indicator[col]                                                                                                     
                    else:                                                                                                                                 
                        idf[technical_indicator] = indicator                                                                                              
                                                                                                                                                          
                figraph = px.line(idf, x=idf.index, y=idf.columns,  title=f'İndikatörler ve  {ticker}  Kapanış Fiyatı')                                   
                                                                                                                                                          
                figraph.update_layout(xaxis_title='Tarih',                                                                                                
                                      yaxis_title='Fiyat',                                                                                                
                                      width=900,                                                                                                          
                                      height=500,                                                                                                         
                                      )                                                                                                                   
                                                                                                                                                          
                st.plotly_chart(figraph)                                                                                                                  
        else:                                                                                                                                             
            st.write("Bu özelliği kullanabilmek için sadece 1 hisse seçiniz")                                                                             
                                                                                                                                                          
    with st.expander("CandleStick Grafiği"):                                                                                                              
                                                                                                                                                          
        if len(ticker) == 1:                                                                                                                              
                                                                                                                                                          
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
                width=900,                                                                                                                                
                height=600,                                                                                                                               
            )                                                                                                                                             
                                                                                                                                                          
            st.plotly_chart(figcs)                                                                                                                        
                                                                                                                                                          
        else:                                                                                                                                             
            st.write("Bu özelliği kullanabilmek için sadece 1 hisse seçiniz")                                                                             
                                                                                                                                                          
    with st.expander("Hareketli Ortalamalar ve Bollinger Bantları"):                                                                                      
                                                                                                                                                          
        if len(ticker) == 1:                                                                                                                              
                                                                                                                                                          
                df['MA20'] = df['Close'].rolling(window=20).mean()                                                                                        
                df['STD20'] = df['Close'].rolling(window=20).std()                                                                                        
                df['Upper Band'] = df['MA20'] + (df['STD20'] * 2)                                                                                         
                df['Lower Band'] = df['MA20'] - (df['STD20'] * 2)                                                                                         
                                                                                                                                                          
                fig2 = go.Figure()                                                                                                                        
                                                                                                                                                          
                fig2.add_trace(go.Scatter(x=df.index,                                                                                                     
                                          y=df['Close'],                                                                                                  
                                          mode='lines',                                                                                                   
                                          name='Kapanış Fiyatı'))                                                                                         
                                                                                                                                                          
                fig2.add_trace(go.Scatter(x=df.index,                                                                                                     
                                          y=df['MA20'],                                                                                                   
                                          mode='lines',                                                                                                   
                                          name='20 Günlük MA'))                                                                                           
                                                                                                                                                          
                fig2.add_trace(go.Scatter(x=df.index,                                                                                                     
                                          y=df['Upper Band'],                                                                                             
                                          mode='lines',                                                                                                   
                                          name='Üst Bant',                                                                                                
                                          line=dict(color='rgba(255, 0, 0, 0.5)')))                                                                       
                                                                                                                                                          
                fig2.add_trace(go.Scatter(x=df.index,                                                                                                     
                                          y=df['Lower Band'],                                                                                             
                                          mode='lines',                                                                                                   
                                          name='Alt Bant',                                                                                                
                                          line=dict(color='rgba(0, 0, 255, 0.5)')))                                                                       
                st.plotly_chart(fig2)                                                                                                                     
                                                                                                                                                          
                df['MA50'] = df['Close'].rolling(window=50).mean()                                                                                        
                df['STD50'] = df['Close'].rolling(window=50).std()                                                                                        
                df['Upper Band'] = df['MA50'] + (df['STD50'] * 2)                                                                                         
                df['Lower Band'] = df['MA50'] - (df['STD50'] * 2)                                                                                         
                                                                                                                                                          
                fig5 = go.Figure()                                                                                                                        
                                                                                                                                                          
                fig5.add_trace(go.Scatter(x=df.index,                                                                                                     
                                          y=df['Close'],                                                                                                  
                                          mode='lines',                                                                                                   
                                          name='Kapanış Fiyatı'))                                                                                         
                                                                                                                                                          
                fig5.add_trace(go.Scatter(x=df.index,                                                                                                     
                                          y=df['MA50'],                                                                                                   
                                          mode='lines',                                                                                                   
                                          name='50 Günlük MA'))                                                                                           
                                                                                                                                                          
                fig5.add_trace(go.Scatter(x=df.index,                                                                                                     
                                          y=df['Upper Band'],                                                                                             
                                          mode='lines',                                                                                                   
                                          name='Üst Bant',                                                                                                
                                          line=dict(color='rgba(255, 0, 0, 0.5)')))                                                                       
                                                                                                                                                          
                fig5.add_trace(go.Scatter(x=df.index,                                                                                                     
                                          y=df['Lower Band'],                                                                                             
                                          mode='lines',                                                                                                   
                                          name='Alt Bant',                                                                                                
                                          line=dict(color='rgba(0, 0, 255, 0.5)')))                                                                       
                                                                                                                                                          
                st.plotly_chart(fig5)                                                                                                                     
                                                                                                                                                          
        else:                                                                                                                                             
            st.write("Bu özelliği kullanabilmek için sadece 1 hisse seçiniz")                                                                             
                                                                                                                                                          
    with st.expander("Hisseleri Karşılaştır"):                                                                                                            
                                                                                                                                                          
        if len(ticker) > 1:                                                                                                                               
            st.write("{} Değerleri arasındaki ilişki".format(ticker))                                                                                     
            df = dest(yf.download(ticker, start=sdate, end=edate)["Close"])                                                                               
            st.area_chart(df)                                                                                                                             
        else:                                                                                                                                             
            st.write("Bu özelliği kullanabilmek için 1'den fazla hisse seçiniz")                                                                          
                                                                                                                                                          
    with st.expander("Tahmin"):                                                                                                                           
        if len(ticker) == 1:                                                                                                                              
            df = df["Close"]                                                                                                                              
            df_values = df.values.reshape(-1, 1)                                                                                                          
                                                                                                                                                          
            df_train_len = int(np.ceil(len(df_values) * .95))                                                                                             
                                                                                                                                                          
            mms = MinMaxScaler()                                                                                                                          
            scaled_df = mms.fit_transform(df_values)                                                                                                      
                                                                                                                                                          
            train_df = scaled_df[0:df_train_len, :]                                                                                                       
            x_train = []                                                                                                                                  
            y_train = []                                                                                                                                  
                                                                                                                                                          
            for i in range(60, len(train_df)):                                                                                                            
                x_train.append(train_df[i - 60:i, 0])                                                                                                     
                y_train.append(train_df[i, 0])                                                                                                            
                                                                                                                                                          
            x_train, y_train = np.array(x_train), np.array(y_train)                                                                                       
            x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))                                                                        
                                                                                                                                                          
            model = Sequential()                                                                                                                          
            model.add(LSTM(128, return_sequences=True, input_shape=(x_train.shape[1], 1)))                                                                
            model.add(LSTM(64, return_sequences=False))                                                                                                   
            model.add(Dense(25))                                                                                                                          
            model.add(Dense(1))                                                                                                                           
                                                                                                                                                          
            model.compile(optimizer="adam", loss="mean_squared_error")                                                                                    
                                                                                                                                                          
            model.fit(x_train, y_train, batch_size=1, epochs=1, verbose=0)                                                                                           
                                                                                                                                                          
            test_df = scaled_df[df_train_len - 60:, :]                                                                                                    
            x_test = []                                                                                                                                   
            y_test = df_values[df_train_len:, :]                                                                                                          
                                                                                                                                                          
            for i in range(60, len(test_df)):                                                                                                             
                x_test.append(test_df[i - 60:i, 0])                                                                                                       
                                                                                                                                                          
            x_test = np.array(x_test)                                                                                                                     
                                                                                                                                                          
            x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))                                                                            
            preds = model.predict(x_test, verbose=0)                                                                                                                 
            preds = mms.inverse_transform(preds)                                                                                                          
            train = df[:df_train_len]                                                                                                                     
            valid = df[df_train_len:]                                                                                                                     
                                                                                                                                                          
            preds = pd.Series(index=valid.index, data=preds.reshape(1, len(preds))[0])                                                                    
                                                                                                                                                          
            figp = px.line(x=train.index, y=train.values)                                                                                                 
            figp.add_trace(go.Scatter(x=valid.index, y=valid.values, mode='lines', name='Valid', line=dict(color='orange')))                              
            figp.add_trace(go.Scatter(x=valid.index, y=preds, mode='lines', name='Preds', line=dict(color='green')))                                      
            st.line_chart(figp)                                                                                                                           
                                                                                                                                                          
