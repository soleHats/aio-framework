import uuid
from aio import utilities

class Task(object):
    def __init__(self, task_data={}):
        self.id = str(uuid.uuid4())
        self.data = task_data
        self.process = None
        self.status = ''
        self.logger = utilities.create_logger(self.id)

    def is_active(self):
        return self.process is not None and self.process.is_alive()
