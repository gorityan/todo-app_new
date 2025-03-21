拡張ToDoリストアプリケーション
Pythonで開発されたデスクトップToDoリストアプリケーションです。FlaskとSQLAlchemyを使用しており、タスクの優先度設定、カテゴリ分類、検索機能、進捗管理などの機能を備えています。
特徴

タスクの追加、編集、削除（基本的なCRUD操作）
優先度設定（高・中・低）と色分け表示
カテゴリによるタスク分類とフィルタリング
キーワード検索機能
進捗管理（0%〜100%）とプログレスバー表示
カレンダー表示機能
デスクトップアプリケーションとして動作

必要条件

Python 3.7以上
必要なパッケージ: Flask, SQLAlchemy, Flask-SQLAlchemy, PyWebView

インストール手順

リポジトリをクローン:

コピーgit clone https://github.com/gorityan/todo-app.git
cd todo-app

必要なパッケージをインストール:

コピーpip install -r requirements.txt
使い方
Webアプリケーションとして実行
コピーpython app.py
その後、ブラウザで http://127.0.0.1:5001 にアクセス
デスクトップアプリケーションとして実行
コピーpython desktop.py
実行ファイルのビルド (Windows)
コピーpython build_todo_app.py
ビルドが完了すると、distフォルダにToDoApp.exeが生成されます。
プロジェクト構成

app.py: メインのFlaskアプリケーション
desktop.py: デスクトップアプリケーションランチャー
templates/: HTMLテンプレート

index.html: メインのタスク管理画面
calendar.html: カレンダー表示画面


requirements.txt: 必要なパッケージリスト
build_todo_app.py: PyInstallerビルドスクリプト
migrate_db.py: データベース移行スクリプト（既存データベースからの移行用）
