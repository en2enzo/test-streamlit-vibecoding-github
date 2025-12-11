import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import yfinance as yf

# ページ設定
st.set_page_config(
    page_title="Streamlit サンプルアプリ",
    page_icon="🚀",
    layout="wide"
)

# タイトル
st.title("🚀 Streamlit サンプルアプリケーション")
st.markdown("---")

# サイドバー
st.sidebar.header("設定")
option = st.sidebar.selectbox(
    "表示するデモを選択",
    ["ホーム", "データ可視化", "インタラクティブUI", "チャート", "株価分析"]
)

# ホーム画面
if option == "ホーム":
    st.header("👋 ようこそ！")
    st.write("""
    これはStreamlitで作成されたサンプルアプリケーションです。

    **主な機能:**
    - データ可視化
    - インタラクティブなUI要素
    - リアルタイムチャート

    左のサイドバーから各デモを選択してください。
    """)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(label="ユーザー数", value="1,234", delta="123")

    with col2:
        st.metric(label="アクティブセッション", value="456", delta="-12")

    with col3:
        st.metric(label="処理数", value="7,890", delta="345")

# データ可視化
elif option == "データ可視化":
    st.header("📊 データ可視化デモ")

    # サンプルデータの生成
    df = pd.DataFrame({
        '日付': pd.date_range('2024-01-01', periods=100),
        '売上': np.random.randint(100, 1000, 100),
        'カテゴリ': np.random.choice(['A', 'B', 'C'], 100)
    })

    st.subheader("データテーブル")
    st.dataframe(df.head(10))

    st.subheader("売上推移グラフ")
    fig = px.line(df, x='日付', y='売上', color='カテゴリ',
                  title='カテゴリ別売上推移')
    st.plotly_chart(fig, use_container_width=True)

    # ダウンロードボタン
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="CSVダウンロード",
        data=csv,
        file_name='sample_data.csv',
        mime='text/csv',
    )

# インタラクティブUI
elif option == "インタラクティブUI":
    st.header("🎮 インタラクティブUIデモ")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("入力要素")

        name = st.text_input("名前を入力してください")
        age = st.slider("年齢を選択", 0, 100, 25)
        color = st.color_picker("好きな色を選択", "#00f900")

        if st.button("送信"):
            st.success(f"こんにちは、{name}さん！ {age}歳ですね。")

    with col2:
        st.subheader("選択要素")

        choice = st.radio(
            "好きな果物は？",
            ["リンゴ", "バナナ", "オレンジ"]
        )

        multi = st.multiselect(
            "趣味を選択（複数可）",
            ["読書", "スポーツ", "音楽", "旅行", "料理"]
        )

        date = st.date_input("日付を選択", datetime.now())

        st.write(f"選択: {choice}")
        if multi:
            st.write(f"趣味: {', '.join(multi)}")

# チャート
elif option == "チャート":
    st.header("📈 各種チャートデモ")

    # ランダムデータ生成
    chart_data = pd.DataFrame(
        np.random.randn(20, 3),
        columns=['A', 'B', 'C']
    )

    st.subheader("ラインチャート")
    st.line_chart(chart_data)

    st.subheader("エリアチャート")
    st.area_chart(chart_data)

    st.subheader("バーチャート")
    st.bar_chart(chart_data)

    # マップデータ
    st.subheader("マップ")
    map_data = pd.DataFrame(
        np.random.randn(100, 2) / [50, 50] + [35.6762, 139.6503],
        columns=['lat', 'lon']
    )
    st.map(map_data)

