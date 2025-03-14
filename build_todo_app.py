import PyInstaller.__main__
import os
import shutil

# 実行前に dist/templates フォルダを作成
os.makedirs('dist/templates', exist_ok=True)

# PyInstallerを使用してアプリをビルド
PyInstaller.__main__.run([
    'desktop.py',
    '--name=ToDoApp',
    '--onefile',
    '--windowed',
    '--add-data=templates;templates'
])

print("ビルドが完了しました！dist/ToDoApp.exe を実行してください。")