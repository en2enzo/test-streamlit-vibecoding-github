import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import yfinance as yf
import folium
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import time
import re
import fastf1
import warnings
import os

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
    ["ホーム", "データ可視化", "インタラクティブUI", "チャート", "株価分析", "イトーヨーカドー店舗マップ", "F1分析"]
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

# イトーヨーカドー店舗マップ
elif option == "イトーヨーカドー店舗マップ":
    st.header("🏪 イトーヨーカドー店舗マップ")
    st.write("日本全国のイトーヨーカドー店舗を地図上に表示します。")

    # list_store.txtから店舗データを読み込む
    @st.cache_data
    def load_store_data():
        """list_store.txtから店舗データ（緯度経度を含む）を読み込む"""
        try:
            # ファイルを読み込み
            with open('list_store.txt', 'r', encoding='utf-8') as f:
                lines = f.readlines()

            # データをパース
            stores = []
            for line in lines[2:]:  # ヘッダー行をスキップ
                if line.strip() and line.startswith('|'):
                    parts = [p.strip() for p in line.split('|')]
                    if len(parts) >= 4 and parts[1].strip():
                        no = parts[1]
                        name = parts[2]
                        address = parts[3]

                        # 緯度経度がある場合は取得
                        lat = parts[4] if len(parts) > 4 and parts[4].strip() else None
                        lon = parts[5] if len(parts) > 5 and parts[5].strip() else None

                        # 郵便番号を削除して住所のみ抽出
                        address_clean = re.sub(r'〒\d{3}-\d{4}\s*', '', address)

                        # 都道府県を抽出
                        pref_match = re.match(r'([^都道府県]+[都道府県])', address_clean)
                        prefecture = pref_match.group(1) if pref_match else '不明'

                        # 緯度経度が空でない場合のみ追加
                        if lat and lon:
                            try:
                                stores.append({
                                    'No': no,
                                    '店舗名': name,
                                    '住所': address_clean,
                                    '緯度': float(lat),
                                    '経度': float(lon),
                                    '都道府県': prefecture
                                })
                            except ValueError:
                                # 緯度経度の変換に失敗した場合はスキップ
                                pass

            df = pd.DataFrame(stores)
            return df

        except FileNotFoundError:
            st.error("list_store.txtファイルが見つかりません。")
            return pd.DataFrame()
        except Exception as e:
            st.error(f"エラーが発生しました: {str(e)}")
            return pd.DataFrame()

    # データ読み込み
    with st.spinner('店舗データを読み込み中...'):
        df_stores = load_store_data()

    if df_stores.empty:
        st.warning("店舗データを読み込めませんでした。")
    else:
        # サイドバーでフィルター
        st.sidebar.subheader("表示設定")
        selected_prefectures = st.sidebar.multiselect(
            "都道府県で絞り込み",
            options=sorted(df_stores['都道府県'].unique()),
            default=sorted(df_stores['都道府県'].unique())
        )

        # フィルタリング
        filtered_df = df_stores[df_stores['都道府県'].isin(selected_prefectures)]

        # 統計情報
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("総店舗数", len(df_stores))
        with col2:
            st.metric("表示店舗数", len(filtered_df))
        with col3:
            st.metric("都道府県数", len(filtered_df['都道府県'].unique()))

        st.markdown("---")

        # タブで表示切り替え
        tab1, tab2 = st.tabs(["🗺️ 地図表示", "📋 店舗一覧"])

        with tab1:
            st.subheader("店舗マップ")

            if len(filtered_df) == 0:
                st.warning("選択された都道府県に店舗がありません。")
            else:
                # 地図の中心を計算
                center_lat = filtered_df['緯度'].mean()
                center_lon = filtered_df['経度'].mean()

                # Foliumマップの作成
                m = folium.Map(
                    location=[center_lat, center_lon],
                    zoom_start=6,
                    tiles='OpenStreetMap'
                )

                # マーカーを追加
                for idx, row in filtered_df.iterrows():
                    # ポップアップの内容
                    popup_html = f"""
                    <div style="font-family: Arial; width: 200px;">
                        <h4 style="color: #00843D; margin-bottom: 10px;">🏪 {row['店舗名']}</h4>
                        <p style="margin: 5px 0;"><strong>住所:</strong><br>{row['住所']}</p>
                        <p style="margin: 5px 0;"><strong>都道府県:</strong> {row['都道府県']}</p>
                    </div>
                    """

                    folium.Marker(
                        location=[row['緯度'], row['経度']],
                        popup=folium.Popup(popup_html, max_width=300),
                        tooltip=row['店舗名'],
                        icon=folium.Icon(color='green', icon='shopping-cart', prefix='fa')
                    ).add_to(m)

                # マップを表示
                st_folium(m, width=None, height=600)

                # 地図の使い方
                with st.expander("💡 地図の使い方"):
                    st.write("""
                    - **マーカーをクリック**: 店舗の詳細情報を表示
                    - **マーカーにホバー**: 店舗名を表示
                    - **ズーム**: マウスホイールまたは+/-ボタンでズーム
                    - **移動**: 地図をドラッグして移動
                    - **絞り込み**: 左のサイドバーで都道府県を選択
                    """)

        with tab2:
            st.subheader("店舗一覧")

            # 検索機能
            search_query = st.text_input("🔍 店舗名で検索", "")

            search_filtered_df = filtered_df.copy()
            if search_query:
                search_filtered_df = search_filtered_df[search_filtered_df['店舗名'].str.contains(search_query, case=False)]

            # 並び替え
            sort_by = st.selectbox("並び替え", ["店舗名", "都道府県"])
            search_filtered_df = search_filtered_df.sort_values(by=sort_by)

            # 店舗一覧表示
            st.dataframe(
                search_filtered_df[['店舗名', '都道府県', '住所', '緯度', '経度']],
                use_container_width=True,
                hide_index=True
            )

            # CSVダウンロード
            csv = search_filtered_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 CSVダウンロード",
                data=csv,
                file_name='ito_yokado_stores.csv',
                mime='text/csv',
            )

            # 都道府県別統計
            st.markdown("---")
            st.subheader("都道府県別店舗数")

            prefecture_counts = filtered_df['都道府県'].value_counts().reset_index()
            prefecture_counts.columns = ['都道府県', '店舗数']

            fig = px.bar(
                prefecture_counts,
                x='都道府県',
                y='店舗数',
                title='都道府県別イトーヨーカドー店舗数',
                color='店舗数',
                color_continuous_scale='Greens'
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)

        # 注意事項
        st.markdown("---")
        st.info("ℹ️ **情報**: list_store.txtに記載されている緯度経度情報を使用して店舗を表示しています。")

