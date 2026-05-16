#!/usr/bin/env python3
import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
import calendar
import csv
import os
import json
import re

from google import genai

# Model Configuration
GEMINI_MODEL = "gemini-2.5-flash"


client = genai.Client(api_key="API_KEY")

CSV_FILE = "tasks.csv"
def extract_json(text):
    try:
        text = text.replace("```json", "").replace("```", "")

        start = text.find("{")
        end = text.rfind("}")

        if start == -1 or end == -1:
            return None

        return json.loads(text[start:end+1])

    except:
        return None



class Task:
    def __init__(self, description, location, duedate, category):
        self.description = description
        self.location = location
        self.duedate = duedate
        self.category = category
        self.priority = ""
        self.suggested_time = ""
        self.completed = False

class TaskManager:
    def __init__(self):
        self.tasks = []
        self.load_tasks()

    def load_tasks(self):
        self.tasks = []
        if not os.path.exists(CSV_FILE):
            return

        with open(CSV_FILE, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                t = Task(
                    row["description"],
                    row["location"],
                    row["duedate"],
                    row["category"]
                )
                t.priority = row.get("priority", "")
                t.suggested_time = row.get("suggested_time", "")
                t.completed = row.get("completed", "False") == "True"
                self.tasks.append(t)

    def save_tasks(self):
        with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=[
                "description",
                "location",
                "duedate",
                "category",
                "suggested_time",
                "priority",
                "completed"
            ])
            writer.writeheader()

            for t in self.tasks:
                writer.writerow({
                    "description": t.description,
                    "location": t.location,
                    "duedate": t.duedate,
                    "category": t.category,
                    "suggested_time": t.suggested_time,
                    "priority": t.priority,
                    "completed": t.completed
                })

    def add_task(self, task):
        for t in self.tasks:
            if t.description.lower() == task.description.lower():
                return False
        self.tasks.append(task)
        self.save_tasks()
        return True

    def delete_task(self, description):
        self.tasks = [
            t for t in self.tasks
            if t.description.lower() != description.lower()
        ]
        self.save_tasks()

    # AI will priortize task from 1 to 10
    def ai_prioritize(self):
        task_data = [
            {
                "description": t.description,
                "duedate": t.duedate,
                "category": t.category
            }
            for t in self.tasks if not t.completed
        ]

        prompt = f"""
You are a strict task prioritization engine.

You must rank tasks based ONLY on:
- due date (most important)
- urgency implied by category

Rules:
- priority is INTEGER from 1 to 10
- 10 = must be done today or overdue
- 7–9 = due soon (1–2 days)
- 4–6 = this week
- 1–3 = low urgency / flexible

Return ONLY valid JSON (no explanations, no extra text):

[
  {{
    "description": "task name",
    "priority": 1-10
  }}
]

Tasks:
{task_data}
"""

        try:
            response = client.models.generate_content(
                model=GEMINI_MODEL,
                contents=prompt
            )

            match = re.search(r'\[.*\]', response.text, re.DOTALL)
            if not match:
                return []

            result = json.loads(match.group())

            for t in self.tasks:
                for r in result:
                    if r["description"] == t.description:
                        t.priority = r["priority"]

            self.save_tasks()
            return result

        except Exception as e:
            messagebox.showerror("AI Error", str(e))
            return []

    # AI will set the schedule of task
    def ai_schedule(self):
        task_data = [
            {
                "description": t.description,
                "duedate": t.duedate,
                "priority": t.priority
            }
            for t in self.tasks if not t.completed
        ]

        prompt = f"""
You are a smart daily scheduler.

Your job is to assign time blocks to tasks.

Rules:
- Use only: morning (08:00–12:00), afternoon (12:00–17:00), evening (17:00–21:00)
- High priority tasks must come first
- Do NOT overlap tasks
- Keep schedule realistic (max 3–6 tasks per day)
- Respect due dates (urgent tasks go earlier in the day)

Return ONLY valid JSON:

[
  {{
    "description": "task name",
    "start": "HH:MM",
    "end": "HH:MM"
  }}
]

Tasks:
{task_data}
"""

        try:
            response = client.models.generate_content(
                model=GEMINI_MODEL,
                contents=prompt
            )

            match = re.search(r'\[.*\]', response.text, re.DOTALL)
            if not match:
                return []

            result = json.loads(match.group())

            for t in self.tasks:
                for r in result:
                    if r["description"] == t.description:
                        t.suggested_time = f"{r['start']} - {r['end']}"

            self.save_tasks()
            return result

        except Exception as e:
            messagebox.showerror("AI Error", str(e))
            return []
        
    # AI will give insights to task
    def ai_insights(self):
        if not self.tasks:
            return "No tasks available."

        task_data = [
            {
                "description": t.description,
                "duedate": t.duedate,
                "priority": t.priority
            }
            for t in self.tasks
        ]

        prompt = f"""
    You are a productivity assistant.

    Analyze the task list and return structured insights.

    Return ONLY valid JSON in this format:

    {{
    "workload": "light | moderate | heavy",
    "urgent_tasks": ["task1", "task2"],
    "overdue_tasks": ["task1"],
    "advice": ["tip1", "tip2", "tip3"]
    }}

    Tasks:
    {task_data}
    """

        try:
            response = client.models.generate_content(
                model=GEMINI_MODEL,
                contents=prompt
            )

            data = extract_json(response.text)

            if not data:
                return "Failed to parse insights.\n\nRaw output:\n" + response.text

            # Format nicely for display
            output = f"""
    Workload: {data['workload'].upper()}

    Urgent Tasks:
    - """ + "\n- ".join(data["urgent_tasks"] or ["None"]) + """

    Overdue Tasks:
    - """ + "\n- ".join(data["overdue_tasks"] or ["None"]) + """

    Advice:
    - """ + "\n- ".join(data["advice"] or ["No suggestions"]) 

            return output

        except Exception as e:
            return f"Insight generation failed: {e}"

