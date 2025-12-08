from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/")
async def root():
    return HTMLResponse("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Streamlit App</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 800px;
                margin: 50px auto;
                padding: 20px;
                text-align: center;
            }
            .warning {
                background-color: #fff3cd;
                border: 1px solid #ffc107;
                border-radius: 5px;
                padding: 20px;
                margin: 20px 0;
            }
            .info {
                background-color: #d1ecf1;
                border: 1px solid #0c5460;
                border-radius: 5px;
                padding: 20px;
                margin: 20px 0;
            }
            a {
                color: #007bff;
                text-decoration: none;
            }
            a:hover {
                text-decoration: underline;
            }
        </style>
    </head>
    <body>
        <h1>🚀 Streamlit アプリケーション</h1>

        <div class="warning">
            <h2>⚠️ 重要なお知らせ</h2>
            <p>StreamlitはWebSocketを使用する長時間実行型のアプリケーションのため、Vercelのサーバーレス環境では<strong>正常に動作しません</strong>。</p>
        </div>

        <div class="info">
            <h2>✅ 推奨デプロイ方法</h2>
            <ul style="text-align: left;">
                <li><strong>Streamlit Community Cloud</strong> - 無料で簡単にデプロイ可能<br>
                    <a href="https://streamlit.io/cloud" target="_blank">https://streamlit.io/cloud</a>
                </li>
                <li><strong>Railway</strong> - Dockerコンテナで簡単デプロイ<br>
                    <a href="https://railway.app" target="_blank">https://railway.app</a>
                </li>
                <li><strong>Render</strong> - 無料プランあり<br>
                    <a href="https://render.com" target="_blank">https://render.com</a>
                </li>
            </ul>
        </div>

        <h2>📦 ローカルでの実行</h2>
        <pre style="background-color: #f5f5f5; padding: 15px; border-radius: 5px; text-align: left;">
pip install -r requirements.txt
streamlit run app.py
        </pre>

        <h2>🐳 Dockerでの実行</h2>
        <pre style="background-color: #f5f5f5; padding: 15px; border-radius: 5px; text-align: left;">
docker build -t streamlit-app .
docker run -p 8501:8501 streamlit-app
        </pre>

        <p style="margin-top: 40px; color: #6c757d;">
            詳細は<a href="https://github.com/en2enzo/test-streamlit-vibecoding-github" target="_blank">GitHubリポジトリ</a>をご覧ください。
        </p>
    </body>
    </html>
    """)
