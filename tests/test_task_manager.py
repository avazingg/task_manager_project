from app.task_manager import TaskManager
import pytest
def task_manager():
    return TaskManager()

def test_add_task():
    TaskManager = task_manager()
    task = TaskManager.add_task("Task1", priority="high")
    assert task["name"] == "Task1"
    assert  task["priority"] == "high"
    assert  task["completed"] == False
    assert  len(TaskManager.list_tasks()) == 1
    with pytest.raises(ValueError, match="Приоритет должен быть 'low', 'normal' или 'high'"):
        TaskManager.add_task("Task2", priority=1)

def test_list_tasks():
    TaskManager = task_manager()
    TaskManager.add_task("Task1", priority="high")
    TaskManager.add_task("Task2")
    assert  TaskManager.list_tasks() == [{"name": "Task1", "priority": "high", "completed": False},
                                         {"name": "Task2", "priority": "normal", "completed": False}]

def test_mark_task_completed():
    TaskManager = task_manager()
    task = TaskManager.add_task("Task1", priority="high")
    TaskManager.mark_task_completed("Task1")
    assert  task["completed"] == True

    with pytest.raises(ValueError, match="Задача с таким названием не найдена"):
        TaskManager.mark_task_completed("TASK99")

def test_remove_task():
    TaskManager = task_manager()
    task = TaskManager.add_task("Task1", priority="high")
    TaskManager.remove_task("Task1")
    assert len(TaskManager.list_tasks()) == 0

    with pytest.raises(ValueError, match="Задача с таким названием не найдена"):
        TaskManager.remove_task("TASK99")
