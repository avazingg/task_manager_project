from app.task_manager import TaskManager
import pytest
import allure

@pytest.fixture
def task_manager():
    return TaskManager()

@pytest.fixture
def task_manager_with_tasks():
    """
        Creates new instance with tasks
    """
    task_manager = TaskManager()
    task_manager.add_task(name="Task0", priority="high")
    task_manager.add_task(name="Task1", priority="low")
    task_manager.add_task(name="Task2")
    return task_manager

@pytest.mark.parametrize(
    "name, priority, expected",
    [
        ("Task0", "high", [{"completed": False,
                            "name": "Task0",
                            "priority": "high"}]),
        ("Task1", "low", [{"completed": False,
                           "name": "Task1",
                           "priority": "low"}])
    ]
)
@allure.feature("add task")
@allure.story("add correct task")
def test_add_task(task_manager, name, priority, expected):
    """
      Test the add_task method with valid input
    """
    with allure.step("add task"):
        if priority is None:
            task_manager.add_task(name)
        else:
            task_manager.add_task(name, priority)
    with allure.step("check task"):
        assert task_manager.tasks == expected

@allure.feature("add task")
@allure.story("add task with wrong priority")
def test_add_task_with_wrong_priority(task_manager):
    """
      Test the add_task method with invalid input
    """
    with allure.step("add task with wrong priority"):
        with pytest.raises(ValueError, match="Приоритет должен быть 'low', 'normal' или 'high'"):
            task_manager.add_task("Task2", priority=1)

@allure.feature("list of tasks")
@allure.story("shows correct list of the tasks")
def test_list_tasks(task_manager_with_tasks):
    """
        Test how works the method which shows our tasks
    """
    with allure.step("shows our tasks"):
        assert  task_manager_with_tasks.list_tasks() == [{"completed": False, "name": "Task0", "priority": "high"},
                                             {"completed": False, "name": "Task1", "priority": "low"},
                                             {"completed": False, "name": "Task2", "priority": "normal"}]

@allure.feature("mark task as completed")
@allure.story("mark existing task")
def test_mark_task_completed_valid(task_manager_with_tasks):
    """
        test marking existing task as valid
    """
    with allure.step("mark task completed"):
        completed_task = task_manager_with_tasks.mark_task_completed("Task0")
    with allure.step("check if task is completed"):
        assert  completed_task["completed"] == True

@allure.feature("mark task as completed")
@allure.story("mark unexisting task")
def test_mark_task_completed_invalid(task_manager):
    """
          test marking unexisting task as valid
      """
    with allure.step("mark task unexisting task ascompleted"):
        with pytest.raises(ValueError, match="Задача с таким названием не найдена"):
            task_manager.mark_task_completed("TASK99")

@allure.feature("remove task")
@allure.story("remove existing task")
def test_remove_task_valid(task_manager_with_tasks):
    """
          test removing existing task from the list
    """
    with allure.step("remove tasks"):
        task_manager_with_tasks.remove_task("Task0")
        task_manager_with_tasks.remove_task("Task1")
    with allure.step("check if task was removed"):
        assert len(task_manager_with_tasks.list_tasks()) == 1

@allure.feature("remove task")
@allure.story("remove unexisting task")
def test_remove_task_invalid(task_manager):
    with allure.step("check if we can remove unexisting task"):
        with pytest.raises(ValueError, match="Задача с таким названием не найдена"):
            task_manager.remove_task("TASK99")
