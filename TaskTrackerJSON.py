### JSON Based Tool to add,remove, modify and list the tasks dynamically
### Authored by Shubhra Rana

import argparse
import os
import json
from datetime import datetime
from xml.etree.ElementTree import indent

TASKS_FILE = 'listtask.json'

#Creating the parser to run the tool from CLI
def create_parser():
    parser = argparse.ArgumentParser(description="Command-line JSON based Task Tracker App")
    parser.add_argument("-a", "--add", metavar="", help="Add a new task")
    parser.add_argument("-l", "--list", action="store_true", help="List all tasks")
    parser.add_argument("-r", "--remove", metavar="", help="Remove a task by index")
    return parser

def load_tasks():
    try:
        with open(TASKS_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_tasks(tasks):
    with open(TASKS_FILE, 'w') as file:
        json.dump(tasks, file, indent=4)

# Add Task
def add_task(taskname):
    tasks = load_tasks()
    task = {
        'id': len(tasks) + 1,
        'description': taskname,
        'status': 'todo',
        'createdAt': datetime.now().isoformat(),
        'updatedAt': datetime.now().isoformat()
    }
    tasks.append(task)
    save_tasks(tasks)
    print(f"Task added: " + taskname)



#List the tasks
def list_tasks():
    tasks = load_tasks()
    for task in tasks:
        print(f"{task['id']}: {task['description']} [{task['status']}]")

#Remove Task
def remove_task(task_id):
    tasks = load_tasks()
    tasks = [task for task in tasks if task['id'] != task_id]
    save_tasks(tasks)
    tasks = load_tasks()
    for obj in tasks:
        if (obj['id'] > task_id):
            obj['id'] -= 1
    save_tasks(tasks)
    print(f"Task with ID {task_id} deleted.")

#Update the Task Description
def update_task(task_id, description):
    tasks = load_tasks()
    print("Task ID to be updated")
    print(task_id)
    for task in tasks:
        if task['id'] == task_id:
            task['description'] = description
            task['updatedAt'] = datetime.now().isoformat()
            save_tasks(tasks)
            print(f"Task updated: {description}")
            return
    print(f"Task with ID {task_id} not found.")

def mark_task(task_id, status):
    tasks = load_tasks()
    for task in tasks:
        if task['id'] == task_id:
            task['status'] = status
            task['updatedAt'] = datetime.now().isoformat()
            save_tasks(tasks)
            print(f"Task with ID {task_id} marked as {status}.")
            return
    print(f"Task with ID {task_id} not found.")

def main():
    while True:
        print("\nTask Tracker")
        print("1. Add Task")
        print("2. Update Task Description")
        print("3. Update Task Status")
        print("4. Delete Task")
        print("5. View Tasks")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            task_name = input("Enter task name: ")
            add_task(task_name)
        elif choice == '2':
            task_id = input("Enter task ID to update: ")
            task_name = input("Enter new task name: ")
            update_task(int(task_id), task_name)
        elif choice == '4':
            task_id = input("Enter task ID to delete: ")
            remove_task(int(task_id))
        elif choice == '5':
            list_tasks()
        elif choice == '3':
            task_id = input("Enter task ID to update: ")
            task_status = input("Enter new task Status [Todo or In Progress or Completed]")
            mark_task(int(task_id),task_status)
        elif choice == '6':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()