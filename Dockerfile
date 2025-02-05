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

# コンテナがリッスンするポートを指定
EXPOSE 5000

# アプリケーションの起動コマンド
CMD ["flask", "run", "--host=0.0.0.0"]
