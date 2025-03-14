#!/bin/bash
# macOSやLinux用の起動スクリプト

# アプリディレクトリに移動
cd "$(dirname "$0")"

# 仮想環境がある場合はアクティベート
# source venv/bin/activate

# アプリケーションを実行
python3 desktop.py