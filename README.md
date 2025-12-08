# Streamlit サンプルアプリケーション 🚀

Streamlitを使用したインタラクティブなWebアプリケーションのサンプルです。

## 機能

- 📊 データ可視化（Plotly使用）
- 🎮 インタラクティブなUI要素
- 📈 各種チャート表示
- 🗺️ マップ表示
- 💾 CSVダウンロード機能

## ローカルでの実行

### 前提条件
- Python 3.11以上
- pip

### セットアップ

1. リポジトリをクローン
```bash
git clone <repository-url>
cd test-streamlit-vibecoding-github
```

2. 依存パッケージをインストール
```bash
pip install -r requirements.txt
```

3. アプリケーションを起動
```bash
streamlit run app.py
```

ブラウザで `http://localhost:8501` にアクセスしてください。

## Dockerでの実行

### Dockerイメージのビルド
```bash
docker build -t streamlit-app .
```

### コンテナの起動
```bash
docker run -p 8501:8501 streamlit-app
```

ブラウザで `http://localhost:8501` にアクセスしてください。

## デプロイ

### Streamlit Community Cloud（推奨）
1. [Streamlit Community Cloud](https://streamlit.io/cloud)にサインイン
2. GitHubリポジトリを接続
3. `app.py`を指定してデプロイ

### Docker対応ホスティング
以下のプラットフォームでDockerコンテナとしてデプロイ可能：
- Railway
- Render
- Google Cloud Run
- AWS ECS/Fargate
- Azure Container Apps

## プロジェクト構造

```
.
├── app.py              # メインアプリケーション
├── requirements.txt    # Python依存パッケージ
├── Dockerfile         # Dockerコンテナ設定
├── .dockerignore      # Docker除外ファイル
├── .gitignore         # Git除外ファイル
└── README.md          # このファイル
```

## 技術スタック

- **Streamlit**: Webアプリフレームワーク
- **Pandas**: データ操作
- **NumPy**: 数値計算
- **Plotly**: インタラクティブなグラフ作成

## ライセンス

MIT
