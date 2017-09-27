import logging
import os
import traceback
import time

def create_logger(logger_name):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    os.makedirs('logs', exist_ok=True)
    log_file_path = 'logs/{}'.format(logger_name)
    handler = logging.FileHandler(log_file_path, 'a')
    handler.setFormatter(formatter)
    logger.addHandler(handler) # Log to file

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler) # Log to console

    return logger

def run_until_complete(target=None, args=(), logger=None, interval=0.01):
    result = None
    while (not result or (isinstance(result, tuple) and not all(result)) and not (isinstance(result, list) and not result)):
        try:
            result = target(*args)
        except Exception:
            error = traceback.format_exc()
            if logger:
                logger.error(error)
        time.sleep(interval) # Avoid busy waiting
    return result

class Runner(object):
    def __init__(self, logger=None):
        self.logger = logger

    def run_until_complete(self, target=None, args=(), interval=0.01):
        run_until_complete(target=target, args=args, logger=self.logger, interval=interval)
