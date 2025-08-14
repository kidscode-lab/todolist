# storage.py
import json
import os
import re
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List

# Base folder (Azure App Service has a writable /home)
BASE_DIR = Path(os.environ.get("DATA_DIR", "./data")).resolve()

SAFE = re.compile(r"^[A-Za-z0-9_-]{1,64}$")  # simple sanitizer

def _safe(name: str) -> str:
    if not SAFE.match(name):
        raise ValueError("Only letters, digits, underscore, and dash are allowed (max 64).")
    return name

def _file_path(class_code: str, student_id: str) -> Path:
    class_code = _safe(class_code)
    student_id = _safe(student_id)
    folder = BASE_DIR / class_code
    folder.mkdir(parents=True, exist_ok=True)
    return folder / f"{student_id}.json"

def _atomic_write(path: Path, data: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", delete=False, dir=path.parent, encoding="utf-8") as tmp:
        json.dump(data, tmp, ensure_ascii=False, indent=2)
        tmp.flush()
        os.fsync(tmp.fileno())
        tmp_path = Path(tmp.name)
    os.replace(tmp_path, path)  # atomic on same filesystem

def load_tasks(class_code: str, student_id: str) -> Dict[str, Any]:
    path = _file_path(class_code, student_id)
    if not path.exists():
        return {"next_id": 1, "tasks": []}
    with path.open("r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            # fallback if file was manually edited wrong
            return {"next_id": 1, "tasks": []}

def save_tasks(class_code: str, student_id: str, state: Dict[str, Any]) -> None:
    path = _file_path(class_code, student_id)
    _atomic_write(path, state)

def add_task(class_code: str, student_id: str, title: str, due_date: str | None) -> Dict[str, Any]:
    state = load_tasks(class_code, student_id)
    tid = state.get("next_id", 1)
    task = {
        "id": tid,
        "title": title,
        "due_date": due_date,  # "YYYY-MM-DD" or None
        "done": False,
        "created_at": datetime.utcnow().isoformat() + "Z",
    }
    state["tasks"].append(task)
    state["next_id"] = tid + 1
    save_tasks(class_code, student_id, state)
    return task

def list_tasks(class_code: str, student_id: str) -> List[Dict[str, Any]]:
    state = load_tasks(class_code, student_id)
    tasks = state.get("tasks", [])
    # Sort by: not done first, then due_date (None last), then id
    return sorted(
        tasks,
        key=lambda t: (
            t.get("done", False),
            t.get("due_date") is None,
            t.get("due_date") or "",
            t.get("id", 0)
        )
    )

def update_task(class_code: str, student_id: str, task_id: int, patch: Dict[str, Any]) -> Dict[str, Any] | None:
    state = load_tasks(class_code, student_id)
    for t in state.get("tasks", []):
        if t["id"] == task_id:
            if "done" in patch:
                t["done"] = bool(patch["done"])
            if "title" in patch and str(patch["title"]).strip():
                t["title"] = str(patch["title"]).strip()
            if "due_date" in patch:
                v = patch["due_date"]
                t["due_date"] = None if v in (None, "") else str(v)
            save_tasks(class_code, student_id, state)
            return t
    return None

def delete_task(class_code: str, student_id: str, task_id: int) -> bool:
    state = load_tasks(class_code, student_id)
    before = len(state.get("tasks", []))
    state["tasks"] = [t for t in state["tasks"] if t["id"] != task_id]
    after = len(state["tasks"])
    if after != before:
        save_tasks(class_code, student_id, state)
        return True
    return False
