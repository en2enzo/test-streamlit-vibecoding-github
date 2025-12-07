import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime

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
    ["ホーム", "データ可視化", "インタラクティブUI", "チャート"]
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
