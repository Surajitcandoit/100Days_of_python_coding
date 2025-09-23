import datetime, time
import json
import os
import readline
import shlex

# Color codes
rest = "\033[0m"
clrs = [
    "\033[91m",  # Red
    "\033[92m",  # Green
    "\033[93m",  # Yellow
    "\033[94m",  # Blue
    "\033[95m",  # Magenta
    "\033[96m"   # Cyan
]

# Simple color function
def colorText(color, text, reset):
    print(f"{color}{text}{reset}")

clr = clrs[2]  # Yellow

msg = [
    f"Welcome to My_To-Do",
    f"To use the app please read the instructions below!..",
    f"Command\t\t\t\t Descriptions\n____________\t\t\t__________________\nmtd -l\t\t\t\tto see your to-do list.",
    "mtd -add <new_todo> <detail>\tto create a to-do named 'new_todo' with task detail\n"
    "mtd -r <todo1>\t\t\tto mark as complete the todo1 named to-do of your list.\n"
    "mtd -ur <todo1>\t\t\tto unread or mark as uncomplete the todo1 named to-do of your list.\n"
    "mtd -del <mytodo>\t\tto delete the mytodo from your to-do list.\n"
    "mtd -al\t\t\t\tto select all to-do in your list.\n"
    "mtd -aldel\t\t\tto delete the entire selected list.\n"
    "mtd -ar\t\t\t\tto select all completed to-do in your list.\n"
    "mtd -aur\t\t\tsame as '-ar' select all uncompleted to-do from the list.\n"
    "You can perform one operation on multiple todo with their space separated names like: "
    "'mtd -r todo1 todo2 todo3'\n"
]

try:
    for i in msg:
        colorText(clr, i, rest)
        time.sleep(0.3)
except Exception as e:
    print(f"{clrs[0]}Error displaying welcome message: {e}{rest}")


class TodoItem:
    def __init__(self, name, text, status="uncomplete"):
        self.name = name
        self.text = text
        self.status = status
        self.crtime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


