from app import db, app, Task, Category
import sqlite3
import os

# 既存のデータベースからデータを取得
def migrate_old_data():
    # 既存のDBファイルが存在するか確認
    db_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'todo.db')
    if not os.path.exists(db_path):
        print("既存のデータベースが見つかりません。")
        return
    
    # 既存のデータを読み込む
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # テーブル構造を確認
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    if ('task',) in tables:
        try:
            # 古いタスクデータを取得
            cursor.execute("SELECT id, task, deadline, completed FROM task")
            old_tasks = cursor.fetchall()
            
            # バックアップを作成
            os.rename(db_path, db_path + '.backup')
            print(f"バックアップファイルを作成しました: {db_path}.backup")
            
            # 新しいデータベースを初期化
            with app.app_context():
                db.create_all()
                
                # デフォルトカテゴリの作成
                default_category = Category(name='その他')
                db.session.add(default_category)
                db.session.commit()
                
                # 古いタスクを新しい形式に移行
                for task_id, task_content, deadline, completed in old_tasks:
                    new_task = Task(
                        task=task_content,
                        deadline=deadline,
                        completed=completed,
                        priority='中',  # デフォルト優先度
                        category_id=default_category.id,
                        progress=100 if completed else 0
                    )
                    db.session.add(new_task)
                
                db.session.commit()
                print(f"{len(old_tasks)}件のタスクをマイグレーションしました。")
                
        except Exception as e:
            print(f"マイグレーション中にエラーが発生しました: {e}")
            # エラーが発生した場合はバックアップを復元
            if os.path.exists(db_path + '.backup'):
                if os.path.exists(db_path):
                    os.remove(db_path)
                os.rename(db_path + '.backup', db_path)
                print("バックアップからデータベースを復元しました。")
    else:
        print("タスクテーブルが見つかりません。")
    
    conn.close()

if __name__ == "__main__":
    migrate_old_data()