import time
from .context import Bot, Task

class MockBot(Bot):
    def execute_task(self, task):
        time.sleep(0.1)
        return 'Done!'

def test_create_task():
    task_data = 'abc123'
    task = Task(task_data)
    assert task.data == task_data

def test_add_task():
    task = Task()
    bot = MockBot()
    bot.add_task(task)
    assert bot.tasks[task.id].id == task.id

def test_remove_task():
    task = Task()
    bot = MockBot()
    bot.add_task(task)
    bot.remove_task(task.id)
    assert task.id not in bot.tasks

def test_start_task():
    task = Task()
    bot = MockBot()
    bot.add_task(task)
    bot.start_task(task.id)
    assert bot.tasks[task.id].is_active()

def test_run_task():
    task = Task()
    bot = MockBot()
    bot.add_task(task)
    bot.start_task(task.id)
    time.sleep(0.2)
    assert not bot.tasks[task.id].is_active()
