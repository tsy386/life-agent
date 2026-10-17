import json
import os
import threading

MEMORY_FILE = "memory.json"
lock = threading.Lock()

def _load_memory():
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, "r", encoding="utf-8") as f:
                content = f.read()
                return json.loads(content) if content.strip() else {}
        except Exception:
            return {}
    return {}

def _save_memory(data):
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# ================= 饮食管家 =================
def add_diet(preference: str) -> str:
    """饮食管家：新增/替换饮食偏好。若包含“替换”“改成”，请先调用 delete_diet 再调用本工具"""
    with lock:
        mem = _load_memory()
        prefs = mem.setdefault("diet_preferences", [])
        if preference not in prefs:
            prefs.append(preference)
        _save_memory(mem)
    return f"已为您记录饮食偏好：{preference}。"

def get_diet() -> str:
    """饮食管家：查询所有饮食偏好"""
    with lock:
        mem = _load_memory()
        prefs = mem.get("diet_preferences", [])
    return f"您的饮食偏好是：{', '.join(prefs)}" if prefs else "您目前还没有记录饮食偏好。"

def delete_diet(preference: str) -> str:
    """饮食管家：删除某条饮食偏好（当用户说“不要了”“删除”时调用）"""
    with lock:
        mem = _load_memory()
        prefs = mem.get("diet_preferences", [])
        if preference in prefs:
            prefs.remove(preference)
            _save_memory(mem)
            return f"已删除饮食偏好：{preference}。"
    return f"未找到饮食偏好：{preference}。"

# ================= 日程管家 =================
def add_schedule(event: str) -> str:
    """日程管家：新增日程（添加会议、吃药等安排）"""
    with lock:
        mem = _load_memory()
        mem.setdefault("schedule", []).append(event)
        _save_memory(mem)
    return f"已添加日程：{event}。"

def get_schedule() -> str:
    """日程管家：查询日程安排"""
    with lock:
        mem = _load_memory()
        schedules = mem.get("schedule", [])
    return "您的日程如下：\n" + "\n".join([f"- {s}" for s in schedules]) if schedules else "没有日程安排。"

def delete_schedule(keyword: str) -> str:
    """日程管家：删除日程（当用户要取消、删除某个日程时调用，输入要匹配的关键词）"""
    with lock:
        mem = _load_memory()
        schedules = mem.get("schedule", [])
        new_schedules = [s for s in schedules if keyword not in s]
        if len(new_schedules) != len(schedules):
            mem["schedule"] = new_schedules
            _save_memory(mem)
            return f"已删除包含“{keyword}”的日程。"
    return f"未找到包含“{keyword}”的日程。"

# ================= 财务管家 =================
def add_expense(record: str) -> str:
    """财务管家：记录开销"""
    with lock:
        mem = _load_memory()
        mem.setdefault("expenses", []).append(record)
        _save_memory(mem)
    return f"已记账：{record}。"

def get_expenses() -> str:
    """财务管家：查询账单"""
    with lock:
        mem = _load_memory()
        expenses = mem.get("expenses", [])
    return "您的消费记录：\n" + "\n".join([f"- {e}" for e in expenses]) if expenses else "没有消费记录。"

def delete_expense(keyword: str) -> str:
    """财务管家：删除某条消费记录（当用户说记错了、删除账单时调用）"""
    with lock:
        mem = _load_memory()
        expenses = mem.get("expenses", [])
        new_expenses = [e for e in expenses if keyword not in e]
        if len(new_expenses) != len(expenses):
            mem["expenses"] = new_expenses
            _save_memory(mem)
            return f"已删除包含“{keyword}”的消费记录。"
    return f"未找到包含“{keyword}”的消费记录。"