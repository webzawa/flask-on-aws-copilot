## AWS Copilotとは
ChatGPTの回答
AWS Copilot
開発者: Amazon Web Servicesによって開発されました。
特徴: AWS上でコンテナ化されたアプリケーションの開発、リリース、および運用を簡素化するためのコマンドラインインターフェース(CLI)ツールです。
機能: Amazon ECS(弾性コンテナサービス)やAWS Fargateの使用を簡素化し、アプリケーションのデプロイ、モニタリング、およびインフラストラクチャの管理を支援します。
利点: コンテナ化されたアプリケーションの開発者に焦点を当て、インフラストラクチャの管理よりもアプリケーションのビルドやデプロイメントに重点を置いています。


## AWS CopilotでFlaskアプリケーションをデプロイする
mkdir ~/flask-on-aws-copilot
cd ~/flask-on-aws-copilot

touch app.py
```
from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello_world():
    return "Hello, World!"

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
```

touch requirements.txt
```
flask
```

touch Dockerfile
```
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
```

## ローカルで動作確認
docker build -t flask-on-aws-copilot .
docker run -p 5000:5000 flask-on-aws-copilot

### 5000番ポートがMacのAirPlay Receiverで使用されている場合は、以下記事の手順で解放する
[Mac を Monterey にアップデートしたら Flask が 5000 番ポートで起動できなくなった - Sweet Escape](https://www.keisuke69.net/entry/2021/10/29/012608)

## AWS Copilotでデプロイ(AWS CLIがインストールされている前提)
[AWS Copilot CLIのススメ](https://zenn.dev/praha/articles/f42467cd6a9e79)
[Overview - AWS Copilot CLI](https://aws.github.io/copilot-cli/ja/docs/overview/)

### AWS Copilot CLIのインストール
brew install aws/tap/copilot-cli

### AWS Copilot CLIの初期設定
export AWS_REGION=ap-northeast-1
copilot app init aws-copilot-practice-my-flask-app

### AWS Copilot CLIでFlaskアプリケーションをデプロイ --profileは自身の環境に合わせて変更
copilot env init --name development --profile default --app aws-copilot-practice-my-flask-app

#### 環境設定はデフォルトで行う
> Default environment configuration? Yes, use default.

### サービスの作成: アプリケーションに含まれるサービス（例: Web APIやバックエンドサービス）を定義します。
copilot svc init --name flask-service --svc-type "Load Balanced Web Service" --dockerfile ./Dockerfile --port 5000

### development環境をデプロイ
copilot env deploy --name development

### サービスをdevelopment環境にデプロイ
copilot svc deploy --name flask-service --env development