tm = TaskManager()


def refresh():
    for i in tree.get_children():
        tree.delete(i)

    for t in tm.tasks:
        item = tree.insert("", "end", values=(
            t.description,
            t.location,
            t.duedate,
            t.category,
            t.priority,
            t.suggested_time
        ))

        if t.completed:
            tree.item(item, tags=("done",))
        else:
            try:
                p = int(t.priority)
                if p >= 8:
                    tree.item(item, tags=("high",))
                elif p >= 4:
                    tree.item(item, tags=("mid",))
                else:
                    tree.item(item, tags=("low",))
            except:
                tree.item(item, tags=("low",))

    tree.tag_configure("done", background="#dddddd")
    tree.tag_configure("high", background="#ffb3b3")
    tree.tag_configure("mid", background="#ffe6a6")
    tree.tag_configure("low", background="#c7f7c7")

def open_calendar_view():
    win = tk.Toplevel(root)
    win.title("Calendar View")
    win.geometry("980x650")
    win.configure(bg="#f4f6f8")

    year = datetime.now().year
    month = datetime.now().month

    cal = calendar.monthcalendar(year, month)

    task_map = {}
    for t in tm.tasks:
        if t.duedate:
            task_map.setdefault(t.duedate, []).append(t)

    # Header
    header = tk.Frame(win, bg="#f4f6f8")
    header.pack(pady=10)

    title_var = tk.StringVar(value=f"{calendar.month_name[month]} {year}")

    tk.Label(
        header,
        textvariable=title_var,
        font=("Segoe UI", 16, "bold"),
        bg="#f4f6f8"
    ).pack()

    # Calendar Grid Frame
    frame = tk.Frame(win, bg="#f4f6f8")
    frame.pack(expand=True, fill="both", padx=10, pady=10)

    def render():
        for w in frame.winfo_children():
            w.destroy()

        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

        # Day headers
        for i, d in enumerate(days):
            tk.Label(
                frame,
                text=d,
                font=("Segoe UI", 10, "bold"),
                bg="#f4f6f8"
            ).grid(row=0, column=i, sticky="nsew", padx=2, pady=2)

        for i in range(7):
            frame.grid_columnconfigure(i, weight=1)

        # Calendar cells
        for r, week in enumerate(cal):
            frame.grid_rowconfigure(r + 1, weight=1)

            for c, day in enumerate(week):
                cell = tk.Frame(
                    frame,
                    bg="white",
                    highlightbackground="#ddd",
                    highlightthickness=1
                )
                cell.grid(row=r + 1, column=c, sticky="nsew", padx=3, pady=3)

                cell.grid_propagate(False)
                cell.config(width=120, height=100)

                if day == 0:
                    continue

                date = f"{year}-{month:02d}-{day:02d}"

                # Day number
                tk.Label(
                    cell,
                    text=str(day),
                    bg="white",
                    font=("Segoe UI", 9, "bold")
                ).pack(anchor="nw")

                # Tasks
                if date in task_map:
                    for t in task_map[date]:

                        try:
                            p = int(t.priority)
                            color = "#e74c3c" if p >= 8 else "#f39c12" if p >= 4 else "#2ecc71"
                        except:
                            color = "gray"

                        row = tk.Frame(cell, bg="white")
                        row.pack(anchor="w", fill="x")

                        tk.Label(
                            row,
                            text="●",
                            fg=color,
                            bg="white"
                        ).pack(side="left")

                        tk.Label(
                            row,
                            text=t.description,
                            bg="white",
                            wraplength=90,
                            justify="left",
                            font=("Segoe UI", 8)
                        ).pack(side="left")

    # Calendar navigation
    def prev_month():
        nonlocal month, year
        month -= 1
        if month == 0:
            month = 12
            year -= 1
        title_var.set(f"{calendar.month_name[month]} {year}")
        nonlocal cal
        cal = calendar.monthcalendar(year, month)
        render()

    def next_month():
        nonlocal month, year
        month += 1
        if month == 13:
            month = 1
            year += 1
        title_var.set(f"{calendar.month_name[month]} {year}")
        nonlocal cal
        cal = calendar.monthcalendar(year, month)
        render()

    nav = tk.Frame(win, bg="#f4f6f8")
    nav.pack()

    tk.Button(nav, text="◀", command=prev_month).pack(side="left", padx=10)
    tk.Button(nav, text="▶", command=next_month).pack(side="left", padx=10)

    render()


