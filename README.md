# Python Laboratory Projects

This repository contains two Python projects developed for laboratory classes:

1. **Currency Wallet Manager**
2. **Task Manager**

## 1. Currency Wallet Manager

A command-line tool for managing currency wallets, fetching exchange rates, and performing currency conversions.

### Features
- Generate random wallets for different currencies
- Fetch current exchange rates from the National Bank of Poland API
- Calculate total value of multiple currencies in a specified target currency

### Usage

```bash
python main.py [command] [options]
```

#### Available Commands:
- `generate`: Generate random wallets for available currencies
  - `--show`: Display generated wallets
- `rates`: Show current exchange rates (to PLN)
- `calculate [currency] [values]`: Calculate total value in specified currency
  - Example: `calculate USD USD:100 EUR:50`

### Example Usage
```bash
# Generate wallets and show them
python main.py generate --show

# Show current exchange rates
python main.py rates

# Calculate total value in USD
python main.py calculate USD USD:100 EUR:50 PLN:200
```

### Dependencies
- `requests` - for API communication

---

## 2. Task Manager

A command-line task management system with multiple task lists support.

### Features
- Create, update, and remove tasks
- Multiple task lists support
- Task status tracking (Started, Paused, Completed)
- Automatic task expiration (7-day TTL)
- Color-coded output for better visibility

### Usage

```bash
python main.py [command] [arguments] [options]
```

#### Available Commands:
- `add [name] [description]`: Add a new task
  - `--list`: Specify task list name
- `list`: List all tasks
  - `--status`: Filter by status (1=Started, 2=Paused, 3=Completed)
  - `--list`: Specify task list name
- `update [task_id] [status]`: Update task status
  - `--list`: Specify task list name
- `remove [task_id]`: Remove a task
  - `--list`: Specify task list name
- `lists`: List all available task lists
- `new-list [name]`: Create a new task list
- `delete-list [name]`: Delete a task list

### Example Usage
```bash
# Add a new task
python main.py add "Complete project" "Finish the Python laboratory project"

# List all tasks
python main.py list

# Update task status
python main.py update 1 3  # Mark task 1 as completed

# Create a new task list
python main.py new-list "work"

# Switch to work list and add a task
python main.py add "Meeting" "Team meeting at 2pm" --list work
```

### Dependencies
- `termcolor` - for colored console output
- `dataclasses` - for Task data structure

---

## Installation

1. Clone the repository
2. Install required dependencies:
   ```bash
   pip install requests termcolor
   ```

## Notes
- The Currency Wallet Manager uses the National Bank of Poland API for exchange rates
- Task Manager data is stored in JSON files (one file per task list)
- Both projects follow clean code practices and use Python type hints