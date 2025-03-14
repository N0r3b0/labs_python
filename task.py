class Task:
    id_counter = 0
    tasks = {}

    def __init__(self, name, description=""):
        self.id = Task.id_counter
        self.name = name
        self.description = description

        TaskManager.add_task(self)
        Task.id_counter += 1
        

class TaskManager:
    tasks = {}

    '''
    use @classmethod decorator when you modify class state and want to be able to subclass your class. 
    First argument is a class state and it works like using class name.
    @staticmethod should contain simple logic that fit to the class but doesn't change its state
    '''

    @classmethod
    def add_task(cls, task: Task):
        cls.tasks[task.id] = task


    @classmethod
    def remove_task(cls, task: Task):
        if task.id in cls.tasks:
            del cls.tasks[task.id]


    @classmethod
    def modify_task(cls, task: Task, name):
        if task.id in cls.tasks:
            task.name = name


    @classmethod
    def modify_task(cls, task: Task, **kwargs):
        if task.id in cls.tasks:
            if "name" in kwargs:
                task.name = kwargs["name"]
            if "description" in kwargs:
                task.description = kwargs["description"]


    @classmethod
    def show_tasks(cls):
        if not cls.tasks:
            print("No tasks available.")
        else:
            for task in cls.tasks.values():
                print(f"Task ID: {task.id}, \nName: {task.name}, \nDescription: {task.description}")