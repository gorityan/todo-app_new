from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
import os



app = Flask(__name__)

# SQLite データベースの設定
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'todo.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# カテゴリモデルの定義
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    
    def __repr__(self):
        return f'<Category {self.name}>'

# 拡張されたタスクモデルの定義
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(200), nullable=False)
    deadline = db.Column(db.String(10), nullable=False)  # 例: 'YYYY-MM-DD'
    completed = db.Column(db.Boolean, default=False)
    priority = db.Column(db.String(10), default='中')  # '高', '中', '低'
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=True)
    progress = db.Column(db.Integer, default=0)  # 進捗率: 0-100
    
    # カテゴリとのリレーション
    category = db.relationship('Category', backref=db.backref('tasks', lazy=True))

    def __repr__(self):
        return f'<Task {self.task}>'

# 初回起動時にデータベースとデフォルトカテゴリを作成
@app.before_first_request
def create_tables_and_defaults():
    db.create_all()
    
    # デフォルトカテゴリの作成（存在しない場合のみ）
    default_categories = ['仕事', '勉強', 'プライベート', 'その他']
    for cat_name in default_categories:
        if not Category.query.filter_by(name=cat_name).first():
            new_cat = Category(name=cat_name)
            db.session.add(new_cat)
    
    db.session.commit()

@app.route('/')
def index():
    # カテゴリとフィルタリング
    category_id = request.args.get('category', type=int)
    search_query = request.args.get('search', '')
    
    # 検索とフィルタリングのロジック
    tasks_query = Task.query.filter_by(completed=False)
    completed_query = Task.query.filter_by(completed=True)
    
    if category_id:
        tasks_query = tasks_query.filter_by(category_id=category_id)
        completed_query = completed_query.filter_by(category_id=category_id)
    
    if search_query:
        tasks_query = tasks_query.filter(Task.task.contains(search_query))
        completed_query = completed_query.filter(Task.task.contains(search_query))
    
    tasks_todo = tasks_query.all()
    tasks_done = completed_query.all()
    categories = Category.query.all()
    
    return render_template('index.html', 
                           tasks=tasks_todo, 
                           completed_tasks=tasks_done, 
                           categories=categories,
                           current_category=category_id,
                           search_query=search_query)

@app.route('/add', methods=['POST'])
def add_task():
    task_content = request.form.get('task')
    deadline = request.form.get('deadline')
    priority = request.form.get('priority', '中')
    category_id = request.form.get('category_id')
    
    if task_content and deadline:
        new_task = Task(
            task=task_content, 
            deadline=deadline,
            priority=priority,
            category_id=category_id if category_id else None
        )
        db.session.add(new_task)
        db.session.commit()
    
    return redirect(url_for('index'))

@app.route('/done/<int:task_id>')
def mark_done(task_id):
    task = Task.query.get(task_id)
    if task:
        task.completed = True
        task.progress = 100  # 完了時は進捗100%に設定
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/restore/<int:task_id>')
def restore_task(task_id):
    task = Task.query.get(task_id)
    if task:
        task.completed = False
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    task = Task.query.get(task_id)
    if task:
        db.session.delete(task)
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete_completed/<int:task_id>')
def delete_completed_task(task_id):
    task = Task.query.get(task_id)
    if task:
        db.session.delete(task)
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/calendar')
def calendar():
    tasks = Task.query.all()
    events = []
    
    for task in tasks:
        # 優先度に応じた色の設定
        color = '#3788d8'  # デフォルト色（中）
        if task.priority == '高':
            color = '#d9534f'  # 赤
        elif task.priority == '低':
            color = '#5cb85c'  # 緑
        
        # カテゴリ名を取得
        category_name = task.category.name if task.category else 'その他'
        
        # イベント情報
        event = {
            'title': f"[{category_name}] {task.task}",
            'start': task.deadline,
            'backgroundColor': color,
            'extendedProps': {
                'progress': task.progress,
                'completed': task.completed
            }
        }
        
        events.append(event)
    
    return render_template('todo_calendar.html', events=events)

@app.route('/update_progress/<int:task_id>', methods=['POST'])
def update_progress(task_id):
    task = Task.query.get(task_id)
    if task:
        progress = request.form.get('progress', type=int)
        if 0 <= progress <= 100:
            task.progress = progress
            # 進捗が100%なら完了にする
            if progress == 100:
                task.completed = True
            db.session.commit()
            return jsonify({'success': True})
    
    return jsonify({'success': False}), 400

@app.route('/categories')
def list_categories():
    categories = Category.query.all()
    return jsonify([{'id': c.id, 'name': c.name} for c in categories])

@app.route('/categories/add', methods=['POST'])
def add_category():
    name = request.form.get('name')
    if name and not Category.query.filter_by(name=name).first():
        new_category = Category(name=name)
        db.session.add(new_category)
        db.session.commit()
    return redirect(url_for('index'))

# if __name__ == '__main__':
#     app.run(debug=True)
if __name__ == '__main__':
    print("サーバーを起動します: http://127.0.0.1:5001")
    app.run(host='127.0.0.1', port=5001, debug=True)