### JSnewstatus=Noneto add,remove, modify and list the tasks dynamically
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
    parser.add_argument("-l", "--list",metavar="", help="List all tasks or by status")
    parser.add_argument("-r", "--remove", metavar="", help="Remove a task by index")
    parser.add_argument("-taskid","--TaskID", metavar="", help="Enter task index for which status needs to be modified")
    parser.add_argument("-nS","--NewStatus", metavar="", help="Enter new status")
    parser.add_argument("-nD","--NewDescription", metavar="", help="Enter new description")
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
def list_tasks(Mstatus='All'):
    tasks = load_tasks()

    if Mstatus == 'All' :
        for task in tasks:
            print(f"{task['id']}: {task['description']} [{task['status']}]")
    else:
        filteredtasks = [task for task in tasks if task['status'] == Mstatus]
        for task in filteredtasks :
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

#Mark/Update Task status
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
    parser = create_parser()
    args = parser.parse_args()
    print(args)
    if args.add:
        add_task(args.add)
    elif args.list:
        print(args.list)
        list_tasks(args.list)
    elif args.remove:
        remove_task(int(args.remove))
    elif (args.TaskID and args.NewStatus):
        print("Inside Update status")
        mark_task(int(args.TaskID), args.NewStatus)
    elif (args.TaskID and args.NewDescription):
        update_task(int(args.TaskID), args.NewDescription)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
