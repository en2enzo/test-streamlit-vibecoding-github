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

### Vercel（情報ページのみ）
1. [Vercel](https://vercel.com)にサインイン
2. GitHubリポジトリをインポート
3. デプロイ

**重要**: StreamlitはWebSocketを使用する長時間実行型アプリのため、Vercelのサーバーレス環境では**Streamlitアプリ本体は動作しません**。Vercelにデプロイすると、代わりに情報ページが表示され、推奨デプロイ方法とローカル実行手順が案内されます。

### Streamlit Community Cloud（推奨）
Streamlitアプリを実際に動かすには以下を推奨：

1. [Streamlit Community Cloud](https://streamlit.io/cloud)にサインイン
2. GitHubリポジトリを接続
3. `app.py`を指定してデプロイ

### Docker対応ホスティング（推奨）
以下のプラットフォームでDockerコンテナとしてデプロイ可能：
- **Railway** - 簡単で初心者向け
- **Render** - 無料プランあり
- **Google Cloud Run** - スケーラブル
- **AWS ECS/Fargate** - エンタープライズ向け
- **Azure Container Apps** - Azure環境

## プロジェクト構造

```
.
├── api/
│   └── index.py       # Vercel用情報ページ
├── app.py             # メインStreamlitアプリ
├── requirements.txt   # Python依存パッケージ
├── Dockerfile         # Dockerコンテナ設定
├── vercel.json        # Vercel設定
├── .dockerignore      # Docker除外ファイル
├── .gitignore         # Git除外ファイル
└── README.md          # このファイル
```

## 技術スタック

- **Streamlit**: Webアプリフレームワーク
- **Pandas**: データ操作
- **NumPy**: 数値計算
- **Plotly**: インタラクティブなグラフ作成
- **FastAPI**: Vercel用情報ページ

## ライセンス

MIT