# Button action
def parse_date(date_str):
    formats = ["%m/%d/%Y", "%Y-%m-%d", "%m-%d-%Y"]
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt).strftime("%Y-%m-%d")
        except:
            continue
    return None

def clear_fields():
    desc.delete(0, tk.END)
    loc.delete(0, tk.END)
    due.delete(0, tk.END)
    cat.delete(0, tk.END)

def add():
    formatted_date = parse_date(due.get())
    if not formatted_date:
        messagebox.showerror("Invalid Date", "Try formats like MM/DD/YYYY")
        return

    t = Task(desc.get(), loc.get(), formatted_date, cat.get())
    tm.add_task(t)
    refresh()
    clear_fields()

def delete():
    sel = tree.selection()
    if not sel:
        return
    name = tree.item(sel[0])["values"][0]
    tm.delete_task(name)
    refresh()


def mark_completed():
    sel = tree.selection()
    if not sel:
        return

    name = tree.item(sel[0])["values"][0]

    for t in tm.tasks:
        if t.description == name:
            t.completed = True
            break

    tm.save_tasks()
    refresh()

def show_insights():
    win = tk.Toplevel(root)
    win.title("AI Insights")
    win.geometry("400x400")

    text = tk.Text(win, wrap="word")
    text.pack(expand=True, fill="both")

    text.insert("1.0", tm.ai_insights())
    text.config(state="disabled")

# GUI
root = tk.Tk()
root.title("AI To-Do List")
root.geometry("980x550")


tk.Label(root, text="Description").grid(row=0, column=0)
desc = tk.Entry(root); desc.grid(row=0, column=1)

tk.Label(root, text="Location").grid(row=1, column=0)
loc = tk.Entry(root); loc.grid(row=1, column=1)

tk.Label(root, text="Due Date").grid(row=2, column=0)
due = tk.Entry(root); due.grid(row=2, column=1)

tk.Label(root, text="Category").grid(row=3, column=0)
cat = tk.Entry(root); cat.grid(row=3, column=1)

tk.Button(root, text="Calendar View",
          command=open_calendar_view).grid(row=5, column=2)
tk.Button(root, text="Add", command=add).grid(row=4, column=0)
tk.Button(root, text="AI Prioritize", command=lambda: [tm.ai_prioritize(), refresh()]).grid(row=4, column=1)
tk.Button(root, text="AI Schedule", command=lambda: [tm.ai_schedule(), refresh()]).grid(row=4, column=2)
tk.Button(root, text="AI Insights", command=show_insights).grid(row=4, column=3)
tk.Button(root, text="Clear Input", command=clear_fields).grid(row=5, column=3)
tk.Button(root, text="Delete", command=delete).grid(row=5, column=0)
tk.Button(root, text="Mark Completed", command=mark_completed).grid(row=5, column=1)


cols = ("Task","Location","Due","Category","Priority","Time")
tree = ttk.Treeview(root, columns=cols, show="headings")

for c in cols:
    tree.heading(c, text=c)

tree.grid(row=6, column=0, columnspan=4)

refresh()
root.mainloop()