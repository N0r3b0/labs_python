from task import Task, TaskManager

task1 = Task("Zrób zakupy", "mleko, jajka, mąka, cukier waniliowy.")
task2 = Task("Napisz inżynierkę", "strona 12 rozdział 2 podrodział 2.3 dodać parametr xyz")


TaskManager.show_tasks()
TaskManager.remove_task(task1)
print()
TaskManager.show_tasks()
print("_________________")
TaskManager.modify_task(task2, name="Nowa_nazwa", description="Nowy opis")
TaskManager.show_tasks()