# F1分析
elif option == "F1分析":
    st.header("🏎️ F1分析ダッシュボード")
    st.write("Fast-F1ライブラリを使用してF1データを分析・可視化します。")

    # Fast-F1のキャッシュを有効化
    warnings.filterwarnings('ignore')
    cache_dir = 'cache'
    os.makedirs(cache_dir, exist_ok=True)
    fastf1.Cache.enable_cache(cache_dir)

    # サイドバー設定
    st.sidebar.subheader("分析設定")

    # 年とグランプリを選択
    year = st.sidebar.selectbox(
        "シーズンを選択",
        [2024, 2023, 2022, 2021, 2020],
        index=0
    )

    # サンプルのグランプリリスト
    grand_prix_options = {
        2024: ["Bahrain", "Saudi Arabia", "Australia", "Japan", "Miami", "Monaco", "Spain", "Canada", "Austria", "Great Britain"],
        2023: ["Bahrain", "Saudi Arabia", "Australia", "Japan", "Miami", "Monaco", "Spain", "Canada", "Austria", "Great Britain"],
        2022: ["Bahrain", "Saudi Arabia", "Australia", "Japan", "Miami", "Monaco", "Spain", "Canada", "Austria", "Great Britain"],
        2021: ["Bahrain", "Saudi Arabia", "Australia", "Japan", "Miami", "Monaco", "Spain", "Canada", "Austria", "Great Britain"],
        2020: ["Bahrain", "Saudi Arabia", "Australia", "Japan", "Miami", "Monaco", "Spain", "Canada", "Austria", "Great Britain"]
    }

    gp = st.sidebar.selectbox(
        "グランプリを選択",
        grand_prix_options.get(year, ["Bahrain"]),
        index=0
    )

    session_type = st.sidebar.selectbox(
        "セッション種別",
        ["Race", "Qualifying", "Sprint", "Practice 1", "Practice 2", "Practice 3"],
        index=0
    )

    # データ読み込み
    try:
        with st.spinner(f'{year} {gp} Grand Prix {session_type}のデータを読み込み中...'):
            # セッションデータを取得
            session = fastf1.get_session(year, gp, session_type)
            session.load()

            # 統計情報
            st.markdown("---")
            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("シーズン", year)
            with col2:
                st.metric("グランプリ", gp)
            with col3:
                st.metric("セッション", session_type)

            st.markdown("---")

            # タブで表示を切り替え
            tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 ラップタイム分析", "🏎️ ドライビング特性", "🏁 ドライバー比較", "⚡ テレメトリ", "📋 データ"])

            with tab1:
                st.subheader("ラップタイム分析")

                # ラップデータを取得
                laps = session.laps

                if not laps.empty:
                    # ドライバーごとのラップタイムをプロット
                    drivers = laps['Driver'].unique()

                    # ラップタイムを秒に変換
                    laps['LapTimeSeconds'] = laps['LapTime'].dt.total_seconds()

                    # 外れ値を除外（例：ピットインラップ）
                    laps_clean = laps[laps['LapTimeSeconds'].notna()]
                    median_time = laps_clean['LapTimeSeconds'].median()
                    laps_clean = laps_clean[
                        (laps_clean['LapTimeSeconds'] < median_time * 1.1) &
                        (laps_clean['LapTimeSeconds'] > median_time * 0.9)
                    ]

                    # ドライバー選択（複数選択可能）
                    selected_drivers = st.multiselect(
                        "表示するドライバーを選択（複数選択可）",
                        options=sorted(drivers.tolist()),
                        default=sorted(drivers.tolist())[:5] if len(drivers) > 5 else sorted(drivers.tolist())
                    )

                    if selected_drivers:
                        # 選択されたドライバーのデータをフィルタ
                        filtered_laps = laps_clean[laps_clean['Driver'].isin(selected_drivers)]

                        # ラップタイム推移グラフ（折れ線）
                        fig = px.line(
                            filtered_laps,
                            x='LapNumber',
                            y='LapTimeSeconds',
                            color='Driver',
                            title=f'{year} {gp} GP - ラップタイム推移',
                            labels={'LapNumber': 'ラップ番号', 'LapTimeSeconds': 'ラップタイム (秒)'},
                            markers=True,
                            hover_data=['Compound', 'TyreLife']
                        )

                        fig.update_layout(height=500, hovermode='x unified')
                        st.plotly_chart(fig, use_container_width=True)

                        # ドライバー別平均ラップタイム
                        st.subheader("ドライバー別統計")
                        avg_laptimes = filtered_laps.groupby('Driver')['LapTimeSeconds'].agg(['mean', 'min', 'max', 'std']).reset_index()

                        # ラップ数も追加
                        lap_counts = filtered_laps.groupby('Driver').size().reset_index(name='ラップ数')
                        avg_laptimes = avg_laptimes.merge(lap_counts, on='Driver')

                        # カラム名を日本語に変更
                        avg_laptimes.columns = ['ドライバー', '平均 (秒)', '最速 (秒)', '最遅 (秒)', '標準偏差', 'ラップ数']
                        avg_laptimes = avg_laptimes.sort_values('平均 (秒)')

                        # 平均ラップタイムの棒グラフ
                        fig_avg = px.bar(
                            avg_laptimes,
                            x='ドライバー',
                            y='平均 (秒)',
                            title='ドライバー別平均ラップタイム',
                            color='平均 (秒)',
                            color_continuous_scale='Viridis',
                            text='平均 (秒)'
                        )
                        fig_avg.update_traces(texttemplate='%{text:.2f}', textposition='outside')
                        fig_avg.update_layout(height=400)
                        st.plotly_chart(fig_avg, use_container_width=True)

                        # データテーブル
                        st.dataframe(avg_laptimes.round(3), hide_index=True, use_container_width=True)
                    else:
                        st.warning("ドライバーを選択してください。")
                else:
                    st.warning("ラップデータが見つかりませんでした。")

            with tab2:
                st.subheader("ドライビング特性比較")

                # ラップデータを取得
                laps = session.laps

                if not laps.empty:
                    # ラップタイムを秒に変換（最初に設定）
                    if 'LapTimeSeconds' not in laps.columns:
                        laps['LapTimeSeconds'] = laps['LapTime'].dt.total_seconds()

                    # ドライバー選択（複数選択可能）
                    drivers = laps['Driver'].unique()
                    selected_drivers_char = st.multiselect(
                        "比較するドライバーを選択",
                        options=sorted(drivers.tolist()),
                        default=sorted(drivers.tolist())[:3] if len(drivers) > 3 else sorted(drivers.tolist()),
                        key='char_drivers'
                    )

                    if selected_drivers_char:
                        # セクタータイム比較
                        st.markdown("### セクタータイム比較")
                        sector_data = []
                        for driver in selected_drivers_char:
                            driver_laps = laps.pick_driver(driver)
                            if not driver_laps.empty:
                                # セクタータイムを秒に変換
                                s1 = driver_laps['Sector1Time'].dt.total_seconds()
                                s2 = driver_laps['Sector2Time'].dt.total_seconds()
                                s3 = driver_laps['Sector3Time'].dt.total_seconds()

                                # 有効なラップのみ
                                valid_s1 = s1[s1.notna()]
                                valid_s2 = s2[s2.notna()]
                                valid_s3 = s3[s3.notna()]

                                if not valid_s1.empty and not valid_s2.empty and not valid_s3.empty:
                                    sector_data.append({
                                        'ドライバー': driver,
                                        'セクター1 (秒)': valid_s1.mean(),
                                        'セクター2 (秒)': valid_s2.mean(),
                                        'セクター3 (秒)': valid_s3.mean()
                                    })

                        if sector_data:
                            sector_df = pd.DataFrame(sector_data)

                            # セクター別の折れ線グラフ
                            fig_sector = go.Figure()

                            for sector in ['セクター1 (秒)', 'セクター2 (秒)', 'セクター3 (秒)']:
                                fig_sector.add_trace(go.Scatter(
                                    x=sector_df['ドライバー'],
                                    y=sector_df[sector],
                                    mode='lines+markers',
                                    name=sector,
                                    line=dict(width=3),
                                    marker=dict(size=10)
                                ))

                            fig_sector.update_layout(
                                title='セクター別平均タイム比較',
                                xaxis_title='ドライバー',
                                yaxis_title='平均タイム (秒)',
                                height=400,
                                hovermode='x unified'
                            )
                            st.plotly_chart(fig_sector, use_container_width=True)

                            # セクタータイムのデータテーブル
                            st.dataframe(sector_df.round(3), hide_index=True, use_container_width=True)
                        else:
                            st.warning("セクタータイムデータが見つかりませんでした。")

                        # タイヤコンパウンド別ペース比較
                        st.markdown("### タイヤコンパウンド別ペース")

                        compound_data = []
                        for driver in selected_drivers_char:
                            driver_laps = laps.pick_driver(driver)
                            if not driver_laps.empty and 'Compound' in driver_laps.columns:
                                for compound in driver_laps['Compound'].dropna().unique():
                                    compound_laps = driver_laps[driver_laps['Compound'] == compound]
                                    valid_times = compound_laps['LapTimeSeconds'].dropna()
                                    if len(valid_times) > 0:
                                        # 外れ値除去
                                        median = valid_times.median()
                                        valid_times = valid_times[
                                            (valid_times < median * 1.1) &
                                            (valid_times > median * 0.9)
                                        ]
                                        if len(valid_times) > 0:
                                            compound_data.append({
                                                'ドライバー': driver,
                                                'タイヤ': compound,
                                                '平均ラップタイム (秒)': valid_times.mean(),
                                                'ラップ数': len(valid_times)
                                            })

                        if compound_data:
                            compound_df = pd.DataFrame(compound_data)

                            fig_compound = px.line(
                                compound_df,
                                x='タイヤ',
                                y='平均ラップタイム (秒)',
                                color='ドライバー',
                                title='タイヤコンパウンド別平均ラップタイム',
                                markers=True,
                                line_shape='linear'
                            )
                            fig_compound.update_layout(height=400, hovermode='x unified')
                            st.plotly_chart(fig_compound, use_container_width=True)

                            st.dataframe(compound_df.round(3), hide_index=True, use_container_width=True)
                        else:
                            st.warning("タイヤコンパウンドデータが見つかりませんでした。")

                        # ペース安定性比較（標準偏差）
                        st.markdown("### ペース安定性比較")

                        stability_data = []
                        for driver in selected_drivers_char:
                            driver_laps = laps.pick_driver(driver)
                            if not driver_laps.empty:
                                valid_times = driver_laps['LapTimeSeconds'].dropna()
                                if len(valid_times) > 1:
                                    # 外れ値除去
                                    median = valid_times.median()
                                    valid_times = valid_times[
                                        (valid_times < median * 1.1) &
                                        (valid_times > median * 0.9)
                                    ]
                                    if len(valid_times) > 1:
                                        stability_data.append({
                                            'ドライバー': driver,
                                            '標準偏差 (秒)': valid_times.std(),
                                            '平均 (秒)': valid_times.mean(),
                                            '変動係数 (%)': (valid_times.std() / valid_times.mean() * 100)
                                        })

                        if stability_data:
                            stability_df = pd.DataFrame(stability_data).sort_values('標準偏差 (秒)')

                            fig_stability = go.Figure()
                            fig_stability.add_trace(go.Scatter(
                                x=stability_df['ドライバー'],
                                y=stability_df['標準偏差 (秒)'],
                                mode='lines+markers',
                                name='標準偏差',
                                line=dict(color='red', width=3),
                                marker=dict(size=12)
                            ))
                            fig_stability.update_layout(
                                title='ペース安定性（標準偏差が小さいほど安定）',
                                xaxis_title='ドライバー',
                                yaxis_title='標準偏差 (秒)',
                                height=400
                            )
                            st.plotly_chart(fig_stability, use_container_width=True)

                            st.dataframe(stability_df.round(3), hide_index=True, use_container_width=True)
                            st.info("💡 **標準偏差が小さいほどペースが安定しています。変動係数はペースのばらつきをパーセンテージで表します。**")
                        else:
                            st.warning("ペース安定性データを計算できませんでした。")

                    else:
                        st.warning("ドライバーを選択してください。")
                else:
                    st.warning("ラップデータが見つかりませんでした。")

            with tab3:
                st.subheader("ドライバー比較")

                # ドライバー選択
                available_drivers = laps['Driver'].unique().tolist()

                col1, col2 = st.columns(2)
                with col1:
                    driver1 = st.selectbox("ドライバー 1", available_drivers, index=0)
                with col2:
                    driver2_index = min(1, len(available_drivers) - 1)
                    driver2 = st.selectbox("ドライバー 2", available_drivers, index=driver2_index)

                # 2人のドライバーのラップを比較
                driver1_laps = laps.pick_driver(driver1)
                driver2_laps = laps.pick_driver(driver2)

                if not driver1_laps.empty and not driver2_laps.empty:
                    # ラップタイム比較
                    driver1_laps['LapTimeSeconds'] = driver1_laps['LapTime'].dt.total_seconds()
                    driver2_laps['LapTimeSeconds'] = driver2_laps['LapTime'].dt.total_seconds()

                    # 比較データフレームを作成
                    comparison_df = pd.DataFrame({
                        'LapNumber': list(driver1_laps['LapNumber']) + list(driver2_laps['LapNumber']),
                        'LapTime': list(driver1_laps['LapTimeSeconds']) + list(driver2_laps['LapTimeSeconds']),
                        'Driver': [driver1] * len(driver1_laps) + [driver2] * len(driver2_laps)
                    })

                    # 外れ値除去
                    comparison_df = comparison_df[comparison_df['LapTime'].notna()]
                    median = comparison_df['LapTime'].median()
                    comparison_df = comparison_df[
                        (comparison_df['LapTime'] < median * 1.1) &
                        (comparison_df['LapTime'] > median * 0.9)
                    ]

                    # プロット
                    fig_comp = px.line(
                        comparison_df,
                        x='LapNumber',
                        y='LapTime',
                        color='Driver',
                        title=f'{driver1} vs {driver2} - ラップタイム比較',
                        labels={'LapNumber': 'ラップ番号', 'LapTime': 'ラップタイム (秒)'},
                        markers=True
                    )
                    fig_comp.update_layout(height=500)
                    st.plotly_chart(fig_comp, use_container_width=True)

                    # 統計比較
                    col1, col2 = st.columns(2)

                    with col1:
                        st.markdown(f"### {driver1} 統計")
                        d1_clean = driver1_laps[driver1_laps['LapTimeSeconds'].notna()]
                        if not d1_clean.empty:
                            st.metric("平均ラップタイム", f"{d1_clean['LapTimeSeconds'].mean():.3f}秒")
                            st.metric("最速ラップ", f"{d1_clean['LapTimeSeconds'].min():.3f}秒")
                            st.metric("ラップ数", len(d1_clean))

                    with col2:
                        st.markdown(f"### {driver2} 統計")
                        d2_clean = driver2_laps[driver2_laps['LapTimeSeconds'].notna()]
                        if not d2_clean.empty:
                            st.metric("平均ラップタイム", f"{d2_clean['LapTimeSeconds'].mean():.3f}秒")
                            st.metric("最速ラップ", f"{d2_clean['LapTimeSeconds'].min():.3f}秒")
                            st.metric("ラップ数", len(d2_clean))

                    # セクタータイム比較
                    st.markdown("---")
                    st.subheader("セクタータイム比較")

                    # セクタータイムデータを取得
                    sector_comparison = []
                    for driver, driver_laps_data in [(driver1, driver1_laps), (driver2, driver2_laps)]:
                        s1 = driver_laps_data['Sector1Time'].dt.total_seconds()
                        s2 = driver_laps_data['Sector2Time'].dt.total_seconds()
                        s3 = driver_laps_data['Sector3Time'].dt.total_seconds()

                        valid_s1 = s1[s1.notna()]
                        valid_s2 = s2[s2.notna()]
                        valid_s3 = s3[s3.notna()]

                        if not valid_s1.empty and not valid_s2.empty and not valid_s3.empty:
                            sector_comparison.append({
                                'ドライバー': driver,
                                'セクター1': valid_s1.mean(),
                                'セクター2': valid_s2.mean(),
                                'セクター3': valid_s3.mean()
                            })

                    if sector_comparison:
                        sector_comp_df = pd.DataFrame(sector_comparison)

                        # セクター別比較グラフ
                        fig_sector_comp = go.Figure()

                        sectors = ['セクター1', 'セクター2', 'セクター3']
                        colors = ['blue', 'green', 'red']

                        for i, sector in enumerate(sectors):
                            fig_sector_comp.add_trace(go.Scatter(
                                x=sector_comp_df['ドライバー'],
                                y=sector_comp_df[sector],
                                mode='lines+markers',
                                name=sector,
                                line=dict(width=3, color=colors[i]),
                                marker=dict(size=12)
                            ))

                        fig_sector_comp.update_layout(
                            title=f'{driver1} vs {driver2} - セクター別平均タイム',
                            xaxis_title='ドライバー',
                            yaxis_title='平均タイム (秒)',
                            height=400,
                            hovermode='x unified'
                        )
                        st.plotly_chart(fig_sector_comp, use_container_width=True)

                        # セクタータイムの差分表示
                        if len(sector_comp_df) == 2:
                            st.markdown("### セクター別タイム差")
                            diff_data = {
                                'セクター': sectors,
                                f'{driver1} (秒)': [sector_comp_df.iloc[0]['セクター1'],
                                                  sector_comp_df.iloc[0]['セクター2'],
                                                  sector_comp_df.iloc[0]['セクター3']],
                                f'{driver2} (秒)': [sector_comp_df.iloc[1]['セクター1'],
                                                  sector_comp_df.iloc[1]['セクター2'],
                                                  sector_comp_df.iloc[1]['セクター3']],
                                '差 (秒)': [
                                    sector_comp_df.iloc[1]['セクター1'] - sector_comp_df.iloc[0]['セクター1'],
                                    sector_comp_df.iloc[1]['セクター2'] - sector_comp_df.iloc[0]['セクター2'],
                                    sector_comp_df.iloc[1]['セクター3'] - sector_comp_df.iloc[0]['セクター3']
                                ]
                            }
                            diff_df = pd.DataFrame(diff_data)
                            st.dataframe(diff_df.round(3), hide_index=True, use_container_width=True)
                    else:
                        st.warning("セクタータイムデータが見つかりませんでした。")
                else:
                    st.warning("選択したドライバーのデータが見つかりませんでした。")

            with tab4:
                st.subheader("テレメトリデータ")

                # ドライバー選択
                selected_driver = st.selectbox(
                    "ドライバーを選択",
                    available_drivers,
                    key='telemetry_driver'
                )

                # ラップ番号選択
                driver_laps = laps.pick_driver(selected_driver)
                if not driver_laps.empty:
                    lap_numbers = driver_laps['LapNumber'].unique().tolist()
                    selected_lap = st.selectbox("ラップ番号を選択", lap_numbers)

                    # テレメトリデータを取得
                    try:
                        lap = driver_laps[driver_laps['LapNumber'] == selected_lap].iloc[0]
                        telemetry = lap.get_telemetry()

                        if not telemetry.empty:
                            # 速度グラフ
                            st.markdown("#### 速度")
                            fig_speed = go.Figure()
                            fig_speed.add_trace(go.Scatter(
                                x=telemetry['Distance'],
                                y=telemetry['Speed'],
                                mode='lines',
                                name='速度',
                                line=dict(color='red')
                            ))
                            fig_speed.update_layout(
                                xaxis_title='距離 (m)',
                                yaxis_title='速度 (km/h)',
                                height=300
                            )
                            st.plotly_chart(fig_speed, use_container_width=True)

                            # スロットル・ブレーキ
                            st.markdown("#### スロットル・ブレーキ")
                            fig_tb = go.Figure()
                            fig_tb.add_trace(go.Scatter(
                                x=telemetry['Distance'],
                                y=telemetry['Throttle'],
                                mode='lines',
                                name='スロットル',
                                line=dict(color='green')
                            ))
                            fig_tb.add_trace(go.Scatter(
                                x=telemetry['Distance'],
                                y=telemetry['Brake'],
                                mode='lines',
                                name='ブレーキ',
                                line=dict(color='red')
                            ))
                            fig_tb.update_layout(
                                xaxis_title='距離 (m)',
                                yaxis_title='入力 (%)',
                                height=300
                            )
                            st.plotly_chart(fig_tb, use_container_width=True)

                            # ギア
                            st.markdown("#### ギア")
                            fig_gear = go.Figure()
                            fig_gear.add_trace(go.Scatter(
                                x=telemetry['Distance'],
                                y=telemetry['nGear'],
                                mode='lines',
                                name='ギア',
                                line=dict(color='blue')
                            ))
                            fig_gear.update_layout(
                                xaxis_title='距離 (m)',
                                yaxis_title='ギア',
                                height=300
                            )
                            st.plotly_chart(fig_gear, use_container_width=True)
                        else:
                            st.warning("テレメトリデータが見つかりませんでした。")
                    except Exception as e:
                        st.error(f"テレメトリデータの読み込みエラー: {str(e)}")
                else:
                    st.warning("選択したドライバーのデータが見つかりませんでした。")

            with tab5:
                st.subheader("セッションデータ")

                # ラップデータ表示
                if not laps.empty:
                    # 表示するカラムを選択
                    display_columns = ['LapNumber', 'Driver', 'LapTime', 'Sector1Time', 'Sector2Time',
                                       'Sector3Time', 'Compound', 'TyreLife', 'TrackStatus']

                    # カラムが存在するか確認
                    available_columns = [col for col in display_columns if col in laps.columns]

                    display_df = laps[available_columns].copy()

                    # 日本語カラム名
                    column_mapping = {
                        'LapNumber': 'ラップ番号',
                        'Driver': 'ドライバー',
                        'LapTime': 'ラップタイム',
                        'Sector1Time': 'セクター1',
                        'Sector2Time': 'セクター2',
                        'Sector3Time': 'セクター3',
                        'Compound': 'タイヤ',
                        'TyreLife': 'タイヤ寿命',
                        'TrackStatus': 'トラック状況'
                    }

                    display_df = display_df.rename(columns=column_mapping)

                    # 表示行数選択
                    show_rows = st.selectbox("表示行数", [10, 25, 50, 100, "全て"], index=0, key='f1_rows')

                    if show_rows == "全て":
                        st.dataframe(display_df, use_container_width=True, hide_index=True)
                    else:
                        st.dataframe(display_df.head(int(show_rows)), use_container_width=True, hide_index=True)

                    # CSVダウンロード
                    csv = display_df.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="📥 CSVダウンロード",
                        data=csv,
                        file_name=f'f1_{year}_{gp}_{session_type}_data.csv',
                        mime='text/csv',
                    )
                else:
                    st.warning("データが見つかりませんでした。")

            # セッション情報
            st.markdown("---")
            st.subheader("📋 セッション情報")

            col1, col2, col3 = st.columns(3)

            with col1:
                st.write(f"**イベント名:** {session.event['EventName']}")
                st.write(f"**開催地:** {session.event['Location']}")
                st.write(f"**国:** {session.event['Country']}")

            with col2:
                st.write(f"**サーキット:** {session.event.get('OfficialEventName', 'N/A')}")
                st.write(f"**セッション:** {session_type}")
                st.write(f"**シーズン:** {year}")

            with col3:
                if hasattr(session, 'date'):
                    st.write(f"**日付:** {session.date}")
                st.write(f"**総ラップ数:** {len(laps)}")
                st.write(f"**参加ドライバー数:** {len(laps['Driver'].unique())}")

    except Exception as e:
        st.error(f"データの読み込みに失敗しました: {str(e)}")
        st.info("""
        **ヒント:**
        - インターネット接続を確認してください
        - 別のグランプリまたはシーズンを選択してみてください
        - Fast-F1のキャッシュが破損している可能性があります
        """)

    # 注意事項
    st.markdown("---")
    st.info("""
    ℹ️ **情報**:
    - このページはFast-F1ライブラリを使用してF1の公式データを取得・分析しています
    - データの読み込みには時間がかかる場合があります
    - キャッシュを使用して2回目以降の読み込みを高速化しています
    """)

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
