from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import sqlite3
import os
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
auth = HTTPBasicAuth()

# ユーザー情報（本来はデータベースで管理すべき）
users = {"admin": generate_password_hash("secret")}


@auth.verify_password
def verify_password(username, password):
    if username in users and check_password_hash(users.get(username), password):
        return username


# データベースパスを環境変数から取得（デフォルト値付き）
DATABASE_PATH = os.getenv("DATABASE_PATH", "data/todos.db")

# データベースディレクトリの作成
os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)


# データベースの初期化
def init_db():
    with sqlite3.connect(DATABASE_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS todos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                completed BOOLEAN NOT NULL DEFAULT 0,
                created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """
        )
        conn.commit()


# データベース接続のヘルパー関数
def get_db():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/")
@auth.login_required
def index():
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM todos ORDER BY created_at DESC")
        todos = cursor.fetchall()
    return render_template("index.html", todos=todos, username=auth.current_user())


@app.route("/todo/create", methods=["POST"])
@auth.login_required
def create_todo():
    title = request.form.get("title")
    if title:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO todos (title, completed, created_at) VALUES (?, ?, ?)",
                (title, False, datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
            )
            conn.commit()
    return redirect(url_for("index"))


@app.route("/todo/<int:todo_id>/update", methods=["POST"])
@auth.login_required
def update_todo(todo_id):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT completed FROM todos WHERE id = ?", (todo_id,))
        todo = cursor.fetchone()
        if todo:
            new_status = not todo["completed"]
            cursor.execute(
                "UPDATE todos SET completed = ? WHERE id = ?", (new_status, todo_id)
            )
            conn.commit()
    return redirect(url_for("index"))


@app.route("/todo/<int:todo_id>/delete", methods=["POST"])
@auth.login_required
def delete_todo(todo_id):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM todos WHERE id = ?", (todo_id,))
        conn.commit()
    return redirect(url_for("index"))


@app.route("/sample")
@auth.login_required
def sample():
    return render_template("sample.html", username=auth.current_user())


# アプリケーション起動時にデータベースを初期化
init_db()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
