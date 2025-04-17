from manager import TaskListManager
import sys

if __name__ == "__main__":
    manager = TaskListManager()
    manager.handle_command(sys.argv[1:])

    