# 株価分析
elif option == "株価分析":
    st.header("📊 トヨタ自動車 株価分析ダッシュボード")

    # サイドバーで期間設定
    st.sidebar.subheader("分析設定")
    period_options = {
        "1ヶ月": 30,
        "3ヶ月": 90,
        "6ヶ月": 180,
        "1年": 365,
        "2年": 730,
        "5年": 1825
    }
    period = st.sidebar.selectbox("期間を選択", list(period_options.keys()), index=3)
    days = period_options[period]

    # データ取得
    ticker = "7203.T"  # トヨタ自動車

    with st.spinner('株価データを取得中...'):
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)

        stock = yf.Ticker(ticker)
        df = stock.history(start=start_date, end=end_date)

        if df.empty:
            st.error("データを取得できませんでした。")
        else:
            # 基本情報
            info = stock.info

            # メトリクス表示
            col1, col2, col3, col4 = st.columns(4)

            current_price = df['Close'].iloc[-1]
            prev_price = df['Close'].iloc[-2]
            price_change = current_price - prev_price
            price_change_pct = (price_change / prev_price) * 100

            with col1:
                st.metric(
                    label="現在値",
                    value=f"¥{current_price:,.2f}",
                    delta=f"{price_change:+.2f} ({price_change_pct:+.2f}%)"
                )

            with col2:
                st.metric(
                    label="出来高",
                    value=f"{df['Volume'].iloc[-1]:,.0f}"
                )

            with col3:
                high_52w = df['High'].max()
                st.metric(
                    label=f"{period}高値",
                    value=f"¥{high_52w:,.2f}"
                )

            with col4:
                low_52w = df['Low'].min()
                st.metric(
                    label=f"{period}安値",
                    value=f"¥{low_52w:,.2f}"
                )

            # テクニカル指標の計算
            df['MA5'] = df['Close'].rolling(window=5).mean()
            df['MA25'] = df['Close'].rolling(window=25).mean()
            df['MA75'] = df['Close'].rolling(window=75).mean()

            # RSI計算
            delta = df['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            df['RSI'] = 100 - (100 / (1 + rs))

            # MACD計算
            exp1 = df['Close'].ewm(span=12, adjust=False).mean()
            exp2 = df['Close'].ewm(span=26, adjust=False).mean()
            df['MACD'] = exp1 - exp2
            df['Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()
            df['Histogram'] = df['MACD'] - df['Signal']

            # ボラティリティ計算
            df['Returns'] = df['Close'].pct_change()
            volatility = df['Returns'].std() * np.sqrt(252) * 100

            st.markdown("---")

            # タブで表示を切り替え
            tab1, tab2, tab3, tab4 = st.tabs(["📈 価格チャート", "📊 テクニカル分析", "📉 統計情報", "📋 データ"])

            with tab1:
                st.subheader("ローソク足チャート + 移動平均線")

                # ローソク足チャート
                fig = make_subplots(
                    rows=2, cols=1,
                    shared_xaxes=True,
                    vertical_spacing=0.03,
                    row_heights=[0.7, 0.3],
                    subplot_titles=('株価', '出来高')
                )

                # ローソク足
                fig.add_trace(
                    go.Candlestick(
                        x=df.index,
                        open=df['Open'],
                        high=df['High'],
                        low=df['Low'],
                        close=df['Close'],
                        name='株価'
                    ),
                    row=1, col=1
                )

                # 移動平均線
                fig.add_trace(
                    go.Scatter(x=df.index, y=df['MA5'], name='MA5', line=dict(color='orange', width=1)),
                    row=1, col=1
                )
                fig.add_trace(
                    go.Scatter(x=df.index, y=df['MA25'], name='MA25', line=dict(color='blue', width=1)),
                    row=1, col=1
                )
                fig.add_trace(
                    go.Scatter(x=df.index, y=df['MA75'], name='MA75', line=dict(color='red', width=1)),
                    row=1, col=1
                )

                # 出来高
                colors = ['red' if row['Close'] < row['Open'] else 'green' for idx, row in df.iterrows()]
                fig.add_trace(
                    go.Bar(x=df.index, y=df['Volume'], name='出来高', marker_color=colors),
                    row=2, col=1
                )

                fig.update_layout(
                    height=700,
                    xaxis_rangeslider_visible=False,
                    hovermode='x unified'
                )

                fig.update_yaxes(title_text="価格 (¥)", row=1, col=1)
                fig.update_yaxes(title_text="出来高", row=2, col=1)

                st.plotly_chart(fig, use_container_width=True)

            with tab2:
                st.subheader("テクニカル指標")

                # RSI
                col1, col2 = st.columns(2)

                with col1:
                    st.markdown("### RSI (相対力指数)")
                    fig_rsi = go.Figure()
                    fig_rsi.add_trace(go.Scatter(x=df.index, y=df['RSI'], name='RSI', line=dict(color='purple')))
                    fig_rsi.add_hline(y=70, line_dash="dash", line_color="red", annotation_text="買われすぎ")
                    fig_rsi.add_hline(y=30, line_dash="dash", line_color="green", annotation_text="売られすぎ")
                    fig_rsi.update_layout(height=300, yaxis_range=[0, 100])
                    st.plotly_chart(fig_rsi, use_container_width=True)

                    current_rsi = df['RSI'].iloc[-1]
                    if current_rsi > 70:
                        st.warning(f"現在のRSI: {current_rsi:.2f} - 買われすぎの可能性")
                    elif current_rsi < 30:
                        st.info(f"現在のRSI: {current_rsi:.2f} - 売られすぎの可能性")
                    else:
                        st.success(f"現在のRSI: {current_rsi:.2f} - 中立")

                with col2:
                    st.markdown("### MACD")
                    fig_macd = go.Figure()
                    fig_macd.add_trace(go.Scatter(x=df.index, y=df['MACD'], name='MACD', line=dict(color='blue')))
                    fig_macd.add_trace(go.Scatter(x=df.index, y=df['Signal'], name='Signal', line=dict(color='red')))
                    fig_macd.add_trace(go.Bar(x=df.index, y=df['Histogram'], name='Histogram', marker_color='gray'))
                    fig_macd.update_layout(height=300)
                    st.plotly_chart(fig_macd, use_container_width=True)

                    if df['MACD'].iloc[-1] > df['Signal'].iloc[-1]:
                        st.success("MACD: 買いシグナル")
                    else:
                        st.warning("MACD: 売りシグナル")

                # ボリンジャーバンド
                st.markdown("### ボリンジャーバンド")
                df['BB_middle'] = df['Close'].rolling(window=20).mean()
                df['BB_upper'] = df['BB_middle'] + 2 * df['Close'].rolling(window=20).std()
                df['BB_lower'] = df['BB_middle'] - 2 * df['Close'].rolling(window=20).std()

                fig_bb = go.Figure()
                fig_bb.add_trace(go.Scatter(x=df.index, y=df['Close'], name='終値', line=dict(color='black')))
                fig_bb.add_trace(go.Scatter(x=df.index, y=df['BB_upper'], name='上限', line=dict(color='red', dash='dash')))
                fig_bb.add_trace(go.Scatter(x=df.index, y=df['BB_middle'], name='中央', line=dict(color='blue')))
                fig_bb.add_trace(go.Scatter(x=df.index, y=df['BB_lower'], name='下限', line=dict(color='green', dash='dash')))
                fig_bb.update_layout(height=400)
                st.plotly_chart(fig_bb, use_container_width=True)

            with tab3:
                st.subheader("統計情報")

                col1, col2 = st.columns(2)

                with col1:
                    st.markdown("### 価格統計")
                    stats_df = pd.DataFrame({
                        '指標': ['平均値', '中央値', '標準偏差', '最高値', '最安値', '変動率'],
                        '値': [
                            f"¥{df['Close'].mean():,.2f}",
                            f"¥{df['Close'].median():,.2f}",
                            f"¥{df['Close'].std():,.2f}",
                            f"¥{df['Close'].max():,.2f}",
                            f"¥{df['Close'].min():,.2f}",
                            f"{((df['Close'].iloc[-1] / df['Close'].iloc[0] - 1) * 100):+.2f}%"
                        ]
                    })
                    st.dataframe(stats_df, hide_index=True, use_container_width=True)

                    st.metric(
                        label=f"年率ボラティリティ ({period})",
                        value=f"{volatility:.2f}%"
                    )

                with col2:
                    st.markdown("### リターン分布")
                    fig_hist = go.Figure()
                    fig_hist.add_trace(go.Histogram(x=df['Returns'].dropna() * 100, nbinsx=50, name='日次リターン'))
                    fig_hist.update_layout(
                        xaxis_title='リターン (%)',
                        yaxis_title='頻度',
                        height=300
                    )
                    st.plotly_chart(fig_hist, use_container_width=True)

                    # シャープレシオ（リスクフリーレート0%と仮定）
                    sharpe_ratio = (df['Returns'].mean() / df['Returns'].std()) * np.sqrt(252)
                    st.metric(
                        label="シャープレシオ (年率)",
                        value=f"{sharpe_ratio:.2f}"
                    )

                # 月次リターン
                st.markdown("### 月次リターン")
                df_monthly = df['Close'].resample('M').last().pct_change() * 100
                fig_monthly = go.Figure()
                colors_monthly = ['red' if x < 0 else 'green' for x in df_monthly]
                fig_monthly.add_trace(go.Bar(
                    x=df_monthly.index,
                    y=df_monthly.values,
                    marker_color=colors_monthly,
                    name='月次リターン'
                ))
                fig_monthly.update_layout(
                    xaxis_title='月',
                    yaxis_title='リターン (%)',
                    height=300
                )
                st.plotly_chart(fig_monthly, use_container_width=True)

            with tab4:
                st.subheader("株価データ")

                # データ表示オプション
                show_rows = st.selectbox("表示行数", [10, 25, 50, 100, "全て"], index=0)

                display_df = df[['Open', 'High', 'Low', 'Close', 'Volume', 'MA5', 'MA25', 'RSI', 'MACD']].copy()
                display_df.columns = ['始値', '高値', '安値', '終値', '出来高', 'MA5', 'MA25', 'RSI', 'MACD']

                if show_rows == "全て":
                    st.dataframe(display_df, use_container_width=True)
                else:
                    st.dataframe(display_df.tail(int(show_rows)), use_container_width=True)

                # CSVダウンロード
                csv = display_df.to_csv().encode('utf-8')
                st.download_button(
                    label="📥 CSVダウンロード",
                    data=csv,
                    file_name=f'toyota_{period}_stock_data.csv',
                    mime='text/csv',
                )

            # 企業情報
            st.markdown("---")
            st.subheader("📋 企業情報")

            col1, col2, col3 = st.columns(3)

            with col1:
                st.write(f"**企業名:** {info.get('longName', 'N/A')}")
                st.write(f"**セクター:** {info.get('sector', 'N/A')}")
                st.write(f"**産業:** {info.get('industry', 'N/A')}")

            with col2:
                st.write(f"**時価総額:** ¥{info.get('marketCap', 0):,.0f}")
                st.write(f"**PER:** {info.get('trailingPE', 'N/A')}")
                st.write(f"**PBR:** {info.get('priceToBook', 'N/A')}")

            with col3:
                st.write(f"**配当利回り:** {info.get('dividendYield', 0) * 100:.2f}%" if info.get('dividendYield') else "N/A")
                st.write(f"**52週高値:** ¥{info.get('fiftyTwoWeekHigh', 'N/A')}")
                st.write(f"**52週安値:** ¥{info.get('fiftyTwoWeekLow', 'N/A')}")

# フッター
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center'>
        <p>Streamlit サンプルアプリ | Powered by Streamlit 🎈</p>
    </div>
    """,
    unsafe_allow_html=True
)
