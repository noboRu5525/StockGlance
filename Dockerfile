# ベースイメージとしてPythonを使用
FROM python:3.11-slim

# 作業ディレクトリを設定
WORKDIR /app

# 必要なパッケージリストをコピー
COPY requirements.txt .

# 依存関係をインストール
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションコードをコピー
COPY app.py .

# コンテナが起動した際に実行するコマンド
CMD ["streamlit", "run", "app.py"]