class TodoList:
    def __init__(self, filename="todos.json"):
        self.filename = filename
        self.todos = {}
        self.load_todos()

    def load_todos(self):
        """Load todos from JSON file"""
        try:
            if os.path.exists(self.filename) and os.path.getsize(self.filename) > 0:
                with open(self.filename, 'r') as f:
                    data = json.load(f)
                    for name, todo_data in data.items():
                        todo = TodoItem(
                            todo_data['name'],
                            todo_data['text'],
                            todo_data['status']
                        )
                        todo.crtime = todo_data['crtime']
                        self.todos[name] = todo
        except Exception as e:
            colorText(clrs[0], f"Error loading todos: {e}", rest)

    def save_todos(self):
        """Save todos to JSON file"""
        try:
            data = {
                name: {
                    'name': todo.name,
                    'text': todo.text,
                    'status': todo.status,
                    'crtime': todo.crtime
                } for name, todo in self.todos.items()
            }
            with open(self.filename, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            colorText(clrs[0], f"Error saving todos: {e}", rest)

    def add_todo(self, name, text):
        """Add a new todo"""
        if name in self.todos:
            colorText(clrs[0], f"Todo '{name}' already exists!", rest)
            return False

        self.todos[name] = TodoItem(name, text)
        self.save_todos()
        colorText(clrs[1], f"Todo '{name}' added successfully!", rest)
        return True

    def mark_complete(self, *names):
        """Mark todos as complete"""
        for name in names:
            if name in self.todos:
                self.todos[name].status = "completed"
                colorText(clrs[1], f"Todo '{name}' marked as complete!", rest)
            else:
                colorText(clrs[0], f"Todo '{name}' not found!", rest)
        self.save_todos()

    def mark_uncomplete(self, *names):
        """Mark todos as uncomplete"""
        for name in names:
            if name in self.todos:
                self.todos[name].status = "uncomplete"
                colorText(clrs[3], f"Todo '{name}' marked as uncomplete!", rest)
            else:
                colorText(clrs[0], f"Todo '{name}' not found!", rest)
        self.save_todos()

    def delete_todo(self, *names):
        """Delete todos"""
        for name in names:
            if name in self.todos:
                del self.todos[name]
                colorText(clrs[5], f"Todo '{name}' deleted!", rest)
            else:
                colorText(clrs[0], f"Todo '{name}' not found!", rest)
        self.save_todos()

    def list_todos(self):
        """Display all todos"""
        if not self.todos:
            colorText(clrs[3], "No todos found!", rest)
            return

        colorText(clrs[2], "\n=== Your Todo List ===", rest)
        for todo in self.todos.values():
            status_color = clrs[1] if todo.status == "completed" else clrs[0]
            status_symbol = "✓" if todo.status == "completed" else "✗"

            print(f"{status_color}[{status_symbol}] {todo.name}{rest}")
            print(f"    Detail: {todo.text}")
            print(f"    Created: {todo.crtime}")
            print(f"    Status: {todo.status}")
            print()

    def select_all_completed(self):
        completed = [name for name, todo in self.todos.items() if todo.status == "completed"]
        if completed:
            colorText(clrs[1], f"Completed todos: {', '.join(completed)}", rest)
        else:
            colorText(clrs[3], "No completed todos found!", rest)
        return completed

    def select_all_uncompleted(self):
        uncompleted = [name for name, todo in self.todos.items() if todo.status == "uncomplete"]
        if uncompleted:
            colorText(clrs[0], f"Uncompleted todos: {', '.join(uncompleted)}", rest)
        else:
            colorText(clrs[3], "No uncompleted todos found!", rest)
        return uncompleted

    def select_all(self):
        all_todos = list(self.todos.keys())
        if all_todos:
            colorText(clrs[4], f"All todos: {', '.join(all_todos)}", rest)
        else:
            colorText(clrs[3], "No todos found!", rest)
        return all_todos

    def delete_all_selected(self):
        if self.todos:
            self.todos.clear()
            self.save_todos()
            colorText(clrs[5], "All todos deleted!", rest)
        else:
            colorText(clrs[3], "No todos to delete!", rest)

    def delete_all_completed(self):
        completed_todos = [name for name, todo in self.todos.items() if todo.status == "completed"]
        if completed_todos:
            for name in completed_todos:
                del self.todos[name]
            self.save_todos()
            colorText(clrs[1], f"Deleted {len(completed_todos)} completed todo(s): {', '.join(completed_todos)}", rest)
        else:
            colorText(clrs[3], "No completed todos to delete!", rest)

    def delete_all_uncompleted(self):
        uncompleted_todos = [name for name, todo in self.todos.items() if todo.status == "uncomplete"]
        if uncompleted_todos:
            for name in uncompleted_todos:
                del self.todos[name]
            self.save_todos()
            colorText(clrs[0], f"Deleted {len(uncompleted_todos)} uncompleted todo(s): {', '.join(uncompleted_todos)}", rest)
        else:
            colorText(clrs[3], "No uncompleted todos to delete!", rest)


def parse_command(command_input, todo_list):
    """Parse user input commands"""
    if not command_input.strip():
        colorText(clrs[0], "No command provided! Use '-l' to see your todos.", rest)
        return False

    try:
        parts = shlex.split(command_input)
    except Exception as e:
        colorText(clrs[0], f"Error parsing command: {e}", rest)
        return False

    if not parts:
        return False

    command = parts[0]

    if command == "-l":
        todo_list.list_todos()

    elif command == "-add":
        if len(parts) < 3:
            colorText(clrs[0], "Usage: -add <name> <detail>", rest)
            return False
        name = parts[1]
        detail = " ".join(parts[2:])
        todo_list.add_todo(name, detail)

    elif command == "-r":
        if len(parts) < 2:
            colorText(clrs[0], "Usage: -r <todo1> [todo2] ...", rest)
            return False
        todo_list.mark_complete(*parts[1:])

    elif command == "-ur":
        if len(parts) < 2:
            colorText(clrs[0], "Usage: -ur <todo1> [todo2] ...", rest)
            return False
        todo_list.mark_uncomplete(*parts[1:])

    elif command == "-del":
        if len(parts) < 2:
            colorText(clrs[0], "Usage: -del <todo1> [todo2] ...", rest)
            return False
        todo_list.delete_todo(*parts[1:])

    elif command == "-al":
        todo_list.select_all()

    elif command == "-aldel":
        confirm = input(f"{clrs[0]}Are you sure you want to delete ALL todos? (y/N): {rest}").lower()
        if confirm in ['y', 'yes']:
            todo_list.delete_all_selected()
        else:
            colorText(clrs[3], "Operation cancelled.", rest)

    elif command == "-ar":
        todo_list.select_all_completed()

    elif command == "-aur":
        todo_list.select_all_uncompleted()

    elif command == "-ardel":
        completed = todo_list.select_all_completed()
        if completed:
            confirm = input(f"{clrs[0]}Delete all completed todos? (y/N): {rest}").lower()
            if confirm in ['y', 'yes']:
                todo_list.delete_all_completed()
            else:
                colorText(clrs[3], "Operation cancelled.", rest)

    elif command == "-aurdel":
        uncompleted = todo_list.select_all_uncompleted()
        if uncompleted:
            confirm = input(f"{clrs[0]}Delete all uncompleted todos? (y/N): {rest}").lower()
            if confirm in ['y', 'yes']:
                todo_list.delete_all_uncompleted()
            else:
                colorText(clrs[3], "Operation cancelled.", rest)

    elif command in ["-help", "-h"]:
        show_help()

    elif command in ["quit", "q", "exit"]:
        return True

    else:
        colorText(clrs[0], f"Unknown command: {command}", rest)
        colorText(clrs[2], "Type '-help' for available commands", rest)

    return False


def show_help():
    colorText(clrs[2], "\n=== Available Commands ===", rest)
    help_commands = [
        ("-l", "List all todos"),
        ("-add <name> <detail>", "Add a new todo"),
        ("-r <todo1> [todo2]...", "Mark todos as complete"),
        ("-ur <todo1> [todo2]...", "Mark todos as uncomplete"),
        ("-del <todo1> [todo2]...", "Delete todos"),
        ("-al", "Show all todos"),
        ("-aldel", "Delete all todos"),
        ("-ar", "Show completed todos"),
        ("-aur", "Show uncompleted todos"),
        ("-help or -h", "Show this help"),
        ("quit or q or exit", "Exit the application")
    ]

    for cmd, desc in help_commands:
        colorText(clrs[3], f"{cmd:<25} {desc}", rest)

    print("\nExamples:")
    colorText(clrs[4], "-add homework 'Complete math assignment'", rest)
    colorText(clrs[4], "-r homework project", rest)
    colorText(clrs[4], "-del homework", rest)


def setup_readline():
    history_file = os.path.expanduser("~/.mtd_history")
    try:
        if os.path.exists(history_file):
            readline.read_history_file(history_file)
        return history_file
    except Exception as e:
        colorText(clrs[0], f"Error loading history: {e}", rest)
        return None


def save_history(history_file):
    try:
        if history_file:
            readline.write_history_file(history_file)
    except Exception as e:
        colorText(clrs[0], f"Error saving history: {e}", rest)


def main():
    todo_list = TodoList()
    history_file = setup_readline()

    colorText(clrs[2], "\n=== Interactive Todo Application ===", rest)
    colorText(clrs[3], "Type '-help' for available commands or 'quit' to exit", rest)
    if history_file:
        colorText(clrs[3], "Use ↑/↓ arrow keys to navigate command history", rest)

    while True:
        try:
            user_input = input(f"\n{clrs[4]}mtd> {rest}").strip()

            if user_input and user_input != readline.get_history_item(readline.get_current_history_length()):
                readline.add_history(user_input)

            if parse_command(user_input, todo_list):
                colorText(clrs[2], "Goodbye!", rest)
                break

        except KeyboardInterrupt:
            colorText(clrs[2], "\nGoodbye!", rest)
            break
        except EOFError:
            colorText(clrs[2], "\nGoodbye!", rest)
            break

    save_history(history_file)


if __name__ == "__main__":
    main()
