# トレーニング管理アプリケーション

## 概要

このアプリケーションは、ユーザーがトレーニングの進捗を追跡し、管理者がトレーニングとユーザーを管理できるウェブベースのシステムです。Flask、SQLAlchemy、Flask-Loginを使用して構築されています。

## 主な機能

- ユーザー認証（登録、ログイン、ログアウト）
- トレーニング一覧の表示
- ユーザーごとのトレーニング進捗管理
- 管理者ページ（ユーザー管理、トレーニング管理）

## 技術スタック

- バックエンド: Python (Flask)
- データベース: SQLite (SQLAlchemy ORM)
- フロントエンド: HTML, CSS, JavaScript
- 認証: Flask-Login

## セットアップ

1. リポジトリをクローンする

   ```bash
   git clone https://github.com/takuaki-taku/mytraining_app.git
   cd training_app
   ```

2. 仮想環境を作成し、アクティベートする

   ```bash
   python -m venv venv
   source venv/bin/activate  # Windowsの場合: venv\Scripts\activate
   ```

3. 必要なパッケージをインストールする

   ```bash
   pip install -r requirements.txt
   ```

4. データベースを初期化する

   ```bash
   flask db init
   flask db migrate
   flask db upgrade
   ```

5. アプリケーションを実行する

   ```bash
   flask run
   ```

## プロジェクト構造

```
training_app/
├── app/
│   ├── __init__.py
│   ├── auth/
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── main/
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── models.py
│   └── templates/
│       ├── auth/
│       └── main/
├── migrations/
├── .gitignore
├── config.py
├── requirements.txt
├── dockerfile
└── run.py
```

## 使用方法

1. ブラウザで `http://localhost:5000` にアクセスする
2. 新規ユーザーの場合は登録を行う
3. ログイン後、トレーニング一覧や進捗状況を確認できる
4. 管理者は管理者ページからユーザーやトレーニングを管理できる

## 確認用サンプルアカウント

- 管理者
    - Username: `admin`
    - Password: `your-admin-password`
- 一般
    - Username: `sample`
    - Password: `sample01`

## 管理者アカウントの作成

1. アプリケーションを実行した状態で、別のターミナルウィンドウを開く
2. Flaskシェルを起動する

   ```bash
   flask shell
   ```

3. 以下のコマンドを実行して管理者アカウントを作成する

   ```python
   from app import db
   from app.models import User
   admin = User(username='admin', is_admin=True)
   admin.set_password('your-password')
   db.session.add(admin)
   db.session.commit()
   ```

## 貢献

バグの報告や新機能の提案は、Issueを作成してください。プルリクエストも歓迎します。

## ライセンス

このプロジェクトは [ライセンス名] のもとで公開されています。詳細は `LICENSE` ファイルを参照してください。

## Docker コンテナ化

このアプリケーションは Docker コンテナとして実行できます。

### Dockerfile

```dockerfile:training_app/docker/Dockerfile
# ベースイメージ
FROM python:3.11-slim

# 作業ディレクトリ
WORKDIR /app

# requirements.txt をコピー
COPY requirements.txt ./

# 依存関係をインストール
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションコードをコピー
COPY . .

# 環境変数を設定
ENV FLASK_APP=run.py
ENV FLASK_ENV=development

# アプリケーションを起動
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "run:app"]
```

### コンテナのビルドと実行

1. Dockerfile を使用してイメージをビルドします。

   ```bash
   docker build -f ./docker/Dockerfile -t training_app .
   ```

2. イメージからコンテナを実行します。

   ```bash
   docker run -p 5000:5000 training_app
   ```

3. ブラウザで `http://localhost:5000` にアクセスしてアプリケーションにアクセスします。

## 貢献

バグの報告や新機能の提案は、Issueを作成してください。プルリクエストも歓迎します。

## ライセンス

このプロジェクトは [ライセンス名] のもとで公開されています。詳細は `LICENSE` ファイルを参照してください。