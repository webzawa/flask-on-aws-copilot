from flask import Flask, render_template, request, redirect, url_for
import json
from datetime import datetime

app = Flask(__name__)

# インメモリでTodoを保存
todos = []

@app.route("/")
def index():
    return render_template("index.html", todos=todos)

@app.route("/todo/create", methods=["POST"])
def create_todo():
    title = request.form.get("title")
    if title:
        todo = {
            "id": len(todos) + 1,
            "title": title,
            "completed": False,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        todos.append(todo)
    return redirect(url_for("index"))

@app.route("/todo/<int:todo_id>/update", methods=["POST"])
def update_todo(todo_id):
    for todo in todos:
        if todo["id"] == todo_id:
            todo["completed"] = not todo["completed"]
            break
    return redirect(url_for("index"))

@app.route("/todo/<int:todo_id>/delete", methods=["POST"])
def delete_todo(todo_id):
    global todos
    todos = [todo for todo in todos if todo["id"] != todo_id]
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
