import os
import json
import argparse
from termcolor import colored
from datetime import datetime
from typing import Optional
from task import Task, TaskManager


class TaskListManager:
    STATUS_OPTIONS = {"1": "Started", "2": "Paused", "3": "Completed"}
    TTL_DAYS = 7  # Time-to-live for tasks in days

    def __init__(self):
        self.current_list = "default.json"
        self.load_tasks()

    # File operations
    def create_new_list(self, name: str) -> None:
        self.current_list = f"{name}.json"
        TaskManager.clear_all()
        self.save_tasks()
        print(colored(f"✅ Created new list: {name}", "green"))

    def load_tasks(self) -> None:
        TaskManager.clear_all()
        if os.path.exists(self.current_list):
            with open(self.current_list, "r") as file:
                data = json.load(file)
                for task_data in data:
                    task = Task.from_dict(task_data)
                    TaskManager.add_task(task)

    def save_tasks(self) -> None:
        with open(self.current_list, "w") as file:
            tasks_data = [task.to_dict() for task in TaskManager.tasks.values()]
            json.dump(tasks_data, file, indent=4)

    # Task operations
    def add_task(self, name: str, description: str, list_name: Optional[str] = None) -> None:
        if list_name and not self._validate_list(list_name):
            return

        task = Task(id=TaskManager.id_counter, name=name, description=description)
        TaskManager.id_counter += 1
        TaskManager.add_task(task)
        self.save_tasks()
        print(colored("✅ Task added.", "green"))

    def list_tasks(self, status_filter: Optional[str] = None, 
                  list_name: Optional[str] = None) -> None:
        if list_name and not self._validate_list(list_name):
            return

        if not TaskManager.tasks:
            print(colored("❌ No available tasks.", "red"))
            return

        today = datetime.today()
        active_tasks = []
        outdated_tasks = []

        for task in TaskManager.tasks.values():
            days_passed = (today - task.created_at).days if task.created_at else 0
            if days_passed <= self.TTL_DAYS:
                active_tasks.append(task)
            else:
                outdated_tasks.append((task, days_passed - self.TTL_DAYS))

        self._print_task_list(active_tasks, outdated_tasks, status_filter)

    def update_task_status(self, task_id: int, status_id: str, 
                         list_name: Optional[str] = None) -> None:
        if list_name and not self._validate_list(list_name):
            return

        task = TaskManager.get_task(task_id)
        if task:
            task.status = self.STATUS_OPTIONS.get(status_id, task.status)
            self.save_tasks()
            print(colored(f"'{task.name}' Status updated to: {task.status}", "yellow"))
        else:
            print(colored("❌ Task with the given ID not found!", "red"))

    def remove_task(self, task_id: int, list_name: Optional[str] = None) -> None:
        if list_name and not self._validate_list(list_name):
            return

        task = TaskManager.get_task(task_id)
        if task:
            TaskManager.remove_task(task_id)
            self.save_tasks()
            print(colored(f"✅ Task '{task.name}' has been removed.", "green"))
        else:
            print(colored("❌ Invalid task number.", "red"))

    # List operations
    def delete_list(self, name: str) -> None:
        filename = f"{name}.json"
        if os.path.exists(filename):
            os.remove(filename)
            print(colored(f"✅ List '{name}' has been deleted.", "green"))
            if self.current_list == filename:
                self.current_list = "default.json"
                self.load_tasks()
                print(colored("📋 Switched to the default task list.", "yellow"))
        else:
            print(colored(f"❌ List '{name}' does not exist.", "red"))

    def list_available_lists(self) -> None:
        files = [f[:-5] for f in os.listdir() if f.endswith(".json")]
        if not files:
            print(colored("❌ No available task lists.", "red"))
        else:
            print(colored("📋 Available task lists:", "cyan"))
            for file in files:
                print(f"- {file}")

    # Helper methods
    def _validate_list(self, list_name: str) -> bool:
        filename = f"{list_name}.json"
        if not os.path.exists(filename):
            print(colored(f"❌ List '{list_name}' does not exist.", "red"))
            return False
        self.current_list = filename
        self.load_tasks()
        return True

    def _print_task_list(self, active_tasks: list, outdated_tasks: list, 
                        status_filter: Optional[str] = None) -> None:
        if active_tasks:
            print(colored("✅ Active tasks:", "green"))
            for task in active_tasks:
                if not status_filter or task.status == status_filter:
                    print(colored(
                        f"[{task.id}] - {task.name} - {task.description} - Status: {task.status}",
                        self._get_status_color(task.status)
                    ))
        else:
            print(colored("❌ No active tasks.", "red"))

        if outdated_tasks:
            print(colored("\n⌛ Outdated tasks:", "yellow"))
            for task, outdated_days in outdated_tasks:
                print(colored(
                    f"[{task.id}] - {task.name} - {task.description} - Status: {task.status} "
                    f"(outdated by {outdated_days} days)", "yellow"
                ))

    def _get_status_color(self, status: str) -> str:
        return {"Started": "yellow", "Paused": "red", "Completed": "green"}.get(status, "white")

    # Command handling
    def handle_command(self, args: list) -> None:
        parser = argparse.ArgumentParser(description="Task Manager")
        subparsers = parser.add_subparsers(dest="command", required=True)

        # Add task command
        add_parser = subparsers.add_parser("add", help="Add a new task")
        add_parser.add_argument("name", help="Name of the task")
        add_parser.add_argument("description", help="Task description")
        add_parser.add_argument("--list", help="Task list name")

        # List tasks command
        list_parser = subparsers.add_parser("list", help="List tasks")
        list_parser.add_argument("--status", choices=["1", "2", "3"], help="Filter by status")
        list_parser.add_argument("--list", help="Task list name")

        # Update status command
        update_parser = subparsers.add_parser("update", help="Update task status")
        update_parser.add_argument("task_id", type=int, help="Task ID to update")
        update_parser.add_argument("status", choices=["1", "2", "3"], help="New status")
        update_parser.add_argument("--list", help="Task list name")

        # Remove task command
        remove_parser = subparsers.add_parser("remove", help="Remove a task")
        remove_parser.add_argument("task_id", type=int, help="Task ID to remove")
        remove_parser.add_argument("--list", help="Task list name")

        # List management commands
        subparsers.add_parser("lists", help="List all available task lists")
        subparsers.add_parser("new-list", help="Create a new task list").add_argument("name", help="List name")
        subparsers.add_parser("delete-list", help="Delete a task list").add_argument("name", help="List name")

        args = parser.parse_args(args)

        if args.command == "add":
            self.add_task(args.name, args.description, args.list)
        elif args.command == "list":
            status_filter = self.STATUS_OPTIONS.get(args.status) if args.status else None
            self.list_tasks(status_filter, args.list)
        elif args.command == "update":
            self.update_task_status(args.task_id, args.status, args.list)
        elif args.command == "remove":
            self.remove_task(args.task_id, args.list)
        elif args.command == "lists":
            self.list_available_lists()
        elif args.command == "new-list":
            self.create_new_list(args.name)
        elif args.command == "delete-list":
            self.delete_list(args.name)