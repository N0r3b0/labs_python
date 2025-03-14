class TaskParser:
    
    @staticmethod
    def parse_task_input(task_input):
        """
        Parsuje dane wejściowe i tworzy instancję zadania.
        Task input should be a string in the form of 'task_name, task_description'
        """
        try:
            name, description = task_input.split(", ")
            return Task(name, description)
        except ValueError:
            print("Invalid input format. Ensure it is in the form of 'task_name, task_description'.")
            return None
    
    @staticmethod
    def parse_modify_input(modify_input):
        """
        Parsuje dane wejściowe do modyfikacji zadania.
        Modify input should be in the form of 'task_id, new_name, new_description'
        """
        try:
            parts = modify_input.split(", ")
            task_id = int(parts[0])
            name = parts[1]
            description = parts[2]
            return task_id, name, description
        except ValueError:
            print("Invalid input format. Ensure it is in the form of 'task_id, new_name, new_description'.")
            return None, None, None
    
    @staticmethod
    def parse_remove_input(remove_input):
        """
        Parsuje dane wejściowe do usuwania zadania.
        Remove input should be the task_id as a string.
        """
        try:
            task_id = int(remove_input)
            return task_id
        except ValueError:
            print("Invalid input format. Ensure it is the task_id as a number.")
            return None


# Zastosowanie parsera w kontekście programu:
def test_task_operations():
    # Tworzymy zadania z danych wejściowych
    task1 = TaskParser.parse_task_input("Zrób zakupy, mleko, jajka, mąka, cukier waniliowy.")
    task2 = TaskParser.parse_task_input("Napisz inżynierkę, strona 12 rozdział 2 podrodział 2.3 dodać parametr xyz")

    # Wyświetlamy wszystkie zadania
    TaskManager.show_tasks()

    # Usuwamy zadanie
    task1_id = TaskParser.parse_remove_input("0")
    if task1_id is not None:
        task_to_remove = TaskManager.tasks.get(task1_id)
        if task_to_remove:
            TaskManager.remove_task(task_to_remove)
    print("\nPo usunięciu zadania 1:")
    TaskManager.show_tasks()

    # Modyfikujemy zadanie
    task2_id, new_name, new_description = TaskParser.parse_modify_input("1, Nowa_nazwa, Nowy opis")
    if task2_id is not None:
        task_to_modify = TaskManager.tasks.get(task2_id)
        if task_to_modify:
            TaskManager.modify_task(task_to_modify, name=new_name, description=new_description)
    
    print("\nPo modyfikacji zadania 2:")
    TaskManager.show_tasks()

test_task_operations()
