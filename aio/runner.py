import traceback
import time

class Runner(object):
    def __init__(self, logger=None):
        self.logger = logger

    def run_until_complete(self, target=None, args=(), interval=0.01):
        result = None
        while (not result or (isinstance(result, tuple) and not all(result)) and not (isinstance(result, list) and not result)):
            try:
                result = target(*args)
            except Exception:
                error = traceback.format_exc()
                if self.logger:
                    self.logger.error(error)
            time.sleep(interval) # Avoid busy waiting
        return result
