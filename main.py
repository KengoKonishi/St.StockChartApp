import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
import altair as alt


# メインページ
st.title('株価可視化アプリ')

# 株価取得メソッド
# キャッシュの貯めこみにより高速な読み取りが可能
@st.cache
def getData(days, tickers):
    df = pd.DataFrame()
    for company in tickers.keys():
        tkr = yf.Ticker(tickers[company])
        hist = tkr.history(period=f'{days}d')
        hist.index = hist.index.strftime('%d %B %Y')
        hist = hist[['Close']]
        hist.columns = [company]
        hist = hist.T
        hist.index.name = 'Name'
        df = pd.concat([df, hist])
    return df

# 表示メソッド（図＆チャート）
def displayData(days, tickers, ymin, ymax, type, unit):
    df = getData(days, tickers)

    st.write(f"""
    ### 過去　**{days}日間**の{type}
    """)

    # tickersの社名をリスト化
    key_names = list(tickers.keys())
    # multiseletで社名選択
    companies = st.multiselect(
        '会社名を選択して下さい。',
        list(df.index),
        [key_names[0], key_names[1], key_names[2], key_names[3]]
    )
    if not companies:
        st.error('少なくとも1社は選んでください')
    else:
        data = df.loc[companies]
        st.write(f"### 株価{unit}", data.sort_index())
        data = data.T.reset_index()
        data = pd.melt(data, id_vars = ['Date']).rename(
            columns = {'value': 'Stock Prices(USD)'}
        )

        chart = (
            alt.Chart(data)
            .mark_line(opacity = 0.8, clip = True)
            .encode(
                x = "Date:T",
                y = alt.Y(f"Stock Prices({unit}):Q", stack= None, scale = alt.Scale(domain=[ymin, ymax])),
                color = 'Name:N'
            )
        )
        st.altair_chart(chart, use_container_width = True)

    return



# try:
# サイドバー
st.sidebar.write("""
# 設定
こちらは株価可視化ツールです。以下のオプションから表示日数および株価の範囲を指定できます。
""")

st.sidebar.write("""
## 表示日数選択
""")

days = st.sidebar.slider('日数', 1, 50, 20 )

st.sidebar.write("""
## 株価の範囲指定(単位：USD)
""")

us_ymin, us_ymax = st.sidebar.slider('範囲を指定してください。', 0.0 , 500.0, (0.0, 500.0))




us_tickers = {
    'google': 'GOOGL',
    'amazon': 'AMZN',
    'facebook': 'FB', 
    'apple': 'AAPL',
    'microsoft': 'MSFT',
    'netflix': 'NFLX',
    'tesla': 'TSLA',
    # 'shigabank': '8366.T',
}
type = '米国主要株価'
displayData(days, us_tickers, us_ymin, us_ymax, type, "USD")

st.sidebar.write("""
## 株価の範囲指定(単位：JPY)
""")

jp_ymin, jp_ymax = st.sidebar.slider('範囲を指定してください。', 0.0 , 8500.0, (0.0, 8500.0))

jp_tickers = {
    'ソフトバンクグループ㈱': '9984.T',
    '楽天グループ㈱': '4755.T',
    '東京電力ホールディングス㈱': '9501.T',
    '㈱滋賀銀行': '8366.T',
    '㈱京都銀行': '8369.T'
}
type = '日経主要株価'
displayData(days, jp_tickers, jp_ymin, jp_ymax, type, "JPY")
# us_df = getData(days, us_tickers)

# companies = st.multiselect(
#     '会社名を選択して下さい。',
#     list(us_df.index),
#     ['google', 'amazon', 'facebook', 'apple']
# )
# if not companies:
#     st.error('少なくとも1社は選んでください')
# else:
#     data = us_df.loc[companies]
#     st.write("### 株価(USD)", data.sort_index())
#     data = data.T.reset_index()
#     data = pd.melt(data, id_vars = ['Date']).rename(
#         columns = {'value': 'Stock Prices(USD)'}
#     )

#     chart = (
#         alt.Chart(data)
#         .mark_line(opacity = 0.8, clip = True)
#         .encode(
#             x = "Date:T",
#             y = alt.Y("Stock Prices(USD):Q", stack= None, scale = alt.Scale(domain=[us_ymin, us_ymax])),
#             color = 'Name:N'
#         )
#     )
#     st.altair_chart(chart, use_container_width = True)
# except:
#     st.error(
#         "エラーが発生致しました！"
#     )