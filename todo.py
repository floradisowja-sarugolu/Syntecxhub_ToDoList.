import json
import os

FILE_NAME = "tasks.json"

# ---------- File Handling ----------
def load_tasks():
    if not os.path.exists(FILE_NAME):
        return []
    try:
        with open(FILE_NAME, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

def save_tasks(tasks):
    with open(FILE_NAME, "w") as f:
        json.dump(tasks, f, indent=4)

# ---------- Task Logic ----------
def add_task(tasks):
    title = input("Enter task title: ").strip()
    due_date = input("Enter due date (YYYY-MM-DD) or leave blank: ").strip()
    tags = input("Enter tags (comma separated): ").strip()

    task = {
        "id": len(tasks) + 1,
        "title": title,
        "done": False,
        "due_date": due_date if due_date else None,
        "tags": [t.strip() for t in tags.split(",")] if tags else []
    }

    tasks.append(task)
    save_tasks(tasks)
    print("✅ Task added successfully!")

def view_tasks(tasks):
    if not tasks:
        print("📭 No tasks found.")
        return

    for task in tasks:
        status = "✔ Done" if task["done"] else "⏳ Pending"
        print(f"""
ID: {task['id']}
Task: {task['title']}
Status: {status}
Due Date: {task['due_date']}
Tags: {', '.join(task['tags'])}
---------------------------
""")

def mark_done(tasks):
    try:
        task_id = int(input("Enter task ID to mark as done: "))
        for task in tasks:
            if task["id"] == task_id:
                task["done"] = True
                save_tasks(tasks)
                print("✅ Task marked as done!")
                return
        print("❌ Task not found.")
    except ValueError:
        print("⚠ Invalid input. Enter a number.")

def delete_task(tasks):
    try:
        task_id = int(input("Enter task ID to delete: "))
        new_tasks = [t for t in tasks if t["id"] != task_id]

        if len(new_tasks) == len(tasks):
            print("❌ Task not found.")
            return

        # Reassign IDs
        for i, task in enumerate(new_tasks, start=1):
            task["id"] = i

        save_tasks(new_tasks)
        tasks[:] = new_tasks
        print("🗑 Task deleted successfully!")
    except ValueError:
        print("⚠ Invalid input. Enter a number.")

# ---------- Menu ----------
def menu():
    tasks = load_tasks()

    while True:
        print("""
==== TO-DO LIST MANAGER ====
1. Add Task
2. View Tasks
3. Mark Task as Done
4. Delete Task
5. Exit
===========================
""")
        choice = input("Choose an option: ")

        if choice == "1":
            add_task(tasks)
        elif choice == "2":
            view_tasks(tasks)
        elif choice == "3":
            mark_done(tasks)
        elif choice == "4":
            delete_task(tasks)
        elif choice == "5":
            print("👋 Exiting... Tasks saved.")
            break
        else:
            print("⚠ Invalid choice. Try again.")

if __name__ == "__main__":
    menu()