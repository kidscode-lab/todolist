# app.py
from flask import Flask, jsonify, request, abort
from flask_cors import CORS
import os

import storage  # our JSON file storage helpers

app = Flask(__name__)
CORS(app)

API_KEY = os.environ.get("API_KEY", "")  # optional, set in Azure

def require_key():
    # Only protect write operations; keep GET open for your class demo
    if not API_KEY:
        return
    key = request.headers.get("X-API-Key", "")
    if key != API_KEY:
        abort(401, description="Invalid or missing API key")

def extract_ns():
    """
    Pull namespace from query or headers:
      - class_code: class group (e.g., '7A' or 'summer2025')
      - student_id: the student (e.g., 'alice01')
    """
    class_code = (request.args.get("class_code") or request.headers.get("X-Class-Code") or "").strip()
    student_id = (request.args.get("student_id") or request.headers.get("X-Student-Id") or "").strip()
    if not class_code or not student_id:
        abort(400, description="class_code and student_id are required (query or headers).")
    return class_code, student_id

@app.get("/api/health")
def health():
    return {"ok": True}

@app.get("/api/tasks")
def list_tasks():
    class_code, student_id = extract_ns()
    tasks = storage.list_tasks(class_code, student_id)
    return jsonify(tasks)

@app.post("/api/tasks")
def create_task():
    require_key()
    class_code, student_id = extract_ns()
    payload = request.get_json(force=True, silent=True) or {}
    title = (payload.get("title") or "").strip()
    due_date = (payload.get("due_date") or None)
    if not title:
        abort(400, description="title is required")
    task = storage.add_task(class_code, student_id, title, due_date)
    return jsonify(task), 201

@app.patch("/api/tasks/<int:task_id>")
def update_task(task_id: int):
    require_key()
    class_code, student_id = extract_ns()
    patch = request.get_json(force=True, silent=True) or {}
    updated = storage.update_task(class_code, student_id, task_id, patch)
    if not updated:
        abort(404, description="Task not found")
    return jsonify(updated)

@app.delete("/api/tasks/<int:task_id>")
def delete_task(task_id: int):
    require_key()
    class_code, student_id = extract_ns()
    ok = storage.delete_task(class_code, student_id, task_id)
    if not ok:
        abort(404, description="Task not found")
    return "", 204

# in app.py
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5055))  # 5055 for local; product services sets PORT
    app.run(host="127.0.0.1", port=port, debug=True, use_reloader=False)


