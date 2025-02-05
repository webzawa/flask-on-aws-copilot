# 基本イメージとしてPython 3.9を使用
FROM python:3.9-slim

# 作業ディレクトリの設定
WORKDIR /app

# 依存関係ファイルのコピー
COPY requirements.txt requirements.txt

# 依存関係のインストール
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションのコードをコンテナにコピー
COPY . .

# データベース用のディレクトリを作成
RUN mkdir -p /app/data

# 環境変数を設定
ENV FLASK_ENV=development
ENV FLASK_DEBUG=1
ENV DATABASE_PATH=/app/data/todos.db

# コンテナがリッスンするポートを指定
EXPOSE 5000

# アプリケーションの起動コマンド
CMD ["python", "app.py"]
