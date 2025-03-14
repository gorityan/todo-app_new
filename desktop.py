import threading
import time
import webbrowser
from app import app

def run_flask():
    # Flaskサーバーを起動（ポート5001）
    app.run(host='127.0.0.1', port=5001, debug=False)

if __name__ == '__main__':
    # Flaskをバックグラウンドで起動
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()
    
    # サーバーの起動を待機
    print("サーバー起動中...")
    time.sleep(2)
    
    # ブラウザを開く
    url = 'http://127.0.0.1:5001'
    print(f"ブラウザを開いています: {url}")
    webbrowser.open(url)
    
    # アプリが終了しないようにする
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("アプリケーションを終了します")